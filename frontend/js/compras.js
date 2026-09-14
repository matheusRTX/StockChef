document.addEventListener('DOMContentLoaded', async function () {
  await atualizarMapaFornecedoresPorCategoria();
  carregarListaCompras();
  inicializarFornecedores();
  inicializarAcoesLista();
});

// ---------------------- Carregamento ----------------------

async function carregarListaCompras() {
  try {
    const resposta = await fetch('/api/estoque/listar');

    if (resposta.status === 401) {
      window.location.href = '/login';
      return;
    }

    if (!resposta.ok) {
      throw new Error('Falha ao buscar estoque: ' + resposta.status);
    }

    const produtos = await resposta.json();

    // Só entram na lista de compras os produtos cujo estoque atual
    // está abaixo do estoque mínimo cadastrado.
    const paraComprar = produtos.filter(function (p) {
      return Number(p.quantidade_total) < Number(p.valor_minimo);
    });

    renderizarListaCompras(paraComprar);
  } catch (erro) {
    console.error('Erro ao carregar lista de compras:', erro);
    const lista = document.getElementById('lista-categorias');
    if (lista) {
      lista.innerHTML = '<p id="compras-erro">Não foi possível carregar a lista de compras.</p>';
    }
  }
}

// ---------------------- Helpers de formatação ----------------------

function formatarQuantidade(valor) {
  const numero = Number(valor);
  if (Number.isNaN(numero)) return '0';
  if (Number.isInteger(numero)) return numero.toString();
  return numero.toFixed(2).replace(/0+$/, '').replace(/\.$/, '');
}

function textoContagem(qtd) {
  return qtd === 1 ? '(1 item)' : '(' + qtd + ' itens)';
}

function statusEstoque(produto) {
  const atual = Number(produto.quantidade_total);
  if (atual <= 0) return 'Estoque zerado';
  return 'Abaixo do mínimo (min: ' + formatarQuantidade(produto.valor_minimo) + ' ' + produto.unidade + ')';
}

function escapeHtml(texto) {
  const div = document.createElement('div');
  div.textContent = texto == null ? '' : String(texto);
  return div.innerHTML;
}

// ---------------------- Agrupamento por categoria ----------------------

function agruparPorCategoria(produtos) {
  const grupos = {};
  const ordem = [];

  produtos.forEach(function (p) {
    const nomeCategoria = p.categoria || 'Sem categoria';
    if (!grupos[nomeCategoria]) {
      grupos[nomeCategoria] = [];
      ordem.push(nomeCategoria);
    }
    grupos[nomeCategoria].push(p);
  });

  return ordem.map(function (nome) {
    return { categoria: nome, itens: grupos[nome] };
  });
}

// ---------------------- Renderização ----------------------

function renderizarListaCompras(produtos) {
  const lista = document.getElementById('lista-categorias');
  const vazio = document.getElementById('compras-vazio');
  if (!lista) return;

  lista.innerHTML = '';

  if (!produtos || produtos.length === 0) {
    if (vazio) vazio.style.display = 'block';
    return;
  }

  if (vazio) vazio.style.display = 'none';

  const grupos = agruparPorCategoria(produtos);
  grupos.forEach(function (grupo) {
    lista.appendChild(criarBlocoCategoria(grupo.categoria, grupo.itens));
  });

  inicializarInteracoesLista();
}

