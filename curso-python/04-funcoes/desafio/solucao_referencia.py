"""Desafio do módulo 04 — Fila de emissão de certificados (solução de referência).

Rode na pasta 04-funcoes:  python desafio/solucao_referencia.py

Arquitetura: NÚCLEO PURO (funções que recebem dados e devolvem resultados, sem
print) e CASCA FINA (main, a única que imprime). No fim do arquivo, asserts
testam as peças do núcleo, uma por uma.
"""

# ---------------------------------------------------------------------------
# Dados do dia (no projeto final: banco de regras, planilha e e-mail)
# ---------------------------------------------------------------------------

PADROES_DA_LINHA = {
    "A": {
        "espessura": {"nominal": 50.0, "tol_pct": 10.0},
        "gramatura": {"nominal": 46.0, "tol_pct": 5.0},
        "cof": {"min": 0.15, "max": 0.30},
    },
    "B": {
        "espessura": {"nominal": 20.0, "tol_pct": 8.0},
        "gramatura": {"nominal": 18.5, "tol_pct": 5.0},
        "cof": {"min": 0.20, "max": 0.40},
    },
}

ESPECIFICACOES = {
    "OP-6101": {
        "titulo": "Filme PE 50 µm alta selagem",
        "regras": {"espessura": {"nominal": 50.0, "tol_pct": 5.0}},
    },
    "OP-6104": {
        "titulo": "Filme BOPP 20 µm baixo atrito",
        "regras": {"cof": {"min": 0.10, "max": 0.25}},
    },
}

PEDIDOS = [
    {"op": "OP-6101", "nf": "000501", "peso_kg": 1250.5},
    {"op": " op-6102", "nf": "000502", "peso_kg": 830.0},
    {"op": "OP-6103", "nf": "000503", "peso_kg": 640.2},
    {"op": "OP-6104", "nf": "000504", "peso_kg": 910.0},
    {"op": "OP-61", "nf": "5O5", "peso_kg": 0},
    {"op": "OP-6106", "nf": "000506", "peso_kg": 300.0},
    {"op": "OP-6107", "nf": "000507", "peso_kg": 455.5},
]

RESULTADOS = {
    "OP-6101": {
        "linha": "A",
        "obs": "",
        "medidas": {"espessura": 51.2, "gramatura": 46.3, "cof": 0.22},
    },
    "OP-6102": {
        "linha": "A",
        "obs": "COF: liberado",
        "medidas": {"espessura": 49.1, "gramatura": 45.8, "cof": 0.33},
    },
    "OP-6103": {
        "linha": "B",
        "obs": "",
        "medidas": {"espessura": 22.4, "gramatura": 18.9, "cof": 0.31},
    },
    "OP-6104": {
        "linha": "B",
        "obs": "",
        "medidas": {"espessura": 20.3, "gramatura": 18.2, "cof": 0.18},
    },
    "OP-6107": {"linha": "A", "obs": "", "medidas": {"espessura": 50.6, "cof": 0.19}},
}

UNIDADES = {"espessura": "µm", "gramatura": "g/m²", "cof": ""}
CASAS = {"espessura": 1, "gramatura": 1, "cof": 2}


# ---------------------------------------------------------------------------
# Núcleo puro: validação do pedido
# ---------------------------------------------------------------------------


def limpar_op(op):
    return (op or "").strip().upper()


def problemas_do_pedido(pedido):
    """Lista os problemas de digitação do pedido (vazia = pedido ok)."""
    problemas = []
    op = limpar_op(pedido.get("op"))
    if not (op.startswith("OP-") and op[3:].isdigit() and 4 <= len(op[3:]) <= 6):
        problemas.append(f"OP inválida '{op}'")
    nf = (pedido.get("nf") or "").strip()
    if not nf.isdigit():
        problemas.append(f"NF inválida '{nf}'")
    peso = pedido.get("peso_kg")
    if peso is None or peso <= 0:
        problemas.append("peso deve ser maior que zero")
    return problemas


# ---------------------------------------------------------------------------
# Núcleo puro: regras e conferência
# ---------------------------------------------------------------------------


def regras_da_op(op, linha, especificacoes, padroes):
    """(título, regras): a especificação da OP vale sobre o padrão da linha."""
    padrao = padroes[linha]
    especificacao = especificacoes.get(op)
    if especificacao is None:
        return f"Padrão da linha {linha}", padrao
    return especificacao["titulo"], padrao | especificacao["regras"]


def faixa(regra):
    """Converte {nominal, tol_pct} ou {min, max} em (mínimo, máximo)."""
    if "nominal" in regra:
        nominal, fator = regra["nominal"], regra["tol_pct"] / 100
        return round(nominal * (1 - fator), 2), round(nominal * (1 + fator), 2)
    return regra["min"], regra["max"]


def falhas_das_medidas(medidas, regras):
    """Propriedades fora da faixa ou sem medição, na ordem das regras."""
    falhas = []
    for propriedade, regra in regras.items():
        valor = medidas.get(propriedade)
        minimo, maximo = faixa(regra)
        if valor is None:
            falhas.append(f"{propriedade} (sem medição)")
        elif not minimo <= valor <= maximo:
            falhas.append(propriedade)
    return falhas


