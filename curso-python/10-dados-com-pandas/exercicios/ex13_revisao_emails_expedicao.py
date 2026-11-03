"""
Exercício 10.13 — Revisão: e-mails da expedição viram tabela
Nível: ★★☆

Revisão intercalada: expressões regulares e números brasileiros (módulo 05),
listas e dicionários (módulo 03) e pandas (este módulo).

Contexto: a expedição pede certificados por e-mail. Cada e-mail tem, em algum
lugar do texto, linhas assim:

    OP: 24518
    NF: 123456
    Peso: 1.250,5 kg

Uma mesma OP pode sair em várias notas fiscais (cargas parciais).

Tarefa: implemente três funções.
  1. extrair_pedido(texto): devolve {"op": int, "nf": str, "peso_kg": float}
     ou None se faltar qualquer um dos três. Aceite maiúsculas ou minúsculas
     ("op:", "Peso:") e espaços variados depois dos dois-pontos. O peso vem no
     formato brasileiro ("1.250,5" -> 1250.5; "980" -> 980.0).
  2. pedidos_para_tabela(emails): recebe uma lista de textos e devolve um
     DataFrame com as colunas "op", "nf", "peso_kg", um pedido por linha, na
     ordem dos e-mails, ignorando os incompletos. Sem pedidos válidos: DataFrame
     vazio, mas com essas três colunas.
  3. peso_por_op(pedidos): recebe a tabela do item 2 e devolve um DataFrame com
     as colunas "op", "notas" (quantas NFs) e "peso_total_kg" (soma, 1 casa),
     uma linha por OP, em ordem crescente de OP, índice 0, 1, 2...

Exemplos:
    >>> extrair_pedido("Bom dia!\\nOP: 24518\\nNF: 123456\\nPeso: 1.250,5 kg")
    {'op': 24518, 'nf': '123456', 'peso_kg': 1250.5}
    >>> extrair_pedido("OP: 24518 (NF ainda não emitida)") is None
    True

Dica: re.search(r"OP:\\s*(\\d+)", texto, re.IGNORECASE); para o peso, capture
[\\d.,]+ e converta tirando o ponto e trocando a vírgula. Monte uma lista de
dicionários e passe para pd.DataFrame(lista, columns=[...]).

Teste com:  python curso.py testar 10 ex13
"""

import re  # noqa: F401  (você vai usar)

import pandas as pd


def extrair_pedido(texto: str) -> dict | None:
    """Extrai OP, NF e peso de um e-mail (None se faltar algum)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def pedidos_para_tabela(emails: list[str]) -> pd.DataFrame:
    """Um pedido válido por linha, nas colunas op, nf e peso_kg."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def peso_por_op(pedidos: pd.DataFrame) -> pd.DataFrame:
    """Quantidade de notas e peso total por OP."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
