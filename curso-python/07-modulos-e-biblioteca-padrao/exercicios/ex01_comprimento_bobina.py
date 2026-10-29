"""
Exercício 07.01 — Comprimento da bobina e bobinas por pedido
Nível: ★☆☆

Contexto: A expedição pergunta quantos metros de filme cabem numa bobina e quantas
bobinas são necessárias para atender um pedido. Dá para estimar só com geometria:
a bobina é um "anel" de filme enrolado em volta do tubete.

Tarefa:
1. `comprimento_bobina(diametro_externo_mm, diametro_tubete_mm, espessura_um)` devolve
   o comprimento aproximado do filme em METROS, arredondado com round(..., 1):
       L = π × (D² − d²) / (4 × e)
   D = diâmetro externo, d = diâmetro do tubete, e = espessura, todos em METROS
   (mm → m: divida por 1000; µm → m: divida por 1_000_000). Use math.pi.
   Levante ValueError se a espessura for <= 0 ou se o tubete não for menor que o
   diâmetro externo.
2. `bobinas_necessarias(metros_pedido, metros_por_bobina)` devolve quantas bobinas
   INTEIRAS atendem o pedido (sempre arredonda para cima: use math.ceil).
   Levante ValueError se metros_por_bobina <= 0.

Exemplos:
    >>> comprimento_bobina(600, 152, 25)
    10583.9
    >>> bobinas_necessarias(50000, 10583.9)
    5
    >>> bobinas_necessarias(20000, 10583.9)
    2

Dica: escreva `import math` no topo. math.ceil(4.01) é 5 e math.ceil(4.0) é 4.

Teste com:  python curso.py testar 07 ex01
"""


def comprimento_bobina(
    diametro_externo_mm: float, diametro_tubete_mm: float, espessura_um: float
) -> float:
    """Comprimento aproximado do filme (m) numa bobina."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def bobinas_necessarias(metros_pedido: float, metros_por_bobina: float) -> int:
    """Quantidade mínima de bobinas inteiras para atender o pedido."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
