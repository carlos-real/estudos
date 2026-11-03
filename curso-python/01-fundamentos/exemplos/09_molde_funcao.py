"""Exemplo 09 — o molde dos exercícios: def e return.

Rode com:  python exemplos/09_molde_funcao.py
"""


def area_retangulo(largura: float, comprimento: float) -> float:
    """Devolve a área de um retângulo."""
    return largura * comprimento


def dobro(numero: float) -> float:
    """Devolve o dobro do número."""
    return numero * 2


def mostrar_dobro(numero: float) -> None:
    """Só IMPRIME o dobro; não devolve nada."""
    print(numero * 2)


area = area_retangulo(0.1, 0.1)  # chamar a função = usar a máquina
print("Área do corpo de prova:", round(area, 4), "m²")
print("Posso usar o resultado em outra conta:", dobro(21) + 1)

resultado = mostrar_dobro(21)  # imprime 42 na tela...
print("...mas o valor devolvido é:", resultado)  # ...e devolve None
