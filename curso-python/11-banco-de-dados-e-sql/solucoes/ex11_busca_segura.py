"""
Exercício 11.11 — Busca com filtros, à prova de SQL injection (SOLUÇÃO)

Duas regras, uma para cada pedaço do SQL:
  - VALORES (o que o usuário digitou) -> sempre parâmetros "?".
  - NOMES (colunas, tabelas, ASC/DESC) não podem ser parâmetros -> só entram no
    texto depois de conferidos numa lista permitida ("whitelist").
"""

import sqlite3

FILTROS_PERMITIDOS = {"linha", "produto", "status", "especificacao"}
ORDENACOES_PERMITIDAS = {"numero", "emissao", "quantidade_kg"}


def buscar_ops(
    conexao: sqlite3.Connection, filtros: dict[str, str], ordenar_por: str = "numero"
) -> list[int]:
    """Números das OPs que atendem a todos os filtros."""
    # 1. Validar ANTES de montar qualquer coisa
    desconhecidos = set(filtros) - FILTROS_PERMITIDOS
    if desconhecidos:
        raise ValueError(f"filtro não permitido: {sorted(desconhecidos)}")
    if ordenar_por not in ORDENACOES_PERMITIDAS:
        raise ValueError(f"ordenação não permitida: {ordenar_por!r}")

    # 2. Montar as condições (com nomes já conferidos) e os valores em paralelo
    condicoes = [f"{coluna} = ?" for coluna in filtros]
    valores = list(filtros.values())  # mesma ordem das chaves acima

    # "WHERE 1 = 1" é um truque comum: com ou sem filtros, o SQL fica válido.
    sql = "SELECT numero FROM op WHERE 1 = 1"
    for condicao in condicoes:
        sql += f" AND {condicao}"
    sql += f" ORDER BY {ordenar_por}, numero"

    return [numero for (numero,) in conexao.execute(sql, valores)]
