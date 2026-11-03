"""
Exercício 01.06 — Peso líquido do palete
Nível: ★★☆

Contexto: A expedição pesa o palete inteiro na balança (peso bruto). Para a nota
fiscal, o que vale é o peso líquido do filme: tire o peso do palete de madeira e o peso
de cada tubete (o tubo de papelão no centro de cada bobina).

Tarefa: implemente `calcular_peso_liquido(peso_bruto_kg, tara_palete_kg, qtd_bobinas,
peso_tubete_kg)`, que devolve:
    peso bruto - tara do palete - (quantidade de bobinas x peso de um tubete)
arredondado para 2 casas decimais com round().

Exemplos:
    >>> calcular_peso_liquido(1250.5, 22.0, 8, 1.35)
    1217.7
    >>> calcular_peso_liquido(500.0, 18.7, 4, 1.237)
    476.35

Dica: confira no REPL quanto dá 500.0 - 18.7 - 4 * 1.237 sem arredondar.

Teste com:  python curso.py testar 01 ex06
"""


def calcular_peso_liquido(
    peso_bruto_kg: float, tara_palete_kg: float, qtd_bobinas: int, peso_tubete_kg: float
) -> float:
    """Devolve o peso líquido do palete, arredondado em 2 casas."""
    # Decompor em passos com nomes claros ajuda a conferir cada parte da conta.
    tara_tubetes = qtd_bobinas * peso_tubete_kg
    liquido = peso_bruto_kg - tara_palete_kg - tara_tubetes
    # 500.0 - 18.7 - 4 * 1.237 dá 476.35200000000003 por causa do float.
    # Arredondar no fim (e só no fim) evita acumular erros de arredondamento.
    return round(liquido, 2)
