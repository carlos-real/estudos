"""Exemplo 02 — variáveis e os cinco tipos básicos.

Rode com:  python exemplos/02_variaveis_e_tipos.py
"""

op = "OP12345"  # str: texto
quantidade_bobinas = 8  # int: número inteiro
espessura_um = 25.4  # float: número com casas decimais
liberado = True  # bool: verdadeiro ou falso
observacao = None  # None: "ainda não tem valor"

print(op, type(op))
print(quantidade_bobinas, type(quantidade_bobinas))
print(espessura_um, type(espessura_um))
print(liberado, type(liberado))
print(observacao, type(observacao))

# Reatribuição: o nome passa a apontar para outro valor
quantidade_bobinas = 10
print("Agora são", quantidade_bobinas, "bobinas")

# Constante por convenção (MAIÚSCULAS): um valor que não deve mudar
TOLERANCIA_PADRAO_PCT = 10
print("Tolerância padrão:", TOLERANCIA_PADRAO_PCT, "%")
