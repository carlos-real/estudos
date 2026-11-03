"""Exemplo 11 — Índices: o "sumário" que acelera as buscas.

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/11_indices.py
"""

import random
import sqlite3
import time

conexao = sqlite3.connect(":memory:")
conexao.execute("CREATE TABLE ensaio (id INTEGER PRIMARY KEY, op INTEGER, valor REAL)")
sorteio = random.Random(1)
linhas = [(sorteio.randint(10_000, 99_999), sorteio.uniform(30, 70)) for _ in range(300_000)]
conexao.executemany("INSERT INTO ensaio (op, valor) VALUES (?, ?)", linhas)

consulta = "SELECT COUNT(*) FROM ensaio WHERE op = ?"


def medir() -> float:
    inicio = time.perf_counter()
    for op in range(50_000, 50_200):
        conexao.execute(consulta, (op,)).fetchone()
    return (time.perf_counter() - inicio) * 1000


print("Plano sem índice:", conexao.execute("EXPLAIN QUERY PLAN " + consulta, (1,)).fetchall())
print(f"200 buscas sem índice: {medir():.0f} ms")

conexao.execute("CREATE INDEX idx_ensaio_op ON ensaio (op)")
print("Plano com índice:", conexao.execute("EXPLAIN QUERY PLAN " + consulta, (1,)).fetchall())
print(f"200 buscas com índice: {medir():.1f} ms")
conexao.close()
