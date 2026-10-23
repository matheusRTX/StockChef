function aumentarDiv() {
    document.getElementById("cartao").classList.toggle("aberto");
}

document.querySelector('.btn-sugerir').addEventListener('click', async () => {
    const usarCardapio = document.querySelector('.switch input[type="checkbox"]').checked;
    const tipoCulinaria = document.querySelector('.input').value.trim();

    const btn = document.querySelector('.btn-sugerir');
    btn.textContent = 'Gerando sugestões...';
    btn.disabled = true;

    try {
        const res = await fetch('/api/ia/sugerir-pratos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                usar_cardapio: usarCardapio,
                tipo_culinaria: tipoCulinaria || null,
            }),
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.erro || 'Erro desconhecido');

        renderizarPratos(data.pratos);
    } catch (err) {
        alert('Erro ao gerar sugestões: ' + err.message);
    } finally {
        setTimeout(() => {
            btn.textContent = 'Sugerir Pratos com IA';
            btn.disabled = false;
        }, 10000);
    }
});

function renderizarPratos(pratos) {
    document.querySelectorAll('.card-ia').forEach(el => el.remove());

    const container = document.querySelector('.container');
    const nav = document.querySelector('.navegacao-inferior');

    pratos.forEach(prato => {
        const card = document.createElement('div');
        card.className = 'card-ia';

        const ingredientesHTML = prato.ingredientes.map(ing => {
            const disponivel = ing.disponivel;
            const cls = disponivel ? 'ia-utilizados' : 'ia-comprar';
            const icone = disponivel
                ? `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>`
                : `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>`;
            return `<div class="${cls}"><div class="ia-nome">${ing.quantidade} ${ing.unidade} ${ing.nome}</div><div class="ia-icone">${icone}</div></div>`;
        }).join('');

        const preparoHTML = Array.isArray(prato.modo_preparo)
            ? prato.modo_preparo.map((passo, i) => `${i + 1}. ${passo}`).join('<br>')
            : String(prato.modo_preparo || '');

        card.innerHTML = `
            <div class="flex">
                <div id="chapeu"><svg id="svg-chapeu" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21a1 1 0 0 0 1-1v-5.35c0-.457.316-.844.727-1.041a4 4 0 0 0-2.134-7.589 5 5 0 0 0-9.186 0 4 4 0 0 0-2.134 7.588c.411.198.727.585.727 1.041V20a1 1 0 0 0 1 1Z"/><path d="M6 17h12"/></svg></div>
                <div id="info-prato">
                    <div id="titulo-prato"><h2 id="titulo-info">${prato.nome}</h2></div>
                    <p class="subtitulo-prato">${prato.descricao}</p>
                </div>
            </div>
            <div id="card-vencendo">
                <svg id="svg-alerta" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
                <p class="subtitulo-vencendo">${prato.motivo}</p>
            </div>
            <div id="pessoas">
                <div id="tempo_de_preparo">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="10" x2="14" y1="2" y2="2"/><line x1="12" x2="15" y1="14" y2="11"/><circle cx="12" cy="14" r="8"/></svg>
                    <p class="subtitulo-prato1">${prato.tempo_preparo} min</p>
                </div>
                <div id="porcao">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><path d="M16 3.128a4 4 0 0 1 0 7.744"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><circle cx="9" cy="7" r="4"/></svg>
                    <p class="subtitulo-prato1">${prato.porcoes} porções</p>
                </div>
            </div>
            ${ingredientesHTML}
            <button class="btn-preparo" id="preparo">
                <div>MODO DE PREPARO</div>
            </button>
            <div class="ia-ordem">
                <h4 id="srf">Modo de Preparo:</h4>
                <p id="subtitulo-prato3">${preparoHTML}</p>
            </div>
        `;

        card.querySelector('.btn-preparo').addEventListener('click', function () {
            card.querySelector('.ia-ordem').classList.toggle('visivel');
        });

        container.insertBefore(card, nav);
    });
}
