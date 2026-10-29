"""
Exercício 03.07 — Peso total por OP
Nível: ★★☆

Contexto: A planilha da expedição tem uma coluna com a OP de cada bobina e outra
com o peso (kg). Uma mesma OP pode ter várias bobinas. Para o certificado, você
precisa do peso total de cada OP.

Tarefa: implemente `pesos_por_op(ops, pesos)`.
- `ops` e `pesos` são "colunas": o item i de uma corresponde ao item i da outra.
- Devolva um dicionário  OP -> peso total, com cada total arredondado com
  round(..., 2). As OPs aparecem na ordem da primeira vez que surgem.
- Se as listas tiverem tamanhos diferentes, há erro na planilha: devolva {}.

Exemplos:
    >>> pesos_por_op(["OP-4512", "OP-4513", "OP-4512"], [500.0, 320.5, 250.25])
    {'OP-4512': 750.25, 'OP-4513': 320.5}
    >>> pesos_por_op(["OP-4512"], [500.0, 320.5])
    {}

Dica: zip(ops, pesos) caminha pelas duas listas ao mesmo tempo. Mas zip para em
silêncio na lista mais curta, então confira os tamanhos antes.

Teste com:  python curso.py testar 03 ex07
"""


def pesos_por_op(ops: list[str], pesos: list[float]) -> dict[str, float]:
    """Soma os pesos de cada OP (arredondados em 2 casas)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
