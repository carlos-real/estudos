"""
Exercício 09.06 — Conserte o bug: peso total por NF
Nível: ★★☆

Solução comentada. Veja o enunciado completo em exercicios/ex06_conserte_pesos_por_nf.py.
"""


def somar_pesos_por_nf(pedidos: list[dict]) -> dict[str, float]:
    """Soma o peso (kg) de cada NF. Uma NF pode aparecer em vários pedidos."""
    totais: dict[str, float] = {}
    for pedido in pedidos:
        # BUG 1 (espaços): " 1001" e "1001" viravam chaves diferentes. O strip()
        # normaliza a chave ANTES de usá-la no dicionário.
        nf = pedido["nf"].strip()

        # BUG 2 (sobrescrever): o original fazia totais[nf] = peso, e cada
        # carregamento apagava o anterior: ficava só o ÚLTIMO peso de cada NF.
        # O padrão "acumulador em dicionário" (módulo 03) é: pegue o valor
        # atual (0.0 se a chave ainda não existe) e some.
        totais[nf] = totais.get(nf, 0.0) + pedido["peso"]
    return totais


# Alternativa com collections.defaultdict (módulo 07):
#     totais = defaultdict(float)
#     for pedido in pedidos:
#         totais[pedido["nf"].strip()] += pedido["peso"]
#     return dict(totais)
