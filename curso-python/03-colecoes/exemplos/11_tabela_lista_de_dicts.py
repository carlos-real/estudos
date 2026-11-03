"""Exemplo 11 — Lista de dicionários como tabela (a ponte para pandas e SQL).

Rode na pasta 03-colecoes:  python exemplos/11_tabela_lista_de_dicts.py
"""

# Cada dicionário é uma LINHA da tabela; cada chave é uma COLUNA.
amostras = [
    {"op": "OP-4512", "linha": "A", "espessura": 50.4, "cof": 0.22},
    {"op": "OP-4513", "linha": "B", "espessura": 20.9, "cof": 0.31},
    {"op": "OP-4514", "linha": "A", "espessura": 56.1, "cof": 0.25},
    {"op": "OP-4515", "linha": "C", "espessura": 35.2, "cof": 0.18},
    {"op": "OP-4516", "linha": "A", "espessura": 49.7, "cof": 0.27},
]


def imprimir_tabela(tabela):
    """Mostra a tabela alinhada: < alinha à esquerda, > à direita."""
    print(f"{'OP':<9}{'Linha':<7}{'Esp.(µm)':>9}{'COF':>6}")
    for registro in tabela:
        print(
            f"{registro['op']:<9}{registro['linha']:<7}"
            f"{registro['espessura']:>9.1f}{registro['cof']:>6.2f}"
        )


print("== Tabela completa ==")
imprimir_tabela(amostras)

# WHERE: filtrar linhas
linha_a = [a for a in amostras if a["linha"] == "A"]
print("\n== Só a linha A ==")
imprimir_tabela(linha_a)

# SELECT coluna: pegar uma coluna
espessuras = [a["espessura"] for a in amostras]
print("\nColuna espessura:", espessuras)

# ORDER BY: ordenar pela espessura, da maior para a menor
ordenadas = sorted(amostras, key=lambda a: a["espessura"], reverse=True)
print("\n== Ordenada por espessura (desc) ==")
imprimir_tabela(ordenadas)

# GROUP BY + AVG: média de espessura por linha
grupos = {}
for a in amostras:
    grupos.setdefault(a["linha"], []).append(a["espessura"])
medias = {linha: round(sum(v) / len(v), 2) for linha, v in sorted(grupos.items())}
print("\nMédia por linha:", medias)

# Nova coluna: status (sem alterar a tabela original)
com_status = [{**a, "status": "ok" if a["cof"] <= 0.30 else "COF alto"} for a in amostras]
print("\nStatus:", [(a["op"], a["status"]) for a in com_status])
print("A original continua sem 'status'?", "status" not in amostras[0])

# JOIN: juntar com outra tabela pela OP
pedidos = [
    {"op": "OP-4514", "nf": "000123", "peso_kg": 500.0},
    {"op": "OP-4599", "nf": "000124", "peso_kg": 80.5},
]
indice = {a["op"]: a for a in amostras}  # monta o "PROCV" uma vez
print("\n== Pedidos com o resultado do laboratório ==")
for pedido in pedidos:
    amostra = indice.get(pedido["op"])
    if amostra is None:
        print(f"{pedido['op']}: sem resultado no laboratório")
    else:
        texto = f"{pedido['op']}: NF {pedido['nf']}, linha {amostra['linha']}"
        print(f"{texto}, COF {amostra['cof']}")
