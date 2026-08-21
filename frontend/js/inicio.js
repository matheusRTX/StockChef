document.addEventListener('DOMContentLoaded', () => {
    carregarResumo();
    carregarEstoqueBaixo();
    carregarVencendo();
    carregarMovimentacoes();
});

// Cards do topo: total cadastrados, estoque baixo, vencendo em 7 dias
function carregarResumo() {
    fetch('/api/inicio/resumo')
        .then(res => res.json())
        .then(dados => {
            document.getElementById('total-cadastrados').textContent = dados.total_cadastrados;
            document.getElementById('total-estoque-baixo').textContent = dados.total_estoque_baixo;
            document.getElementById('total-vencendo').textContent = dados.total_vencendo_7_dias;
        })
        .catch(err => console.error('Erro ao carregar resumo do início:', err));
}

// Lista "Estoque Baixo"
function carregarEstoqueBaixo() {
    const container = document.getElementById('lista-estoque-baixo');

    fetch('/api/inicio/estoque-baixo')
        .then(res => res.json())
        .then(itens => {
            if (!itens.length) {
                container.innerHTML = '<p class="meta-item">Nenhum item abaixo do estoque mínimo.</p>';
                return;
            }

            container.innerHTML = itens.map(item => `
                <div class="cartao-linha-perigo">
                    <div>
                        <p class="nome-item">${item.produto}</p>
                        <p class="meta-item">${item.categoria}</p>
                    </div>
                    <div class="texto-direita">
                        <p class="quantidade-baixa">${item.quantidade} kg</p>
                        <p class="meta-item">Mín: ${item.valor_minimo}</p>
                    </div>
                </div>
            `).join('');
        })
        .catch(err => console.error('Erro ao carregar estoque baixo:', err));
}

// Lista "Alertas de Validade" (lotes vencendo em até 7 dias)
function carregarVencendo() {
    const container = document.getElementById('lista-vencendo');

    fetch('/api/inicio/vencendo')
        .then(res => res.json())
        .then(itens => {
            if (!itens.length) {
                container.innerHTML = '<p class="meta-item">Nenhum lote vencendo nos próximos 7 dias.</p>';
                return;
            }

            const hoje = new Date();
            hoje.setHours(0, 0, 0, 0);

            container.innerHTML = itens.map(item => {
                const validade = new Date(item.validade + 'T00:00:00');
                const diffDias = Math.round((validade - hoje) / (1000 * 60 * 60 * 24));
                const dataFormatada = validade.toLocaleDateString('pt-BR');

                const vencido = diffDias < 0;
                const classeCartao = vencido ? 'cartao-alerta-perigo' : 'cartao-alerta-aviso';
                const classeEtiqueta = vencido ? 'etiqueta-perigo' : 'etiqueta-aviso';
                const textoEtiqueta = vencido ? 'Vencido' : `${diffDias}d`;

                return `
                    <div class="${classeCartao}">
                        <div>
                            <p class="nome-item">${item.produto}</p>
                            <p class="meta-item">${item.quantidade_atual} un — Vence ${dataFormatada}</p>
                        </div>
                        <span class="${classeEtiqueta}">${textoEtiqueta}</span>
                    </div>
                `;
            }).join('');
        })
        .catch(err => console.error('Erro ao carregar lotes vencendo:', err));
}

