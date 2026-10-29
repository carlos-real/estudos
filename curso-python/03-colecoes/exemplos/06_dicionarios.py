"""Exemplo 06 — Dicionários: chave -> valor.

Rode na pasta 03-colecoes:  python exemplos/06_dicionarios.py
"""

# Peso (kg) de cada OP: a OP é a chave, o peso é o valor.
peso_da_op = {"OP-4512": 500.0, "OP-4513": 320.5}

print("Peso da OP-4512:", peso_da_op["OP-4512"])
print("get de OP inexistente:", peso_da_op.get("OP-9999"))
print("get com padrão:", peso_da_op.get("OP-9999", 0.0))
print("OP-4513 está no dicionário?", "OP-4513" in peso_da_op)

# Acrescentar e alterar usam a mesma sintaxe
peso_da_op["OP-4514"] = 210.0  # chave nova: acrescenta
peso_da_op["OP-4512"] = 510.0  # chave existente: substitui
print("Depois de acrescentar e alterar:", peso_da_op)

# Remover
removido = peso_da_op.pop("OP-4513")
print("pop devolveu", removido, "| ficou:", peso_da_op)

# Percorrer: items() dá (chave, valor)
for op, peso in peso_da_op.items():
    print(f"  {op}: {peso} kg")

print("Chaves:", list(peso_da_op.keys()))
print("Valores:", list(peso_da_op.values()))
print("Peso total:", sum(peso_da_op.values()), "kg")

# Padrão CONTAGEM
status = ["aprovado", "reprovado", "aprovado", "aprovado", "em análise"]
contagem = {}
for s in status:
    contagem[s] = contagem.get(s, 0) + 1
print("Contagem:", contagem)

# Padrão AGRUPAMENTO
bobinas = [("A", 50.2), ("B", 20.1), ("A", 49.8), ("B", 19.9), ("A", 51.0)]
por_linha = {}
for linha, espessura in bobinas:
    if linha not in por_linha:
        por_linha[linha] = []
    por_linha[linha].append(espessura)
print("Agrupado:", por_linha)

# Juntar dicionários: o da direita vence nas chaves repetidas
padrao_da_linha = {"espessura_nominal": 50.0, "tol_pct": 10.0, "cof_max": 0.30}
especificacao_da_op = {"tol_pct": 5.0}
regra_final = padrao_da_linha | especificacao_da_op
print("Regra final:", regra_final)
