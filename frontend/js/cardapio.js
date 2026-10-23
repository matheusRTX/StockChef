document.addEventListener('DOMContentLoaded', function () {
  inicializarModais();
  carregarCardapio();
});

// ---------------------- Caches em memória ----------------------

var produtosCache = [];
var produtosPorId = {};
var unidadesPorId = {};
var tiposCulinariaCache = [];
var tiposCulinariaPorId = {};

var idPratoEmPreparo = null;

// ---------------------- Helpers de formatação ----------------------

function formatarQuantidade(valor) {
  const numero = Number(valor);
  if (Number.isInteger(numero)) return numero.toString();
  return numero.toFixed(2).replace(/0+$/, '').replace(/\.$/, '');
}

function escaparHtml(texto) {
  if (texto === null || texto === undefined) return '';
  const div = document.createElement('div');
  div.textContent = String(texto);
  return div.innerHTML;
}

function mostrarFeedback(elemento, mensagem, tipo) {
  if (!elemento) return;
  elemento.textContent = mensagem;
  elemento.className = 'feedback ' + tipo;
}

// ---------------------- Carregamento inicial ----------------------

async function carregarCardapio() {
  try {
    const respostaPratos = await fetch('/api/pratos');

    if (respostaPratos.status === 401) {
      window.location.href = '/login';
      return;
    }

    if (!respostaPratos.ok) {
      throw new Error('Falha ao buscar pratos: ' + respostaPratos.status);
    }

    const resumoPratos = await respostaPratos.json();

    await Promise.all([carregarProdutosCache(), carregarUnidadesCache(), carregarTiposCulinariaCache()]);

    const pratosCompletos = await Promise.all(
      resumoPratos.map(function (p) { return buscarPratoCompleto(p.id_prato); })
    );

    renderizarCardapio(pratosCompletos.filter(Boolean));
  } catch (erro) {
    console.error('Erro ao carregar cardápio:', erro);
  }
}

async function buscarPratoCompleto(idPrato) {
  try {
    const resposta = await fetch('/api/pratos/' + idPrato);
    if (!resposta.ok) return null;
    return await resposta.json();
  } catch (erro) {
    console.error('Erro ao buscar prato ' + idPrato + ':', erro);
    return null;
  }
}

async function carregarProdutosCache() {
  try {
    const resposta = await fetch('/api/produtos');
    if (!resposta.ok) throw new Error('Não foi possível carregar os produtos.');

    produtosCache = await resposta.json();
    produtosPorId = {};
    produtosCache.forEach(function (produto) { produtosPorId[produto.id_produto] = produto; });
  } catch (erro) {
    console.error('Erro ao carregar produtos:', erro);
  }
}

async function carregarUnidadesCache() {
  try {
    const resposta = await fetch('/api/unidades-medida');
    if (!resposta.ok) throw new Error('Não foi possível carregar as unidades de medida.');

    const unidades = await resposta.json();
    unidadesPorId = {};
    unidades.forEach(function (unidade) { unidadesPorId[unidade.id_unidade] = unidade; });
  } catch (erro) {
    console.error('Erro ao carregar unidades de medida:', erro);
  }
}

async function carregarTiposCulinariaCache() {
  try {
    const resposta = await fetch('/api/tipos-culinaria');
    if (!resposta.ok) throw new Error('Não foi possível carregar os tipos de culinária.');

    tiposCulinariaCache = await resposta.json();
    tiposCulinariaPorId = {};
    tiposCulinariaCache.forEach(function (tipo) { tiposCulinariaPorId[tipo.id_tipo_culinaria] = tipo; });
  } catch (erro) {
    console.error('Erro ao carregar tipos de culinária:', erro);
  }
}

// ---------------------- Renderização dos cards de prato ----------------------

function renderizarCardapio(pratos) {
  const lista = document.getElementById('listaPratos');
  const vazio = document.getElementById('cardapioVazio');

  lista.querySelectorAll('.prato-card').forEach(function (el) { el.remove(); });

  if (!pratos || pratos.length === 0) {
    if (vazio) vazio.style.display = 'block';
    return;
  }

  if (vazio) vazio.style.display = 'none';

  pratos.forEach(function (prato) {
    lista.appendChild(criarCartaoPrato(prato));
  });
}

