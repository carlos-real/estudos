"""
Solução — Exercício 03.11 — Resumo por linha (o seu primeiro GROUP BY)

Ideia central: agrupar e resumir são DOIS passos. Primeiro junte os valores de
cada grupo (dicionário de listas); depois calcule as estatísticas de cada lista.

É exatamente o que fazem:
    SQL:     SELECT linha, COUNT(espessura), AVG(espessura) ... GROUP BY linha
    pandas:  df.groupby("linha")["espessura"].agg(["count", "mean", "min", "max"])
"""


def agrupar_valores(amostras: list[dict], campo: str) -> dict[str, list[float]]:
    """Agrupa os valores válidos do campo por linha (ordem de aparição)."""
    grupos: dict[str, list[float]] = {}
    for amostra in amostras:
        valor = amostra.get(campo)  # None se a chave falta OU se vale None
        if valor is None:
            continue  # célula vazia: não entra na conta
        linha = amostra["linha"]
        # setdefault: se a linha ainda não existe, cria com [] e devolve essa
        # lista; se já existe, devolve a lista que está lá. Aí é só append.
        grupos.setdefault(linha, []).append(valor)
    return grupos

    # Forma equivalente, mais explícita:
    #     if linha not in grupos:
    #         grupos[linha] = []
    #     grupos[linha].append(valor)


def resumo_por_linha(amostras: list[dict], campo: str) -> dict[str, dict[str, float]]:
    """Devolve qtd, média, mínimo e máximo do campo para cada linha (A-Z)."""
    grupos = agrupar_valores(amostras, campo)  # reaproveita o passo 1

    resumo: dict[str, dict[str, float]] = {}
    # sorted(grupos) ordena as CHAVES; como dicionários guardam a ordem de
    # inserção, inserir em ordem alfabética deixa o resultado em ordem.
    for linha in sorted(grupos):
        valores = grupos[linha]  # nunca vazia: só criamos grupos com valor
        resumo[linha] = {
            "qtd": len(valores),
            "media": round(sum(valores) / len(valores), 2),
            "minimo": min(valores),
            "maximo": max(valores),
        }
    return resumo
