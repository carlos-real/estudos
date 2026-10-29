"""Counter, defaultdict e namedtuple com dados do laboratório.

Rode com:  python exemplos/06_collections_lab.py
"""

from collections import Counter, defaultdict, namedtuple

ensaios = [
    {"op": "OP245101", "linha": "A", "resultado": "aprovado"},
    {"op": "OP245102", "linha": "B", "resultado": "reprovado"},
    {"op": "OP245103", "linha": "C", "resultado": "reprovado"},
    {"op": "OP245104", "linha": "C", "resultado": "reprovado"},
    {"op": "OP245105", "linha": "B", "resultado": "aprovado"},
    {"op": "OP245106", "linha": "C", "resultado": "aprovado"},
]

# Counter: contar sem if/else
reprovacoes = Counter(e["linha"] for e in ensaios if e["resultado"] == "reprovado")
print("Reprovações por linha:", reprovacoes)
print("Pior linha:", reprovacoes.most_common(1))
print("Linha A:", reprovacoes["A"], "(chave ausente vale 0)")

# defaultdict: agrupar sem testar se a chave existe
ops_por_linha = defaultdict(list)
for e in ensaios:
    ops_por_linha[e["linha"]].append(e["op"])
print("OPs por linha:", dict(ops_por_linha))

peso_por_nf = defaultdict(float)
for nf, peso in [("123456", 1250.5), ("123457", 980.0), ("123456", 310.25)]:
    peso_por_nf[nf] += peso
print("Peso por NF:", dict(peso_por_nf))

# namedtuple: tupla com nomes nos campos
Medicao = namedtuple("Medicao", ["op", "ensaio", "valor"])
m = Medicao("OP245101", "espessura", 25.3)
print(m)
print("Valor:", m.valor, "| mesmo que m[2]:", m[2])
op, ensaio, valor = m  # desempacota como tupla
corrigida = m._replace(valor=25.1)  # tupla é imutável: _replace cria OUTRA
print("Original:", m.valor, "| corrigida:", corrigida.valor)
print("Como dict:", corrigida._asdict())
