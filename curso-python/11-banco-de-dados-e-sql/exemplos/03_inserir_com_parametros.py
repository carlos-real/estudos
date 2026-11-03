"""Exemplo 03 — INSERT com parâmetros (?, :nome), executemany, lastrowid, rowcount.

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/03_inserir_com_parametros.py
"""

import sqlite3

conexao = sqlite3.connect(":memory:")
conexao.execute(
    "CREATE TABLE expedicao (id INTEGER PRIMARY KEY, op INTEGER, nf TEXT, peso_kg REAL)"
)

# 1) Parâmetro posicional "?": os valores vão numa tupla, na mesma ordem.
cursor = conexao.execute(
    "INSERT INTO expedicao (op, nf, peso_kg) VALUES (?, ?, ?)", (24518, "123456", 1250.5)
)
print("id gerado:", cursor.lastrowid)

# 2) Parâmetro nomeado ":nome": os valores vão num dicionário.
pedido = {"op": 24541, "nf": "123465", "peso": 2000.25}
cursor = conexao.execute(
    "INSERT INTO expedicao (op, nf, peso_kg) VALUES (:op, :nf, :peso)", pedido
)
print("id gerado:", cursor.lastrowid)

# 3) Muitas linhas de uma vez: executemany com uma lista de tuplas.
cargas = [(24520, "123458", 2400.0), (24521, "123459", 2950.0), (24518, "123470", 1830.0)]
cursor = conexao.executemany(
    "INSERT INTO expedicao (op, nf, peso_kg) VALUES (?, ?, ?)", cargas
)
print("linhas inseridas:", cursor.rowcount)
conexao.commit()

# 4) Texto com apóstrofo: com parâmetros, não há problema nenhum.
conexao.execute(
    "INSERT INTO expedicao (op, nf, peso_kg) VALUES (?, ?, ?)", (24533, "D'Ávila-01", 500.0)
)

# 5) Um parâmetro só ainda precisa ser uma TUPLA: (24518,) com vírgula!
for linha in conexao.execute("SELECT id, nf, peso_kg FROM expedicao WHERE op = ?", (24518,)):
    print(linha)
print(conexao.execute("SELECT COUNT(*) FROM expedicao").fetchone()[0], "cargas no total")
conexao.close()
