"""Ler os e-mails da expedição: encoding com plano B e o que cada padrão encontra.

Rode:  python exemplos/06_emails_da_expedicao.py
"""

import re
from pathlib import Path

PASTA = Path(__file__).resolve().parent.parent / "dados" / "emails"

RE_OP = re.compile(r"\bOP\b\s*(?:n[º°o]\.?\s*)?[:#-]?\s*(\d{4,6})\b", re.IGNORECASE)
RE_NF = re.compile(
    r"\b(?:NF-?e?|nota\s+fiscal)\s*(?:n[º°o]\.?\s*)?[:#-]?\s*(\d[\d.]*)", re.IGNORECASE
)
RE_PESO = re.compile(
    r"\bpeso(?:\s+l[ií]quido)?\s*[:=-]?\s*(\d[\d.]*(?:,\d+)?)\s*kg\b", re.IGNORECASE
)


def ler_texto(caminho: Path) -> str:
    """UTF-8 primeiro; se falhar, cp1252 (arquivo salvo no Windows)."""
    try:
        return caminho.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"  ({caminho.name} não é UTF-8: lendo como cp1252)")
        return caminho.read_text(encoding="cp1252")


for arquivo in sorted(PASTA.glob("*.txt")):
    texto = ler_texto(arquivo)
    ops = sorted(set(RE_OP.findall(texto)))
    nfs = sorted({nf.rstrip(".").replace(".", "") for nf in RE_NF.findall(texto)})
    pesos = sorted(set(RE_PESO.findall(texto)))
    print(f"{arquivo.name:24} OP={ops} NF={nfs} peso={pesos}")