function criarBlocoCategoria(nomeCategoria, itens) {
  const bloco = document.createElement('div');
  bloco.id = 'categoria';
  bloco.className = 'categoria-bloco';

  const fornecedor = fornecedorPorCategoria[normalizarChaveCategoria(nomeCategoria)];
  const tituloWhats = fornecedor && fornecedor.telefone
    ? 'Enviar para ' + fornecedor.nome
    : 'Nenhum fornecedor com WhatsApp cadastrado nesta categoria';
  const tituloEmail = fornecedor && fornecedor.email
    ? 'Enviar para ' + fornecedor.nome
    : 'Nenhum fornecedor com email cadastrado nesta categoria';

  bloco.innerHTML =
    '<button type="button" class="categoria-info categoria-toggle">' +
      '<div id="fle"><h4>' + escapeHtml(nomeCategoria) + '</h4>' +
        '<p id="quant-categoria" class="quant-categoria-texto">' + textoContagem(itens.length) + '</p></div>' +
      '<svg xmlns="http://www.w3.org/2000/svg" id="seta" width="24" height="24" viewBox="0 0 24 24" fill="none" ' +
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ' +
        'class="lucide lucide-chevron-up-icon lucide-chevron-up"><path d="m18 15-6-6-6 6"/></svg>' +
    '</button>' +
    '<div id="dad">' + itens.map(criarCardItem).join('') +
      '<div class="compartilhar-categoria">' +
        '<button type="button" id="whatsapp" class="btn-compartilhar-categoria" data-categoria="' + escapeHtml(nomeCategoria) + '" title="' + escapeHtml(tituloWhats) + '">' +
          '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" ' +
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ' +
            'class="lucide lucide-message-circle-icon lucide-message-circle"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>' +
          '<p>WhatsApp</p>' +
        '</button>' +
        '<button type="button" id="gmail" class="btn-compartilhar-categoria" data-categoria="' + escapeHtml(nomeCategoria) + '" title="' + escapeHtml(tituloEmail) + '">' +
          '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" ' +
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ' +
            'class="lucide lucide-mail-icon lucide-mail"><rect width="20" height="16" x="2" y="4" rx="2"/>' +
            '<path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>' +
          '<p>Gmail</p>' +
        '</button>' +
      '</div>' +
    '</div>';

  return bloco;
}

// ---------------------- Compartilhamento por categoria ----------------------

function textoParaCompartilhar(bloco, nomeCategoria) {
  const linhas = ['Lista de compras - ' + nomeCategoria + ':'];

  bloco.querySelectorAll('.item-compra').forEach(function (item) {
    const nome = item.querySelector('#nome-produto');
    const qtd = item.querySelector('#unidades');
    if (nome && qtd) {
      linhas.push('- ' + nome.textContent + ': ' + qtd.textContent);
    }
  });

  return linhas.join('\n');
}

function compartilharWhatsApp(bloco, nomeCategoria) {
  const fornecedor = fornecedorPorCategoria[normalizarChaveCategoria(nomeCategoria)];

  if (!fornecedor || !fornecedor.telefone) {
    alert('Nenhum fornecedor com WhatsApp cadastrado para a categoria "' + nomeCategoria + '".');
    return;
  }

  const texto = textoParaCompartilhar(bloco, nomeCategoria);
  const numero = fornecedor.telefone.replace(/\D/g, '');
  window.open('https://wa.me/' + numero + '?text=' + encodeURIComponent(texto), '_blank');
}

function compartilharGmail(bloco, nomeCategoria) {
  const fornecedor = fornecedorPorCategoria[normalizarChaveCategoria(nomeCategoria)];

  if (!fornecedor || !fornecedor.email) {
    alert('Nenhum fornecedor com email cadastrado para a categoria "' + nomeCategoria + '".');
    return;
  }

  const texto = textoParaCompartilhar(bloco, nomeCategoria);
  const assunto = 'Lista de compras - ' + nomeCategoria;
  const url = 'https://mail.google.com/mail/?view=cm&fs=1&to=' + encodeURIComponent(fornecedor.email) +
    '&su=' + encodeURIComponent(assunto) + '&body=' + encodeURIComponent(texto);
  window.open(url, '_blank');
}

