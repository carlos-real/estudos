"""
Exercício 11.13 — Revisão: importar a planilha da expedição para o banco
Nível: ★★☆

Revisão intercalada: CSV com ponto e vírgula e exceções (módulo 06), números
brasileiros (módulo 05), datas com datetime (módulo 07), conjuntos (módulo 03)
e INSERT em transação (este módulo).

Contexto: a expedição mantém um CSV (salvo pelo Excel) com as cargas do dia.
Você vai importar esse arquivo para a tabela expedicao do banco do laboratório:
    expedicao(id, op, nf, peso_kg, data)   -- data no formato 'AAAA-MM-DD'

Formato do arquivo (UTF-8 com BOM, separador ";", cabeçalho na linha 1):
    op;nf;peso;data
    24518;123480;1.250,5;30/10/2026

Tarefa: implemente importar_expedicao(conexao, caminho), que devolve a tupla
(quantidade_inserida, linhas_com_erro). Uma linha do arquivo é válida quando:
  - op é um número inteiro de uma OP que EXISTE na tabela op;
  - nf não está vazia (guarde como texto, sem espaços nas pontas);
  - peso, no formato brasileiro ("1.250,5"), é maior que zero;
  - data é uma data válida no formato dd/mm/aaaa (grave como 'AAAA-MM-DD').
Linhas inválidas são puladas e o NÚMERO da linha no arquivo vai para a lista
de erros (o cabeçalho é a linha 1, então o primeiro dado é a linha 2). As
válidas são gravadas todas juntas, numa transação.

Exemplo: com o arquivo acima mais a linha "99999;123481;100,0;30/10/2026"
    >>> importar_expedicao(conexao, "expedicao.csv")
    (1, [3])

Dica: csv.DictReader(arquivo, delimiter=";"); enumerate(leitor, start=2);
datetime.strptime(texto, "%d/%m/%Y").date().isoformat(); pegue os números das
OPs uma vez só, num set, antes do laço.

Teste com:  python curso.py testar 11 ex13
"""

import sqlite3
from pathlib import Path


def importar_expedicao(
    conexao: sqlite3.Connection, caminho: str | Path
) -> tuple[int, list[int]]:
    """Importa as cargas válidas e devolve (inseridas, linhas com erro)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
