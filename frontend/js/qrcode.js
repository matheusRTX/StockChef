// ---------------------------------------------------------------------
// Elementos da página
// ---------------------------------------------------------------------

// Abas Entrada / Saída
const botoes = document.querySelectorAll('.btn');
const abaEntrada = document.getElementById('aba_entrada');
const abaSaida = document.getElementById('aba_saida');

// Select de produtos (controlado pelo Choices.js) — fallback manual
const selectIngredientes = document.getElementById('ingredientes');

// Cards de registro de movimentação
const cartaoEntrada = document.getElementById('ent');
const cartaoSaida = document.getElementById('sai');

// Cards dinâmicos (item já cadastrado / item novo)
const cartaoItemEncontrado = document.getElementById('cartao-item-encontrado');
const cartaoNovoItem = document.getElementById('cartao-novo-item');

// Elementos que trocam de cor conforme a aba (verde = entrada / vermelho = saída)
const aplicativo = document.getElementById('aplicativo');
const iconeQr = document.getElementById('icone-qr');

// Scanner de câmera
const conteudoQrParado = document.getElementById('conteudo-qr-parado');
const conteudoQrEscaneando = document.getElementById('conteudo-qr-escaneando');
const btnEscanear = document.getElementById('btn-escanear');
const btnPararScanner = document.getElementById('btn-parar-scanner');
const scannerErroEl = document.getElementById('scanner-erro');

const ICONE_VERDE = '/static/imagens/imagem.svg';
const ICONE_VERMELHO = '/static/imagens/imagem-vermelha.svg';

// ---------------------------------------------------------------------
// Estado da página
// ---------------------------------------------------------------------

let scannedCode = null;      // código lido que NÃO corresponde a nenhum produto
let produtoAtual = null;     // produto encontrado (por scan ou seleção manual)
let allItems = [];           // cache de /api/produtos
let estoquePorProduto = {};  // id_produto -> { categoria, unidade, quantidade_total }

// Inicializa o Choices.js (a lista de produtos é preenchida depois, via API).
// O <select> começa vazio — o placeholder é adicionado manualmente em
// carregarProdutos(), então NÃO usamos a opção "placeholder: true" aqui
// (evita duplicar o "Selecione um item..." na lista).
const choicesIngredientes = new Choices(selectIngredientes, {
    searchEnabled: false,
    shouldSort: false,
    itemSelectText: '',
});

// ---------------------------------------------------------------------
// Abas Entrada / Saída
// ---------------------------------------------------------------------

botoes.forEach(botao => {
    botao.addEventListener('click', () => {
        botoes.forEach(b => b.classList.remove('ativa'));
        botao.classList.add('ativa');

        atualizarTema();
        atualizarCartaoVisivel();
        ajustarCamposNovoItem();
    });
});

// Choices.js dispara um 'change' nativo no <select> original quando o
// usuário escolhe um item, então basta escutar esse evento normalmente.
selectIngredientes.addEventListener('change', () => {
    const idProduto = selectIngredientes.value;

    if (!idProduto) {
        resetarEstadoDinamico();
        return;
    }

    const produto = allItems.find(p => String(p.id_produto) === String(idProduto));
    if (produto) {
        selecionarProduto(produto);
    }
});

function abaAtivaEhEntrada() {
    return abaEntrada.classList.contains('ativa');
}

// Mostra o card de Entrada ou Saída apenas quando um produto (encontrado
// via scan ou selecionado manualmente) está definido.
function atualizarCartaoVisivel() {
    const temProduto = !!produtoAtual;
    const entradaAtiva = abaAtivaEhEntrada();

    cartaoEntrada.style.display = (temProduto && entradaAtiva) ? 'block' : 'none';
    cartaoSaida.style.display = (temProduto && !entradaAtiva) ? 'block' : 'none';
}

// Alterna o tema entre verde (Entrada) e vermelho (Saída):
// afeta o botão "Escanear QR Code", o símbolo do QR e a borda da quantidade.
function atualizarTema() {
    const saidaAtiva = abaSaida.classList.contains('ativa');

    aplicativo.classList.toggle('tema-saida', saidaAtiva);
    iconeQr.src = saidaAtiva ? ICONE_VERMELHO : ICONE_VERDE;
}

// ---------------------------------------------------------------------
// Carrega produtos, estoque, categorias e unidades (banco de dados)
// ---------------------------------------------------------------------

