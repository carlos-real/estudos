"""chain e groupby: juntar listas e agrupar sequências.

Rode com:  python exemplos/07_itertools_lab.py
"""

from itertools import chain, groupby

# chain: emenda várias listas sem criar listas intermediárias
email_1 = [("OP245101", "123456", 1250.5)]
email_2 = [("OP245102", "123457", 980.0), ("OP245103", "123457", 410.0)]
todos = list(chain(email_1, email_2))
print("Itens da expedição:", len(todos))

abas = {"A": [20.1, 19.8], "B": [25.2], "C": [40.3, 39.9, 41.0]}
todas_as_leituras = list(chain.from_iterable(abas.values()))
print("Todas as leituras:", todas_as_leituras)

# groupby: agrupa itens VIZINHOS com a mesma chave
resultados = ["A", "A", "R", "R", "R", "A", "R"]
for chave, grupo in groupby(resultados):
    print(chave, len(list(grupo)))

# Para agrupar por lote, ORDENE pela mesma chave antes
bobinas = [("L02", 150.0), ("L01", 120.5), ("L02", 149.5), ("L01", 121.0)]
bobinas_ordenadas = sorted(bobinas, key=lambda b: b[0])
for lote, grupo in groupby(bobinas_ordenadas, key=lambda b: b[0]):
    pesos = [peso for _, peso in grupo]
    print(f"Lote {lote}: {len(pesos)} bobinas, {sum(pesos):.1f} kg")
