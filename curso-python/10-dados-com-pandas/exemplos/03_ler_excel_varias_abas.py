"""Exemplo 03 — Ler planilhas Excel: uma aba, várias abas, todas as abas.

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/03_ler_excel_varias_abas.py
"""

from pathlib import Path

import pandas as pd

DADOS = Path(__file__).resolve().parent.parent / "dados"
PLANILHA = DADOS / "planilha_linhas.xlsx"

# 1) Uma aba só. A linha 1 da planilha tem um título; o cabeçalho está na linha 2.
#    header=1 diz: "o cabeçalho está na linha de índice 1" (a segunda linha).
aba_a = pd.read_excel(PLANILHA, sheet_name="Linha A", header=1, dtype={"OP": str})
print(aba_a.columns.tolist())
print(aba_a[["OP", "Bobina", "Espessura (µm)"]].head(3))

# 2) Todas as abas de uma vez: sheet_name=None devolve um DICIONÁRIO
#    {nome da aba: DataFrame}.
abas = pd.read_excel(PLANILHA, sheet_name=None, header=1, dtype={"OP": str})
print(type(abas))
for nome, tabela in abas.items():
    print(f"{nome}: {len(tabela)} linhas")

# 3) Juntar tudo numa tabela só, guardando de qual aba veio cada linha.
partes = []
for nome, tabela in abas.items():
    partes.append(tabela.assign(linha=nome.removeprefix("Linha ")))
todas = pd.concat(partes, ignore_index=True)
print("Total:", todas.shape)

# 4) Nomes de coluna com acento, espaço e unidade são ruins de digitar.
#    Renomeie logo depois de ler.
todas = todas.rename(
    columns={
        "OP": "op",
        "Bobina": "bobina",
        "Data": "data",
        "Espessura (µm)": "espessura_um",
        "Gramatura (g/m²)": "gramatura_gm2",
        "COF": "cof",
        "Peso (kg)": "peso_kg",
        "Observação": "observacao",
    }
)
print(todas[["linha", "op", "data", "espessura_um"]].tail(3))
print("Tipo da coluna data:", todas["data"].dtype)  # o Excel já entrega datas
