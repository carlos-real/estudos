"""
Exercício 11.07 — GROUP BY e HAVING
Nível: ★★☆

Contexto: na reunião de qualidade, duas perguntas: "quais características mais
reprovam?" e "quais OPs saíram em várias cargas?".

Tarefa: use o banco do laboratório. Implemente duas funções:
  1. fora_por_caracteristica(conexao): tuplas (caracteristica, quantidade) com
     quantos ensaios deram resultado 'FORA' em cada característica. Só entram
     as que têm pelo menos 1. Ordem: quantidade decrescente; empate, ordem
     alfabética.
  2. ops_com_varias_cargas(conexao, minimo): tuplas (op, cargas, peso_total) da
     tabela expedicao, só das OPs com pelo menos `minimo` cargas, ordenadas por op.

Exemplos:
    >>> fora_por_caracteristica(conexao)
    [('espessura', 3), ('cof', 2), ('gramatura', 1)]
    >>> ops_com_varias_cargas(conexao, 2)[0]
    (24518, 2, 3080.5)

Dica: WHERE filtra linhas ANTES de agrupar; HAVING filtra grupos DEPOIS.

Teste com:  python curso.py testar 11 ex07
"""

import sqlite3


def fora_por_caracteristica(conexao: sqlite3.Connection) -> list[tuple[str, int]]:
    """Quantidade de ensaios FORA por característica."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def ops_com_varias_cargas(
    conexao: sqlite3.Connection, minimo: int
) -> list[tuple[int, int, float]]:
    """OPs com pelo menos `minimo` cargas expedidas."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