function criarCardItem(produto) {
  const faltante = Math.max(Number(produto.valor_minimo) - Number(produto.quantidade_total), 0);

  return (
    '<div id="card" class="item-compra" data-id-produto="' + produto.id_produto + '">' +
      '<div id="btn-riscar"><input id="btn-clicar" type="checkbox" class="check-comprado"></div>' +
      '<div id="info-produto">' +
        '<h4 id="nome-produto">' + escapeHtml(produto.produto) + '</h4>' +
        '<p id="sub-produto">' + statusEstoque(produto) + '</p>' +
      '</div>' +
      '<div id="quant">' +
        '<h4 id="unidades">' + formatarQuantidade(faltante) + ' ' + escapeHtml(produto.unidade) + '</h4>' +
        '<div id="lixeira" class="remover-item" title="Remover da lista">' +
          '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" ' +
            'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" ' +
            'stroke-linejoin="round" class="lucide lucide-trash2-icon lucide-trash-2">' +
            '<path d="M10 11v6" /><path d="M14 11v6" />' +
            '<path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6" /><path d="M3 6h18" />' +
            '<path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" /></svg>' +
        '</div>' +
      '</div>' +
    '</div>'
  );
}

// ---------------------- Interações ----------------------

function inicializarInteracoesLista() {
  document.querySelectorAll('.categoria-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const bloco = btn.closest('.categoria-bloco');
      const seta = btn.querySelector('#seta');
      if (bloco) bloco.classList.toggle('aberto');
      if (seta) seta.classList.toggle('virar');
    });
  });

  document.querySelectorAll('.remover-item').forEach(function (icone) {
    icone.addEventListener('click', function (e) {
      e.stopPropagation();
      const card = icone.closest('.item-compra');
      const bloco = icone.closest('.categoria-bloco');
      if (card) card.remove();
      atualizarContagemCategoria(bloco);
    });
  });

  document.querySelectorAll('.btn-compartilhar-categoria').forEach(function (botao) {
    botao.addEventListener('click', function (e) {
      e.stopPropagation();
      const bloco = botao.closest('.categoria-bloco');
      const nomeCategoria = botao.dataset.categoria || '';
      if (!bloco) return;

      if (botao.id === 'whatsapp') {
        compartilharWhatsApp(bloco, nomeCategoria);
      } else if (botao.id === 'gmail') {
        compartilharGmail(bloco, nomeCategoria);
      }
    });
  });

  document.querySelectorAll('.check-comprado').forEach(function (checkbox) {
    checkbox.addEventListener('click', function (e) {
      e.stopPropagation();
    });
    checkbox.addEventListener('change', function () {
      const card = checkbox.closest('.item-compra');
      if (card) card.classList.toggle('comprado', checkbox.checked);
    });
  });
}

function atualizarContagemCategoria(bloco) {
  if (!bloco) return;

  const restantes = bloco.querySelectorAll('.item-compra').length;

  if (restantes === 0) {
    bloco.remove();
    const lista = document.getElementById('lista-categorias');
    const vazio = document.getElementById('compras-vazio');
    if (lista && lista.children.length === 0 && vazio) {
      vazio.style.display = 'block';
    }
    return;
  }

  const contagem = bloco.querySelector('.quant-categoria-texto');
  if (contagem) contagem.textContent = textoContagem(restantes);
}

// ---------------------- Ações da lista completa (copiar / pdf / imprimir / enviar) ----------------------

// Lê o estado atual renderizado na tela (mesma fonte usada pelo compartilhamento
// por categoria) para montar a lista completa, já refletindo itens removidos
// e marcados como comprados pelo usuário.
function coletarGruposListaAtual() {
  const grupos = [];

  document.querySelectorAll('#lista-categorias .categoria-bloco').forEach(function (bloco) {
    const tituloEl = bloco.querySelector('#fle h4');
    const nomeCategoria = tituloEl ? tituloEl.textContent : 'Sem categoria';
    const itens = [];

    bloco.querySelectorAll('.item-compra').forEach(function (item) {
      const nome = item.querySelector('#nome-produto');
      const qtd = item.querySelector('#unidades');
      if (nome && qtd) {
        itens.push({
          nome: nome.textContent,
          quantidade: qtd.textContent,
          comprado: item.classList.contains('comprado'),
        });
      }
    });

    if (itens.length > 0) {
      grupos.push({ categoria: nomeCategoria, itens: itens });
    }
  });

  return grupos;
}

