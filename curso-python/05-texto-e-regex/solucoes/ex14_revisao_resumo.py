"""
Exercício 05.14 — Revisão: resumo para responder a expedição
Nível: ★★★

Contexto: Depois de ler o e-mail, o laboratório responde à expedição com um
resumo alinhado, para conferir os pedidos de relance (o Outlook mostra em
fonte de largura fixa quando você cola como texto sem formatação).

Este exercício mistura formatação de texto (módulo 05) com f-strings e
alinhamento (módulo 01), decisões (módulo 02) e listas, sorted e acumuladores
(módulo 03).

Tarefa: implemente `montar_resumo(pedidos)`. `pedidos` é uma lista de
dicionários como os do ex12: {"op": "123456", "nf": "98765", "peso_kg": 1250.5}.
Regras:
- uma linha por pedido, em ordem CRESCENTE de OP, neste formato:
      OP 123456 | NF 000.098.765 |   1.250,50 kg
  (NF com 9 dígitos e pontos, como no ex02; peso no formato brasileiro com
  2 casas, alinhado à direita em 10 caracteres, como no ex06);
- no fim, uma linha de total:
      Total: 2 pedidos           |   2.230,50 kg
  ("Total: N pedidos", ou "Total: 1 pedido" no singular, alinhado à esquerda
  em 26 caracteres; depois " | ", o peso total no mesmo formato e " kg");
- as linhas são separadas por quebra de linha, sem quebra no final;
- lista vazia: devolva "Nenhum pedido encontrado.".

Exemplos:
    >>> pedidos = [
    ...     {"op": "123457", "nf": "98766", "peso_kg": 980.0},
    ...     {"op": "123456", "nf": "98765", "peso_kg": 1250.5},
    ... ]
    >>> print(montar_resumo(pedidos))
    OP 123456 | NF 000.098.765 |   1.250,50 kg
    OP 123457 | NF 000.098.766 |     980,00 kg
    Total: 2 pedidos           |   2.230,50 kg

Dica: copie para este arquivo as funções que você escreveu nos ex02 e ex06 (no
módulo 07 você aprende a importá-las em vez de copiar). Monte uma lista de
linhas e junte no final com "\\n".join(linhas).

Teste com:  python curso.py testar 05 ex14
"""


def formatar_nf(numero: str) -> str:
    """NF com 9 dígitos no formato DDD.DDD.DDD (ex02)."""
    digitos = "".join([c for c in numero if c.isdigit()]).zfill(9)
    return f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:]}"


def float_para_br(valor: float, casas: int = 2) -> str:
    """1250.5 -> "1.250,50" (ex06)."""
    return f"{valor:,.{casas}f}".translate(str.maketrans(",.", ".,"))


def montar_resumo(pedidos: list[dict]) -> str:
    """Monta o texto alinhado com um pedido por linha e o total no fim."""
    if not pedidos:  # retorno antecipado para o caso especial
        return "Nenhum pedido encontrado."

    linhas = []
    total = 0.0  # acumulador (módulo 02)
    # sorted devolve uma lista NOVA e não mexe na lista de quem chamou.
    # Como toda OP tem 6 dígitos, ordenar o texto dá a mesma ordem dos números.
    for pedido in sorted(pedidos, key=lambda p: p["op"]):
        peso = float_para_br(pedido["peso_kg"])
        linhas.append(f"OP {pedido['op']} | NF {formatar_nf(pedido['nf'])} | {peso:>10} kg")
        total += pedido["peso_kg"]

    # Singular ou plural: uma expressão condicional resolve (módulo 02).
    palavra = "pedido" if len(pedidos) == 1 else "pedidos"
    rotulo = f"Total: {len(pedidos)} {palavra}"
    # 26 = largura de "OP 123456 | NF 000.098.765": assim o "|" fica alinhado.
    linhas.append(f"{rotulo:<26} | {float_para_br(total):>10} kg")
    return "\n".join(linhas)
