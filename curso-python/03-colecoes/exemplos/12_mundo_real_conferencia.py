"""Exemplo 12 — No mundo real: conferência do dia e fila de certificados.

Junta tudo do módulo: dicionário aninhado (tolerâncias), lista de dicionários
(a "planilha" de amostras), conjuntos (OPs da expedição) e compreensões.

Rode na pasta 03-colecoes:  python exemplos/12_mundo_real_conferencia.py
"""

# Tolerâncias por linha: espessura e gramatura em nominal ± %, COF em mín/máx.
TOLERANCIAS = {
    "A": {"espessura": (50.0, 10.0), "gramatura": (46.0, 5.0), "cof": (0.15, 0.30)},
    "B": {"espessura": (20.0, 8.0), "gramatura": (18.5, 5.0), "cof": (0.20, 0.40)},
    "C": {"espessura": (35.0, 10.0), "gramatura": (32.0, 6.0), "cof": (0.15, 0.30)},
    "D": {"espessura": (70.0, 7.0), "gramatura": (65.0, 5.0), "cof": (0.10, 0.25)},
}
PERCENTUAIS = {"espessura", "gramatura"}  # as outras são faixa fixa (mín, máx)

# A "planilha" do dia: um cabeçalho e uma tupla por linha, como num CSV.
COLUNAS = ("op", "linha", "espessura", "gramatura", "cof", "obs")
PLANILHA = [
    ("OP-4512", "A", 50.4, 46.3, 0.22, ""),
    ("OP-4513", "B", 21.9, 18.4, 0.31, ""),
    ("OP-4514", "A", 49.1, 45.8, 0.33, "COF: liberado"),
    ("OP-4515", "C", 35.2, 31.0, 0.18, ""),
    ("OP-4516", "D", 76.0, 69.0, 0.12, ""),
    ("OP-4517", "D", 69.5, 64.2, 0.11, ""),
]
# zip casa cada nome de coluna com o valor da linha; dict transforma os pares
# em dicionário. Resultado: uma lista de dicionários (a nossa "tabela").
AMOSTRAS = [dict(zip(COLUNAS, linha, strict=True)) for linha in PLANILHA]

# OPs que a expedição pediu por e-mail (com uma repetida, como acontece).
OPS_PEDIDAS = ["OP-4512", "OP-4514", "OP-4516", "OP-4520", "OP-4512"]


def faixa(propriedade, regra):
    """Converte a regra em (mínimo, máximo)."""
    if propriedade in PERCENTUAIS:
        nominal, pct = regra
        return round(nominal * (1 - pct / 100), 2), round(nominal * (1 + pct / 100), 2)
    return regra  # já é (mínimo, máximo)


def conferir(amostra):
    """Devolve uma cópia da amostra com as colunas 'falhas' e 'status'."""
    regras = TOLERANCIAS[amostra["linha"]]
    falhas = []
    for propriedade, regra in regras.items():
        minimo, maximo = faixa(propriedade, regra)
        if not minimo <= amostra[propriedade] <= maximo:
            falhas.append(propriedade)

    if not falhas:
        status = "APROVADA"
    elif falhas == ["cof"] and "cof: liberado" in amostra["obs"].lower():
        status = "LIBERADA"  # COF fora, mas liberado pela qualidade
    else:
        status = "REPROVADA"
    return {**amostra, "falhas": falhas, "status": status}


conferidas = [conferir(amostra) for amostra in AMOSTRAS]

print("== Conferência do dia ==")
for c in conferidas:
    detalhe = ", ".join(c["falhas"]) if c["falhas"] else "-"
    print(f"{c['op']}  linha {c['linha']}  {c['status']:<9}  fora: {detalhe}")

print("\n== Resumo por linha ==")
for linha in sorted(TOLERANCIAS):
    da_linha = [c for c in conferidas if c["linha"] == linha]
    ok = sum(c["status"] != "REPROVADA" for c in da_linha)
    print(f"Linha {linha}: {ok}/{len(da_linha)} amostras liberadas")

liberadas = {c["op"] for c in conferidas if c["status"] != "REPROVADA"}
reprovadas = {c["op"] for c in conferidas if c["status"] == "REPROVADA"}
pedidas = set(OPS_PEDIDAS)
com_resultado = liberadas | reprovadas

print("\n== Expedição ==")
print("Emitir certificado:", sorted(pedidas & liberadas))
print("Bloqueadas:        ", sorted(pedidas & reprovadas))
print("Sem resultado:     ", sorted(pedidas - com_resultado))
