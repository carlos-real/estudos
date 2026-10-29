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


def montar_resumo(pedidos: list[dict]) -> str:
    """Monta o texto alinhado com um pedido por linha e o total no fim."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
