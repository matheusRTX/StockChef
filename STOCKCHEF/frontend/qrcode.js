// Seleciona todos os botões com a classe btn
const botoes = document.querySelectorAll('.btn');

botoes.forEach(botao => {
    botao.addEventListener('click', () => {
        // 1. Remove a classe 'ativa' de todos os botões
        botoes.forEach(b => b.classList.remove('ativa'));

        // 2. Adiciona a classe 'ativa' apenas no botão que foi clicado
        botao.classList.add('ativa');

        // (Opcional) Mostra no console qual botão foi clicado
        console.log(`Você mudou para: ${botao.innerText}`);
    });
});