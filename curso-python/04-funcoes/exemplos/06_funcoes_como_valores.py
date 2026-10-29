"""Exemplo 06 — Funções são valores: guardar, passar e devolver.

Rode na pasta 04-funcoes:  python exemplos/06_funcoes_como_valores.py
"""


def faixa_fixa(valor, regra):
    return regra["min"] <= valor <= regra["max"]


def nominal_percentual(valor, regra):
    margem = regra["nominal"] * regra["tol_pct"] / 100
    return regra["nominal"] - margem <= valor <= regra["nominal"] + margem


# Um dicionário de FUNÇÕES: o tipo da regra escolhe quem confere.
VERIFICADORES = {"faixa": faixa_fixa, "nominal": nominal_percentual}

regras = {
    "espessura": {"tipo": "nominal", "nominal": 50.0, "tol_pct": 10.0},
    "cof": {"tipo": "faixa", "min": 0.15, "max": 0.30},
}
amostra = {"espessura": 50.4, "cof": 0.33}

for propriedade, regra in regras.items():
    verificar = VERIFICADORES[regra["tipo"]]  # pega a função, sem chamar
    ok = verificar(amostra[propriedade], regra)  # agora chama
    print(f"{propriedade}: {'ok' if ok else 'FORA'} (conferido por {verificar.__name__})")


# Uma função que FABRICA funções (closure)
def criar_verificador(minimo, maximo):
    def verificar(valor):
        return minimo <= valor <= maximo

    return verificar


linha_a = criar_verificador(45.0, 55.0)
linha_b = criar_verificador(18.0, 22.0)
print("50 na linha A?", linha_a(50.0), "| 50 na linha B?", linha_b(50.0))

# Métodos também são funções: str.upper(texto) é o mesmo que texto.upper()
transformar = str.upper
print(transformar("op-4512"))