function nomeUnidade(idUnidade) {
  const unidade = unidadesPorId[idUnidade];
  return unidade ? unidade.sigla : '';
}

function nomeProduto(idProduto) {
  const produto = produtosPorId[idProduto];
  return produto ? produto.nome : 'Produto removido';
}

function criarCartaoPrato(prato) {
  const cartao = document.createElement('div');
  cartao.className = 'prato-card';
  cartao.setAttribute('data-id-prato', prato.id_prato);

  const tipoCulinaria = tiposCulinariaPorId[prato.id_tipo_culinaria];
  const nomeCulinaria = tipoCulinaria ? tipoCulinaria.nome : '';
  const textoPorcoes = prato.rendimento === 1 ? '1 porção' : prato.rendimento + ' porções';

  const ingredientes = prato.ingredientes || [];
  const pillsIngredientes = ingredientes.map(function (ingrediente) {
    const produtoIngrediente = produtosPorId[ingrediente.id_produto];
    const unidadeIngrediente = produtoIngrediente ? nomeUnidade(produtoIngrediente.id_unidade) : '';
    return '<div class="ingrediente-pill">' +
      formatarQuantidade(ingrediente.quantidade) + ' ' +
      escaparHtml(unidadeIngrediente) + ' ' +
      escaparHtml(nomeProduto(ingrediente.id_produto)) +
      '</div>';
  }).join('');

  const passosPreparo = (prato.modo_preparo || '')
    .split('\n')
    .map(function (linha) { return linha.trim(); })
    .filter(function (linha) { return linha.length > 0; })
    .map(function (linha) { return '<li>' + escaparHtml(linha) + '</li>'; })
    .join('');

  cartao.innerHTML = '' +
    '<button class="caixa-item1" type="button">' +
      '<div class="caixa-item2">' +
        '<div class="prato-cabecalho-flex">' +
          '<span class="comida-item' + (prato.favorito ? '' : ' nao-essencial') + '">★</span>' +
          '<p class="text-item">' + escaparHtml(prato.nome) + '</p>' +
          '<svg xmlns="http://www.w3.org/2000/svg" class="prato-seta" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>' +
        '</div>' +
        '<div class="text-desc">' +
          '<span>' + escaparHtml(nomeCulinaria) + '</span>' +
          '<span>' + prato.tempo_preparo + ' min</span>' +
          '<span>' + textoPorcoes + '</span>' +
        '</div>' +
      '</div>' +
    '</button>' +
    '<div class="prato-corpo">' +
      (prato.descricao ? '<div class="text-desc1"><p>' + escaparHtml(prato.descricao) + '</p></div>' : '') +
      '<div class="ingredientes"><p>Ingredientes</p></div>' +
      '<div class="desc-ingredientes"><div class="desc-ingredientes1">' + pillsIngredientes + '</div></div>' +
      '<div class="preparo"><p>Modo de preparo</p><ol>' + passosPreparo + '</ol></div>' +
      '<div class="acoes-prato">' +
        '<button class="btn-preparar" type="button" data-id-prato="' + prato.id_prato + '">Preparar</button>' +
        '<button class="btn-remover" type="button" data-id-prato="' + prato.id_prato + '">Remover</button>' +
      '</div>' +
    '</div>';

  const botaoTopo = cartao.querySelector('.caixa-item1');
  const seta = cartao.querySelector('.prato-seta');
  botaoTopo.addEventListener('click', function () {
    cartao.classList.toggle('aberto');
    seta.classList.toggle('virar');
  });

  cartao.querySelector('.btn-remover').addEventListener('click', function (e) {
    e.stopPropagation();
    removerPrato(prato.id_prato);
  });

  cartao.querySelector('.btn-preparar').addEventListener('click', function (e) {
    e.stopPropagation();
    iniciarPreparo(prato.id_prato);
  });

  return cartao;
}

async function removerPrato(idPrato) {
  if (!confirm('Deseja realmente remover este prato do cardápio?')) return;

  try {
    const resposta = await fetch('/api/pratos/' + idPrato, { method: 'DELETE' });
    const corpo = await resposta.json();

    if (!resposta.ok) {
      throw new Error(corpo.erro || 'Não foi possível remover o prato.');
    }

    carregarCardapio();
  } catch (erro) {
    alert(erro.message);
  }
}

