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

import math


def comprimento_bobina(
    diametro_externo_mm: float, diametro_tubete_mm: float, espessura_um: float
) -> float:
    """Comprimento aproximado do filme (m) numa bobina."""
    # Validar primeiro (retorno antecipado com erro): a conta só faz sentido assim.
    if espessura_um <= 0:
        raise ValueError("A espessura precisa ser maior que zero")
    if diametro_tubete_mm >= diametro_externo_mm:
        raise ValueError("O tubete precisa ser menor que o diâmetro externo")

    # Tudo na mesma unidade (metro) antes da conta: é aqui que mora o erro comum.
    externo = diametro_externo_mm / 1000
    tubete = diametro_tubete_mm / 1000
    espessura = espessura_um / 1_000_000

    # Área do anel (π/4 × (D² − d²)) dividida pela espessura = comprimento
    comprimento = math.pi * (externo**2 - tubete**2) / (4 * espessura)
    return round(comprimento, 1)


def bobinas_necessarias(metros_pedido: float, metros_por_bobina: float) -> int:
    """Quantidade mínima de bobinas inteiras para atender o pedido."""
    if metros_por_bobina <= 0:
        raise ValueError("metros_por_bobina precisa ser maior que zero")
    # math.ceil arredonda para cima: 4,2 bobinas viram 5 (não dá para mandar 0,2 bobina).
    # Alternativa sem math: -(-metros_pedido // metros_por_bobina), mas fica obscuro.
    return math.ceil(metros_pedido / metros_por_bobina)
