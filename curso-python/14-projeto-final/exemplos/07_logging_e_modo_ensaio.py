"""Logging e modo ensaio: o robô que primeiro só DIZ o que faria.

Rode:  python exemplos/07_logging_e_modo_ensaio.py
"""

import logging
import sys

logger = logging.getLogger("robo")


class Emissor:
    """Interface: todo emissor tem `ensaio` e `emitir(op, nf) -> comprovante`."""

    ensaio = False

    def emitir(self, op: str, nf: str) -> str:
        raise NotImplementedError


class EmissorEnsaio(Emissor):
    ensaio = True

    def emitir(self, op: str, nf: str) -> str:
        logger.info("ENSAIO: emitiria certificado da OP %s / NF %s", op, nf)
        return f"ENSAIO-{op}-{nf}"


def emitir_todos(pedidos: list[tuple[str, str]], emissor: Emissor) -> None:
    feitos: set[tuple[str, str]] = set()
    for op, nf in pedidos:
        if (op, nf) in feitos:
            logger.warning("OP %s / NF %s repetida: ignorada", op, nf)
            continue
        comprovante = emissor.emitir(op, nf)
        feitos.add((op, nf))
        logger.debug("comprovante %s", comprovante)


if __name__ == "__main__":
    # stream=sys.stdout só para a saída aparecer junto com os prints neste exemplo.
    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s",
                        stream=sys.stdout)  # fmt: skip
    emitir_todos([("24518", "123456"), ("24541", "123789"), ("24518", "123456")],
                 EmissorEnsaio())  # fmt: skip
