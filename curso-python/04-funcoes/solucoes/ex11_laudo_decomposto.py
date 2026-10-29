"""
Solução — Exercício 04.11 — Laudo decomposto em funções pequenas

Ideia central: cada função responde UMA pergunta e pode ser testada sozinha.
A função de cima (resumo_lote) vira uma "receita" legível que só chama as de
baixo. Se a regra de classificação mudar, você mexe em UM lugar.

    resumo_lote
    ├── calcular_limites
    ├── classificar_todas
    │   └── classificar
    └── contar_por_classe
"""


def calcular_limites(nominal: float, tol_pct: float) -> tuple[float, float]:
    """Devolve (mínimo, máximo) para nominal ± tol_pct %, com 2 casas."""
    fator = tol_pct / 100
    return round(nominal * (1 - fator), 2), round(nominal * (1 + fator), 2)


def classificar(valor: float, limites: tuple[float, float]) -> str:
    """Classifica um valor como "abaixo", "ok" ou "acima" dos limites."""
    minimo, maximo = limites
    if valor < minimo:
        return "abaixo"
    if valor > maximo:
        return "acima"
    return "ok"


def classificar_todas(medicoes: list[float], limites: tuple[float, float]) -> list[str]:
    """Classifica cada medição, na mesma ordem."""
    return [classificar(valor, limites) for valor in medicoes]


def contar_por_classe(classes: list[str]) -> dict[str, int]:
    """Conta "abaixo", "ok" e "acima" (as três chaves sempre presentes)."""
    # Começar com as três chaves zeradas garante a ordem e evita KeyError
    # em quem usar o resultado (contagem["acima"] sempre existe).
    contagem = {"abaixo": 0, "ok": 0, "acima": 0}
    for classe in classes:
        contagem[classe] += 1
    return contagem


def resumo_lote(op: str, medicoes: list[float], nominal: float, tol_pct: float) -> str:
    """Monta a linha de resumo do lote usando as outras funções."""
    if not medicoes:  # retorno antecipado: evita divisão por zero lá embaixo
        return f"{op} | sem medições"

    limites = calcular_limites(nominal, tol_pct)
    contagem = contar_por_classe(classificar_todas(medicoes, limites))

    total = len(medicoes)
    pct = 100 * contagem["ok"] / total
    situacao = "APROVADO" if contagem["ok"] == total else "REPROVADO"
    return (
        f"{op} | {contagem['ok']}/{total} conformes ({pct:.1f}%) | "
        f"{contagem['abaixo']} abaixo, {contagem['acima']} acima | {situacao}"
    )
