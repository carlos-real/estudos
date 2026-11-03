"""Pedidos da expedição: leitura dos e-mails (OP, NF e peso).

Um e-mail = um pedido. Se faltar algo, ou se houver dois valores diferentes para o
mesmo campo (duas OPs, por exemplo), o e-mail fica "fora do padrão": o sistema não
escolhe por você.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from .modelos import Pedido, PedidoInvalido
from .texto import numero_br

logger = logging.getLogger(__name__)

RE_OP = re.compile(r"\bOP\b\s*(?:n[º°o]\.?\s*)?[:#-]?\s*(\d{4,6})\b", re.IGNORECASE)
RE_NF = re.compile(
    r"\b(?:NF-?e?|nota\s+fiscal)\s*(?:n[º°o]\.?\s*)?[:#-]?\s*(\d[\d.]*)", re.IGNORECASE
)
RE_PESO = re.compile(
    r"\bpeso(?:\s+l[ií]quido)?\s*[:=-]?\s*(\d[\d.]*(?:,\d+)?)\s*kg\b", re.IGNORECASE
)


def ler_email(texto: str, origem: str = "") -> Pedido:
    """Extrai um Pedido do texto do e-mail ou levanta PedidoInvalido com TODOS os problemas."""
    ops = sorted(set(RE_OP.findall(texto)))
    nfs = sorted({nf.rstrip(".").replace(".", "") for nf in RE_NF.findall(texto)})
    pesos = sorted({numero_br(p) for p in RE_PESO.findall(texto)})

    campos = (
        (ops, "OP não encontrada", "mais de uma OP no e-mail"),
        (nfs, "NF não encontrada", "mais de uma NF no e-mail"),
        ([f"{p:g}" for p in pesos], "peso não encontrado", "mais de um peso no e-mail"),
    )
    problemas = []
    for achados, se_faltar, se_sobrar in campos:
        if not achados:
            problemas.append(se_faltar)
        elif len(achados) > 1:
            problemas.append(f"{se_sobrar} ({', '.join(achados)})")
    if len(pesos) == 1 and pesos[0] <= 0:
        problemas.append("peso deve ser maior que zero")
    if problemas:
        raise PedidoInvalido("; ".join(problemas))
    return Pedido(op=ops[0], nf=nfs[0], peso_kg=pesos[0], origem=origem)


def separar_emails(emails: dict[str, str]) -> tuple[list[Pedido], dict[str, str]]:
    """Separa e-mails válidos (Pedidos) dos fora do padrão ({arquivo: problema})."""
    pedidos: list[Pedido] = []
    fora_do_padrao: dict[str, str] = {}
    for nome, texto in emails.items():
        try:
            pedidos.append(ler_email(texto, origem=nome))
        except PedidoInvalido as erro:
            fora_do_padrao[nome] = str(erro)
    return pedidos, fora_do_padrao


def ler_texto(caminho: Path) -> str:
    """Lê um .txt em UTF-8; se falhar, tenta cp1252 (padrão de arquivos salvos no Windows)."""
    try:
        return caminho.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        logger.debug("%s não é UTF-8; lendo como cp1252", caminho.name)
        return caminho.read_text(encoding="cp1252")


def ler_pasta_emails(pasta: Path) -> dict[str, str]:
    """{nome_do_arquivo: texto} para cada .txt da pasta, em ordem alfabética."""
    pasta = Path(pasta)
    if not pasta.is_dir():
        raise FileNotFoundError(f"pasta de e-mails não encontrada: {pasta}")
    emails = {arquivo.name: ler_texto(arquivo) for arquivo in sorted(pasta.glob("*.txt"))}
    logger.info("expedição: %d e-mails lidos de %s", len(emails), pasta)
    return emails
