"""Exemplo 02 — if, elif, else e a expressão condicional.

Rode com:  python exemplos/02_if_elif_else.py
"""

nominal = 25.0
tolerancia_pct = 10.0
minimo = nominal - nominal * tolerancia_pct / 100
maximo = nominal + nominal * tolerancia_pct / 100
print(f"Faixa: {minimo:.2f} a {maximo:.2f} µm")

# Troque o valor e rode de novo para ver os outros caminhos
valor = 21.9

if valor <= 0:
    print("Leitura inválida: confira o micrômetro.")
elif valor < minimo:
    print(f"{valor} µm: ABAIXO. Abra a matriz.")
elif valor > maximo:
    print(f"{valor} µm: ACIMA. Feche a matriz.")
else:
    print(f"{valor} µm: DENTRO.")

# Expressão condicional: escolhe um entre dois valores numa linha
status = "OK" if minimo <= valor <= maximo else "FORA"
print("Status:", status)

# if aninhado: uma decisão dentro da outra
cof = 0.32
liberado_pelo_cliente = True
if cof > 0.30:
    if liberado_pelo_cliente:
        print("COF acima do padrão, mas liberado pelo cliente.")
    else:
        print("COF acima do padrão: bloquear lote.")
