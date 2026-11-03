"""Triagem dos pedidos: monta a fila de emissão (só OPs liberadas e aprovadas).

Esta é a camada de serviço: não lê arquivo nenhum, só junta as peças do domínio.
"""

from __future__ import annotations

import logging

from .modelos import Especificacao, EspecificacaoDesconhecida, ItemFila, Medicao, Pedido
from .planilha import conferir_linha, normalizar_linha
from .regras import escolher_especificacao, validar_medicao
from .texto import esta_liberado

logger = logging.getLogger(__name__)

SEM_LIBERACAO = "COF sem liberação na observação"


def montar_fila(
    pedidos: list[Pedido],
    medicoes: list[Medicao],
    especificacoes: dict[str, Especificacao],
) -> tuple[list[ItemFila], list[ItemFila]]:
    """Devolve (fila_para_emitir, bloqueados), cada um na ordem dos pedidos."""
    por_op: dict[str, list[Medicao]] = {}
    for medicao in medicoes:
        por_op.setdefault(medicao.op, []).append(medicao)

    fila: list[ItemFila] = []
    bloqueados: list[ItemFila] = []
    for pedido in pedidos:
        item = _triar(pedido, por_op.get(pedido.op, []), especificacoes)
        destino = fila if item.situacao == "emitir" else bloqueados
        destino.append(item)
        logger.debug("OP %s / NF %s -> %s %s", item.op, item.nf, item.situacao, item.motivos)
    logger.info("triagem: %d para emitir, %d bloqueados", len(fila), len(bloqueados))
    return fila, bloqueados


def _triar(
    pedido: Pedido, encontradas: list[Medicao], especificacoes: dict[str, Especificacao]
) -> ItemFila:
    def bloqueado(motivos: list[str], especificacao: str = "") -> ItemFila:
        return ItemFila(
            op=pedido.op,
            nf=pedido.nf,
            peso_kg=pedido.peso_kg,
            situacao="bloqueado",
            especificacao=especificacao,
            motivos=motivos,
        )

    # 1) A OP precisa existir na planilha, uma vez só.
    if not encontradas:
        return bloqueado(["OP não encontrada na planilha"])
    if len(encontradas) > 1:
        return bloqueado([f"OP aparece {len(encontradas)} vezes na planilha"])
    medicao = encontradas[0]

    # 2) A linha digitada tem que bater com a aba.
    problema = conferir_linha(medicao.aba, medicao.linha)
    if problema:
        return bloqueado([problema])

    # 3) Especificação: título conhecido ou padrão da linha. Nunca chuta.
    try:
        especificacao = escolher_especificacao(
            medicao.especificacao, normalizar_linha(medicao.aba), especificacoes
        )
    except EspecificacaoDesconhecida as erro:
        return bloqueado([str(erro)])

    # 4) Tolerâncias e 5) liberação: junta TODOS os motivos.
    motivos = list(validar_medicao(medicao, especificacao).motivos)
    if not esta_liberado(medicao.observacao):
        motivos.append(SEM_LIBERACAO)
    if motivos:
        return bloqueado(motivos, especificacao.titulo)
    return ItemFila(
        op=pedido.op,
        nf=pedido.nf,
        peso_kg=pedido.peso_kg,
        situacao="emitir",
        especificacao=especificacao.titulo,
    )
