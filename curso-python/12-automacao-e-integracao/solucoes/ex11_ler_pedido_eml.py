"""
Exercício 12.11 — Ler o pedido da expedição num arquivo .eml (SOLUÇÃO)

Decomposição: (1) bytes -> mensagem, (2) mensagem -> texto limpo,
(3) texto -> campos. Cada etapa é uma função pequena; ler_pedido só as encadeia.
"""

import re
from email import policy
from email.message import EmailMessage
from email.parser import BytesParser
from email.utils import parseaddr

# re.IGNORECASE: aceita "OP", "op", "Op". \s* aceita espaços (ou nenhum).
RE_OP = re.compile(r"\bOP\s*:?\s*(\d{6})\b", re.IGNORECASE)
RE_NF = re.compile(r"\bNF\s*:?\s*(\d+)", re.IGNORECASE)
# Peso no formato brasileiro: dígitos com pontos de milhar e vírgula opcional.
RE_PESO = re.compile(r"\bPeso\s*:?\s*([\d.]+(?:,\d+)?)\s*kg", re.IGNORECASE)
RE_TAG = re.compile(r"<[^>]+>")


def texto_do_corpo(msg: EmailMessage) -> str:
    """Prefere o texto puro; se só houver HTML, remove as tags."""
    corpo = msg.get_body(preferencelist=("plain", "html"))
    if corpo is None:
        return ""
    texto = corpo.get_content()
    if corpo.get_content_type() == "text/html":
        # Trocar por ESPAÇO (e não por "") evita grudar palavras:
        # "OP:<b>124001</b>" vira "OP: 124001 " e não "OP:124001".
        texto = RE_TAG.sub(" ", texto)
    return texto


def numero_br(texto: str) -> float:
    """'1.250,5' -> 1250.5 (o mesmo truque do módulo 05)."""
    return float(texto.replace(".", "").replace(",", "."))


def ler_pedido(conteudo: bytes) -> dict:
    """Extrai remetente, assunto, OP, NF e peso de um e-mail (.eml em bytes)."""
    msg = BytesParser(policy=policy.default).parsebytes(conteudo)
    texto = texto_do_corpo(msg)

    achados = {"OP": RE_OP.search(texto), "NF": RE_NF.search(texto), "peso": RE_PESO.search(texto)}
    # Um dicionário mantém a ordem de inserção: checamos OP, NF e peso nessa ordem.
    for campo, achado in achados.items():
        if achado is None:
            raise ValueError(f"Campo não encontrado: {campo}")

    _, endereco = parseaddr(msg["From"])
    return {
        "remetente": endereco,
        "assunto": msg["Subject"],  # policy.default já decodifica os acentos
        "op": achados["OP"].group(1),
        "nf": achados["NF"].group(1),
        "peso_kg": numero_br(achados["peso"].group(1)),
    }