async function carregarProdutosEEstoque() {
    try {
        const [respostaProdutos, respostaEstoque] = await Promise.all([
            fetch('/api/produtos'),
            fetch('/api/estoque/listar'),
        ]);

        if (!respostaProdutos.ok) throw new Error('Não foi possível carregar os produtos.');
        if (!respostaEstoque.ok) throw new Error('Não foi possível carregar o estoque.');

        allItems = await respostaProdutos.json();
        const estoque = await respostaEstoque.json();

        estoquePorProduto = {};
        estoque.forEach(item => {
            estoquePorProduto[item.id_produto] = {
                categoria: item.categoria,
                unidade: item.unidade,
                quantidade_total: item.quantidade_total,
            };
        });

        const opcoes = [
            { value: '', label: 'Selecione um item...', placeholder: true, selected: true },
            ...allItems.map(produto => ({
                value: String(produto.id_produto),
                label: produto.nome,
            })),
        ];

        choicesIngredientes.clearStore();
        choicesIngredientes.setChoices(opcoes, 'value', 'label', true);
    } catch (erro) {
        console.error('Erro ao carregar produtos do estoque:', erro);
    }
}

async function carregarCategorias(selectAlvo) {
    try {
        const resposta = await fetch('/api/categorias');
        if (!resposta.ok) throw new Error('Não foi possível carregar as categorias.');

        const categorias = await resposta.json();

        selectAlvo.innerHTML = '<option value="">Selecione...</option>';
        categorias.forEach(categoria => {
            const opcao = document.createElement('option');
            opcao.value = categoria.id_categoria;
            opcao.textContent = categoria.nome;
            selectAlvo.appendChild(opcao);
        });
    } catch (erro) {
        console.error('Erro ao carregar categorias:', erro);
    }
}

async function carregarUnidades(selectAlvo) {
    try {
        const resposta = await fetch('/api/unidades-medida');
        if (!resposta.ok) throw new Error('Não foi possível carregar as unidades de medida.');

        const unidades = await resposta.json();

        selectAlvo.innerHTML = '<option value="">Selecione...</option>';
        unidades.forEach(unidade => {
            const opcao = document.createElement('option');
            opcao.value = unidade.id_unidade;
            opcao.textContent = unidade.sigla;
            selectAlvo.appendChild(opcao);
        });
    } catch (erro) {
        console.error('Erro ao carregar unidades de medida:', erro);
    }
}

// ---------------------------------------------------------------------
// Scanner de câmera (componente QrScanner)
// ---------------------------------------------------------------------

const scanner = new QrScanner({
    readerId: 'leitor-camera',
    onScan: tratarCodigoEscaneado,
    onError: mostrarErroScanner,
});

btnEscanear.addEventListener('click', () => {
    mostrarErroScanner('');
    conteudoQrParado.style.display = 'none';
    conteudoQrEscaneando.style.display = 'flex';
    scanner.iniciar();
});

btnPararScanner.addEventListener('click', () => {
    scanner.parar().then(voltarParaTelaInicialDoScanner);
});

function voltarParaTelaInicialDoScanner() {
    conteudoQrEscaneando.style.display = 'none';
    conteudoQrParado.style.display = 'flex';
}

function mostrarErroScanner(mensagem) {
    voltarParaTelaInicialDoScanner();
    scannerErroEl.textContent = mensagem || '';
}

function tratarCodigoEscaneado(codigo) {
    voltarParaTelaInicialDoScanner();
    choicesIngredientes.removeActiveItems();

    const produtoExistente = allItems.find(p => p.qr_code === codigo);

    if (produtoExistente) {
        selecionarProduto(produtoExistente);
    } else {
        mostrarNovoItem(codigo);
    }
}

// Limpa a câmera se a pessoa sair da página com o scanner ligado
window.addEventListener('beforeunload', () => scanner.destruir());

// ---------------------------------------------------------------------
// Fluxo: item já cadastrado
// ---------------------------------------------------------------------

function selecionarProduto(produto) {
    scannedCode = null;
    produtoAtual = produto;

    cartaoNovoItem.style.display = 'none';

    const dadosEstoque = estoquePorProduto[produto.id_produto] || {};

    document.getElementById('info-nome-item').textContent = produto.nome;
    document.getElementById('info-categoria-item').textContent = dadosEstoque.categoria || '—';

    const quantidade = dadosEstoque.quantidade_total !== undefined ? dadosEstoque.quantidade_total : 0;
    const unidade = dadosEstoque.unidade || '';
    document.getElementById('info-estoque-item').textContent = formatarQuantidade(quantidade) + (unidade ? ' ' + unidade : '');

    cartaoItemEncontrado.style.display = 'block';

    // Reflete a seleção no select manual, caso o produto tenha vindo de um scan
    const valorAtual = String(produto.id_produto);
    if (selectIngredientes.value !== valorAtual) {
        choicesIngredientes.setChoiceByValue(valorAtual);
    }

    atualizarCartaoVisivel();
}

