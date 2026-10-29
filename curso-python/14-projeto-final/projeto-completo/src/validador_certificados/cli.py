"""Interface de linha de comando: traduz argumentos em uma chamada a executar_serie.

Códigos de saída:
    0  série processada, sem falhas de emissão
    1  erro esperado (arquivo, planilha, banco) ou alguma falha de emissão
    2  argumentos inválidos (o argparse cuida disso)
    3  erro inesperado (bug): o traceback completo vai para o log
"""

from __future__ import annotations

import argparse
import logging
import sqlite3
import sys
from pathlib import Path

from . import __version__
from .emissao import EmissaoIndisponivel, EmissorTotvs
from .modelos import PlanilhaInvalida
from .serie import ResumoSerie, executar_serie

logger = logging.getLogger("validador_certificados")

ERROS_ESPERADOS = (
    FileNotFoundError,
    PermissionError,
    PlanilhaInvalida,
    sqlite3.Error,
    EmissaoIndisponivel,
)


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="validador",
        description="Confere OPs da planilha contra as regras e prepara os certificados.",
    )
    parser.add_argument("--planilha", type=Path, required=True, help="planilha de valores")
    parser.add_argument("--regras", type=Path, required=True, help="banco de regras (.db)")
    parser.add_argument("--emails", type=Path, required=True, help="pasta com os e-mails .txt")
    parser.add_argument(
        "--saida",
        type=Path,
        default=Path("saida"),
        help="pasta dos relatórios (padrão: saida)",
    )
    parser.add_argument(
        "--emitir",
        action="store_true",
        help="emite de verdade no TOTVS (ainda não disponível; o padrão é modo ensaio)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="log detalhado (DEBUG)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def configurar_logging(verbose: bool, arquivo: Path) -> None:
    """Log no terminal (stderr) e em arquivo. O arquivo sempre guarda DEBUG."""
    encerrar_logging()
    logger.setLevel(logging.DEBUG)
    terminal = logging.StreamHandler(sys.stderr)
    terminal.setLevel(logging.DEBUG if verbose else logging.INFO)
    terminal.setFormatter(logging.Formatter("%(levelname)-8s %(message)s"))
    em_arquivo = logging.FileHandler(arquivo, encoding="utf-8")
    em_arquivo.setLevel(logging.DEBUG)
    em_arquivo.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s")
    )
    logger.addHandler(terminal)
    logger.addHandler(em_arquivo)


def encerrar_logging() -> None:
    """Fecha os handlers (no Windows, arquivo de log aberto não pode ser apagado)."""
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()


def imprimir_resumo(resumo: ResumoSerie, ensaio: bool) -> None:
    if ensaio:
        print("Série processada em modo ENSAIO (nada foi enviado ao TOTVS)")
    else:
        print("Série processada (emissão real)")
    for situacao, quantidade in resumo.contagem.items():
        print(f"  {situacao:<24}{quantidade:>3}")
    print(f"  {'e-mails fora do padrão':<24}{len(resumo.fora_do_padrao):>3}")
    print(f"Relatório: {resumo.relatorio_excel}")


def main(argv: list[str] | None = None) -> int:
    args = criar_parser().parse_args(argv)
    args.saida.mkdir(parents=True, exist_ok=True)
    configurar_logging(args.verbose, args.saida / "validador.log")
    try:
        emissor = EmissorTotvs(ensaio=not args.emitir)
        resumo = executar_serie(args.planilha, args.regras, args.emails, args.saida, emissor)
    except ERROS_ESPERADOS as erro:
        logger.error("%s", erro)
        return 1
    except Exception:
        logger.exception("erro inesperado; detalhes no log %s", args.saida / "validador.log")
        return 3
    finally:
        encerrar_logging()
    imprimir_resumo(resumo, emissor.ensaio)
    return 1 if resumo.contagem.get("falha") else 0
