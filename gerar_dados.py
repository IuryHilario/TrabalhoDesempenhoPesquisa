from faker import Faker
import sqlite3
import random

ranks_mmr = [
    ("Bronze I", 0, 200),
    ("Bronze II", 200, 250),
    ("Bronze III", 250, 300),
    ("Silver I", 300, 400),
    ("Silver II", 400, 500),
    ("Silver III", 500, 600),
    ("Gold I", 600, 700),
    ("Gold II", 700, 800),
    ("Gold III", 800, 900),
    ("Platinum I", 900, 1000),
    ("Platinum II", 1000, 1100),
    ("Platinum III", 1100, 1200),
    ("Diamond I", 1200, 1300),
    ("Diamond II", 1300, 1400),
    ("Diamond III", 1400, 1515),
    ("Champion I", 1515, 1595),
    ("Champion II", 1595, 1675),
    ("Champion III", 1675, 1755),
    ("Grand Champion I", 1755, 1835),
    ("Grand Champion II", 1835, 1915),
    ("Grand Champion III", 1915, 1995),
    ("Supersonic Legend", 1995, 2300)
]

fake = Faker()
conn = sqlite3.connect('dados.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS pessoas")

cur.execute("""
CREATE TABLE IF NOT EXISTS pessoas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    partidas INTEGER,
    rank TEXT,
    mmr INTEGER,
    gols INTEGER,
    assists INTEGER,
    saves INTEGER,
    winRate REAL
)
""")

cur.execute("DELETE FROM pessoas")

for _ in range(10000):
    nome = fake.first_name()
    sobrenome = fake.last_name()
    nomeCompleto = f"{nome}{sobrenome}"

    # Selecionar rank aleatório
    rank_data = random.choice(ranks_mmr)
    rank = rank_data[0]
    mmr = random.randint(rank_data[1], rank_data[2])

    skill_multiplier = 1 + (mmr / 2300) * 4

    # Número base de partidas jogadas
    partidas_base = random.randint(100, 2000)
    partidas = int(partidas_base * skill_multiplier)

    gols_por_partida = 0.3 + (mmr / 2300) * 1.2
    gols = int(partidas * gols_por_partida * random.uniform(0.7, 1.3))

    # Assistências baseadas em gols
    assists = int(gols * random.uniform(0.3, 0.6))

    # Defesas baseadas em MMR
    saves_por_partida = 0.5 + (mmr / 2300) * 1.5
    saves = int(partidas * saves_por_partida * random.uniform(0.8, 1.2))

    # Win rate baseado no MMR
    base_winrate = 45 + (mmr / 2300) * 20
    winRate = round(base_winrate + random.uniform(-3, 3), 2)
    winRate = max(35, min(70, winRate))

    cur.execute(
        "INSERT INTO pessoas (nome, partidas, rank, mmr, gols, assists, saves, winRate) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (nomeCompleto, partidas, rank, mmr, gols, assists, saves, winRate)
    )

conn.commit()
conn.close()
print("✅ Banco 'dados.db' criado com 10.000 registros consistentes.")
