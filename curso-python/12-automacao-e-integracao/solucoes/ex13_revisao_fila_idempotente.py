"""
Exercício 12.13 — Revisão: fila de emissão idempotente (SOLUÇÃO)

Idempotente = rodar uma vez ou dez vezes dá o mesmo resultado final. O segredo
é sempre PERGUNTAR ao registro antes de agir e ANOTAR logo depois de agir.
"""

import csv
import logging
from collections.abc import Callable
from pathlib import Path

CABECALHO = ["op", "nf", "certificado"]

log = logging.getLogger(__name__)


def ler_registro(registro: Path) -> set[tuple[str, str]]:
    """Lê o CSV (criando-o se preciso) e devolve os pares (op, nf) já emitidos."""
    if not registro.exists():
        with registro.open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo, delimiter=";").writerow(CABECALHO)
        return set()
    with registro.open(encoding="utf-8", newline="") as arquivo:
        return {(linha["op"], linha["nf"]) for linha in csv.DictReader(arquivo, delimiter=";")}


def anotar(registro: Path, op: str, nf: str, certificado: str) -> None:
    """Acrescenta UMA linha. Modo "a" (append) nunca apaga o que já existe."""
    with registro.open("a", encoding="utf-8", newline="") as arquivo:
        csv.writer(arquivo, delimiter=";").writerow([op, nf, certificado])


def processar_fila(
    pedidos: list[dict], emitir: Callable[[dict], str], registro: Path
) -> dict[str, int]:
    """Emite os pedidos ainda não registrados; nunca emite o mesmo par (OP, NF) duas vezes."""
    feitos = ler_registro(registro)
    contagem = {"emitidos": 0, "pulados": 0, "falhas": 0}

    for pedido in pedidos:
        chave = (pedido["op"], pedido["nf"])
        if chave in feitos:  # pergunta ANTES de agir
            contagem["pulados"] += 1
            continue
        try:
            certificado = emitir(pedido)
        except Exception:
            # Capturar Exception "genérica" costuma ser má ideia, mas aqui é a
            # fronteira do robô: um pedido com problema não pode derrubar a fila
            # inteira. Em troca, REGISTRAMOS a falha com o traceback no log.
            log.exception("Falha ao emitir OP %s / NF %s", *chave)
            contagem["falhas"] += 1
            continue
        anotar(registro, pedido["op"], pedido["nf"], certificado)  # anota DEPOIS de agir
        feitos.add(chave)  # vale também para repetidos dentro desta mesma fila
        contagem["emitidos"] += 1

    return contagem
