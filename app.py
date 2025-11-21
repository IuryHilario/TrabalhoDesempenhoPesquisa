from flask import Flask, render_template, request, jsonify
import sqlite3, time
import pesquisa

app = Flask(__name__)

# Rota principal
@app.route('/')
def index():
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = 25
    offset = (page - 1) * per_page

    conn = sqlite3.connect('dados.db')
    cur = conn.cursor()

    # Conta total de registros
    cur.execute("SELECT COUNT(*) FROM pessoas")
    total_registros = cur.fetchone()[0]

    # Busca registros da página atual
    cur.execute("SELECT nome, email, idade FROM pessoas LIMIT ? OFFSET ?", (per_page, offset))
    pessoas = [{"nome": n, "email": e, "idade": i} for n, e, i in cur.fetchall()]
    conn.close()

    # Calcula total de páginas
    total_pages = (total_registros + per_page - 1) // per_page

    return render_template('index.html',
                         pessoas=pessoas,
                         total_registros=total_registros,
                         page=page,
                         total_pages=total_pages)


# Rota de Resultado de Busca
@app.route('/buscar', methods=['POST'])
def buscar():
    termo = request.form['termo']

    conn = sqlite3.connect('dados.db')
    cur = conn.cursor()
    cur.execute("SELECT nome, email, idade FROM pessoas")
    registros = [{"nome": n, "email": e, "idade": i} for n, e, i in cur.fetchall()]
    conn.close()

    # Cria estruturas
    indice = {}
    for r in registros:
        primeira_letra = r["nome"].lower()[0]
        if primeira_letra not in indice:
            indice[primeira_letra] = []
        indice[primeira_letra].append(r)

    tabela_hash = {r["nome"].lower(): r for r in registros}

    tempos = {}
    resultados = {}

    # --- Sequencial ---
    t1 = time.time()
    resultados["sequencial"] = pesquisa.busca_sequencial(registros, termo)
    tempos["sequencial"] = round((time.time() - t1) * 1000, 3)

    # --- Indexada ---
    t2 = time.time()
    resultados["indexada"] = pesquisa.busca_indexada(indice, termo)
    tempos["indexada"] = round((time.time() - t2) * 1000, 3)

    # --- HashMap ---
    t3 = time.time()
    resultados["hashmap"] = pesquisa.busca_hash(tabela_hash, termo)
    tempos["hashmap"] = round((time.time() - t3) * 1000, 3)

    return jsonify(
        tempos=tempos,
        resultados=resultados
    )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
