"""Usa o pacote labqualidade (pasta exemplos/labqualidade/).

Rode com:  python exemplos/04_usando_pacote.py
Funciona porque a pasta do script (exemplos/) entra no sys.path automaticamente.
"""

import labqualidade
from labqualidade import faixa_nominal, numero_br
from labqualidade.tolerancias import dentro_da_faixa

leituras = ["25,1", "24,8", "27,9", "25,3"]
valores = [numero_br(texto) for texto in leituras]
minimo, maximo = faixa_nominal(25.0, 10)

print(f"labqualidade versão {labqualidade.__version__}")
print(f"Faixa: {minimo} a {maximo} µm")
for valor in valores:
    situacao = "ok" if dentro_da_faixa(valor, minimo, maximo) else "FORA"
    print(f"  {valor:5.1f} µm -> {situacao}")
print("Resumo:", labqualidade.resumo(valores))
print("Na vitrine (__all__):", labqualidade.__all__)
