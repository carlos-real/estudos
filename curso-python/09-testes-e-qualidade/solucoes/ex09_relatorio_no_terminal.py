"""
Exercício 09.09 — Relatório no terminal (testado com capsys)
Nível: ★★☆

Solução comentada. Veja o enunciado completo em exercicios/ex09_relatorio_no_terminal.py.
"""


def formatar_br(valor: float) -> str:
    """1250.5 -> '1.250,50' (2 casas, vírgula decimal, ponto de milhar)."""
    # Formata no padrão americano e troca os separadores usando um caractere
    # temporário ("_"), senão o segundo replace desfaria o primeiro.
    return f"{valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def imprimir_relatorio(resultados: list[tuple[str, float, bool]]) -> None:
    """Imprime o relatório da conferência no terminal."""
    # Caso especial primeiro, com retorno antecipado.
    if not resultados:
        print("Nenhuma amostra.")
        return

    print("OP | VALOR | SITUAÇÃO")
    for op, valor, dentro in resultados:
        situacao = "OK" if dentro else "FORA"
        print(f"{op} | {formatar_br(valor)} | {situacao}")

    # sum() de booleanos conta os True; aqui contamos os que NÃO estão dentro.
    fora = sum(1 for _, _, dentro in resultados if not dentro)
    print(f"Total: {len(resultados)} amostra(s), {fora} fora")


# Separar formatar_br() da impressão é "código limpo": a regra de formatação
# ganha um nome, pode ser testada sozinha e reaproveitada no certificado.
