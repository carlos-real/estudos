"""Exemplo 02 — CREATE TABLE com tipos e restrições, e os erros que elas evitam.

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/02_criar_tabelas_e_restricoes.py
"""

import sqlite3

conexao = sqlite3.connect(":memory:")
conexao.execute("PRAGMA foreign_keys = ON")  # no SQLite, a FK só vale com isto ligado!

conexao.executescript(
    """
    CREATE TABLE cliente (
        id   INTEGER PRIMARY KEY,
        nome TEXT NOT NULL UNIQUE
    );
    CREATE TABLE op (
        numero        INTEGER PRIMARY KEY,
        cliente_id    INTEGER NOT NULL REFERENCES cliente (id),
        quantidade_kg REAL    NOT NULL CHECK (quantidade_kg > 0),
        status        TEXT    NOT NULL DEFAULT 'ABERTA'
    );
    """
)
conexao.execute("INSERT INTO cliente (nome) VALUES ('Agro Campo S.A.')")
conexao.execute("INSERT INTO op (numero, cliente_id, quantidade_kg) VALUES (24520, 1, 5200)")
print(conexao.execute("SELECT * FROM op").fetchall())  # o status veio do DEFAULT

testes = [
    ("NOT NULL", "INSERT INTO cliente (nome) VALUES (NULL)"),
    ("UNIQUE", "INSERT INTO cliente (nome) VALUES ('Agro Campo S.A.')"),
    ("CHECK", "INSERT INTO op (numero, cliente_id, quantidade_kg) VALUES (24521, 1, -5)"),
    (
        "FOREIGN KEY",
        "INSERT INTO op (numero, cliente_id, quantidade_kg) VALUES (24522, 99, 10)",
    ),
    (
        "PRIMARY KEY",
        "INSERT INTO op (numero, cliente_id, quantidade_kg) VALUES (24520, 1, 10)",
    ),
]
for regra, comando in testes:
    try:
        conexao.execute(comando)
    except sqlite3.IntegrityError as erro:
        print(f"{regra:<12} -> IntegrityError: {erro}")

# Tipagem flexível do SQLite: a coluna REAL aceitou um texto que não é número!
conexao.execute("CREATE TABLE teste (valor REAL)")
conexao.execute("INSERT INTO teste VALUES ('12abc'), ('38.5'), (40)")
print(conexao.execute("SELECT valor, typeof(valor) FROM teste").fetchall())

# Com STRICT (SQLite 3.37+), o tipo é conferido de verdade
conexao.execute("CREATE TABLE teste_estrito (valor REAL) STRICT")
try:
    conexao.execute("INSERT INTO teste_estrito VALUES ('12abc')")
except sqlite3.IntegrityError as erro:
    print("STRICT       -> IntegrityError:", erro)

# Quais colunas a tabela tem? PRAGMA table_info responde.
for coluna in conexao.execute("PRAGMA table_info(op)"):
    print(coluna)
conexao.close()