// ---------------------- Preparar prato (abater ingredientes do estoque) ----------------------

async function iniciarPreparo(idPrato) {
  try {
    const resposta = await fetch('/api/pratos/' + idPrato + '/disponibilidade');
    const dados = await resposta.json();

    if (!resposta.ok) {
      alert(dados.erro || 'Não foi possível verificar a disponibilidade dos ingredientes.');
      return;
    }

    if (dados.disponivel) {
      abrirModalConfirmarPreparo(idPrato);
    } else {
      abrirModalFaltantes(dados);
    }
  } catch (erro) {
    console.error('Erro ao verificar disponibilidade:', erro);
    alert('Não foi possível verificar a disponibilidade dos ingredientes.');
  }
}

function abrirModalConfirmarPreparo(idPrato) {
  idPratoEmPreparo = idPrato;
  mostrarFeedback(feedbackConfirmarPreparo, '', '');
  btnSimPreparar.disabled = false;
  btnNaoPreparar.disabled = false;
  modalConfirmarPreparoOverlay.classList.add('aberto');
}

function fecharModalConfirmarPreparo() {
  modalConfirmarPreparoOverlay.classList.remove('aberto');
  idPratoEmPreparo = null;
}

async function confirmarPreparo() {
  if (!idPratoEmPreparo) return;

  btnSimPreparar.disabled = true;
  btnNaoPreparar.disabled = true;

  try {
    const resposta = await fetch('/api/pratos/' + idPratoEmPreparo + '/preparar', { method: 'POST' });
    const corpo = await resposta.json();

    if (!resposta.ok) {
      throw new Error(corpo.erro || 'Não foi possível preparar o prato.');
    }

    mostrarFeedback(feedbackConfirmarPreparo, corpo.mensagem || 'Prato preparado com sucesso!', 'sucesso');
    setTimeout(function () {
      fecharModalConfirmarPreparo();
      carregarCardapio();
    }, 1000);
  } catch (erro) {
    mostrarFeedback(feedbackConfirmarPreparo, erro.message, 'erro');
    btnSimPreparar.disabled = false;
    btnNaoPreparar.disabled = false;
  }
}

function criarSvgConcluido() {
  return '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="m9 12 2 2 4-4"></path></svg>';
}

function criarSvgCarrinho() {
  return '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1" /><circle cx="19" cy="21" r="1" /><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12" /></svg>';
}

function abrirModalFaltantes(dados) {
  const lista = document.getElementById('listaFaltantesPrato');
  lista.innerHTML = dados.itens.map(function (item) {
    if (item.suficiente) {
      return '' +
        '<div class="item-disponivel">' +
          '<span>' + formatarQuantidade(item.quantidade_necessaria) + ' ' + escaparHtml(item.unidade) + ' de ' + escaparHtml(item.produto) + '</span>' +
          criarSvgConcluido() +
        '</div>';
    }
    return '' +
      '<div class="item-faltante">' +
        '<span>Comprar ' + formatarQuantidade(item.quantidade_faltante) + ' ' + escaparHtml(item.unidade) + ' de ' + escaparHtml(item.produto) + '</span>' +
        criarSvgCarrinho() +
      '</div>';
  }).join('');

  modalFaltantesOverlay.classList.add('aberto');
}

function fecharModalFaltantes() {
  modalFaltantesOverlay.classList.remove('aberto');
}

// ---------------------- Modal: Novo Prato ----------------------