function textoListaCompleta() {
  const grupos = coletarGruposListaAtual();
  const linhas = ['Lista de Compras'];

  grupos.forEach(function (grupo) {
    linhas.push('');
    linhas.push(grupo.categoria + ':');
    grupo.itens.forEach(function (item) {
      linhas.push('- ' + item.nome + ': ' + item.quantidade + (item.comprado ? ' (comprado)' : ''));
    });
  });

  return linhas.join('\n');
}

async function tratarCopiarLista() {
  const grupos = coletarGruposListaAtual();
  if (grupos.length === 0) {
    alert('Não há itens na lista de compras para copiar.');
    return;
  }

  const texto = textoListaCompleta();

  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(texto);
    } else {
      const area = document.createElement('textarea');
      area.value = texto;
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.focus();
      area.select();
      document.execCommand('copy');
      document.body.removeChild(area);
    }
    alert('Lista de compras copiada!');
  } catch (erro) {
    console.error('Erro ao copiar lista de compras:', erro);
    alert('Não foi possível copiar a lista de compras.');
  }
}

function tratarImprimirLista() {
  const grupos = coletarGruposListaAtual();
  if (grupos.length === 0) {
    alert('Não há itens na lista de compras para imprimir.');
    return;
  }

  const janela = window.open('', '_blank');
  if (!janela) {
    alert('Não foi possível abrir a janela de impressão. Verifique o bloqueador de pop-ups.');
    return;
  }

  const html =
    '<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Lista de Compras</title>' +
    '<style>' +
      'body{font-family:Arial,Helvetica,sans-serif;padding:24px;color:#111;}' +
      'h1{font-size:20px;margin-bottom:16px;}' +
      'h2{font-size:15px;margin:18px 0 6px;border-bottom:1px solid #ccc;padding-bottom:4px;}' +
      'ul{list-style:none;padding:0;margin:0;}' +
      'li{padding:4px 0;font-size:13px;display:flex;justify-content:space-between;}' +
      'li.comprado{text-decoration:line-through;opacity:0.5;}' +
    '</style></head><body>' +
    '<h1>Lista de Compras</h1>' +
    grupos.map(function (grupo) {
      return '<h2>' + escapeHtml(grupo.categoria) + '</h2><ul>' +
        grupo.itens.map(function (item) {
          return '<li class="' + (item.comprado ? 'comprado' : '') + '"><span>' + escapeHtml(item.nome) +
            '</span><span>' + escapeHtml(item.quantidade) + '</span></li>';
        }).join('') +
        '</ul>';
    }).join('') +
    '</body></html>';

  janela.document.open();
  janela.document.write(html);
  janela.document.close();

  janela.onload = function () {
    janela.focus();
    janela.print();
  };
}

function tratarGerarPdf() {
  const grupos = coletarGruposListaAtual();
  if (grupos.length === 0) {
    alert('Não há itens na lista de compras para gerar o PDF.');
    return;
  }

  if (!window.jspdf || !window.jspdf.jsPDF) {
    alert('Não foi possível carregar o gerador de PDF.');
    return;
  }

  const jsPDF = window.jspdf.jsPDF;
  const doc = new jsPDF();
  const margemEsquerda = 14;
  const alturaMaxima = 280;
  let y = 18;

  doc.setFontSize(16);
  doc.text('Lista de Compras', margemEsquerda, y);
  y += 10;

  grupos.forEach(function (grupo) {
    if (y > alturaMaxima - 10) {
      doc.addPage();
      y = 18;
    }

    doc.setFontSize(12);
    doc.setFont(undefined, 'bold');
    doc.text(grupo.categoria, margemEsquerda, y);
    y += 7;

    doc.setFont(undefined, 'normal');
    doc.setFontSize(11);

    grupo.itens.forEach(function (item) {
      if (y > alturaMaxima) {
        doc.addPage();
        y = 18;
      }
      const texto = '- ' + item.nome + ': ' + item.quantidade + (item.comprado ? ' (comprado)' : '');
      doc.text(texto, margemEsquerda + 2, y);
      y += 6;
    });

    y += 4;
  });

  doc.save('lista-de-compras.pdf');
}

