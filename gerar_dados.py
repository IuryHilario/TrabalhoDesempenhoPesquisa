from faker import Faker
import sqlite3

fake = Faker()
conn = sqlite3.connect('dados.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS pessoas")

cur.execute("""
CREATE TABLE IF NOT EXISTS pessoas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    idade INTEGER
)
""")

cur.execute("DELETE FROM pessoas")

for _ in range(10000):
    nome = fake.name()
    email = fake.email()
    idade = fake.random_int(min=18, max=80)
    cur.execute("INSERT INTO pessoas (nome, email, idade) VALUES (?, ?, ?)", (nome, email, idade))

conn.commit()
conn.close()
print("✅ Banco 'dados.db' criado com 5.000 registros.")
