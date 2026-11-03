"""
Exercício 11.11 — Busca com filtros, à prova de SQL injection
Nível: ★★★

Contexto: a tela de consulta de OPs tem campos opcionais (linha, produto,
status, especificação) e um seletor "ordenar por". O que o usuário digita NÃO
pode virar código SQL. Um colega sugeriu montar tudo com f-string... não!

Tarefa: implemente buscar_ops(conexao, filtros, ordenar_por="numero"), que
devolve a lista dos NÚMEROS das OPs (tabela op do banco do laboratório):
  - filtros é um dicionário {coluna: valor}. Colunas permitidas: "linha",
    "produto", "status", "especificacao". Cada filtro é uma igualdade, e todos
    se combinam com AND. Dicionário vazio -> todas as OPs.
  - Os VALORES entram sempre como parâmetros (?), nunca colados no SQL.
  - Coluna de filtro fora da lista -> ValueError.
  - ordenar_por: "numero", "emissao" ou "quantidade_kg" (crescente; no empate,
    por número). Qualquer outro -> ValueError.

Exemplos:
    >>> buscar_ops(conexao, {"linha": "A", "status": "LIBERADA"})
    [24518, 24520, 24521]
    >>> buscar_ops(conexao, {"linha": "B"}, ordenar_por="quantidade_kg")
    [24527, 24550, 24528]
    >>> buscar_ops(conexao, {"linha": "A' OR '1'='1"})
    []
    >>> buscar_ops(conexao, {}, ordenar_por="numero; DROP TABLE op")
    Traceback (most recent call last):
    ValueError: ...

Dica: NOMES de coluna não podem ser parâmetros (só valores). Por isso confira
os nomes numa lista permitida e monte só essa parte do texto; os valores vão
numa lista de parâmetros, na mesma ordem dos "?".

Teste com:  python curso.py testar 11 ex11
"""

import sqlite3


def buscar_ops(
    conexao: sqlite3.Connection, filtros: dict[str, str], ordenar_por: str = "numero"
) -> list[int]:
    """Números das OPs que atendem a todos os filtros."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