// ---------------------------------------------------------------------
// Fluxo: item não cadastrado (novo item)
// ---------------------------------------------------------------------

function mostrarNovoItem(codigo) {
    scannedCode = codigo;
    produtoAtual = null;

    cartaoItemEncontrado.style.display = 'none';
    cartaoEntrada.style.display = 'none';
    cartaoSaida.style.display = 'none';

    document.getElementById('titulo-novo-item').textContent = 'Novo Item — QR: ' + codigo;
    document.getElementById('novo-item-nome').value = '';
    document.getElementById('novo-item-categoria').value = '';
    document.getElementById('novo-item-unidade').value = '';
    document.getElementById('novo-item-quantidade').value = '';
    document.getElementById('novo-item-validade').value = '';
    mostrarFeedback(document.getElementById('feedback-novo-item'), '', '');

    ajustarCamposNovoItem();

    cartaoNovoItem.style.display = 'block';
}

// Na aba Entrada, o card de novo item também pede quantidade + validade e o
// botão vira "Cadastrar e Dar Entrada". Na aba Saída não existe estoque para
// tirar de um item que ainda não existe, então só é possível cadastrá-lo.
function ajustarCamposNovoItem() {
    if (cartaoNovoItem.style.display === 'none') return;

    const entradaAtiva = abaAtivaEhEntrada();
    const blocoQuantidade = document.getElementById('bloco-novo-item-quantidade');
    const blocoValidade = document.getElementById('bloco-novo-item-validade');
    const botao = document.getElementById('botao-novo-item');

    blocoQuantidade.style.display = entradaAtiva ? 'block' : 'none';
    blocoValidade.style.display = entradaAtiva ? 'block' : 'none';
    botao.textContent = entradaAtiva ? 'Cadastrar e Dar Entrada' : 'Cadastrar Item';
}

document.getElementById('botao-novo-item').addEventListener('click', tratarSubmitNovoItem);

async function tratarSubmitNovoItem() {
    const feedback = document.getElementById('feedback-novo-item');
    const entradaAtiva = abaAtivaEhEntrada();

    const nome = document.getElementById('novo-item-nome').value.trim();
    const idCategoria = document.getElementById('novo-item-categoria').value;
    const idUnidade = document.getElementById('novo-item-unidade').value;
    const quantidade = document.getElementById('novo-item-quantidade').value;
    const validade = document.getElementById('novo-item-validade').value;

    if (!nome || !idCategoria || !idUnidade) {
        mostrarFeedback(feedback, 'Preencha nome, categoria e unidade.', 'erro');
        return;
    }
    if (entradaAtiva && (!quantidade || Number(quantidade) <= 0)) {
        mostrarFeedback(feedback, 'Informe uma quantidade válida.', 'erro');
        return;
    }
    if (entradaAtiva && !validade) {
        mostrarFeedback(feedback, 'Informe a data de validade do lote.', 'erro');
        return;
    }

    try {
        const produto = await cadastrarProduto({
            nome,
            id_categoria: Number(idCategoria),
            id_unidade: Number(idUnidade),
            qr_code: scannedCode,
            estoque_minimo: 0,
        });

        if (entradaAtiva) {
            await enviarMovimentacao('Entrada', produto.id_produto, quantidade, validade);
            mostrarFeedback(feedback, 'Item cadastrado e entrada registrada com sucesso!', 'sucesso');
        } else {
            mostrarFeedback(feedback, 'Item cadastrado com sucesso!', 'sucesso');
        }

        setTimeout(async () => {
            resetarEstadoDinamico();
            await carregarProdutosEEstoque();
        }, 1200);
    } catch (erro) {
        mostrarFeedback(feedback, mapearMensagemErro(erro.message), 'erro');
    }
}

async function cadastrarProduto(dados) {
    const resposta = await fetch('/api/produtos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados),
    });

    const corpo = await resposta.json();

    if (!resposta.ok) {
        throw new Error(corpo.erro || 'Não foi possível cadastrar o item.');
    }

    return corpo;
}

// ---------------------------------------------------------------------
// Registrar Entrada / Registrar Saída (item já cadastrado)
// ---------------------------------------------------------------------

document.getElementById('botao').addEventListener('click', registrarEntrada);
document.getElementById('botao-saida').addEventListener('click', registrarSaida);

