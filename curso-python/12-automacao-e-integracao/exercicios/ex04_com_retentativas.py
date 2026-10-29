"""
Exercício 12.04 — Tentar de novo com espera crescente (backoff)
Nível: ★★★

Contexto: a rede da fábrica oscila. Uma consulta que falha às 7h02 costuma
funcionar às 7h03. Um robô profissional não desiste na primeira falha, mas
também não martela o servidor: espera um pouco, e cada vez um pouco mais.

Tarefa: implemente com_retentativas(funcao, tentativas=3, espera=1.0, dormir=time.sleep).
- Chame funcao() (sem argumentos) e devolva o que ela devolver.
- Se ela levantar requests.ConnectionError ou requests.Timeout, espere e tente
  de novo, até completar `tentativas` chamadas no total.
- As esperas dobram: espera, espera*2, espera*4, ... Use dormir(segundos) para
  esperar (os testes trocam dormir por uma função que só anota os valores,
  para não esperar de verdade).
- Não espere depois da ÚLTIMA tentativa: se todas falharem, levante de novo a
  última exceção (use `raise` sozinho ou `raise erro`).
- Qualquer outra exceção (por exemplo requests.HTTPError ou ValueError) sobe
  na hora, sem nova tentativa: repetir não resolve.
- tentativas menor que 1 -> ValueError.

Exemplos:
    Uma função que falha 2 vezes com ConnectionError e depois devolve "ok":
    >>> esperas = []
    >>> com_retentativas(funcao, tentativas=3, espera=1.0, dormir=esperas.append)
    'ok'
    >>> esperas
    [1.0, 2.0]

Dica: um for tentativa in range(tentativas) com try/except dentro. Pergunte
"esta é a última tentativa?" antes de dormir.

Teste com:  python curso.py testar 12 ex04
"""

import time
from collections.abc import Callable
from typing import Any

import requests  # noqa: F401  (você vai usar requests.ConnectionError e requests.Timeout)


def com_retentativas(
    funcao: Callable[[], Any],
    tentativas: int = 3,
    espera: float = 1.0,
    dormir: Callable[[float], None] = time.sleep,
) -> Any:
    """Chama funcao() repetindo em falhas de rede, com espera que dobra."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
