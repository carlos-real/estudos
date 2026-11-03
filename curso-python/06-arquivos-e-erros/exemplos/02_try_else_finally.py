"""Exemplo 02 — try, except, else e finally (seções 2 e 3).

Rode na pasta curso-python:
    python 06-arquivos-e-erros/exemplos/02_try_else_finally.py
"""


def rendimento(area_texto, peso_texto):
    """m² por kg a partir de dois textos da planilha (ou None)."""
    try:
        area = float(area_texto.replace(",", "."))
        peso = float(peso_texto.replace(",", "."))
        return area / peso
    except ValueError:
        print(f"  Número inválido: área={area_texto!r}, peso={peso_texto!r}")
    except ZeroDivisionError:
        print("  Peso zero: não dá para calcular o rendimento")
    return None


for area, peso in [("1250", "25,5"), ("1250", ""), ("1250", "0")]:
    print(f"rendimento({area!r}, {peso!r}) = {rendimento(area, peso)}")

print()
for texto in ["10", "0", "x"]:
    try:
        resultado = 100 / int(texto)
    except ZeroDivisionError:
        print(texto, "-> divisão por zero")
    except ValueError:
        print(texto, "-> não é número")
    else:
        print(texto, "->", resultado)
    finally:
        print("fim de", texto)
