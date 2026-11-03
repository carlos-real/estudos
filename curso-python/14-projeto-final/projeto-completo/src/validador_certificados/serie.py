"""Orquestração de uma série: do e-mail ao relatório.

É a única função que conhece TODAS as peças. Cada peça continua testável sozinha.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from . import banco, expedicao, historico, planilha, relatorio
from .emissao import Emissor, emitir_fila
from .fila import montar_fila
from .modelos import ItemFila

logger = logging.getLogger(__name__)


@dataclass
class ResumoSerie:
    """O que a série produziu (a CLI usa para imprimir o resumo)."""

    itens: list[ItemFila]
    fora_do_padrao: dict[str, str]
    relatorio_excel: Path
    relatorio_csv: Path
    contagem: dict[str, int] = field(default_factory=dict)


def executar_serie(
    planilha_valores: Path,
    regras: Path,
    pasta_emails: Path,
    saida: Path,
    emissor: Emissor,
) -> ResumoSerie:
    """Lê tudo, faz a triagem, emite (ou simula) e grava os relatórios."""
    modo = "ENSAIO" if emissor.ensaio else "REAL"
    logger.info("série iniciada em modo %s", modo)

    especificacoes = banco.carregar_do_arquivo(regras)
    medicoes = planilha.ler_planilha(planilha_valores)
    pedidos, fora_do_padrao = expedicao.separar_emails(
        expedicao.ler_pasta_emails(pasta_emails)
    )
    for arquivo, problema in fora_do_padrao.items():
        logger.warning("e-mail fora do padrão: %s (%s)", arquivo, problema)

    fila, bloqueados = montar_fila(pedidos, medicoes, especificacoes)
    for item in bloqueados:
        logger.warning("OP %s bloqueada: %s", item.op, "; ".join(item.motivos))

    arquivo_historico = Path(saida) / "emitidos.csv"
    resultados = emitir_fila(fila, emissor, historico.carregar_emitidas(arquivo_historico))
    if not emissor.ensaio:  # ensaio nunca grava histórico
        historico.registrar_emitidas(arquivo_historico, resultados)

    itens = resultados + bloqueados
    carimbo = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    excel = relatorio.gerar_relatorio_excel(
        itens, fora_do_padrao, Path(saida) / f"relatorio_{carimbo}.xlsx"
    )
    csv = relatorio.escrever_relatorio_csv(itens, Path(saida) / f"relatorio_{carimbo}.csv")
    logger.info("relatórios gravados: %s e %s", excel.name, csv.name)
    return ResumoSerie(
        itens=itens,
        fora_do_padrao=fora_do_padrao,
        relatorio_excel=excel,
        relatorio_csv=csv,
        contagem=relatorio.resumir(itens),
    )
