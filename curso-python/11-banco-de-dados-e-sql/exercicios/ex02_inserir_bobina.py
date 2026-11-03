"""
Exercício 11.02 — Inserir com parâmetros
Nível: ★☆☆

Contexto: a balança da expedição manda OP, número da bobina e peso. Seu
programa grava cada leitura no banco.

Tarefa: a tabela já existe:
    CREATE TABLE bobina (
        id INTEGER PRIMARY KEY, op INTEGER NOT NULL, numero INTEGER NOT NULL,
        peso_kg REAL NOT NULL CHECK (peso_kg > 0), UNIQUE (op, numero))
Implemente duas funções:
  1. inserir_bobina(conexao, op, numero, peso_kg): insere a bobina usando
     PARÂMETROS (?), faz commit e devolve o id gerado. Se o banco recusar
     (peso <= 0, bobina repetida), deixe o sqlite3.IntegrityError subir.
  2. contar_bobinas(conexao, op): quantas bobinas a OP tem (0 se nenhuma).

Exemplos:
    >>> inserir_bobina(conexao, 24518, 1, 1250.5)
    1
    >>> inserir_bobina(conexao, 24518, 2, 980.0)
    2
    >>> contar_bobinas(conexao, 24518)
    2

Dica: cursor = conexao.execute(sql, (a, b, c)); cursor.lastrowid. Para um valor
só: (op,) com vírgula. fetchone() devolve uma tupla: pegue o [0].

Teste com:  python curso.py testar 11 ex02
"""

import sqlite3


def inserir_bobina(conexao: sqlite3.Connection, op: int, numero: int, peso_kg: float) -> int:
    """Insere a bobina, grava e devolve o id gerado."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def contar_bobinas(conexao: sqlite3.Connection, op: int) -> int:
    """Quantidade de bobinas da OP."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
