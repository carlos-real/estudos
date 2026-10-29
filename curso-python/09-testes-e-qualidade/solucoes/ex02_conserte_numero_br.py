"""
Exercício 09.02 — Conserte o bug: número no formato brasileiro
Nível: ★☆☆

Solução comentada. Veja o enunciado completo em exercicios/ex02_conserte_numero_br.py.
"""


def converter_numero_br(texto: str) -> float:
    """Converte '1.250,50' (formato brasileiro) em 1250.5."""
    # O BUG: o código original trocava a vírgula por ponto ANTES de remover os
    # pontos de milhar. Assim, o ponto decimal recém-criado também era apagado:
    #     "12,5" -> "12.5" -> "125"  (125.0 em vez de 12.5)
    #
    # A correção é inverter a ordem: primeiro tira os pontos de milhar, depois
    # transforma a vírgula decimal em ponto.
    #     "1.250,50" -> "1250,50" -> "1250.50" -> 1250.5
    limpo = texto.strip()
    limpo = limpo.replace(".", "")
    limpo = limpo.replace(",", ".")
    return float(limpo)


# Como achar esse tipo de bug: rode um caso pequeno no REPL e imprima o valor
# intermediário depois de cada passo (ou use breakpoint() e o comando "p limpo").
