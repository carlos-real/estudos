"""Exemplo 01 — def, return e a diferença entre mostrar e devolver.

Rode na pasta 04-funcoes:  python exemplos/01_def_e_return.py
"""


def dentro_da_faixa(valor: float, minimo: float, maximo: float) -> bool:
    """Diz se o valor está entre mínimo e máximo (inclusive)."""
    return minimo <= valor <= maximo


def mostrar_media(valores):
    """Só MOSTRA a média. Não devolve nada (devolve None)."""
    print("média:", sum(valores) / len(valores))


def calcular_media(valores):
    """DEVOLVE a média. Quem chamou decide o que fazer com ela."""
    return sum(valores) / len(valores)


print(dentro_da_faixa(50.2, 45.0, 55.0))
print(dentro_da_faixa(56.3, 45.0, 55.0))

medicoes = [50.2, 49.8, 51.0]
resultado = mostrar_media(medicoes)  # imprime, mas devolve None
print("mostrar_media devolveu:", resultado)

media = calcular_media(medicoes)  # não imprime nada; devolve o número
print("calcular_media devolveu:", round(media, 2))
print("dá para continuar calculando:", round(media * 1.1, 2))
