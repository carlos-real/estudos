"""
Exercício 11.04 — Buscar os ensaios de uma OP
Nível: ★☆☆

Contexto: na hora de emitir o certificado, o sistema precisa listar os ensaios
da OP, numa ordem previsível, e saber se a OP existe.

Tarefa: use o banco do laboratório (tabelas op e ensaio, veja a aula ou
dados/laboratorio.sql). Implemente duas funções, sempre com parâmetros (?):
  1. ensaios_da_op(conexao, op): lista de tuplas (bobina, caracteristica, valor)
     da OP, ordenada por bobina e, dentro da bobina, por caracteristica (ordem
     alfabética). OP sem ensaios (ou inexistente) -> lista vazia.
  2. existe_op(conexao, numero): True se a OP está na tabela op, senão False.

Exemplos:
    >>> ensaios_da_op(conexao, 24534)[:2]
    [(1, 'cof', 0.23), (1, 'espessura', 69.8)]
    >>> existe_op(conexao, 24534), existe_op(conexao, 99999)
    (True, False)

Dica: ORDER BY a, b. fetchone() devolve None quando não há linha.

Teste com:  python curso.py testar 11 ex04
"""

import sqlite3


def ensaios_da_op(conexao: sqlite3.Connection, op: int) -> list[tuple[int, str, float | None]]:
    """(bobina, caracteristica, valor) da OP, ordenados."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def existe_op(conexao: sqlite3.Connection, numero: int) -> bool:
    """A OP está cadastrada?"""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