async function tratarEnviarLista() {
  const grupos = coletarGruposListaAtual();
  if (grupos.length === 0) {
    alert('Não há itens na lista de compras para enviar.');
    return;
  }

  const texto = textoListaCompleta();

  if (navigator.share) {
    try {
      await navigator.share({ title: 'Lista de Compras', text: texto });
    } catch (erro) {
      if (erro && erro.name !== 'AbortError') {
        console.error('Erro ao compartilhar lista de compras:', erro);
      }
    }
    return;
  }

  // Sem suporte a compartilhamento nativo: usa o WhatsApp como alternativa,
  // seguindo a mesma via já usada pelo compartilhamento por categoria.
  window.open('https://wa.me/?text=' + encodeURIComponent(texto), '_blank');
}

function inicializarAcoesLista() {
  const btnCopiar = document.getElementById('btn-copiar');
  const btnPdf = document.getElementById('btn-pdf');
  const btnImprimir = document.getElementById('btn-imprimir');
  const btnEnviar = document.getElementById('btn-enviar');

  if (btnCopiar) btnCopiar.addEventListener('click', tratarCopiarLista);
  if (btnPdf) btnPdf.addEventListener('click', tratarGerarPdf);
  if (btnImprimir) btnImprimir.addEventListener('click', tratarImprimirLista);
  if (btnEnviar) btnEnviar.addEventListener('click', tratarEnviarLista);
}

// ==================== Fornecedores (integrado ao banco de dados) ====================

// Mapa "nome da categoria em minúsculas" -> fornecedor {nome, telefone, email, categoria, ...}
// usado para descobrir com qual fornecedor falar ao clicar em WhatsApp/Gmail de uma categoria.
var fornecedorPorCategoria = {};

function normalizarChaveCategoria(nome) {
  return (nome || '').trim().toLowerCase();
}

async function atualizarMapaFornecedoresPorCategoria() {
  try {
    const fornecedores = await carregarFornecedores();
    const mapa = {};
    (fornecedores || []).forEach(function (f) {
      const chave = normalizarChaveCategoria(f.categoria);
      if (chave && !mapa[chave]) {
        mapa[chave] = f;
      }
    });
    fornecedorPorCategoria = mapa;
  } catch (erro) {
    console.error('Erro ao carregar fornecedores por categoria:', erro);
  }
}

function mostrarFeedbackFornecedor(elemento, mensagem, tipo) {
  if (!elemento) return;
  elemento.textContent = mensagem;
  elemento.className = 'feedback' + (tipo ? ' ' + tipo : '');
}

var modalFornecedoresOverlay = null;
var modalFornecedorOverlay = null;
var listaFornecedoresEl = null;
var fornecedoresVazioEl = null;
var feedbackListaFornecedoresEl = null;
var formFornecedor = null;
var selectCategoriaFornecedor = null;
var feedbackModalFornecedorEl = null;
var tituloModalFornecedorEl = null;
var inputIdFornecedor = null;

async function carregarCategoriasFornecedor(selectAlvo) {
  try {
    const resposta = await fetch('/api/categorias');
    if (!resposta.ok) throw new Error('Não foi possível carregar as categorias.');

    const categorias = await resposta.json();
    const valorAtual = selectAlvo.value;

    selectAlvo.innerHTML = '<option value="">Sem categoria</option>';
    categorias.forEach(function (categoria) {
      const opcao = document.createElement('option');
      opcao.value = categoria.id_categoria;
      opcao.textContent = categoria.nome;
      selectAlvo.appendChild(opcao);
    });

    if (valorAtual && selectAlvo.querySelector('option[value="' + valorAtual + '"]')) {
      selectAlvo.value = valorAtual;
    }

    return categorias;
  } catch (erro) {
    console.error('Erro ao carregar categorias:', erro);
    return [];
  }
}

async function carregarFornecedores() {
  const resposta = await fetch('/api/fornecedores');

  if (resposta.status === 401) {
    window.location.href = '/login';
    return [];
  }

  if (!resposta.ok) {
    throw new Error('Não foi possível carregar os fornecedores.');
  }

  return resposta.json();
}

