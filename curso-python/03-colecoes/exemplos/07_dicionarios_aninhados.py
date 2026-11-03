"""Exemplo 07 — Dicionários aninhados: tolerâncias por linha.

Rode na pasta 03-colecoes:  python exemplos/07_dicionarios_aninhados.py
"""

TOLERANCIAS = {
    "A": {
        "espessura": {"nominal": 50.0, "tol_pct": 10.0},
        "gramatura": {"nominal": 46.0, "tol_pct": 5.0},
        "cof": {"min": 0.15, "max": 0.30},
    },
    "B": {
        "espessura": {"nominal": 20.0, "tol_pct": 8.0},
        "cof": {"min": 0.20, "max": 0.40},
    },
}

# Acesso em cadeia: cada [] desce um nível
print("Nominal de espessura da A:", TOLERANCIAS["A"]["espessura"]["nominal"])

# Guardar um nível numa variável deixa o código legível
regra = TOLERANCIAS["A"]["espessura"]
minimo = round(regra["nominal"] * (1 - regra["tol_pct"] / 100), 2)
maximo = round(regra["nominal"] * (1 + regra["tol_pct"] / 100), 2)
print(f"Espessura da linha A: {minimo} a {maximo} µm")

# Acesso seguro: .get com {} como padrão permite encadear
print("Linha E:", TOLERANCIAS.get("E", {}).get("espessura"))
print("Gramatura da B:", TOLERANCIAS.get("B", {}).get("gramatura"))

# Percorrer dois níveis
for linha, propriedades in TOLERANCIAS.items():
    print(f"Linha {linha}:")
    for nome, regra in propriedades.items():
        print(f"  {nome}: {regra}")
