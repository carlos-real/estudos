"""Exemplo 01 — Series e DataFrame, as duas estruturas do pandas.

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/01_series_e_dataframe.py
"""

import pandas as pd

print("pandas versão", pd.__version__)

# Uma Series é uma coluna: valores + rótulos (o índice) + um tipo (dtype).
espessuras = pd.Series([50.2, 49.1, 51.8, 47.9], name="espessura_um")
print(espessuras)

# Operações valem para a coluna inteira de uma vez (vetorização).
print("Média:", espessuras.mean())
print("Máximo:", espessuras.max())
print(espessuras - 50)

# Comparar também é vetorizado: o resultado é uma Series de True/False.
print(espessuras < 49.5)

# Um DataFrame é uma tabela: várias Series com o mesmo índice.
df = pd.DataFrame(
    {
        "op": ["024412", "024412", "024413", "024420"],
        "linha": ["A", "A", "B", "C"],
        "espessura_um": [40.2, 39.1, 35.3, 69.8],
        "peso_kg": [1250.5, 980.0, 1310.2, 845.7],
    }
)
print(df)
print("Formato (linhas, colunas):", df.shape)
print("Colunas:", list(df.columns))
print(df.dtypes)

# Cada coluna é uma Series.
print(type(df["peso_kg"]))
print("Peso total:", df["peso_kg"].sum())

# Também dá para criar a partir de uma lista de dicionários (a "tabela" do módulo 03).
registros = [
    {"aluno": "Ana", "nota": 8.5},
    {"aluno": "Bruno", "nota": 6.0},
    {"aluno": "Carla", "nota": 9.5},
]
notas = pd.DataFrame(registros)
print(notas)
print("Média da turma:", notas["nota"].mean())
