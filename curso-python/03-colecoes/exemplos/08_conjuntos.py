"""Exemplo 08 — Conjuntos (set): sem repetição, sem ordem, busca rápida.

Rode na pasta 03-colecoes:  python exemplos/08_conjuntos.py
"""

lidos = ["L-101", "L-102", "L-101", "L-103", "L-102"]
unicos = set(lidos)
print("Lotes lidos:", len(lidos), "| lotes únicos:", len(unicos))
print("Únicos, em ordem:", sorted(unicos))

ops_pedidas = {"OP-4512", "OP-4513", "OP-4514", "OP-4520"}  # e-mail da expedição
ops_com_resultado = {"OP-4512", "OP-4514", "OP-4515"}  # planilha do lab

print("Prontas (nos dois):        ", sorted(ops_pedidas & ops_com_resultado))
print("Pedidas sem resultado:     ", sorted(ops_pedidas - ops_com_resultado))
print("Com resultado, não pedidas:", sorted(ops_com_resultado - ops_pedidas))
print("Todas as OPs envolvidas:   ", sorted(ops_pedidas | ops_com_resultado))
print("Só em um dos lados:        ", sorted(ops_pedidas ^ ops_com_resultado))

ops_pedidas.add("OP-4530")
ops_pedidas.discard("OP-9999")  # discard não reclama se não existir
print("OP-4530 foi pedida?", "OP-4530" in ops_pedidas)

vazio = set()
nao_e_set = {}
print(type(vazio), type(nao_e_set))
