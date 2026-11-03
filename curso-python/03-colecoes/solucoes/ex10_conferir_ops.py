"""
Solução — Exercício 03.10 — OPs pedidas x OPs com resultado

Ideia central: perguntas do tipo "o que está em A e em B?", "o que está em A mas
não em B?" são operações de CONJUNTO. Sem laços, sem ifs.
"""


def conferir_ops(ops_pedidas: list[str], ops_com_resultado: list[str]) -> dict[str, list[str]]:
    """Cruza OPs pedidas com OPs que têm resultado (listas ordenadas)."""
    # set() já elimina as repetições.
    pedidas = set(ops_pedidas)
    com_resultado = set(ops_com_resultado)

    # &  -> interseção: está nos dois
    # -  -> diferença: está no da esquerda e NÃO no da direita
    # sorted() devolve uma LISTA ordenada (conjuntos não têm ordem garantida).
    return {
        "prontas": sorted(pedidas & com_resultado),
        "sem_resultado": sorted(pedidas - com_resultado),
        "nao_pedidas": sorted(com_resultado - pedidas),
    }

    # Os métodos equivalentes também funcionam e aceitam listas direto:
    #     pedidas.intersection(ops_com_resultado)
    #     pedidas.difference(ops_com_resultado)
