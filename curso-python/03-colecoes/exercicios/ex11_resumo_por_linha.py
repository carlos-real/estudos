"""
Exercício 03.11 — Resumo por linha (o seu primeiro GROUP BY)
Nível: ★★★

Contexto: As amostras do dia estão numa "tabela": uma lista de dicionários, um
por amostra. Algumas células vieram vazias (a chave falta ou o valor é None).
O supervisor quer, para cada linha de produção, quantas amostras têm valor e a
média, o mínimo e o máximo de uma propriedade (espessura, gramatura...).

Tarefa: implemente duas funções (a segunda usa a primeira).
1. `agrupar_valores(amostras, campo)` devolve  linha -> lista de valores do
   campo, na ordem em que aparecem. Ignore amostras em que o campo falta ou é
   None. Linhas sem nenhum valor válido não aparecem.
2. `resumo_por_linha(amostras, campo)` devolve  linha -> {"qtd": ...,
   "media": ..., "minimo": ..., "maximo": ...}, com "media" arredondada com
   round(..., 2) e as linhas em ORDEM ALFABÉTICA.

Exemplos:
    >>> amostras = [
    ...     {"op": "OP-4512", "linha": "B", "espessura": 20.9},
    ...     {"op": "OP-4513", "linha": "A", "espessura": 50.4},
    ...     {"op": "OP-4514", "linha": "A", "espessura": 49.7},
    ...     {"op": "OP-4515", "linha": "A", "espessura": None},
    ...     {"op": "OP-4516", "linha": "C"},
    ... ]
    >>> agrupar_valores(amostras, "espessura")
    {'B': [20.9], 'A': [50.4, 49.7]}
    >>> resumo_por_linha(amostras, "espessura")["A"]
    {'qtd': 2, 'media': 50.05, 'minimo': 49.7, 'maximo': 50.4}
    >>> list(resumo_por_linha(amostras, "espessura"))
    ['A', 'B']

Dica: amostra.get(campo) devolve None tanto se a chave falta quanto se o valor
é None. Para a ordem alfabética, percorra sorted(grupos).

Teste com:  python curso.py testar 03 ex11
"""


def agrupar_valores(amostras: list[dict], campo: str) -> dict[str, list[float]]:
    """Agrupa os valores válidos do campo por linha (ordem de aparição)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def resumo_por_linha(amostras: list[dict], campo: str) -> dict[str, dict[str, float]]:
    """Devolve qtd, média, mínimo e máximo do campo para cada linha (A-Z)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
