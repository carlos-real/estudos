"""Emissão dos certificados: a fronteira com o TOTVS.

O resto do sistema só conhece a interface `Emissor` (um método `emitir`). Hoje existe
o `EmissorTotvs` em modo ensaio, que só registra o que faria. O robô de verdade
(Playwright no Edge) vai implementar a mesma interface: veja robo_playwright.py.
"""

from __future__ import annotations

import logging
from dataclasses import replace

from .modelos import ItemFila

logger = logging.getLogger(__name__)


class ErroEmissao(Exception):
    """Falha esperada ao emitir UM certificado (tela não abriu, campo recusou...)."""


class EmissaoIndisponivel(Exception):
    """O modo real de emissão ainda não está disponível."""


class Emissor:
    """Interface: qualquer emissor tem `ensaio` e `emitir(item) -> comprovante`."""

    ensaio: bool = False

    def emitir(self, item: ItemFila) -> str:
        raise NotImplementedError


class EmissorTotvs(Emissor):
    """Emissor do TOTVS. Por enquanto só o modo ensaio: registra o que faria."""

    def __init__(self, ensaio: bool = True) -> None:
        if not ensaio:
            raise EmissaoIndisponivel(
                "emissão real no TOTVS ainda não implementada "
                "(veja robo_playwright.py); rode em modo ensaio"
            )
        self.ensaio = True
        self.registro: list[str] = []

    def emitir(self, item: ItemFila) -> str:
        acao = (
            f"emitiria certificado: OP {item.op} | NF {item.nf} | "
            f"{item.peso_kg:.2f} kg | {item.especificacao}"
        )
        self.registro.append(acao)
        logger.info("ENSAIO: %s", acao)
        return f"ENSAIO-{item.op}-{item.nf}"


def emitir_fila(
    fila: list[ItemFila],
    emissor: Emissor,
    ja_emitidas: set[tuple[str, str]] | None = None,
) -> list[ItemFila]:
    """Emite cada item da fila e devolve NOVOS itens com a situação final.

    - (OP, NF) já emitido antes ou repetido na fila -> "ignorado" (idempotência);
    - sucesso -> "ensaio" (emissor de ensaio) ou "emitido", com o comprovante;
    - ErroEmissao -> "falha", e a série CONTINUA com o próximo item;
    - item que não está "emitir" volta sem mudança;
    - qualquer outra exceção é bug: sobe.
    """
    vistas = set(ja_emitidas or ())  # cópia: não altera o conjunto de quem chamou
    resultado: list[ItemFila] = []
    for item in fila:
        if item.situacao != "emitir":
            resultado.append(item)
            continue
        chave = (item.op, item.nf)
        if chave in vistas:
            motivos = item.motivos + ["certificado já emitido para esta OP/NF"]
            resultado.append(replace(item, situacao="ignorado", motivos=motivos))
            continue
        try:
            comprovante = emissor.emitir(item)
        except ErroEmissao as erro:
            logger.error("falha ao emitir OP %s / NF %s: %s", item.op, item.nf, erro)
            motivos = item.motivos + [f"falha na emissão: {erro}"]
            resultado.append(replace(item, situacao="falha", motivos=motivos))
            continue
        vistas.add(chave)
        situacao = "ensaio" if emissor.ensaio else "emitido"
        resultado.append(replace(item, situacao=situacao, comprovante=comprovante))
    return resultado
