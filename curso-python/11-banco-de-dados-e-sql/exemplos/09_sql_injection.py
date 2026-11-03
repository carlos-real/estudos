"""Exemplo 09 — SQL injection na prática, e a forma correta (parâmetros).

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/09_sql_injection.py
"""

import sqlite3

from utilitarios import abrir_banco_exemplo


def buscar_cliente_inseguro(conexao: sqlite3.Connection, nome: str) -> list[tuple]:
    """NUNCA faça assim: o texto do usuário vira parte do comando SQL."""
    sql = f"SELECT id, nome, cidade FROM cliente WHERE nome = '{nome}'"
    print("  SQL montado:", sql)
    return conexao.execute(sql).fetchall()


def buscar_cliente_seguro(conexao: sqlite3.Connection, nome: str) -> list[tuple]:
    """Correto: o valor vai SEPARADO do comando, como parâmetro."""
    sql = "SELECT id, nome, cidade FROM cliente WHERE nome = ?"
    return conexao.execute(sql, (nome,)).fetchall()


banco = abrir_banco_exemplo()

print("1) Uso normal:")
print(" ", buscar_cliente_inseguro(banco, "Biscoitos Aurora"))

print("2) Um nome com apóstrofo já quebra a versão insegura:")
try:
    buscar_cliente_inseguro(banco, "Plásticos D'Ávila")
except sqlite3.OperationalError as erro:
    print("  OperationalError:", erro)

print("3) Ataque: ' OR '1'='1  -> devolve TODOS os clientes")
print(" ", len(buscar_cliente_inseguro(banco, "x' OR '1'='1")), "clientes vazaram")

print("4) Ataque com UNION: lê outra tabela inteira")
ataque = "x' UNION SELECT numero, produto, status FROM op --"
print(" ", len(buscar_cliente_inseguro(banco, ataque)), "linhas de OUTRA tabela")

print("5) Versão segura com os mesmos textos:")
for texto in ["Biscoitos Aurora", "Plásticos D'Ávila", "x' OR '1'='1", ataque]:
    print(f"  {texto!r:55} -> {buscar_cliente_seguro(banco, texto)}")

print("6) Nome de tabela/coluna NÃO pode ser parâmetro: use lista permitida")
COLUNAS_PERMITIDAS = {"numero", "emissao", "quantidade_kg"}


def ops_ordenadas(conexao: sqlite3.Connection, coluna: str) -> list[int]:
    if coluna not in COLUNAS_PERMITIDAS:
        raise ValueError(f"ordenação não permitida: {coluna!r}")
    sql = f"SELECT numero FROM op ORDER BY {coluna} LIMIT 3"  # seguro: coluna conferida
    return [numero for (numero,) in conexao.execute(sql)]


print(" ", ops_ordenadas(banco, "quantidade_kg"))
try:
    ops_ordenadas(banco, "numero; DROP TABLE op")
except ValueError as erro:
    print("  ValueError:", erro)
banco.close()