function criarLinhaIngrediente() {
  const linha = document.createElement('div');
  linha.className = 'linha-ingrediente';

  const opcoesProdutos = produtosCache.map(function (produto) {
    return '<option value="' + produto.id_produto + '">' + escaparHtml(produto.nome) + '</option>';
  }).join('');

  linha.innerHTML = '' +
    '<select class="select-ingrediente-produto">' +
      '<option value="" disabled selected>Selecione</option>' +
      opcoesProdutos +
    '</select>' +
    '<input type="number" class="input-ingrediente-qtd" min="0" step="any" placeholder="Qtd">' +
    '<span class="unidade-ingrediente">unidade</span>' +
    '<button type="button" class="btn-remover-ingrediente" aria-label="Remover ingrediente">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
        '<polyline points="3 6 5 6 21 6" />' +
        '<path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />' +
        '<path d="M10 11v6" />' +
        '<path d="M14 11v6" />' +
        '<path d="M9 6V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2" />' +
      '</svg>' +
    '</button>';

  const select = linha.querySelector('.select-ingrediente-produto');
  const unidadeSpan = linha.querySelector('.unidade-ingrediente');

  select.addEventListener('change', function () {
    const produto = produtosPorId[select.value];
    unidadeSpan.textContent = produto ? nomeUnidade(produto.id_unidade) : 'unidade';
  });

  linha.querySelector('.btn-remover-ingrediente').addEventListener('click', function () {
    const linhas = listaIngredientesPrato.querySelectorAll('.linha-ingrediente');
    if (linhas.length > 1) {
      linha.remove();
    } else {
      select.value = '';
      linha.querySelector('.input-ingrediente-qtd').value = '';
      unidadeSpan.textContent = 'unidade';
    }
  });

  return linha;
}

function popularIngredientesIniciais() {
  listaIngredientesPrato.innerHTML = '';
  listaIngredientesPrato.appendChild(criarLinhaIngrediente());
  listaIngredientesPrato.appendChild(criarLinhaIngrediente());
}

function popularDatalistCulinaria() {
  listaTiposCulinaria.innerHTML = tiposCulinariaCache.map(function (tipo) {
    return '<option value="' + escaparHtml(tipo.nome) + '">';
  }).join('');
}

async function abrirModalPrato() {
  formNovoPrato.reset();
  mostrarFeedback(feedbackModalPrato, '', '');

  if (produtosCache.length === 0) await carregarProdutosCache();
  if (tiposCulinariaCache.length === 0) await carregarTiposCulinariaCache();

  popularDatalistCulinaria();
  popularIngredientesIniciais();

  modalPratoOverlay.classList.add('aberto');
}

function fecharModalPrato() {
  modalPratoOverlay.classList.remove('aberto');
}

async function obterIdTipoCulinaria(nomeDigitado) {
  const nomeNormalizado = nomeDigitado.trim().toLowerCase();
  const existente = tiposCulinariaCache.find(function (tipo) {
    return tipo.nome.trim().toLowerCase() === nomeNormalizado;
  });

  if (existente) return existente.id_tipo_culinaria;

  const resposta = await fetch('/api/tipos-culinaria', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nome: nomeDigitado.trim() }),
  });

  const corpo = await resposta.json();

  if (!resposta.ok) {
    throw new Error(corpo.erro || 'Não foi possível salvar o tipo de culinária.');
  }

  tiposCulinariaCache.push(corpo);
  tiposCulinariaPorId[corpo.id_tipo_culinaria] = corpo;
  return corpo.id_tipo_culinaria;
}

function coletarIngredientesDoFormulario() {
  const ingredientes = [];

  listaIngredientesPrato.querySelectorAll('.linha-ingrediente').forEach(function (linha) {
    const idProduto = linha.querySelector('.select-ingrediente-produto').value;
    const quantidade = linha.querySelector('.input-ingrediente-qtd').value;

    if (idProduto && quantidade && Number(quantidade) > 0) {
      ingredientes.push({ id_produto: Number(idProduto), quantidade: Number(quantidade) });
    }
  });

  return ingredientes;
}

async function tratarSubmitNovoPrato(evento) {
  evento.preventDefault();

  const nome = document.getElementById('inputNomePrato').value.trim();
  const descricao = document.getElementById('inputDescricaoPrato').value.trim();
  const culinaria = document.getElementById('inputCulinariaPrato').value.trim();
  const tempoPreparo = document.getElementById('inputTempoPrato').value;
  const porcoes = document.getElementById('inputPorcoesPrato').value;
  const favorito = document.getElementById('inputFavoritoPrato').checked;
  const modoPreparo = document.getElementById('inputModoPreparoPrato').value.trim();

  if (!nome || !culinaria || !tempoPreparo || !porcoes || !modoPreparo) {
    mostrarFeedback(feedbackModalPrato, 'Preencha nome, culinária, tempo, porções e modo de preparo.', 'erro');
    return;
  }

  const ingredientes = coletarIngredientesDoFormulario();
  if (ingredientes.length === 0) {
    mostrarFeedback(feedbackModalPrato, 'Adicione ao menos um ingrediente.', 'erro');
    return;
  }

  try {
    const idTipoCulinaria = await obterIdTipoCulinaria(culinaria);

    const resposta = await fetch('/api/pratos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nome: nome,
        descricao: descricao || null,
        id_tipo_culinaria: idTipoCulinaria,
        tempo_preparo: Number(tempoPreparo),
        rendimento: Number(porcoes),
        modo_preparo: modoPreparo,
        favorito: favorito,
        ingredientes: ingredientes,
      }),
    });

    const corpo = await resposta.json();

    if (!resposta.ok) {
      throw new Error(corpo.erro || 'Não foi possível criar o prato.');
    }

    fecharModalPrato();
    carregarCardapio();
  } catch (erro) {
    mostrarFeedback(feedbackModalPrato, erro.message, 'erro');
  }
}

