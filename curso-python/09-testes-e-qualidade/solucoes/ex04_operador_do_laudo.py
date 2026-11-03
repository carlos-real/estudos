"""
Exercício 09.04 — Operador do laudo (variável de ambiente)
Nível: ★☆☆

Solução comentada. Veja o enunciado completo em exercicios/ex04_operador_do_laudo.py.
"""

import os


def operador_atual() -> str:
    """Nome do operador (variável LAB_OPERADOR) ou 'não informado'."""
    # .get com valor padrão "" trata o caso "variável não existe" sem if extra.
    # O strip() resolve espaços em volta, e o texto vazio é falsy: o "or"
    # escolhe "não informado" tanto para variável ausente quanto para "   ".
    return os.environ.get("LAB_OPERADOR", "").strip() or "não informado"


def assinatura_laudo(op: str) -> str:
    """Texto 'OP <op> | operador: <nome>' para o rodapé do laudo."""
    # Reaproveita operador_atual(): a regra do operador fica num lugar só.
    return f"OP {op} | operador: {operador_atual()}"


# Por que ler a variável DENTRO da função (e não numa constante no topo do
# arquivo)? Porque o valor é lido na hora da chamada. Se fosse lido ao importar
# o módulo, o monkeypatch.setenv do teste chegaria tarde demais.
