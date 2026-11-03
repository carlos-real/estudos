"""
Exercício 11.01 — Criar a tabela de bobinas (SOLUÇÃO)

Cada restrição é uma regra de negócio que o BANCO passa a garantir, não importa
qual programa (ou pessoa) insira os dados.
"""

import sqlite3

SQL_BOBINA = """
CREATE TABLE IF NOT EXISTS bobina (
    id      INTEGER PRIMARY KEY,                    -- numerado sozinho
    op      INTEGER NOT NULL,
    numero  INTEGER NOT NULL,
    peso_kg REAL    NOT NULL CHECK (peso_kg > 0),   -- peso zero ou negativo: recusado
    UNIQUE (op, numero)                             -- a bobina 1 da OP só existe uma vez
)
"""


def criar_tabela_bobinas(conexao: sqlite3.Connection) -> None:
    """Cria a tabela 'bobina' (se ainda não existir)."""
    # IF NOT EXISTS torna a função "idempotente": rodar duas vezes dá o mesmo
    # resultado que rodar uma. Bom para scripts que sobem o banco ao iniciar.
    conexao.execute(SQL_BOBINA)
    conexao.commit()
