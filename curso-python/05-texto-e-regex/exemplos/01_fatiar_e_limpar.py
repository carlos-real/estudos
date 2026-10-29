"""Exemplo 01 — Fatiar, procurar, limpar, quebrar e juntar textos (seções 1 a 4).

Rode na pasta curso-python:
    python 05-texto-e-regex/exemplos/01_fatiar_e_limpar.py
"""

# --- 1. Fatiamento --------------------------------------------------------
lote = "2025-A-0153"
print("Ano:", lote[:4], "| Linha:", lote[5], "| Sequencial:", lote[-4:])
print("De trás para frente:", lote[::-1])

# Strings são imutáveis: os métodos devolvem uma string NOVA.
codigo = "op-004512"
codigo_maiusculo = codigo.upper()
print(f"Original: {codigo!r} | Nova: {codigo_maiusculo!r}")

# --- 2. Procurar ----------------------------------------------------------
assunto = "Liberação de carga - OP 004512 - Cliente Plastifort"
print("Tem OP?", "OP" in assunto, "| Posição:", assunto.find("OP"))
print("Tem NF?", "NF" in assunto, "| Posição:", assunto.find("NF"))
print("É PDF ou Excel?", "LAUDO_0153.PDF".lower().endswith((".pdf", ".xlsx")))

# --- 3. Limpar ------------------------------------------------------------
print(repr("   embalagens   DO sul  ltda \n".strip()))
print("rstrip('.csv')      ->", "laudos.csv".rstrip(".csv"), "  (cuidado!)")
print("removesuffix('.csv') ->", "laudos.csv".removesuffix(".csv"))
print("zfill(9):", "12345".zfill(9))

# --- 4. split, partition e join -------------------------------------------
linha = "OP: 123456 | NF: 98765 | Peso: 1.250,5 kg"
partes = [parte.strip() for parte in linha.split("|")]
print(partes)
for parte in partes:
    rotulo, _, valor = parte.partition(":")
    print(f"  {rotulo.strip():>5} = {valor.strip()}")

print("Espaços normalizados:", " ".join("  embalagens   DO sul\tltda ".split()))


# Exemplo resolvido da aula: padronizar o código de lote.
def padronizar_lote(texto):
    ano, linha_producao, seq = texto.replace("-", " ").split()
    return "-".join([ano, linha_producao.upper(), seq.zfill(4)])


for digitado in [" 2025 a 153 ", "2025-b-7", "2025 C 0042"]:
    print(f"{digitado!r:>16} -> {padronizar_lote(digitado)}")
