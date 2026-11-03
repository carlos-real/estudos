"""Exemplo 05 — *args e **kwargs: quantos argumentos vierem.

Rode na pasta 04-funcoes:  python exemplos/05_args_kwargs.py
"""


def media(*valores):
    print("  valores chegou como", type(valores).__name__, valores)
    if not valores:
        return None
    return sum(valores) / len(valores)


print(media(50.2, 49.8, 51.0))
print(media())
medicoes = [50.0, 52.0]
print(media(*medicoes))  # * na CHAMADA espalha a lista em argumentos


def criar_amostra(op, linha, **medidas):
    print("  medidas chegou como", type(medidas).__name__, medidas)
    return {"op": op, "linha": linha, **medidas}


print(criar_amostra("OP-4512", "A", espessura=50.2, cof=0.22))
dados = {"op": "OP-4513", "linha": "B", "gramatura": 18.4}
print(criar_amostra(**dados))  # ** na CHAMADA espalha o dicionário em nomeados
