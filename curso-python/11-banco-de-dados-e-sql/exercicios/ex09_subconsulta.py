"""
Exercício 11.09 — Subconsultas
Nível: ★★☆

Contexto: algumas perguntas dependem de outra pergunta: "quais OPs são maiores
que a média?" precisa primeiro da média; "quais OPs tiveram reprovação?"
precisa primeiro da lista de ensaios FORA.

Tarefa: use o banco do laboratório. Resolva com subconsultas (SELECT dentro de
SELECT). Implemente três funções:
  1. ops_acima_da_media(conexao): tuplas (numero, quantidade_kg) das OPs com
     quantidade acima da média de todas as OPs, da maior para a menor.
  2. ops_com_reprovacao(conexao): números das OPs com pelo menos um ensaio
     'FORA', em ordem crescente.
  3. clientes_sem_op(conexao): nomes dos clientes sem nenhuma OP, em ordem
     alfabética.

Exemplos:
    >>> ops_acima_da_media(conexao)[:2]
    [(24521, 6000.0), (24520, 5200.0)]
    >>> ops_com_reprovacao(conexao)
    [24519, 24527, 24533, 24546]
    >>> clientes_sem_op(conexao)
    ['Café do Vale']

Dica: WHERE x > (SELECT AVG(...) ...); WHERE numero IN (SELECT ...);
WHERE NOT EXISTS (SELECT 1 FROM ... WHERE ...).

Teste com:  python curso.py testar 11 ex09
"""

import sqlite3


def ops_acima_da_media(conexao: sqlite3.Connection) -> list[tuple[int, float]]:
    """OPs com quantidade acima da média."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def ops_com_reprovacao(conexao: sqlite3.Connection) -> list[int]:
    """OPs com algum ensaio FORA."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def clientes_sem_op(conexao: sqlite3.Connection) -> list[str]:
    """Clientes sem nenhuma OP."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
