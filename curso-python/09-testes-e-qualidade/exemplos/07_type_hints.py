"""Type hints: documentação que uma ferramenta (mypy) consegue conferir.

O Python NÃO confere os tipos ao rodar. Este script mostra isso.
Rode:  python exemplos/07_type_hints.py
Para conferir os tipos (precisa instalar):  python -m pip install mypy
                                           mypy exemplos/07_type_hints.py
"""


def somar_pesos(pesos: list[float]) -> float:
    """Soma os pesos (kg) das bobinas de uma NF."""
    total = 0.0
    for peso in pesos:
        total += peso
    return total


def descrever_nf(numero: str, pesos: list[float]) -> str:
    return f"NF {numero}: {len(pesos)} bobina(s), {somar_pesos(pesos):.1f} kg"


# As anotações ficam guardadas na função, mas ninguém as confere ao rodar
print("Anotações:", somar_pesos.__annotations__)

# Uso correto
print(descrever_nf("4512", [250.5, 120.0, 98.7]))


# Uso errado que o Python aceita sem reclamar: somar textos concatena!
def juntar(a: int, b: int) -> int:
    return a + b


print("juntar('10', '20') =", juntar("10", "20"), "<- o Python não reclamou")
