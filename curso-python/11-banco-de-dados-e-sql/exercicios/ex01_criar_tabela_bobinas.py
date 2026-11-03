"""
Exercício 11.01 — Criar a tabela de bobinas
Nível: ★☆☆

Contexto: o laboratório vai registrar cada bobina pesada num banco SQLite, em
vez de uma planilha. Antes de inserir qualquer coisa, a tabela precisa existir,
com regras que impeçam dados absurdos.

Tarefa: implemente criar_tabela_bobinas(conexao), que cria a tabela "bobina"
com as colunas, nesta ordem:
    id       inteiro, chave primária (o SQLite numera sozinho)
    op       inteiro, obrigatório (NOT NULL)
    numero   inteiro, obrigatório (o número da bobina dentro da OP)
    peso_kg  real, obrigatório e maior que zero (CHECK)
e com a regra: não pode haver duas bobinas com o mesmo par (op, numero).
Chamar a função duas vezes não pode dar erro (use IF NOT EXISTS). Grave com
commit.

Exemplo:
    >>> conexao = sqlite3.connect(":memory:")
    >>> criar_tabela_bobinas(conexao)
    >>> conexao.execute("INSERT INTO bobina (op, numero, peso_kg) VALUES (24518, 1, 1250.5)")
    >>> conexao.execute("INSERT INTO bobina (op, numero, peso_kg) VALUES (24518, 1, 980)")
    Traceback (most recent call last):
    sqlite3.IntegrityError: UNIQUE constraint failed: bobina.op, bobina.numero

Dica: CREATE TABLE IF NOT EXISTS nome (coluna TIPO RESTRIÇÕES, ..., UNIQUE (a, b)).

Teste com:  python curso.py testar 11 ex01
"""

import sqlite3


def criar_tabela_bobinas(conexao: sqlite3.Connection) -> None:
    """Cria a tabela 'bobina' (se ainda não existir)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
