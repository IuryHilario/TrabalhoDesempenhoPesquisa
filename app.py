from flask import Flask, render_template, jsonify, request
import time
import sqlite3
import bisect

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

JOGADORES_ORDENADOS = sorted(JOGADORES, key=lambda x: x['id'])
IDS_ORDENADOS = [j['id'] for j in JOGADORES_ORDENADOS]

JOGADORES_HASH = {j['id']: j for j in JOGADORES}

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

    # Paginação
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
    player_id = int(data.get('id'))

    results = {}

    # BUSCA SEQUENCIAL
    start = time.perf_counter()
    sequential_result = None
    for jogador in JOGADORES:
        if jogador['id'] == player_id:
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
    idx = bisect.bisect_left(IDS_ORDENADOS, player_id)
    indexed_result = None
    if idx < len(IDS_ORDENADOS) and IDS_ORDENADOS[idx] == player_id:
        indexed_result = JOGADORES_ORDENADOS[idx]
    end = time.perf_counter()

    results['indexed'] = {
        'time': round((end - start) * 1000, 6),
        'found': indexed_result is not None,
        'player': indexed_result
    }

    # BUSCA HASHMAP
    start = time.perf_counter()
    hashmap_result = JOGADORES_HASH.get(player_id)
    end = time.perf_counter()

    results['hashmap'] = {
        'time': round((end - start) * 1000, 6),
        'found': hashmap_result is not None,
        'player': hashmap_result
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
