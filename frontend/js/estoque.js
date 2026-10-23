document.addEventListener('DOMContentLoaded', function () {
  carregarEstoque();
  inicializarModais();
});

async function carregarEstoque() {
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

    renderizarEstoque(produtos);
    montarFiltros(produtos);
    inicializarInteracoes();
  } catch (erro) {
    console.error('Erro ao carregar estoque:', erro);
  }
}

// ---------------------- Helpers de formatação ----------------------

function formatarQuantidade(valor) {
  const numero = Number(valor);
  if (Number.isInteger(numero)) return numero.toString();
  return numero.toFixed(2).replace(/0+$/, '').replace(/\.$/, '');
}

function formatarData(dataIso) {
  if (!dataIso) return null;
  const [ano, mes, dia] = dataIso.split('-');
  return dia + '/' + mes + '/' + ano;
}

function estaVencido(dataIso) {
  if (!dataIso) return false;
  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);
  const validade = new Date(dataIso + 'T00:00:00');
  return validade < hoje;
}

// ---------------------- Renderização ----------------------

function criarCartaoProduto(produto) {
  const cartao = document.createElement('div');
  cartao.className = 'item-cartao';
  cartao.setAttribute('data-category', produto.categoria);

  const numLotes = produto.lotes.length;
  const textoLotes = numLotes === 1 ? '1 lote' : numLotes + ' lotes';

  let detalhesHTML;

  if (numLotes === 0) {
    detalhesHTML = '' +
      '<div class="item-detalhe">' +
        '<div class="lote">Sem lotes cadastrados</div>' +
      '</div>';
  } else if (numLotes === 1) {
    const lote = produto.lotes[0];
    const dataFormatada = formatarData(lote.validade);
    const vencido = estaVencido(lote.validade);

    let textoValidade;
    let classeValidade;
    if (!dataFormatada) {
      textoValidade = 'Sem data de vencimento';
      classeValidade = 'validade-ok';
    } else if (vencido) {
      textoValidade = 'Vence ' + dataFormatada + ' (vencido)';
      classeValidade = 'validade';
    } else {
      textoValidade = 'Vence ' + dataFormatada;
      classeValidade = 'validade-ok';
    }

    detalhesHTML = '' +
      '<div class="item-detalhe">' +
        '<div class="lote">' + formatarQuantidade(lote.quantidade_atual) + ' ' + produto.unidade + '</div>' +
        '<div class="lote-acoes">' +
          '<div class="' + classeValidade + '">' + textoValidade + '</div>' +
          criarBotaoExcluirLote(lote.id_lote) +
        '</div>' +
      '</div>';
  } else {
    detalhesHTML = produto.lotes.map(function (lote) {
      const dataFormatada = formatarData(lote.validade);
      const textoData = dataFormatada ? ('— Vence ' + dataFormatada) : '— Sem vencimento';
      return '' +
        '<div class="item-detalhe item-detalhe-multi">' +
          '<div class="lote">' + formatarQuantidade(lote.quantidade_atual) + ' ' + produto.unidade + ' ' + textoData + '</div>' +
          criarBotaoExcluirLote(lote.id_lote) +
        '</div>';
    }).join('');
  }

  cartao.innerHTML = '' +
    '<div class="item-topo">' +
      '<div class="item-informacoes">' +
        '<h2>' + produto.produto + '</h2>' +
        '<div class="etiquetas">' +
          '<span class="etiqueta">' + produto.categoria + '</span>' +
          '<span class="etiqueta pilula">' + textoLotes + '</span>' +
        '</div>' +
      '</div>' +
      '<div class="item-qtd">' +
        '<div class="qtd-informacoes">' +
          '<span class="qtd-valor">' + formatarQuantidade(produto.quantidade_total) + ' ' + produto.unidade + '</span>' +
          '<span class="qtd-minimo">Min: ' + formatarQuantidade(produto.valor_minimo) + '</span>' +
        '</div>' +
        criarBotaoExcluirProduto(produto.id_produto) +
        '<button class="seta-btn" aria-label="Expandir">' +
          '<svg class="seta" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
            'stroke-linecap="round" stroke-linejoin="round">' +
            '<polyline points="6 9 12 15 18 9" />' +
          '</svg>' +
        '</button>' +
      '</div>' +
    '</div>' +
    detalhesHTML;

  anexarBotoesExcluirLote(cartao);
  anexarBotaoExcluirProduto(cartao);

  return cartao;
}

