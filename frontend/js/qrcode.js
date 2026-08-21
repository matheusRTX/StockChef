// Abas Entrada / Saída
const botoes = document.querySelectorAll('.btn');
const abaEntrada = document.getElementById('aba_entrada');
const abaSaida = document.getElementById('aba_saida');

// Select de produtos (controlado pelo Choices.js)
const selectIngredientes = document.getElementById('ingredientes');

// Cards de registro
const cartaoEntrada = document.getElementById('ent');
const cartaoSaida = document.getElementById('sai');

// Elementos que trocam de cor conforme a aba (verde = entrada / vermelho = saída)
const aplicativo = document.getElementById('aplicativo');
const iconeQr = document.getElementById('icone-qr');

const ICONE_VERDE = '/static/imagens/imagem.svg';
const ICONE_VERMELHO = '/static/imagens/imagem-vermelha.svg';

// Inicializa o Choices.js (a lista de produtos é preenchida depois, via API).
// O <select> começa vazio — o placeholder é adicionado manualmente em
// carregarProdutos(), então NÃO usamos a opção "placeholder: true" aqui
// (evita duplicar o "Selecione um item..." na lista).
const choicesIngredientes = new Choices(selectIngredientes, {
    searchEnabled: false,
    shouldSort: false,
    itemSelectText: '',
});

botoes.forEach(botao => {
    botao.addEventListener('click', () => {
        // 1. Remove a classe 'ativa' de todos os botões
        botoes.forEach(b => b.classList.remove('ativa'));

        // 2. Adiciona a classe 'ativa' apenas no botão que foi clicado
        botao.classList.add('ativa');

        // 3. Atualiza qual card deve aparecer
        atualizarCartaoVisivel();

        // 4. Atualiza o tema de cor (verde/vermelho) da página
        atualizarTema();
    });
});

// Choices.js dispara um 'change' nativo no <select> original quando o
// usuário escolhe um item, então basta escutar esse evento normalmente.
selectIngredientes.addEventListener('change', atualizarCartaoVisivel);

function atualizarCartaoVisivel() {
    const produtoSelecionado = selectIngredientes.value !== '';
    const entradaAtiva = abaEntrada.classList.contains('ativa');

    cartaoEntrada.style.display = (produtoSelecionado && entradaAtiva) ? 'block' : 'none';
    cartaoSaida.style.display = (produtoSelecionado && !entradaAtiva) ? 'block' : 'none';
}

// Alterna o tema entre verde (Entrada) e vermelho (Saída):
// afeta o botão "Escanear QR Code", o símbolo do QR e a borda da quantidade.
function atualizarTema() {
    const saidaAtiva = abaSaida.classList.contains('ativa');

    aplicativo.classList.toggle('tema-saida', saidaAtiva);
    iconeQr.src = saidaAtiva ? ICONE_VERMELHO : ICONE_VERDE;
}

// ---------------------------------------------------------------------
// Carrega os produtos do estoque (banco de dados) para o select manual
// ---------------------------------------------------------------------
async function carregarProdutos() {
    try {
        const resposta = await fetch('/api/produtos');
        if (!resposta.ok) throw new Error('Não foi possível carregar os produtos.');

        const produtos = await resposta.json();

        const opcoes = [
            { value: '', label: 'Selecione um item...', placeholder: true, selected: true },
            ...produtos.map(produto => ({
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

// ---------------------------------------------------------------------
// Registrar Entrada / Registrar Saída
// ---------------------------------------------------------------------
document.getElementById('botao').addEventListener('click', registrarEntrada);
document.getElementById('botao-saida').addEventListener('click', registrarSaida);

async function registrarEntrada() {
    const feedback = document.getElementById('feedback-entrada');
    const idProduto = selectIngredientes.value;
    const quantidade = document.getElementById('quantidade-entrada').value;
    const validade = document.getElementById('validade-entrada').value;

    if (!idProduto) {
        mostrarFeedback(feedback, 'Selecione um produto.', 'erro');
        return;
    }
    if (!validade) {
        mostrarFeedback(feedback, 'Informe a data de validade do lote.', 'erro');
        return;
    }
    if (!quantidade || Number(quantidade) <= 0) {
        mostrarFeedback(feedback, 'Informe uma quantidade válida.', 'erro');
        return;
    }

    try {
        await enviarMovimentacao('Entrada', idProduto, quantidade, validade);
        mostrarFeedback(feedback, 'Entrada registrada com sucesso!', 'sucesso');
        setTimeout(() => resetarFormulario('entrada'), 1200);
    } catch (erro) {
        mostrarFeedback(feedback, erro.message, 'erro');
    }
}

async function registrarSaida() {
    const feedback = document.getElementById('feedback-saida');
    const idProduto = selectIngredientes.value;
    const quantidade = document.getElementById('quantidade-saida').value;
    const validade = document.getElementById('validade-saida').value;

    if (!idProduto) {
        mostrarFeedback(feedback, 'Selecione um produto.', 'erro');
        return;
    }
    if (!validade) {
        mostrarFeedback(feedback, 'Informe a data de validade do lote de onde sairá o produto.', 'erro');
        return;
    }
    if (!quantidade || Number(quantidade) <= 0) {
        mostrarFeedback(feedback, 'Informe uma quantidade válida.', 'erro');
        return;
    }

    try {
        await enviarMovimentacao('Saida', idProduto, quantidade, validade);
        mostrarFeedback(feedback, 'Saída registrada com sucesso!', 'sucesso');
        setTimeout(() => resetarFormulario('saida'), 1200);
    } catch (erro) {
        mostrarFeedback(feedback, erro.message, 'erro');
    }
}

async function enviarMovimentacao(tipo, idProduto, quantidade, validade) {
    const resposta = await fetch('/api/movimentacoes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            tipo,
            itens: [{
                id_produto: Number(idProduto),
                quantidade: Number(quantidade),
                validade,
            }],
        }),
    });

    const dados = await resposta.json();

    if (!resposta.ok) {
        throw new Error(dados.erro || 'Não foi possível registrar a movimentação.');
    }

    return dados;
}

function mostrarFeedback(elemento, mensagem, tipo) {
    if (!elemento) return;
    elemento.textContent = mensagem;
    elemento.className = 'feedback ' + tipo;
}

function resetarFormulario(tipo) {
    // Volta o select para "Selecione um item..." e esconde os cards de novo
    choicesIngredientes.removeActiveItems();
    selectIngredientes.value = '';

    document.getElementById(`quantidade-${tipo}`).value = 6;
    document.getElementById(`validade-${tipo}`).value = '';

    atualizarCartaoVisivel();

    // Recarrega a lista de produtos (estoque pode ter mudado) para a próxima operação
    carregarProdutos();
}

// Garante o estado correto ao carregar a página (nenhum produto selecionado ainda)
atualizarCartaoVisivel();
atualizarTema();
carregarProdutos();
