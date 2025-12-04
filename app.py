from flask import Flask, render_template, jsonify, request
import time
import sqlite3

app = Flask(__name__)

def carregar_dados():
    conn = sqlite3.connect('dados.db')
    cur = conn.cursor()
    cur.execute("SELECT id, nome, partidas, rank, mmr, gols, assists, saves, winRate FROM pessoas")
    rows = cur.fetchall()
    conn.close()

    jogadores = []
    for row in rows:
        jogadores.append({
            'id': row[0],
            'name': row[1],
            'matches': row[2],
            'rank': row[3],
            'mmr': row[4],
            'goals': row[5],
            'assists': row[6],
            'saves': row[7],
            'winRate': round(row[8], 2)
        })

    return jogadores

JOGADORES = carregar_dados()

JOGADORES_ORDENADOS = sorted(JOGADORES, key=lambda x: x['name'].lower())
NOMES_ORDENADOS = [j['name'].lower() for j in JOGADORES_ORDENADOS]

INDICE_LETRAS = {}
for i, nome in enumerate(NOMES_ORDENADOS):
    letra = nome[0] if nome else ''
    if letra not in INDICE_LETRAS:
        INDICE_LETRAS[letra] = [i, i]
    else:
        INDICE_LETRAS[letra][1] = i

JOGADORES_HASH = {j['name'].lower(): j for j in JOGADORES}

print(f"✅ {len(JOGADORES)} jogadores carregados com sucesso!")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jogadores')
def jogadores():
    return render_template('jogadores.html')

@app.route('/api/jogadores')
def api_jogadores():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    start = (page - 1) * per_page
    end = start + per_page

    return jsonify({
        'jogadores': JOGADORES[start:end],
        'total': len(JOGADORES),
        'page': page,
        'per_page': per_page,
        'total_pages': (len(JOGADORES) + per_page - 1) // per_page
    })

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    player_name = data.get('name').strip()

    results = {}

    # BUSCA SEQUENCIAL
    start = time.perf_counter()
    sequential_result = None
    for jogador in JOGADORES:
        if jogador['name'].lower() == player_name.lower():
            sequential_result = jogador
            break
    end = time.perf_counter()

    results['sequential'] = {
        'time': round((end - start) * 1000, 6),
        'found': sequential_result is not None,
        'player': sequential_result
    }

    # BUSCA INDEXADA
    start = time.perf_counter()
    indexed_result = None

    search_name = player_name.lower()
    primeira_letra = search_name[0] if search_name else ''

    if primeira_letra in INDICE_LETRAS:
        inicio, fim = INDICE_LETRAS[primeira_letra]
        for i in range(inicio, fim + 1):
            if NOMES_ORDENADOS[i] == search_name:
                indexed_result = JOGADORES_ORDENADOS[i]
                break

    end = time.perf_counter()

    results['indexed'] = {
        'time': round((end - start) * 1000, 6),
        'found': indexed_result is not None,
        'player': indexed_result
    }

    # BUSCA HASHMAP
    start = time.perf_counter()
    hashmap_result = JOGADORES_HASH.get(player_name.lower())
    end = time.perf_counter()

    results['hashmap'] = {
        'time': round((end - start) * 1000, 6),
        'found': hashmap_result is not None,
        'player': hashmap_result
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
