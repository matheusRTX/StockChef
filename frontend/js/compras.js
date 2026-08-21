document.addEventListener('DOMContentLoaded', function () {
  carregarListaCompras();
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
        '<button type="button" id="whatsapp" class="btn-compartilhar-categoria" data-categoria="' + escapeHtml(nomeCategoria) + '">' +
          '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" ' +
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ' +
            'class="lucide lucide-message-circle-icon lucide-message-circle"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>' +
          '<p>WhatsApp</p>' +
        '</button>' +
        '<button type="button" id="gmail" class="btn-compartilhar-categoria" data-categoria="' + escapeHtml(nomeCategoria) + '">' +
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
  const texto = textoParaCompartilhar(bloco, nomeCategoria);
  window.open('https://wa.me/?text=' + encodeURIComponent(texto), '_blank');
}

function compartilharGmail(bloco, nomeCategoria) {
  const texto = textoParaCompartilhar(bloco, nomeCategoria);
  const assunto = 'Lista de compras - ' + nomeCategoria;
  const url = 'https://mail.google.com/mail/?view=cm&fs=1&su=' +
    encodeURIComponent(assunto) + '&body=' + encodeURIComponent(texto);
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