async function registrarEntrada() {
    const feedback = document.getElementById('feedback-entrada');

    if (!produtoAtual) {
        mostrarFeedback(feedback, 'Selecione um produto.', 'erro');
        return;
    }

    const quantidade = document.getElementById('quantidade-entrada').value;
    const validade = document.getElementById('validade-entrada').value;

    if (!validade) {
        mostrarFeedback(feedback, 'Informe a data de validade do lote.', 'erro');
        return;
    }
    if (!quantidade || Number(quantidade) <= 0) {
        mostrarFeedback(feedback, 'Informe uma quantidade válida.', 'erro');
        return;
    }

    try {
        await enviarMovimentacao('Entrada', produtoAtual.id_produto, quantidade, validade);
        mostrarFeedback(feedback, 'Entrada registrada com sucesso!', 'sucesso');
        setTimeout(async () => {
            resetarEstadoDinamico();
            await carregarProdutosEEstoque();
        }, 1200);
    } catch (erro) {
        mostrarFeedback(feedback, mapearMensagemErro(erro.message), 'erro');
    }
}

async function registrarSaida() {
    const feedback = document.getElementById('feedback-saida');

    if (!produtoAtual) {
        mostrarFeedback(feedback, 'Selecione um produto.', 'erro');
        return;
    }

    const quantidade = document.getElementById('quantidade-saida').value;

    if (!quantidade || Number(quantidade) <= 0) {
        mostrarFeedback(feedback, 'Informe uma quantidade válida.', 'erro');
        return;
    }

    try {
        // Sem informar validade: o backend abate os lotes em FIFO/FEFO,
        // consumindo primeiro os que vencem mais cedo.
        await enviarMovimentacao('Saida', produtoAtual.id_produto, quantidade, null);
        mostrarFeedback(feedback, 'Saída registrada com sucesso!', 'sucesso');
        setTimeout(async () => {
            resetarEstadoDinamico();
            await carregarProdutosEEstoque();
        }, 1200);
    } catch (erro) {
        mostrarFeedback(feedback, mapearMensagemErro(erro.message), 'erro');
    }
}

async function enviarMovimentacao(tipo, idProduto, quantidade, validade) {
    const item = {
        id_produto: Number(idProduto),
        quantidade: Number(quantidade),
    };
    if (validade) item.validade = validade;

    const resposta = await fetch('/api/movimentacoes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tipo, itens: [item] }),
    });

    const dados = await resposta.json();

    if (!resposta.ok) {
        throw new Error(dados.erro || 'Não foi possível registrar a movimentação.');
    }

    return dados;
}

// Deixa a mensagem de estoque insuficiente mais direta para quem está usando o app.
function mapearMensagemErro(mensagem) {
    if (mensagem && mensagem.toLowerCase().includes('insuficiente')) {
        return 'Estoque insuficiente!';
    }
    return mensagem;
}

// ---------------------------------------------------------------------
// Helpers de UI
// ---------------------------------------------------------------------

function mostrarFeedback(elemento, mensagem, tipo) {
    if (!elemento) return;
    elemento.textContent = mensagem;
    elemento.className = 'feedback ' + tipo;
}

function formatarQuantidade(valor) {
    const numero = Number(valor);
    if (Number.isNaN(numero)) return String(valor);
    if (Number.isInteger(numero)) return numero.toString();
    return numero.toFixed(2).replace(/0+$/, '').replace(/\.$/, '');
}

// Volta a página para o estado inicial: nenhum item selecionado/escaneado.
function resetarEstadoDinamico() {
    scannedCode = null;
    produtoAtual = null;

    choicesIngredientes.removeActiveItems();
    selectIngredientes.value = '';

    cartaoItemEncontrado.style.display = 'none';
    cartaoNovoItem.style.display = 'none';
    cartaoEntrada.style.display = 'none';
    cartaoSaida.style.display = 'none';

    document.getElementById('quantidade-entrada').value = '';
    document.getElementById('validade-entrada').value = '';
    document.getElementById('quantidade-saida').value = '';

    mostrarFeedback(document.getElementById('feedback-entrada'), '', '');
    mostrarFeedback(document.getElementById('feedback-saida'), '', '');
}

// ---------------------------------------------------------------------
// Inicialização
// ---------------------------------------------------------------------

atualizarTema();
atualizarCartaoVisivel();
carregarProdutosEEstoque();
carregarCategorias(document.getElementById('novo-item-categoria'));
carregarUnidades(document.getElementById('novo-item-unidade'));
