"""
Solução — Exercício 03.12 — Revisão: relatório de tolerâncias

Ideia central: navegar num dicionário aninhado com .get e .items(), e montar o
resultado em funções pequenas, cada uma reaproveitando a anterior.
"""

TOLERANCIAS = {
    "A": {
        "espessura": {"nominal": 50.0, "tol_pct": 10.0},
        "gramatura": {"nominal": 46.0, "tol_pct": 5.0},
    },
    "B": {"espessura": {"nominal": 20.0, "tol_pct": 8.0}},
}


def limites(nominal: float, tol_pct: float) -> tuple[float, float]:
    """Devolve (mínimo, máximo) para nominal ± tol_pct %, em 2 casas."""
    fator = tol_pct / 100
    # Sem round, 46 * 0.95 daria 43.699999999999996 (problema do float, módulo
    # 01), e um valor medido de 43.7 seria reprovado injustamente.
    return round(nominal * (1 - fator), 2), round(nominal * (1 + fator), 2)


def falhas_da_amostra(amostra: dict, tolerancias: dict) -> list[str] | None:
    """Lista as propriedades fora da tolerância (None se a linha não existe)."""
    linha = amostra["linha"].strip().upper()
    regras = tolerancias.get(linha)  # dicionário de propriedades ou None
    if regras is None:
        return None

    falhas = []
    # regras.items() dá pares ("espessura", {"nominal": 50.0, "tol_pct": 10.0})
    for propriedade, regra in regras.items():
        valor = amostra.get(propriedade)
        if valor is None:
            continue  # sem medição dessa propriedade: nada a conferir
        minimo, maximo = limites(regra["nominal"], regra["tol_pct"])
        if not minimo <= valor <= maximo:
            falhas.append(f"{propriedade} {valor:.1f} fora de {minimo:.1f} a {maximo:.1f}")
    return falhas


def linha_do_relatorio(amostra: dict, tolerancias: dict) -> str:
    """Monta o texto de uma amostra: APROVADA, REPROVADA: ... ou PENDENTE: ..."""
    falhas = falhas_da_amostra(amostra, tolerancias)
    inicio = f"{amostra['op']} | linha {amostra['linha'].strip().upper()} | "

    # Atenção à ordem dos testes: None e [] são ambos falsy, mas significam
    # coisas diferentes aqui. Por isso testamos "is None" primeiro.
    if falhas is None:
        return inicio + "PENDENTE: sem tolerância cadastrada"
    if not falhas:
        return inicio + "APROVADA"
    return inicio + "REPROVADA: " + "; ".join(falhas)


def relatorio(amostras: list[dict], tolerancias: dict) -> list[str]:
    """Uma linha por amostra e uma linha final de total."""
    linhas = []
    aprovadas = 0  # acumulador (módulo 02)
    for amostra in amostras:
        texto = linha_do_relatorio(amostra, tolerancias)
        linhas.append(texto)
        if texto.endswith("APROVADA"):
            aprovadas += 1
    # Contar pelo texto é prático aqui. Uma alternativa mais robusta seria
    # chamar falhas_da_amostra(...) == [] para cada amostra.

    total = len(amostras)
    percentual = 100 * aprovadas / total if total else 0.0
    linhas.append(f"Total: {total} amostras, {aprovadas} aprovadas ({percentual:.1f}%)")
    return linhas