// ---------------------- Inicialização dos modais ----------------------

var modalPratoOverlay, formNovoPrato, feedbackModalPrato, listaIngredientesPrato, listaTiposCulinaria;
var modalConfirmarPreparoOverlay, feedbackConfirmarPreparo, btnSimPreparar, btnNaoPreparar;
var modalFaltantesOverlay;

function inicializarModais() {
  modalPratoOverlay = document.getElementById('modalPratoOverlay');
  formNovoPrato = document.getElementById('formNovoPrato');
  feedbackModalPrato = document.getElementById('feedbackModalPrato');
  listaIngredientesPrato = document.getElementById('listaIngredientesPrato');
  listaTiposCulinaria = document.getElementById('listaTiposCulinaria');

  modalConfirmarPreparoOverlay = document.getElementById('modalConfirmarPreparoOverlay');
  feedbackConfirmarPreparo = document.getElementById('feedbackConfirmarPreparo');
  btnSimPreparar = document.getElementById('btnSimPreparar');
  btnNaoPreparar = document.getElementById('btnNaoPreparar');

  modalFaltantesOverlay = document.getElementById('modalFaltantesOverlay');

  const btnNovoPrato = document.getElementById('btnNovoPrato');
  const fecharModalPratoBtn = document.getElementById('fecharModalPrato');
  const cancelarModalPratoBtn = document.getElementById('cancelarModalPrato');
  const fecharModalConfirmarPreparoBtn = document.getElementById('fecharModalConfirmarPreparo');
  const fecharModalFaltantesBtn = document.getElementById('fecharModalFaltantes');
  const btnAdicionarIngrediente = document.getElementById('btnAdicionarIngrediente');

  btnNovoPrato.addEventListener('click', abrirModalPrato);
  fecharModalPratoBtn.addEventListener('click', fecharModalPrato);
  cancelarModalPratoBtn.addEventListener('click', fecharModalPrato);
  formNovoPrato.addEventListener('submit', tratarSubmitNovoPrato);

  btnAdicionarIngrediente.addEventListener('click', function () {
    listaIngredientesPrato.appendChild(criarLinhaIngrediente());
  });

  fecharModalConfirmarPreparoBtn.addEventListener('click', fecharModalConfirmarPreparo);
  btnNaoPreparar.addEventListener('click', fecharModalConfirmarPreparo);
  btnSimPreparar.addEventListener('click', confirmarPreparo);

  fecharModalFaltantesBtn.addEventListener('click', fecharModalFaltantes);

  // Fecha ao clicar fora do conteúdo do modal
  modalPratoOverlay.addEventListener('click', function (e) {
    if (e.target === modalPratoOverlay) fecharModalPrato();
  });
  modalConfirmarPreparoOverlay.addEventListener('click', function (e) {
    if (e.target === modalConfirmarPreparoOverlay) fecharModalConfirmarPreparo();
  });
  modalFaltantesOverlay.addEventListener('click', function (e) {
    if (e.target === modalFaltantesOverlay) fecharModalFaltantes();
  });

  // Fecha com a tecla Esc
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (modalPratoOverlay.classList.contains('aberto')) fecharModalPrato();
    if (modalConfirmarPreparoOverlay.classList.contains('aberto')) fecharModalConfirmarPreparo();
    if (modalFaltantesOverlay.classList.contains('aberto')) fecharModalFaltantes();
  });
}
