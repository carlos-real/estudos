"""Exemplo 03 — A armadilha do valor padrão mutável (e a correção).

Rode na pasta 04-funcoes:  python exemplos/03_padrao_mutavel.py
"""


# ERRADO de propósito: a lista padrão é criada UMA vez, quando o def roda.
# O ruff avisa (regra B006); o "noqa" abaixo silencia o aviso só neste exemplo.
def registrar_errado(defeito, defeitos=[]):  # noqa: B006
    defeitos.append(defeito)
    return defeitos


print("--- versão com defeito ---")
print(registrar_errado("bolha"))
print(registrar_errado("risco"))  # esperava ['risco']...
print("padrão guardado na função:", registrar_errado.__defaults__)


# CERTO: None como padrão, lista criada dentro, a cada chamada.
def registrar(defeito, defeitos=None):
    if defeitos is None:
        defeitos = []
    defeitos.append(defeito)
    return defeitos


print("--- versão corrigida ---")
print(registrar("bolha"))
print(registrar("risco"))
anotados = ["gel"]
print(registrar("bolha", anotados), "| anotados:", anotados)
