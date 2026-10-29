"""
Exercício 14.03 — Regra de tolerância fixa (mínimo/máximo)
Nível: ★☆☆

Contexto: COF, tração e selagem têm limites fixos. Às vezes só um lado existe
(tração: só mínimo). O relatório precisa dizer POR QUE a OP reprovou, então a regra
não devolve True/False: devolve None (passou) ou um texto com o motivo.

Tarefa: implemente `verificar_fixa(caracteristica, valor, minimo, maximo)`.
- minimo ou maximo None significa "sem limite daquele lado".
- Os limites são inclusivos: valor igual ao mínimo ou ao máximo passa.
- Abaixo do mínimo: devolva "<caracteristica> <valor> abaixo do mínimo <minimo>".
- Acima do máximo: devolva "<caracteristica> <valor> acima do máximo <maximo>".
- Dentro: devolva None.
- Formate os números com :g (0.30 vira 0.3; 8.0 vira 8).

Exemplos:
    >>> verificar_fixa("cof", 0.22, 0.15, 0.35) is None
    True
    >>> verificar_fixa("cof", 0.38, 0.15, 0.35)
    'cof 0.38 acima do máximo 0.35'
    >>> verificar_fixa("selagem", 7.6, 8.0, None)
    'selagem 7.6 abaixo do mínimo 8'
    >>> verificar_fixa("tracao", 999.0, 20.0, None) is None
    True

Dica: teste "minimo is not None" ANTES de comparar: None < 0.15 dá TypeError.

Teste com:  python curso.py testar 14 ex03
"""


def verificar_fixa(
    caracteristica: str, valor: float, minimo: float | None, maximo: float | None
) -> str | None:
    """Devolve None se o valor está nos limites, ou o motivo da reprovação."""
    # "and" curto-circuita: se minimo for None, a comparação nem é avaliada.
    if minimo is not None and valor < minimo:
        return f"{caracteristica} {valor:g} abaixo do mínimo {minimo:g}"
    if maximo is not None and valor > maximo:
        return f"{caracteristica} {valor:g} acima do máximo {maximo:g}"
    # Usamos < e > (e não <= e >=) porque os limites são aceitos.
    return None
