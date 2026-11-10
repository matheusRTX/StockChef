var selectPeriodo = null;
var selectTipo = null;

document.addEventListener('DOMContentLoaded', function () {
  selectPeriodo = document.getElementById('filtro-periodo');
  selectTipo = document.getElementById('filtro-tipo');

  selectPeriodo.addEventListener('change', carregarHistorico);
  selectTipo.addEventListener('change', carregarHistorico);

  carregarHistorico();
});

async function carregarHistorico() {
  try {
    const params = new URLSearchParams({
      data: selectPeriodo.value,
      tipo: selectTipo.value,
    });

    const resposta = await fetch('/api/historico/listar?' + params.toString());

    if (resposta.status === 401) {
      window.location.href = '/login';
      return;
    }

    if (!resposta.ok) {
      throw new Error('Falha ao buscar histórico: ' + resposta.status);
    }

    const movimentacoes = await resposta.json();
    renderizarHistorico(movimentacoes);
  } catch (erro) {
    console.error('Erro ao carregar histórico:', erro);
  }
}

// ---------------------- Helpers de formatação ----------------------

function formatarQuantidade(valor) {
  const numero = Number(valor);
  if (Number.isInteger(numero)) return numero.toString();
  return numero.toFixed(2).replace(/0+$/, '').replace(/\.$/, '');
}

function formatarDataHora(dataIso) {
  if (!dataIso) return '';
  const data = new Date(dataIso);
  const dia = String(data.getDate()).padStart(2, '0');
  const mes = String(data.getMonth() + 1).padStart(2, '0');
  const ano = data.getFullYear();
  const horas = String(data.getHours()).padStart(2, '0');
  const minutos = String(data.getMinutes()).padStart(2, '0');
  return dia + '/' + mes + '/' + ano + ' às ' + horas + ':' + minutos;
}

function iconeSvg(classeTipo) {
  if (classeTipo === 'entrada') {
    return '' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" ' +
        'stroke-linecap="round" stroke-linejoin="round">' +
        '<line x1="12" y1="19" x2="12" y2="5" />' +
        '<polyline points="5 12 12 5 19 12" />' +
      '</svg>';
  }
  return '' +
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" ' +
      'stroke-linecap="round" stroke-linejoin="round">' +
      '<line x1="12" y1="5" x2="12" y2="19" />' +
      '<polyline points="19 12 12 19 5 12" />' +
    '</svg>';
}

// ---------------------- Renderização ----------------------

function criarCartaoMovimentacao(mov) {
  const cartao = document.createElement('div');
  cartao.className = 'cartao';

  const classeTipo = mov.tipo === 'Entrada' ? 'entrada' : 'saida';
  const sinal = mov.tipo === 'Entrada' ? '+' : '-';

  cartao.innerHTML = '' +
    '<div class="cartao2">' +
      '<div class="icone ' + classeTipo + '">' + iconeSvg(classeTipo) + '</div>' +
      '<div class="informacoes">' +
        '<p class="nome"></p>' +
        '<p class="data">' + formatarDataHora(mov.data_registro) + '</p>' +
      '</div>' +
    '</div>' +
    '<span class="etiqueta ' + classeTipo + '">' + sinal + formatarQuantidade(mov.quantidade) + ' ' + mov.unidade + '</span>';

  // Usa textContent para o nome do produto, evitando problemas de HTML injetado.
  cartao.querySelector('.nome').textContent = mov.produto;

  return cartao;
}

function renderizarHistorico(movimentacoes) {
  const lista = document.getElementById('listaHistorico');
  const vazio = document.getElementById('historicoVazio');

  lista.querySelectorAll('.cartao').forEach(function (el) { el.remove(); });

  if (!movimentacoes || movimentacoes.length === 0) {
    if (vazio) vazio.style.display = 'block';
    return;
  }

  if (vazio) vazio.style.display = 'none';

  movimentacoes.forEach(function (mov) {
    lista.appendChild(criarCartaoMovimentacao(mov));
  });
}