function criarCardFornecedor(fornecedor) {
  const card = document.createElement('div');
  card.className = 'card-fornecedor';
  card.dataset.idFornecedor = fornecedor.id_fornecedor;

  card.innerHTML =
    '<div>' +
      '<span class="nome-fornecedor">' + escapeHtml(fornecedor.nome) + '</span>' +
      (fornecedor.categoria ? '<div class="categoria-fornecedor">' + escapeHtml(fornecedor.categoria) + '</div>' : '') +
      (fornecedor.telefone ? '<div class="linha-fornecedor">📱 ' + escapeHtml(fornecedor.telefone) + '</div>' : '') +
      (fornecedor.email ? '<div class="linha-fornecedor">✉️ ' + escapeHtml(fornecedor.email) + '</div>' : '') +
    '</div>' +
    '<div class="acoes-fornecedor">' +
      '<button type="button" class="btn-editar-fornecedor" title="Editar">✏️</button>' +
      '<button type="button" class="btn-remover-fornecedor" title="Remover">🗑️</button>' +
    '</div>';

  card.querySelector('.btn-editar-fornecedor').addEventListener('click', function () {
    abrirModalFornecedor(fornecedor);
  });

  card.querySelector('.btn-remover-fornecedor').addEventListener('click', function () {
    tratarRemoverFornecedor(fornecedor.id_fornecedor);
  });

  return card;
}

function renderizarListaFornecedores(fornecedores) {
  if (!listaFornecedoresEl) return;
  listaFornecedoresEl.innerHTML = '';

  if (!fornecedores || fornecedores.length === 0) {
    if (fornecedoresVazioEl) fornecedoresVazioEl.style.display = 'block';
    return;
  }

  if (fornecedoresVazioEl) fornecedoresVazioEl.style.display = 'none';

  fornecedores.forEach(function (fornecedor) {
    listaFornecedoresEl.appendChild(criarCardFornecedor(fornecedor));
  });
}

async function abrirModalFornecedores() {
  mostrarFeedbackFornecedor(feedbackListaFornecedoresEl, '', '');
  modalFornecedoresOverlay.classList.add('aberto');

  try {
    const fornecedores = await carregarFornecedores();
    renderizarListaFornecedores(fornecedores);
  } catch (erro) {
    mostrarFeedbackFornecedor(feedbackListaFornecedoresEl, erro.message, 'erro');
  }
}

function fecharModalFornecedores() {
  modalFornecedoresOverlay.classList.remove('aberto');
}

function abrirModalFornecedor(fornecedor) {
  formFornecedor.reset();
  mostrarFeedbackFornecedor(feedbackModalFornecedorEl, '', '');
  carregarCategoriasFornecedor(selectCategoriaFornecedor).then(function () {
    if (fornecedor && fornecedor.id_categoria) {
      selectCategoriaFornecedor.value = fornecedor.id_categoria;
    }
  });

  if (fornecedor) {
    tituloModalFornecedorEl.textContent = 'Editar fornecedor';
    inputIdFornecedor.value = fornecedor.id_fornecedor;
    document.getElementById('inputNomeFornecedor').value = fornecedor.nome || '';
    document.getElementById('inputTelefoneFornecedor').value = fornecedor.telefone || '';
    document.getElementById('inputEmailFornecedor').value = fornecedor.email || '';
  } else {
    tituloModalFornecedorEl.textContent = 'Novo fornecedor';
    inputIdFornecedor.value = '';
  }

  modalFornecedorOverlay.classList.add('aberto');
}

function fecharModalFornecedor() {
  modalFornecedorOverlay.classList.remove('aberto');
}

