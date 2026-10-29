"""O molde dos exercícios: def + return.

Rode na pasta curso-python:
    python 00-preparacao/exemplos/03_molde_da_funcao.py
"""


def dobro(numero: float) -> float:
    """Devolve o dobro de um número."""
    return numero * 2


def mensagem_liberacao(ensaio: str) -> str:
    """Devolve a observação de liberação de um ensaio, ex.: 'COF: liberado'."""
    return ensaio + ": liberado"


def ola_com_print() -> None:
    """Só MOSTRA um texto na tela. Não devolve nada (devolve None)."""
    print("Olá (mostrado com print)")


# Chamando as funções e mostrando o que elas DEVOLVEM:
print(dobro(21))
print(dobro(2.5))
print(mensagem_liberacao("COF"))
print(mensagem_liberacao("Selagem"))

# A diferença entre print e return:
resultado = ola_com_print()
print(resultado)
