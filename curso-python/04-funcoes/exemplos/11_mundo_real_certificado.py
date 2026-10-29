"""Exemplo 11 — No mundo real: o texto do certificado, montado por funções puras.

Regra do projeto: se a OP tem especificação própria, ela vale; o que a
especificação não define vem do padrão da linha. COF fora da faixa pode ser
liberado pela qualidade com a observação "COF: liberado".

Rode na pasta 04-funcoes:  python exemplos/11_mundo_real_certificado.py
"""

PADROES_DA_LINHA = {
    "A": {
        "espessura": {"nominal": 50.0, "tol_pct": 10.0},
        "gramatura": {"nominal": 46.0, "tol_pct": 5.0},
        "cof": {"min": 0.15, "max": 0.30},
    },
}
ESPECIFICACOES = {  # OP -> especificação própria (título + regras que mudam)
    "OP-4512": {
        "titulo": "Filme PE 50 µm alta selagem",
        "regras": {"espessura": {"nominal": 50.0, "tol_pct": 5.0}},
    },
}
UNIDADES = {"espessura": "µm", "gramatura": "g/m²", "cof": ""}
CASAS = {"espessura": 1, "gramatura": 1, "cof": 2}


# ------------------------- núcleo puro -------------------------
def regras_da_op(op, linha):
    """Devolve (título, regras): especificação da OP sobre o padrão da linha."""
    padrao = PADROES_DA_LINHA[linha]
    especificacao = ESPECIFICACOES.get(op)
    if especificacao is None:
        return f"Padrão da linha {linha}", padrao
    return especificacao["titulo"], padrao | especificacao["regras"]


def faixa(regra):
    """Converte {nominal, tol_pct} ou {min, max} em (mínimo, máximo)."""
    if "nominal" in regra:
        fator = regra["tol_pct"] / 100
        return round(regra["nominal"] * (1 - fator), 2), round(
            regra["nominal"] * (1 + fator), 2
        )
    return regra["min"], regra["max"]


def conforme(valor, regra):
    minimo, maximo = faixa(regra)
    return minimo <= valor <= maximo


def numero(valor, propriedade):
    """Formata com as casas decimais da propriedade (0.3 vira 0.30 no COF)."""
    return f"{valor:.{CASAS[propriedade]}f}"


def linha_da_tabela(propriedade, valor, regra):
    minimo, maximo = faixa(regra)
    resultado = f"{numero(valor, propriedade)} {UNIDADES[propriedade]}".strip()
    especificado = f"{numero(minimo, propriedade)} a {numero(maximo, propriedade)}"
    situacao = "conforme" if conforme(valor, regra) else "NÃO conforme"
    return f"{propriedade:<11}{resultado:<12}{especificado:<15}{situacao}"


def parecer(falhas, observacao):
    """APROVADO, APROVADO COM RESSALVA (só COF fora e liberado) ou REPROVADO."""
    if not falhas:
        return "APROVADO"
    if falhas == ["cof"] and "cof: liberado" in observacao.lower():
        return "APROVADO COM RESSALVA (COF: liberado)"
    return "REPROVADO"


def montar_certificado(pedido, resultado):
    """Texto completo do certificado. Não imprime nada: devolve uma string."""
    titulo, regras = regras_da_op(pedido["op"], resultado["linha"])
    medidas = resultado["medidas"]
    falhas = [p for p, regra in regras.items() if not conforme(medidas[p], regra)]
    cabecalho = [
        "CERTIFICADO DE QUALIDADE",
        f"OP: {pedido['op']}   NF: {pedido['nf']}   Peso: {pedido['peso_kg']} kg",
        f"Especificação: {titulo}",
        "-" * 50,
    ]
    tabela = [linha_da_tabela(p, medidas[p], regra) for p, regra in regras.items()]
    rodape = ["-" * 50, f"Parecer: {parecer(falhas, resultado['obs'])}"]
    return "\n".join(cabecalho + tabela + rodape)  # "\n" = quebra de linha


# ------------------------- casca (efeitos) -------------------------
def main():
    pedidos = [
        {"op": "OP-4512", "nf": "000123456", "peso_kg": 1250.5},
        {"op": "OP-4514", "nf": "000123457", "peso_kg": 830.0},
    ]
    resultados = {
        "OP-4512": {
            "linha": "A",
            "obs": "",
            "medidas": {"espessura": 51.2, "gramatura": 46.3, "cof": 0.22},
        },
        "OP-4514": {
            "linha": "A",
            "obs": "COF: liberado",
            "medidas": {"espessura": 49.1, "gramatura": 45.8, "cof": 0.33},
        },
    }
    for pedido in pedidos:
        print(montar_certificado(pedido, resultados[pedido["op"]]))
        print()


main()
