"""Exemplo 03 — match-case (Python 3.10+).

Rode com:  python exemplos/03_match_case.py
"""

ensaio = " Gramatura "

match ensaio.strip().lower():
    case "espessura":
        unidade = "µm"
    case "gramatura":
        unidade = "g/m²"
    case "tração" | "tracao":
        unidade = "MPa"
    case "cof":
        unidade = "(adimensional)"
    case _:
        unidade = None

print("Unidade do ensaio:", unidade)

comando = "relatorio"
match comando:
    case "medir":
        print("Iniciando medição...")
    case "relatorio" | "relatório":
        print("Gerando relatório...")
    case "sair":
        print("Até logo!")
    case _:
        print(f"Comando desconhecido: {comando}")