async function tratarSubmitFornecedor(evento) {
  evento.preventDefault();

  const idFornecedor = inputIdFornecedor.value;
  const nome = document.getElementById('inputNomeFornecedor').value.trim();
  const telefone = document.getElementById('inputTelefoneFornecedor').value.trim();
  const email = document.getElementById('inputEmailFornecedor').value.trim();
  const idCategoria = selectCategoriaFornecedor.value;

  if (!nome) {
    mostrarFeedbackFornecedor(feedbackModalFornecedorEl, 'Informe o nome do fornecedor.', 'erro');
    return;
  }

  const dados = {
    nome: nome,
    telefone: telefone,
    email: email,
    id_categoria: idCategoria ? Number(idCategoria) : null,
  };

  try {
    const resposta = await fetch(
      idFornecedor ? '/api/fornecedores/' + idFornecedor : '/api/fornecedores',
      {
        method: idFornecedor ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados),
      }
    );

    const corpo = await resposta.json();
    if (!resposta.ok) {
      throw new Error(corpo.erro || 'Não foi possível salvar o fornecedor.');
    }

    fecharModalFornecedor();
    const fornecedores = await carregarFornecedores();
    renderizarListaFornecedores(fornecedores);
    await atualizarMapaFornecedoresPorCategoria();
    carregarListaCompras();
  } catch (erro) {
    mostrarFeedbackFornecedor(feedbackModalFornecedorEl, erro.message, 'erro');
  }
}

async function tratarRemoverFornecedor(idFornecedor) {
  if (!window.confirm('Remover este fornecedor?')) return;

  try {
    const resposta = await fetch('/api/fornecedores/' + idFornecedor, { method: 'DELETE' });
    const corpo = await resposta.json();
    if (!resposta.ok) {
      throw new Error(corpo.erro || 'Não foi possível remover o fornecedor.');
    }

    const fornecedores = await carregarFornecedores();
    renderizarListaFornecedores(fornecedores);
    await atualizarMapaFornecedoresPorCategoria();
    carregarListaCompras();
  } catch (erro) {
    mostrarFeedbackFornecedor(feedbackListaFornecedoresEl, erro.message, 'erro');
  }
}

function inicializarFornecedores() {
  const btnAbreFornecedores = document.getElementById('btn-fornecedores');
  modalFornecedoresOverlay = document.getElementById('modalFornecedoresOverlay');
  modalFornecedorOverlay = document.getElementById('modalFornecedorOverlay');
  listaFornecedoresEl = document.getElementById('listaFornecedores');
  fornecedoresVazioEl = document.getElementById('fornecedoresVazio');
  feedbackListaFornecedoresEl = document.getElementById('feedbackListaFornecedores');
  formFornecedor = document.getElementById('formFornecedor');
  selectCategoriaFornecedor = document.getElementById('selectCategoriaFornecedor');
  feedbackModalFornecedorEl = document.getElementById('feedbackModalFornecedor');
  tituloModalFornecedorEl = document.getElementById('tituloModalFornecedor');
  inputIdFornecedor = document.getElementById('inputIdFornecedor');

  const btnNovoFornecedor = document.getElementById('btnNovoFornecedor');
  const fecharModalFornecedoresBtn = document.getElementById('fecharModalFornecedores');
  const fecharModalFornecedorBtn = document.getElementById('fecharModalFornecedor');

  if (!btnAbreFornecedores || !modalFornecedoresOverlay || !modalFornecedorOverlay) return;

  btnAbreFornecedores.addEventListener('click', abrirModalFornecedores);
  fecharModalFornecedoresBtn.addEventListener('click', fecharModalFornecedores);
  fecharModalFornecedorBtn.addEventListener('click', fecharModalFornecedor);

  btnNovoFornecedor.addEventListener('click', function () {
    abrirModalFornecedor(null);
  });

  formFornecedor.addEventListener('submit', tratarSubmitFornecedor);

  modalFornecedoresOverlay.addEventListener('click', function (e) {
    if (e.target === modalFornecedoresOverlay) fecharModalFornecedores();
  });
  modalFornecedorOverlay.addEventListener('click', function (e) {
    if (e.target === modalFornecedorOverlay) fecharModalFornecedor();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (modalFornecedorOverlay.classList.contains('aberto')) {
      fecharModalFornecedor();
    } else if (modalFornecedoresOverlay.classList.contains('aberto')) {
      fecharModalFornecedores();
    }
  });
}
