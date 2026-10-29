"""
Exercício 01.13 — Diâmetro da bobina
Nível: ★★★

Contexto: Na rebobinadeira, ninguém mede o comprimento de uma bobina desenrolando o
filme. Usa-se geometria: o filme enrolado ocupa a área de uma "rosca" entre o tubete e
o diâmetro externo. Com a espessura do filme, dá para ir do comprimento ao diâmetro e
do diâmetro ao comprimento.

Fórmulas (todas as medidas em MILÍMETROS):
    diâmetro externo  D = raiz quadrada de ( d² + 4 x L x e / pi )
    comprimento       L = pi x (D² - d²) / (4 x e)
onde d = diâmetro do tubete, L = comprimento do filme e e = espessura do filme.

Tarefa:
1. `diametro_bobina_mm(comprimento_m, espessura_um, diametro_tubete_mm)` devolve o
   diâmetro externo em mm, arredondado para 1 casa decimal.
2. `comprimento_bobina_m(diametro_externo_mm, espessura_um, diametro_tubete_mm)`
   devolve o comprimento em METROS, arredondado para o metro inteiro com round(x)
   (sem o segundo argumento, round devolve um int).
Converta as unidades antes de usar as fórmulas: 1 m = 1000 mm e 1 µm = 0,001 mm.

Exemplos:
    >>> diametro_bobina_mm(4000, 25, 76)
    364.8
    >>> comprimento_bobina_m(500, 50, 152)
    3564

Dica: comece o arquivo com `import math` (logo abaixo desta docstring) para usar
math.sqrt e math.pi.

Teste com:  python curso.py testar 01 ex13
"""


def diametro_bobina_mm(
    comprimento_m: float, espessura_um: float, diametro_tubete_mm: float
) -> float:
    """Devolve o diâmetro externo da bobina (mm), em 1 casa decimal."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def comprimento_bobina_m(
    diametro_externo_mm: float, espessura_um: float, diametro_tubete_mm: float
) -> int:
    """Devolve o comprimento de filme na bobina, em metros inteiros."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
