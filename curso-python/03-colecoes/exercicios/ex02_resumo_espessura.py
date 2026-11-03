"""
Exercício 03.02 — Resumo de espessura
Nível: ★☆☆

Contexto: No fim de cada turno, o laboratório anota um resumo das medições de
espessura (µm) de uma bobina: menor valor, maior valor, média e amplitude.

Tarefa: implemente `resumo_espessura(medicoes)`, que devolve um dicionário com
as chaves exatamente nesta forma:
    {"minimo": ..., "maximo": ..., "media": ..., "amplitude": ...}
- "media" e "amplitude" (máximo − mínimo) arredondadas com round(..., 2).
- Lista vazia: devolva um dicionário vazio {}.

Exemplos:
    >>> resumo_espessura([50.2, 49.8, 51.0, 50.6])
    {'minimo': 49.8, 'maximo': 51.0, 'media': 50.4, 'amplitude': 1.2}
    >>> resumo_espessura([])
    {}

Dica: sum, min, max e len fazem quase todo o trabalho. Sem round, a amplitude
acima sairia 1.2000000000000028 (lembra do problema do float no módulo 01?).

Teste com:  python curso.py testar 03 ex02
"""


def resumo_espessura(medicoes: list[float]) -> dict[str, float]:
    """Devolve mínimo, máximo, média e amplitude das medições."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