// ---------------------- Exclusão de produto ----------------------

function criarBotaoExcluirProduto(idProduto) {
  return '' +
    '<button class="produto-excluir-btn" type="button" data-id-produto="' + idProduto + '" aria-label="Excluir produto">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
        '<polyline points="3 6 5 6 21 6" />' +
        '<path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />' +
        '<path d="M10 11v6" />' +
        '<path d="M14 11v6" />' +
        '<path d="M9 6V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2" />' +
      '</svg>' +
    '</button>';
}

function anexarBotaoExcluirProduto(cartao) {
  var btn = cartao.querySelector('.produto-excluir-btn');
  if (!btn) return;

  btn.addEventListener('click', function (e) {
    e.stopPropagation();
    excluirProduto(btn.getAttribute('data-id-produto'));
  });
}

async function excluirProduto(idProduto) {
  if (!confirm('Deseja realmente excluir este produto? Todos os seus lotes também serão removidos do estoque.')) return;

  try {
    const resposta = await fetch('/api/produtos/' + idProduto, { method: 'DELETE' });
    const corpo = await resposta.json();

    if (!resposta.ok) {
      throw new Error(corpo.erro || 'Não foi possível excluir o produto.');
    }

    carregarEstoque();
  } catch (erro) {
    alert(erro.message);
  }
}

// ---------------------- Exclusão de lote ----------------------

function criarBotaoExcluirLote(idLote) {
  return '' +
    '<button class="lote-excluir-btn" type="button" data-id-lote="' + idLote + '" aria-label="Excluir lote">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
        '<polyline points="3 6 5 6 21 6" />' +
        '<path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />' +
        '<path d="M10 11v6" />' +
        '<path d="M14 11v6" />' +
        '<path d="M9 6V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2" />' +
      '</svg>' +
    '</button>';
}

function anexarBotoesExcluirLote(cartao) {
  cartao.querySelectorAll('.lote-excluir-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      excluirLote(btn.getAttribute('data-id-lote'));
    });
  });
}

async function excluirLote(idLote) {
  if (!confirm('Deseja realmente excluir este lote? Essa ação não pode ser desfeita.')) return;

  try {
    const resposta = await fetch('/api/lotes/' + idLote, { method: 'DELETE' });
    const corpo = await resposta.json();

    if (!resposta.ok) {
      throw new Error(corpo.erro || 'Não foi possível excluir o lote.');
    }

    carregarEstoque();
  } catch (erro) {
    alert(erro.message);
  }
}

function renderizarEstoque(produtos) {
  const lista = document.getElementById('listaEstoque');
  const vazio = document.getElementById('estoqueVazio');

  lista.querySelectorAll('.item-cartao').forEach(function (el) { el.remove(); });

  if (!produtos || produtos.length === 0) {
    if (vazio) vazio.style.display = 'block';
    return;
  }

  if (vazio) vazio.style.display = 'none';

  produtos.forEach(function (produto) {
    lista.appendChild(criarCartaoProduto(produto));
  });
}

function montarFiltros(produtos) {
  const filtroMenu = document.getElementById('filtroMenu');
  const categorias = Array.from(new Set(produtos.map(function (p) { return p.categoria; }))).sort();

  categorias.forEach(function (categoria) {
    const botao = document.createElement('button');
    botao.className = 'filtro-opcao';
    botao.setAttribute('data-value', categoria);
    botao.textContent = categoria;
    filtroMenu.appendChild(botao);
  });
}

// ---------------------- Interações (busca, filtro, expandir) ----------------------