def parecer(falhas, observacao):
    """APROVADO, APROVADO COM RESSALVA (só COF fora e liberado) ou REPROVADO."""
    if not falhas:
        return "APROVADO"
    if falhas == ["cof"] and "cof: liberado" in observacao.lower():
        return "APROVADO COM RESSALVA (COF: liberado)"
    return "REPROVADO"


# ---------------------------------------------------------------------------
# Núcleo puro: textos
# ---------------------------------------------------------------------------


def numero(valor, propriedade):
    return f"{valor:.{CASAS[propriedade]}f}"


def linha_da_tabela(propriedade, valor, regra):
    minimo, maximo = faixa(regra)
    resultado = f"{numero(valor, propriedade)} {UNIDADES[propriedade]}".strip()
    especificado = f"{numero(minimo, propriedade)} a {numero(maximo, propriedade)}"
    return f"  {propriedade:<11}{resultado:<12}{especificado}"


def montar_certificado(pedido, titulo, regras, resultado, situacao):
    """Texto do certificado (só é chamado para pedidos aprovados)."""
    medidas = resultado["medidas"]
    linhas = [
        f"CERTIFICADO DE QUALIDADE - {pedido['op']}",
        f"  NF {pedido['nf']}  |  {pedido['peso_kg']:.1f} kg  |  {titulo}",
    ]
    linhas += [linha_da_tabela(p, medidas[p], regra) for p, regra in regras.items()]
    linhas.append(f"  Parecer: {situacao}")
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Núcleo puro: a receita
# ---------------------------------------------------------------------------


def processar_pedido(pedido, resultados, especificacoes, padroes):
    """Decide o destino de UM pedido: emitir, bloqueado, aguardando ou inválido."""
    problemas = problemas_do_pedido(pedido)
    if problemas:
        return {
            "op": limpar_op(pedido.get("op")),
            "destino": "inválido",
            "motivo": "; ".join(problemas),
        }

    pedido = {**pedido, "op": limpar_op(pedido["op"]), "nf": pedido["nf"].strip()}
    resultado = resultados.get(pedido["op"])
    if resultado is None:
        return {
            "op": pedido["op"],
            "destino": "aguardando",
            "motivo": "sem resultado do laboratório",
        }

    titulo, regras = regras_da_op(pedido["op"], resultado["linha"], especificacoes, padroes)
    falhas = falhas_das_medidas(resultado["medidas"], regras)
    situacao = parecer(falhas, resultado["obs"])
    if situacao == "REPROVADO":
        return {
            "op": pedido["op"],
            "destino": "bloqueado",
            "motivo": "fora da especificação: " + ", ".join(falhas),
        }

    certificado = montar_certificado(pedido, titulo, regras, resultado, situacao)
    return {
        "op": pedido["op"],
        "destino": "emitir",
        "peso_kg": pedido["peso_kg"],
        "certificado": certificado,
    }


def montar_fila(pedidos, resultados, especificacoes, padroes):
    return [processar_pedido(p, resultados, especificacoes, padroes) for p in pedidos]


def resumo_da_fila(fila):
    """Uma linha com a contagem por destino e o peso a emitir."""
    contagem = {"emitir": 0, "bloqueado": 0, "aguardando": 0, "inválido": 0}
    for item in fila:
        contagem[item["destino"]] += 1
    peso = sum(item["peso_kg"] for item in fila if item["destino"] == "emitir")
    partes = [f"{quantidade} {destino}" for destino, quantidade in contagem.items()]
    return f"Fila: {', '.join(partes)} | peso a emitir: {peso:.1f} kg"


# ---------------------------------------------------------------------------
# Casca: a única parte que imprime
# ---------------------------------------------------------------------------


def main():
    fila = montar_fila(PEDIDOS, RESULTADOS, ESPECIFICACOES, PADROES_DA_LINHA)

    print("=== CERTIFICADOS A EMITIR ===\n")
    for item in fila:
        if item["destino"] == "emitir":
            print(item["certificado"])
            print()

    print("=== PENDÊNCIAS ===")
    for item in fila:
        if item["destino"] != "emitir":
            print(f"  {item['op'] or '(sem OP)':<9} {item['destino']:<11} {item['motivo']}")

    print("\n" + resumo_da_fila(fila))


# ---------------------------------------------------------------------------
# Testes rápidos do núcleo (no módulo 09 viram testes pytest)
# ---------------------------------------------------------------------------

assert faixa({"nominal": 46.0, "tol_pct": 5.0}) == (43.7, 48.3)
assert faixa({"min": 0.15, "max": 0.30}) == (0.15, 0.30)
assert parecer([], "") == "APROVADO"
assert parecer(["cof"], "COF: Liberado") == "APROVADO COM RESSALVA (COF: liberado)"
assert parecer(["cof", "espessura"], "COF: liberado") == "REPROVADO"
assert problemas_do_pedido({"op": "OP-6101", "nf": "1", "peso_kg": 1.0}) == []
assert regras_da_op("OP-9999", "A", ESPECIFICACOES, PADROES_DA_LINHA)[0] == "Padrão da linha A"
assert falhas_das_medidas({"espessura": 50.0, "cof": 0.2}, PADROES_DA_LINHA["A"]) == [
    "gramatura (sem medição)"
]

main()
