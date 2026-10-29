"""
Exercício 01.09 — Gramatura e peso da bobina
Nível: ★★☆

Contexto: Para medir a gramatura, o laboratório corta um corpo de prova retangular do
filme e pesa na balança analítica. Gramatura é massa por área: gramas por metro
quadrado (g/m²). Com a gramatura, dá para estimar o peso de uma bobina inteira.

Tarefa:
1. `calcular_gramatura(massa_g, largura_cm, comprimento_cm)` devolve a gramatura em
   g/m², arredondada para 1 casa decimal. Lembre: 1 cm = 0,01 m.
2. `peso_bobina_kg(gramatura_g_m2, largura_mm, comprimento_m)` devolve o peso da
   bobina em kg, arredondado para 2 casas:
   gramatura (g/m²) x largura (m) x comprimento (m) = gramas; divida por 1000 para kg.
   Lembre: 1 mm = 0,001 m.

Exemplos:
    >>> calcular_gramatura(0.523, 10, 10)
    52.3
    >>> peso_bobina_kg(52.3, 600, 4000)
    125.52

Dica: calcule a área em m² numa variável separada antes de dividir.

Teste com:  python curso.py testar 01 ex09
"""


def calcular_gramatura(massa_g: float, largura_cm: float, comprimento_cm: float) -> float:
    """Devolve a gramatura (g/m²) do corpo de prova, em 1 casa decimal."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def peso_bobina_kg(gramatura_g_m2: float, largura_mm: float, comprimento_m: float) -> float:
    """Devolve o peso estimado da bobina em kg, em 2 casas decimais."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
