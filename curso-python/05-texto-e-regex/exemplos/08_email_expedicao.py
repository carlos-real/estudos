"""Exemplo 08 — Projeto guiado: lendo o e-mail da expedição (seção 15).

Rode na pasta curso-python:
    python 05-texto-e-regex/exemplos/08_email_expedicao.py
"""

import re

EMAIL = """De: expedicao@plastifort.com.br
Assunto: Certificados - carga de 28/10

Bom dia, laboratório!

Favor emitir os certificados dos pedidos abaixo:

OP: 123456 | NF: 98765 | Peso: 1.250,5 kg
OP: 123457 | NF: 98766 | Peso: 980,0 kg
OP: 123458 | NF: 98767 | Peso: 2.040,75 kg

A OP 123459 vai na próxima carga.

Obrigado,
Expedição
"""

PEDIDO = re.compile(
    r"""
    OP:   \s* (?P<op>\d{6})              # OP com 6 dígitos
    \s* \| \s*                           # separador | (escapado!)
    NF:   \s* (?P<nf>\d+)                # NF: só dígitos
    \s* \| \s*
    Peso: \s* (?P<peso>[\d.]+(?:,\d+)?)  # peso no formato brasileiro
    \s* kg
    """,
    re.VERBOSE | re.IGNORECASE,
)


def br_para_float(texto):
    return float(texto.replace(".", "").replace(",", "."))


def float_para_br(valor):
    return f"{valor:,.2f}".translate(str.maketrans(",.", ".,"))


def ler_pedidos(email):
    pedidos = []
    for achado in PEDIDO.finditer(email):
        peso = br_para_float(achado["peso"])
        pedidos.append({"op": achado["op"], "nf": achado["nf"], "peso_kg": peso})
    return pedidos


pedidos = ler_pedidos(EMAIL)
assunto = re.search(r"^Assunto:\s*(.+)$", EMAIL, re.MULTILINE).group(1)

print(f"Assunto: {assunto}")
print(f"{'OP':<8}{'NF':>8}{'Peso (kg)':>14}")
for pedido in pedidos:
    print(f"{pedido['op']:<8}{pedido['nf']:>8}{float_para_br(pedido['peso_kg']):>14}")
total = sum(p["peso_kg"] for p in pedidos)
print(f"{'Total':<16}{float_para_br(total):>14}")

# Passo 5 da aula: depurar uma linha que não casa, cortando o padrão ao meio.
problema = "OP: 123460 | NF: 98.768 | Peso: 500 kg"
print("\nDepurando:", problema)
print("  OP casa?          ", re.search(r"OP:\s*(\d{6})", problema) is not None)
print(
    "  OP + NF + | casa? ",
    re.search(r"OP:\s*\d{6}\s*\|\s*NF:\s*\d+\s*\|", problema) is not None,
)
print(
    "  NF capturada:     ", re.search(r"NF:\s*(\d+)", problema).group(1), "<- parou no ponto!"
)