function inicializarInteracoes() {
  document.querySelectorAll('.seta-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var cartao = btn.closest('.item-cartao');
      cartao.classList.toggle('aberto');
    });
  });

  var filtroWrap = document.querySelector('.filtro-wrap');
  var filtroBtn = document.getElementById('filtroBtn');
  var filtroLabel = document.getElementById('filtroLabel');
  var filtroOpcoes = document.querySelectorAll('.filtro-opcao');
  var cartoes = document.querySelectorAll('.item-cartao');

  filtroBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    filtroWrap.classList.toggle('aberto');
  });

  document.addEventListener('click', function (e) {
    if (!filtroWrap.contains(e.target)) {
      filtroWrap.classList.remove('aberto');
    }
  });

  filtroOpcoes.forEach(function (opt) {
    opt.addEventListener('click', function () {
      var value = opt.getAttribute('data-value');
      filtroLabel.textContent = value;

      filtroOpcoes.forEach(function (o) { o.classList.remove('ativo'); });
      opt.classList.add('ativo');

      cartoes.forEach(function (cartao) {
        if (value === 'Todos' || cartao.getAttribute('data-category') === value) {
          cartao.classList.remove('filtro-oculto');
        } else {
          cartao.classList.add('filtro-oculto');
        }
      });

      filtroWrap.classList.remove('aberto');
    });
  });

  var inputBusca = document.querySelector('.pesquisa input');
  inputBusca.addEventListener('input', function () {
    var termo = inputBusca.value.trim().toLowerCase();
    cartoes.forEach(function (cartao) {
      var nome = cartao.querySelector('h2').textContent.toLowerCase();
      var buscaOk = nome.includes(termo);
      var filtroAtivo = filtroLabel.textContent;
      var filtroOk = filtroAtivo === 'Todos' || cartao.getAttribute('data-category') === filtroAtivo;
      cartao.classList.toggle('filtro-oculto', !(buscaOk && filtroOk));
    });
  });
}

// ---------------------- Feedback de formulário ----------------------

function mostrarFeedback(elemento, mensagem, tipo) {
  if (!elemento) return;
  elemento.textContent = mensagem;
  elemento.className = 'feedback ' + tipo;
}

// ---------------------- Modal: Novo Item ----------------------

var modalItemOverlay = null;
var formNovoItem = null;
var selectCategoriaItem = null;
var selectUnidadeItem = null;
var feedbackModalItem = null;

async function carregarCategorias(selectAlvo) {
  try {
    const resposta = await fetch('/api/categorias');
    if (!resposta.ok) throw new Error('Não foi possível carregar as categorias.');

    const categorias = await resposta.json();
    const valorAtual = selectAlvo.value;

    selectAlvo.innerHTML = '<option value="" disabled' + (valorAtual ? '' : ' selected') + '>Selecione</option>';
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

async function carregarUnidades(selectAlvo) {
  try {
    const resposta = await fetch('/api/unidades-medida');
    if (!resposta.ok) throw new Error('Não foi possível carregar as unidades de medida.');

    const unidades = await resposta.json();

    selectAlvo.innerHTML = '<option value="" disabled selected>Selecione</option>';
    unidades.forEach(function (unidade) {
      const opcao = document.createElement('option');
      opcao.value = unidade.id_unidade;
      opcao.textContent = unidade.sigla;
      selectAlvo.appendChild(opcao);
    });

    return unidades;
  } catch (erro) {
    console.error('Erro ao carregar unidades de medida:', erro);
    return [];
  }
}

function abrirModalItem() {
  formNovoItem.reset();
  mostrarFeedback(feedbackModalItem, '', '');
  carregarCategorias(selectCategoriaItem);
  carregarUnidades(selectUnidadeItem);
  modalItemOverlay.classList.add('aberto');
}

function fecharModalItem() {
  modalItemOverlay.classList.remove('aberto');
}

async function enviarNovoItem(dados) {
  const resposta = await fetch('/api/produtos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados),
  });

  const corpo = await resposta.json();

  if (!resposta.ok) {
    throw new Error(corpo.erro || 'Não foi possível criar o item.');
  }

  return corpo;
}

async function tratarSubmitNovoItem(evento) {
  evento.preventDefault();

  const nome = document.getElementById('inputNomeItem').value.trim();
  const idCategoria = selectCategoriaItem.value;
  const idUnidade = selectUnidadeItem.value;
  const quantidadeMinima = document.getElementById('inputQtdMinimaItem').value;

  if (!nome || !idCategoria || !idUnidade) {
    mostrarFeedback(feedbackModalItem, 'Preencha nome, categoria e unidade.', 'erro');
    return;
  }

  try {
    await enviarNovoItem({
      nome: nome,
      id_categoria: Number(idCategoria),
      id_unidade: Number(idUnidade),
      estoque_minimo: quantidadeMinima ? Number(quantidadeMinima) : 0,
    });

    fecharModalItem();
    carregarEstoque();
  } catch (erro) {
    mostrarFeedback(feedbackModalItem, erro.message, 'erro');
  }
}

// ---------------------- Modal: Nova Categoria ----------------------

var modalCategoriaOverlay = null;
var formNovaCategoria = null;
var feedbackModalCategoria = null;

function abrirModalCategoria() {
  formNovaCategoria.reset();
  mostrarFeedback(feedbackModalCategoria, '', '');
  modalCategoriaOverlay.classList.add('aberto');
}

function fecharModalCategoria() {
  modalCategoriaOverlay.classList.remove('aberto');
}

async function enviarNovaCategoria(dados) {
  const resposta = await fetch('/api/categorias', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados),
  });

  const corpo = await resposta.json();

  if (!resposta.ok) {
    throw new Error(corpo.erro || 'Não foi possível criar a categoria.');
  }

  return corpo;
}

