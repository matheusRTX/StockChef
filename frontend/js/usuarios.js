document.addEventListener('DOMContentLoaded', () => {
    inicializarPagina();
    carregarFuncionarios();
});

const ROTULOS_STATUS = {
    Pendente: 'etiqueta-pendente',
    Aprovado: 'etiqueta-aprovado',
    Recusado: 'etiqueta-recusado',
};

let listaFuncionariosEl = null;
let feedbackListaEl = null;
let funcionariosVazioEl = null;

let modalFuncionarioOverlay = null;
let formFuncionario = null;
let feedbackModalEl = null;
let inputIdFuncionario = null;

function mostrarFeedback(elemento, mensagem, tipo) {
    elemento.textContent = mensagem || '';
    elemento.className = 'feedback' + (tipo ? ' ' + tipo : '');
}

async function carregarFuncionarios() {
    mostrarFeedback(feedbackListaEl, '', '');
    try {
        const resposta = await fetch('/api/usuarios');
        if (!resposta.ok) {
            throw new Error((await resposta.json()).erro || 'Não foi possível carregar os usuários.');
        }
        const funcionarios = await resposta.json();
        renderizarLista(funcionarios);
    } catch (erro) {
        mostrarFeedback(feedbackListaEl, erro.message, 'erro');
    }
}

function renderizarLista(funcionarios) {
    listaFuncionariosEl.innerHTML = '';

    if (!funcionarios.length) {
        funcionariosVazioEl.style.display = 'block';
        return;
    }
    funcionariosVazioEl.style.display = 'none';

    funcionarios.forEach(funcionario => {
        listaFuncionariosEl.appendChild(criarCardFuncionario(funcionario));
    });
}

function criarCardFuncionario(funcionario) {
    const card = document.createElement('div');
    card.className = 'cartao-funcionario';

    const classeStatus = ROTULOS_STATUS[funcionario.status] || 'etiqueta-pendente';

    card.innerHTML = `
        <div class="cartao-funcionario-topo">
            <div>
                <p class="cartao-funcionario-nome">${funcionario.nome}</p>
                <p class="cartao-funcionario-email">${funcionario.email}</p>
            </div>
            <div class="etiquetas">
                <span class="etiqueta ${classeStatus}">${funcionario.status}</span>
                ${!funcionario.ativo ? '<span class="etiqueta etiqueta-inativo">Inativo</span>' : ''}
            </div>
        </div>
        <div class="cartao-funcionario-acoes">
            ${funcionario.status === 'Pendente'
                ? '<button type="button" class="btn-aprovar">Aprovar</button>'
                : ''}
            <button type="button" class="btn-editar">Editar</button>
            ${funcionario.ativo
                ? '<button type="button" class="btn-inativar">Inativar</button>'
                : ''}
        </div>
    `;

    const btnAprovar = card.querySelector('.btn-aprovar');
    if (btnAprovar) {
        btnAprovar.addEventListener('click', () => tratarAprovar(funcionario.id_usuario));
    }

    card.querySelector('.btn-editar').addEventListener('click', () => abrirModalFuncionario(funcionario));

    const btnInativar = card.querySelector('.btn-inativar');
    if (btnInativar) {
        btnInativar.addEventListener('click', () => tratarInativar(funcionario));
    }

    return card;
}

async function tratarAprovar(idUsuario) {
    try {
        const resposta = await fetch(`/api/usuarios/${idUsuario}/aprovar`, { method: 'POST' });
        if (!resposta.ok) {
            throw new Error((await resposta.json()).erro || 'Não foi possível aprovar o funcionário.');
        }
        await carregarFuncionarios();
    } catch (erro) {
        mostrarFeedback(feedbackListaEl, erro.message, 'erro');
    }
}

async function tratarInativar(funcionario) {
    const confirmou = confirm(`Inativar o acesso de ${funcionario.nome}? Ele não poderá mais acessar o sistema.`);
    if (!confirmou) return;

    try {
        const resposta = await fetch(`/api/usuarios/${funcionario.id_usuario}`, { method: 'DELETE' });
        if (!resposta.ok) {
            throw new Error((await resposta.json()).erro || 'Não foi possível inativar o funcionário.');
        }
        await carregarFuncionarios();
    } catch (erro) {
        mostrarFeedback(feedbackListaEl, erro.message, 'erro');
    }
}

function abrirModalFuncionario(funcionario) {
    formFuncionario.reset();
    mostrarFeedback(feedbackModalEl, '', '');

    inputIdFuncionario.value = funcionario.id_usuario;
    document.getElementById('inputNomeFuncionario').value = funcionario.nome || '';
    document.getElementById('inputEmailFuncionario').value = funcionario.email || '';
    document.getElementById('selectStatusFuncionario').value = funcionario.status;
    document.getElementById('inputAtivoFuncionario').checked = !!funcionario.ativo;

    modalFuncionarioOverlay.classList.add('aberto');
}

function fecharModalFuncionario() {
    modalFuncionarioOverlay.classList.remove('aberto');
}

async function tratarSubmitFuncionario(evento) {
    evento.preventDefault();

    const idFuncionario = inputIdFuncionario.value;
    const nome = document.getElementById('inputNomeFuncionario').value.trim();
    const email = document.getElementById('inputEmailFuncionario').value.trim();
    const senha = document.getElementById('inputSenhaFuncionario').value;
    const status = document.getElementById('selectStatusFuncionario').value;
    const ativo = document.getElementById('inputAtivoFuncionario').checked;

    if (!nome || !email) {
        mostrarFeedback(feedbackModalEl, 'Preencha nome e e-mail.', 'erro');
        return;
    }

    const corpo = { nome, email, status, ativo };
    if (senha) corpo.senha = senha;

    try {
        const resposta = await fetch(`/api/usuarios/${idFuncionario}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(corpo),
        });
        if (!resposta.ok) {
            throw new Error((await resposta.json()).erro || 'Não foi possível salvar as alterações.');
        }
        fecharModalFuncionario();
        await carregarFuncionarios();
    } catch (erro) {
        mostrarFeedback(feedbackModalEl, erro.message, 'erro');
    }
}

function inicializarPagina() {
    listaFuncionariosEl = document.getElementById('listaFuncionarios');
    feedbackListaEl = document.getElementById('feedbackLista');
    funcionariosVazioEl = document.getElementById('funcionariosVazio');

    modalFuncionarioOverlay = document.getElementById('modalFuncionarioOverlay');
    formFuncionario = document.getElementById('formFuncionario');
    feedbackModalEl = document.getElementById('feedbackModalFuncionario');
    inputIdFuncionario = document.getElementById('inputIdFuncionario');

    document.getElementById('fecharModalFuncionario').addEventListener('click', fecharModalFuncionario);
    modalFuncionarioOverlay.addEventListener('click', (evento) => {
        if (evento.target === modalFuncionarioOverlay) fecharModalFuncionario();
    });
    formFuncionario.addEventListener('submit', tratarSubmitFuncionario);
}
