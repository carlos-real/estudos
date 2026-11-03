"""
Exercício 14.04 — Regra nominal ± % (espessura e gramatura)
Nível: ★☆☆

Contexto: Espessura e gramatura não têm limite fixo: a tolerância é um percentual
sobre o valor nominal da OP (ex.: 40 µm ± 10% aceita de 36 a 44). Cuidado com o
float: 37 * (1 - 10/100) dá 33.300000000000004, e uma gramatura medida de 33.3
(exatamente no limite) seria reprovada injustamente.

Tarefa: implemente duas funções.
1. `limites_nominal(nominal, percentual)` devolve a tupla (minimo, maximo) =
   nominal ∓ nominal * percentual / 100, cada limite arredondado com round(x, 4).
   Levante ValueError se nominal ou percentual forem zero ou negativos.
2. `verificar_nominal(caracteristica, valor, nominal, percentual)` usa os limites
   (inclusivos) e devolve None se passou, ou o texto
   "<caracteristica> <valor> fora de <nominal> ± <percentual>% (<minimo> a <maximo>)"
   com todos os números formatados com :g.

Exemplos:
    >>> limites_nominal(40, 10)
    (36.0, 44.0)
    >>> limites_nominal(37, 10)
    (33.3, 40.7)
    >>> verificar_nominal("gramatura", 33.3, 37, 10) is None
    True
    >>> verificar_nominal("espessura", 44.8, 40, 10)
    'espessura 44.8 fora de 40 ± 10% (36 a 44)'

Dica: em verificar_nominal, reaproveite limites_nominal e desempacote a tupla.
Uma comparação encadeada (a <= x <= b) lê como na matemática.

Teste com:  python curso.py testar 14 ex04
"""


def limites_nominal(nominal: float, percentual: float) -> tuple[float, float]:
    """Faixa nominal ± percentual, com os limites arredondados em 4 casas."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def verificar_nominal(
    caracteristica: str, valor: float, nominal: float, percentual: float
) -> str | None:
    """Devolve None se o valor está na faixa nominal ± %, ou o motivo."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
