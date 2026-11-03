"""
Exercício 09.05 — Log da inspeção
Nível: ★☆☆

Contexto: o robô que confere as bobinas roda sozinho de madrugada. Ninguém vê
o terminal, então print() não serve: cada conferência precisa ir para o log,
com o nível certo, para quem investigar um problema no dia seguinte.

Tarefa: implemente registrar_resultado(logger, op, valor, minimo, maximo).
  - Se minimo <= valor <= maximo (bordas incluídas): registre no nível INFO a
    mensagem "OP <op>: <valor> dentro de [<minimo>, <maximo>]" e devolva True.
  - Senão: registre no nível WARNING a mensagem
    "OP <op>: <valor> FORA de [<minimo>, <maximo>]" e devolva False.
  - Os três números aparecem com 2 casas decimais (formato :.2f).
  - Use o logger recebido no parâmetro (não use print nem logging.info direto).

Exemplos:
    >>> logger = logging.getLogger("lab")
    >>> registrar_resultado(logger, "123", 25.4, 24.0, 26.0)
    True
    (no log, nível INFO: "OP 123: 25.40 dentro de [24.00, 26.00]")
    >>> registrar_resultado(logger, "124", 27.1, 24.0, 26.0)
    False
    (no log, nível WARNING: "OP 124: 27.10 FORA de [24.00, 26.00]")

Dica: logger.info(...) e logger.warning(...). Os testes usam a fixture caplog,
que captura os registros de log (seção 17 da aula).

Teste com:  python curso.py testar 09 ex05
"""

import logging


def registrar_resultado(
    logger: logging.Logger, op: str, valor: float, minimo: float, maximo: float
) -> bool:
    """Registra no log se o valor está dentro da tolerância e devolve True/False."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
