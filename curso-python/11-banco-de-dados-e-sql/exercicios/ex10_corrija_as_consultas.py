"""
Exercício 11.10 — Corrija as consultas (leitura de código e depuração)
Nível: ★★☆

Contexto: um colega escreveu três consultas para o painel do laboratório. Todas
RODAM sem erro, mas devolvem resultados errados. Leia cada uma e descubra o
defeito antes de rodar qualquer coisa.

    # (1) Ensaios ainda sem valor
    SELECT op, bobina, caracteristica
    FROM ensaio
    WHERE valor = NULL
    ORDER BY op, bobina, caracteristica

    # (2) Quantos ensaios cada OP tem (inclusive as que não têm nenhum)
    SELECT o.numero, COUNT(*)
    FROM op AS o
    LEFT JOIN ensaio AS e ON e.op = o.numero
    GROUP BY o.numero
    ORDER BY o.numero

    # (3) TODOS os clientes, cada um com as suas OPs de uma linha (ou None)
    SELECT c.nome, o.numero
    FROM cliente AS c
    LEFT JOIN op AS o ON o.cliente_id = c.id
    WHERE o.linha = ?
    ORDER BY c.nome, o.numero

Tarefa: escreva as versões corretas (use o banco do laboratório):
  1. ensaios_sem_valor(conexao) -> lista de (op, bobina, caracteristica).
  2. ensaios_por_op(conexao) -> lista de (numero, quantidade) de TODAS as OPs;
     OP sem ensaio tem quantidade 0.
  3. clientes_e_ops_da_linha(conexao, linha) -> lista de (nome, numero) com
     TODOS os clientes; quem não tem OP na linha aparece uma vez, com None.
     Ordem: nome e depois número.

Exemplos:
    >>> ensaios_sem_valor(conexao)
    [(24534, 2, 'cof')]
    >>> ensaios_por_op(conexao)[-1]
    (24551, 0)
    >>> clientes_e_ops_da_linha(conexao, "B")[:2]
    [('Agro Campo S.A.', None), ('Biscoitos Aurora', None)]

Dica: (1) como se compara com NULL? (2) o que COUNT(*) conta numa linha que o
LEFT JOIN completou com NULL? (3) o que o WHERE faz com as linhas em que
o.linha é NULL? Onde mais dá para pôr essa condição?

Teste com:  python curso.py testar 11 ex10
"""

import sqlite3


def ensaios_sem_valor(conexao: sqlite3.Connection) -> list[tuple[int, int, str]]:
    """Ensaios ainda sem valor."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def ensaios_por_op(conexao: sqlite3.Connection) -> list[tuple[int, int]]:
    """Quantidade de ensaios de cada OP (0 se nenhum)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def clientes_e_ops_da_linha(
    conexao: sqlite3.Connection, linha: str
) -> list[tuple[str, int | None]]:
    """Todos os clientes com as OPs da linha (ou None)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