async function tratarSubmitNovaCategoria(evento) {
  evento.preventDefault();

  const nome = document.getElementById('inputNomeCategoria').value.trim();
  const descricao = document.getElementById('inputDescricaoCategoria').value.trim();

  if (!nome) {
    mostrarFeedback(feedbackModalCategoria, 'Informe o nome da categoria.', 'erro');
    return;
  }

  try {
    await enviarNovaCategoria({
      nome: nome,
      descricao: descricao || null,
    });

    fecharModalCategoria();

    // Se o modal de novo item estiver disponível, atualiza a lista de categorias dele
    if (selectCategoriaItem) {
      carregarCategorias(selectCategoriaItem);
    }
  } catch (erro) {
    mostrarFeedback(feedbackModalCategoria, erro.message, 'erro');
  }
}

// ---------------------- Inicialização dos modais ----------------------

function inicializarModais() {
  modalItemOverlay = document.getElementById('modalItemOverlay');
  formNovoItem = document.getElementById('formNovoItem');
  selectCategoriaItem = document.getElementById('selectCategoriaItem');
  selectUnidadeItem = document.getElementById('selectUnidadeItem');
  feedbackModalItem = document.getElementById('feedbackModalItem');

  modalCategoriaOverlay = document.getElementById('modalCategoriaOverlay');
  formNovaCategoria = document.getElementById('formNovaCategoria');
  feedbackModalCategoria = document.getElementById('feedbackModalCategoria');

  const btnNovoItem = document.getElementById('btnNovoItem');
  const btnNovaCategoria = document.getElementById('btnNovaCategoria');
  const fecharModalItemBtn = document.getElementById('fecharModalItem');
  const fecharModalCategoriaBtn = document.getElementById('fecharModalCategoria');

  btnNovoItem.addEventListener('click', abrirModalItem);
  btnNovaCategoria.addEventListener('click', abrirModalCategoria);

  fecharModalItemBtn.addEventListener('click', fecharModalItem);
  fecharModalCategoriaBtn.addEventListener('click', fecharModalCategoria);

  formNovoItem.addEventListener('submit', tratarSubmitNovoItem);
  formNovaCategoria.addEventListener('submit', tratarSubmitNovaCategoria);

  // Fecha ao clicar fora do conteúdo do modal
  modalItemOverlay.addEventListener('click', function (e) {
    if (e.target === modalItemOverlay) fecharModalItem();
  });
  modalCategoriaOverlay.addEventListener('click', function (e) {
    if (e.target === modalCategoriaOverlay) fecharModalCategoria();
  });

  // Fecha com a tecla Esc
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (modalItemOverlay.classList.contains('aberto')) fecharModalItem();
    if (modalCategoriaOverlay.classList.contains('aberto')) fecharModalCategoria();
  });
}
