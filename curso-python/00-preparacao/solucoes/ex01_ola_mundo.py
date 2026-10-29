"""
Solução — Exercício 00.01 — Olá, mundo!

Ideia central: uma função DEVOLVE um valor com `return`. Quem chamou a função (no
caso, o teste) recebe esse valor e pode conferir se está certo.
"""


def ola_mundo() -> str:
    """Devolve o texto 'Olá, mundo!'."""
    # O texto vai entre aspas: é assim que o Python sabe que é texto (str), e não
    # o nome de uma variável. Aspas simples ou duplas funcionam igual.
    return "Olá, mundo!"

    # Armadilha comum:
    #     print("Olá, mundo!")
    # Isso MOSTRA o texto na tela, mas a função devolve None (nada).
    # O teste recebe None e falha com "devolveu None".
