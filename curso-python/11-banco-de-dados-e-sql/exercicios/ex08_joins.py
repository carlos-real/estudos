"""
Exercício 11.08 — JOINs: juntando OPs, clientes e expedição
Nível: ★★☆

Contexto: as informações estão espalhadas: a OP tem o cliente_id, o nome do
cliente está na tabela cliente e as cargas estão na expedicao. Relatório bom
junta tudo.

Tarefa: use o banco do laboratório. Implemente três funções:
  1. relatorio_ops(conexao, linha): lista de dicionários
     {"numero": ..., "cliente": nome do cliente, "produto": ...} das OPs da
     linha, ordenada por número.
  2. ops_sem_ensaio(conexao): números das OPs que não têm nenhum ensaio,
     em ordem crescente.
  3. peso_por_cliente(conexao): tuplas (nome do cliente, peso total expedido)
     de TODOS os clientes (quem não expediu nada aparece com 0.0), ordenadas
     por peso decrescente e, no empate, por nome.

Exemplos:
    >>> relatorio_ops(conexao, "D")[0]
    {'numero': 24541, 'cliente': 'Torrefação Serra Ltda', 'produto': 'Laminado PET/PE 62 µm'}
    >>> ops_sem_ensaio(conexao)
    [24550, 24551]
    >>> peso_por_cliente(conexao)[:2]
    [('Torrefação Serra Ltda', 6830.75), ('Agro Campo S.A.', 5350.0)]

Dica: JOIN ... ON; LEFT JOIN + "IS NULL" acha quem não tem par; dá para
encadear dois LEFT JOIN (cliente -> op -> expedicao); COALESCE(SUM(...), 0).

Teste com:  python curso.py testar 11 ex08
"""

import sqlite3


def relatorio_ops(conexao: sqlite3.Connection, linha: str) -> list[dict]:
    """OPs da linha com o nome do cliente."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def ops_sem_ensaio(conexao: sqlite3.Connection) -> list[int]:
    """OPs sem nenhum ensaio."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def peso_por_cliente(conexao: sqlite3.Connection) -> list[tuple[str, float]]:
    """Peso expedido por cliente (todos os clientes)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
