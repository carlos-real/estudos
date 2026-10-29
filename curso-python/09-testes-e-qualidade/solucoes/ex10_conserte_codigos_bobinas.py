"""
Exercício 09.10 — Conserte o bug: códigos das bobinas
Nível: ★★☆

Solução comentada. Veja o enunciado completo em exercicios/ex10_conserte_codigos_bobinas.py.
"""


def gerar_codigos_bobinas(op: str, quantidade: int) -> list[str]:
    """Gera os códigos '<op>-001', '<op>-002', ... das bobinas de uma OP."""
    # BUG 1 (validação ausente): com quantidade 0 ou negativa, range() fica
    # vazio e a função devolvia [] em silêncio. Um erro explícito é melhor que
    # uma lista vazia que ninguém percebe.
    if quantidade < 1:
        raise ValueError(f"quantidade deve ser pelo menos 1, recebi {quantidade}")

    # BUG 2 (espaços): " 4512 " gerava " 4512 -001". Normalize uma vez, no início.
    op = op.strip()

    # BUG 3 (off-by-one): range(quantidade) vai de 0 a quantidade - 1. As
    # etiquetas começam em 1, então o certo é range(1, quantidade + 1).
    # A compreensão de lista (módulo 03) substitui o "lista vazia + for +
    # append" do original: mesma lógica, menos linhas para ler.
    return [f"{op}-{numero:03d}" for numero in range(1, quantidade + 1)]
