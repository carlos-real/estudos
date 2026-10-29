"""logging: registrar o que o programa faz, no terminal e num arquivo.

Rode:  python exemplos/03_logging_inspecao.py
O arquivo de log fica em exemplos/saida/inspecao.log (a pasta saida/ é ignorada pelo Git).
"""

import logging
from pathlib import Path

PASTA_SAIDA = Path(__file__).resolve().parent / "saida"
ARQUIVO_LOG = PASTA_SAIDA / "inspecao.log"

# Cada módulo pede o seu logger pelo nome. __name__ vira "__main__" quando o
# arquivo é executado direto; aqui usamos um nome fixo para ficar mais claro.
logger = logging.getLogger("inspecao")


def configurar_log() -> None:
    """Configura o log UMA vez, no início do programa (nunca dentro das funções)."""
    PASTA_SAIDA.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,  # DEBUG fica de fora; INFO e acima aparecem
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
        handlers=[
            logging.StreamHandler(),  # terminal
            logging.FileHandler(ARQUIVO_LOG, mode="w", encoding="utf-8"),  # arquivo
        ],
    )


def conferir(op: str, valor: float, minimo: float, maximo: float) -> bool:
    logger.debug("conferindo OP %s com valor %s", op, valor)  # não aparece (nível INFO)
    if minimo <= valor <= maximo:
        logger.info("OP %s: %.2f dentro de [%.2f, %.2f]", op, valor, minimo, maximo)
        return True
    logger.warning("OP %s: %.2f FORA de [%.2f, %.2f]", op, valor, minimo, maximo)
    return False


def main() -> None:
    configurar_log()
    logger.info("Início da conferência")
    conferir("12345", 20.1, 19.0, 21.0)
    conferir("12346", 22.4, 19.0, 21.0)
    try:
        conferir("12347", float("vinte"), 19.0, 21.0)
    except ValueError:
        # exception() registra no nível ERROR e inclui o traceback completo
        logger.exception("OP 12347: valor ilegível na planilha")
    logger.info("Fim da conferência")
    print(f"\nLog gravado em: {ARQUIVO_LOG.name}")


if __name__ == "__main__":
    main()
