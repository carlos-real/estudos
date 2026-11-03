"""
Exercício 12.04 — Tentar de novo com espera crescente (SOLUÇÃO)

Dois truques importantes aqui:
1. `funcao` é uma função passada como valor (módulo 04). Quem chama decide O QUE
   fazer; com_retentativas decide QUANTAS VEZES tentar. Separação de papéis.
2. `dormir` também é injetado. No programa real ele é time.sleep; no teste é
   uma lista.append, e o teste roda em milissegundos.
"""

import time
from collections.abc import Callable
from typing import Any

import requests

# Só falhas de REDE valem nova tentativa. Um HTTPError 404 não vai virar 200
# se tentarmos de novo. (Para repetir 503, combine com o exercício 01.)
ERROS_PASSAGEIROS = (requests.ConnectionError, requests.Timeout)


def com_retentativas(
    funcao: Callable[[], Any],
    tentativas: int = 3,
    espera: float = 1.0,
    dormir: Callable[[float], None] = time.sleep,
) -> Any:
    """Chama funcao() repetindo em falhas de rede, com espera que dobra."""
    if tentativas < 1:
        raise ValueError("tentativas deve ser pelo menos 1")

    for numero in range(tentativas):
        try:
            return funcao()  # deu certo: sai da função na hora
        except ERROS_PASSAGEIROS:
            ultima = numero == tentativas - 1
            if ultima:
                raise  # `raise` sozinho relança a MESMA exceção, com o traceback original
            # Backoff exponencial: 1, 2, 4, 8... (2 ** 0 = 1)
            dormir(espera * 2**numero)
        # Qualquer outra exceção nem é capturada: sobe direto para quem chamou.

    # Nunca chegamos aqui (o laço sempre retorna ou relança), mas deixar
    # explícito ajuda quem lê e agrada ferramentas como o mypy.
    raise AssertionError("inalcançável")
