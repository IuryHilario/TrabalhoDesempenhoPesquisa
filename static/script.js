async function executeSearch() {
    const playerName = document.getElementById('playerId').value;
    const searchBtn = document.getElementById('searchBtn');
    const resultsContainer = document.getElementById('results');

    // Validação
    if (!playerName || playerName.trim() === '') {
        alert('Por favor, insira um nome válido');
        return;
    }

    // Desabilitar botão e mostrar loading
    searchBtn.disabled = true;
    searchBtn.innerHTML = `
        <div class="spinner"></div>
        BUSCANDO
    `;

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: playerName })
        });

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao realizar busca. Tente novamente.');
    } finally {
        searchBtn.disabled = false;
        searchBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            BUSCAR
        `;
    }
}

function displayResults(data) {
    const resultsContainer = document.getElementById('results');

    const html = `
        <!-- Busca Sequencial -->
        <div class="result-card sequential">
            <div class="result-header">
                <div class="result-title">
                    <div class="result-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
                            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
                            <path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"></path>
                        </svg>
                    </div>
                    <div class="result-info">
                        <h3>Busca Sequencial</h3>
                        <p>Verifica item por item até encontrar</p>
                    </div>
                </div>
                <div class="result-time">
                    <div class="time-value">${data.sequential.time.toFixed(4)} ms</div>
                    <p class="complexity"></p>
                </div>
            </div>
            ${data.sequential.found ? createPlayerCard(data.sequential.player) : '<p style="color: #94a3b8;">Jogador não encontrado</p>'}
        </div>

        <!-- Busca Indexada -->
        <div class="result-card indexed">
            <div class="result-header">
                <div class="result-title">
                    <div class="result-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="11" cy="11" r="8"></circle>
                            <path d="m21 21-4.35-4.35"></path>
                        </svg>
                    </div>
                    <div class="result-info">
                        <h3>Busca Indexada</h3>
                        <p>Busca binária em lista ordenada</p>
                    </div>
                </div>
                <div class="result-time">
                    <div class="time-value">${data.indexed.time.toFixed(4)} ms</div>
                    <p class="complexity"></p>
                </div>
            </div>
            ${data.indexed.found ? createPlayerCard(data.indexed.player) : '<p style="color: #94a3b8;">Jogador não encontrado</p>'}
        </div>

        <!-- Busca HashMap -->
        <div class="result-card hashmap">
            <div class="result-header">
                <div class="result-title">
                    <div class="result-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="4" y1="9" x2="20" y2="9"></line>
                            <line x1="4" y1="15" x2="20" y2="15"></line>
                            <line x1="10" y1="3" x2="8" y2="21"></line>
                            <line x1="16" y1="3" x2="14" y2="21"></line>
                        </svg>
                    </div>
                    <div class="result-info">
                        <h3>Busca HashMap</h3>
                        <p>Acesso direto por chave</p>
                    </div>
                </div>
                <div class="result-time">
                    <div class="time-value">${data.hashmap.time.toFixed(4)} ms</div>
                    <p class="complexity"></p>
                </div>
            </div>
            ${data.hashmap.found ? createPlayerCard(data.hashmap.player) : '<p style="color: #94a3b8;">Jogador não encontrado</p>'}
        </div>
    `;

    resultsContainer.innerHTML = html;
}

function createPlayerCard(player) {
    return `
        <div class="player-info">
            <div class="player-main">
                <div class="player-id">
                    <div class="player-id-value">${player.id}</div>
                    <div class="player-id-label">ID</div>
                </div>
                <div class="divider-vertical"></div>
                <div class="player-details">
                    <h4>${player.name}</h4>
                    <div class="player-rank">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="8" r="6"></circle>
                            <path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"></path>
                        </svg>
                        <span class="rank-text">${player.rank}</span>
                        <span style="color: #475569;">|</span>
                        <span class="mmr-text">MMR: ${player.mmr}</span>
                    </div>
                </div>
            </div>
            <div class="player-stats">
                <div class="stat-box goals">
                    <div class="stat-value">${player.goals}</div>
                    <div class="stat-label">Gols</div>
                </div>
                <div class="stat-box assists">
                    <div class="stat-value">${player.assists}</div>
                    <div class="stat-label">Assistências</div>
                </div>
                <div class="stat-box saves">
                    <div class="stat-value">${player.saves}</div>
                    <div class="stat-label">Defesas</div>
                </div>
                <div class="stat-box assists">
                    <div class="stat-value">${player.matches}</div>
                    <div class="stat-label">Partidas</div>
                </div>
                <div class="stat-box goals">
                    <div class="stat-value">${player.winRate}%</div>
                    <div class="stat-label">Taxa de Vitória</div>
                </div>
            </div>
        </div>
    `;
}

// Permitir busca com Enter
document.getElementById('playerId').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        executeSearch();
    }
});