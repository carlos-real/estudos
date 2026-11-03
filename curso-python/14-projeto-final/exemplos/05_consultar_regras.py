"""Consultar o banco de regras: JOIN, parâmetro com ? e abertura só para leitura.

Rode:  python exemplos/05_consultar_regras.py
"""

import sqlite3
from pathlib import Path

BANCO = Path(__file__).resolve().parent.parent / "dados" / "regras.db"

# mode=ro: se o caminho estiver errado, dá erro em vez de criar um banco vazio
conexao = sqlite3.connect(f"{BANCO.as_uri()}?mode=ro", uri=True)
try:
    print("Padrões de linha:")
    for titulo, linha in conexao.execute(
        "SELECT titulo, linha FROM especificacao WHERE linha IS NOT NULL ORDER BY linha"
    ):
        print(f"  linha {linha}: {titulo}")

    titulo = "ESP-0412"
    consulta = """
        SELECT e.texto, t.caracteristica, t.tipo, t.minimo, t.maximo, t.percentual
        FROM especificacao AS e
        JOIN tolerancia AS t ON t.titulo = e.titulo
        WHERE e.titulo = ?
        ORDER BY t.caracteristica
    """
    linhas = conexao.execute(consulta, (titulo,)).fetchall()
    print(f"\n{titulo}: {linhas[0][0]}")
    for _, caracteristica, tipo, minimo, maximo, percentual in linhas:
        print(f"  {caracteristica:<10} {tipo:<8} mín={minimo} máx={maximo} %={percentual}")
finally:
    conexao.close()
