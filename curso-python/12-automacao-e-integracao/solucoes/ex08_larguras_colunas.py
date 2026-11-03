"""
Exercício 12.08 — Calcular a largura das colunas de um relatório (SOLUÇÃO)

Esta função é "pura": recebe listas, devolve números, não abre arquivo nenhum.
Por isso é fácil de testar. O openpyxl entra só na hora de APLICAR o resultado:
    for indice, largura in enumerate(larguras, start=1):
        ws.column_dimensions[get_column_letter(indice)].width = largura
"""


def calcular_larguras(linhas: list[list], minimo: int = 8, maximo: int = 50) -> list[int]:
    """Largura ideal de cada coluna (maior texto + 2, entre mínimo e máximo)."""
    if not linhas:
        return []

    # Quantas colunas? As da linha mais comprida.
    quantidade = max(len(linha) for linha in linhas)
    maiores = [0] * quantidade  # maior texto visto em cada coluna

    for linha in linhas:
        for indice, valor in enumerate(linha):
            texto = "" if valor is None else str(valor)
            maiores[indice] = max(maiores[indice], len(texto))
    # Células que "faltam" numa linha curta simplesmente não atualizam o
    # máximo, que é o mesmo que contar como vazias.

    # min(max(x, minimo), maximo) "prende" x dentro da faixa [minimo, maximo].
    return [min(max(tamanho + 2, minimo), maximo) for tamanho in maiores]
