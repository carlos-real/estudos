"""
Exercício 09.05 — Log da inspeção
Nível: ★☆☆

Solução comentada. Veja o enunciado completo em exercicios/ex05_log_de_inspecao.py.
"""

import logging


def registrar_resultado(
    logger: logging.Logger, op: str, valor: float, minimo: float, maximo: float
) -> bool:
    """Registra no log se o valor está dentro da tolerância e devolve True/False."""
    # Montamos o trecho dos limites uma vez só, para não repetir a formatação.
    faixa = f"[{minimo:.2f}, {maximo:.2f}]"

    if minimo <= valor <= maximo:
        logger.info(f"OP {op}: {valor:.2f} dentro de {faixa}")
        return True

    # Retorno antecipado acima: se chegou aqui, está fora. Nada de else.
    logger.warning(f"OP {op}: {valor:.2f} FORA de {faixa}")
    return False


# Alternativa muito usada: passar os valores como argumentos do logger, no
# estilo "%" (o logging só monta o texto se o nível estiver ativo):
#     logger.info("OP %s: %.2f dentro de %s", op, valor, faixa)
# O resultado (record.getMessage()) é o mesmo. Para iniciantes, a f-string é
# mais legível; em código que registra milhares de linhas, o estilo "%" é
# um pouco mais eficiente.
