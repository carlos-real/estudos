"""
Exercício 11.06 — Funções de agregação
Nível: ★★☆

Contexto: o gerente da qualidade quer números rápidos: quantas medições de uma
característica existem, a média, o mínimo e o máximo; e o peso já expedido.

Tarefa: use o banco do laboratório. Implemente duas funções:
  1. resumo_caracteristica(conexao, caracteristica): devolve o dicionário
       {"n": quantidade de valores medidos (ignore os NULL),
        "media": média com 2 casas (arredonde no SQL),
        "minimo": menor valor, "maximo": maior valor}
     Característica sem medições -> {"n": 0, "media": None, "minimo": None,
     "maximo": None}.
  2. peso_expedido(conexao, op=None): soma do peso_kg da tabela expedicao; se op
     for informada, só dessa OP. Sem nenhuma carga -> 0.0 (nunca None).

Exemplos:
    >>> resumo_caracteristica(conexao, "cof")
    {'n': 19, 'media': 0.25, 'minimo': 0.15, 'maximo': 0.43}
    >>> peso_expedido(conexao, 24518)
    3080.5
    >>> peso_expedido(conexao, 24550)
    0.0

Dica: COUNT(coluna) ignora NULL; ROUND(AVG(x), 2); SUM de nada dá NULL, mas
COALESCE(SUM(x), 0) ou TOTAL(x) dão 0. Uma consulta com agregação e sem GROUP
BY devolve sempre UMA linha.

Teste com:  python curso.py testar 11 ex06
"""

import sqlite3


def resumo_caracteristica(conexao: sqlite3.Connection, caracteristica: str) -> dict:
    """Quantidade, média, mínimo e máximo dos valores medidos."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def peso_expedido(conexao: sqlite3.Connection, op: int | None = None) -> float:
    """Peso total expedido (de todas as OPs ou de uma)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
