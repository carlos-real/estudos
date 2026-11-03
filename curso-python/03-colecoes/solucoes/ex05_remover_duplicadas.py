"""
Solução — Exercício 03.05 — Lotes sem repetição

Ideia central: conjunto para PERGUNTAR ("já vi?"), lista para GUARDAR a ordem.
"""


def remover_duplicadas(itens: list[str]) -> list[str]:
    """Devolve uma lista nova, sem repetidos, na ordem da primeira ocorrência."""
    vistos: set[str] = set()  # set() vazio. Cuidado: {} seria um dicionário!
    resultado: list[str] = []
    for item in itens:
        # "in" num conjunto é muito rápido, mesmo com milhares de itens.
        # Numa lista, o Python teria que comparar item por item.
        if item not in vistos:
            vistos.add(item)
            resultado.append(item)
    return resultado

    # Alternativa curta e idiomática: dicionários guardam a ordem de inserção e
    # não repetem chaves. dict.fromkeys(itens) cria {item: None, ...}:
    #     return list(dict.fromkeys(itens))
