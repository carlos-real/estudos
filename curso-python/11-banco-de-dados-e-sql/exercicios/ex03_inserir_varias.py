"""
Exercício 11.03 — Inserir vários ensaios de uma vez (tudo ou nada)
Nível: ★☆☆

Contexto: ao terminar uma OP, o laboratório lança todos os ensaios de uma vez.
Se UM deles estiver errado, nenhum deve ser gravado: lote pela metade no banco
é pior do que lote nenhum.

Tarefa: a tabela já existe:
    CREATE TABLE ensaio (
        id INTEGER PRIMARY KEY, op INTEGER NOT NULL, bobina INTEGER NOT NULL,
        caracteristica TEXT NOT NULL, valor REAL)
Implemente inserir_ensaios(conexao, ensaios), em que ensaios é uma lista de
tuplas (op, bobina, caracteristica, valor). Insira todas numa transação só
(executemany dentro de "with conexao:") e devolva quantas foram inseridas.
Lista vazia -> 0. Se alguma for recusada pelo banco, o sqlite3.IntegrityError
deve subir e NENHUMA linha do lote pode ficar gravada.

Exemplo:
    >>> inserir_ensaios(conexao, [(24518, 1, "espessura", 38.8),
    ...                           (24518, 1, "cof", 0.31)])
    2

Dica: "with conexao:" faz commit no fim do bloco, ou rollback se der erro.

Teste com:  python curso.py testar 11 ex03
"""

import sqlite3


def inserir_ensaios(
    conexao: sqlite3.Connection, ensaios: list[tuple[int, int, str, float | None]]
) -> int:
    """Insere todos os ensaios numa transação e devolve a quantidade."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
