"""Exemplo 01 — Primeira conexão: criar, inserir, consultar e fechar.

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/01_primeira_conexao.py
"""

import sqlite3

# ":memory:" cria um banco só na memória (some ao fechar). Para um arquivo de
# verdade, passe um caminho: sqlite3.connect("laboratorio.db").
conexao = sqlite3.connect(":memory:")
print("SQLite versão", sqlite3.sqlite_version)

conexao.execute("CREATE TABLE bobina (id INTEGER PRIMARY KEY, op INTEGER, peso_kg REAL)")
conexao.execute("INSERT INTO bobina (op, peso_kg) VALUES (24518, 1250.5)")
conexao.execute("INSERT INTO bobina (op, peso_kg) VALUES (24518, 980.0)")
conexao.execute("INSERT INTO bobina (op, peso_kg) VALUES (24519, 1100.0)")
conexao.commit()  # grava de verdade (sem commit, as alterações podem se perder)

cursor = conexao.execute("SELECT id, op, peso_kg FROM bobina")
print(cursor.fetchall())  # lista de tuplas, uma por linha

cursor = conexao.execute("SELECT op, peso_kg FROM bobina WHERE op = 24518")
print(cursor.fetchone())  # só a próxima linha (ou None se acabou)
print(cursor.fetchone())
print(cursor.fetchone())

# O cursor também pode ser percorrido com for, linha a linha
for op, peso in conexao.execute("SELECT op, peso_kg FROM bobina"):
    print(f"OP {op}: {peso:,.1f} kg".replace(",", "X").replace(".", ",").replace("X", "."))

conexao.close()
