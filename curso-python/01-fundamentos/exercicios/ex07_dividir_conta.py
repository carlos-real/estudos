"""
Exercício 01.07 — Dividir a conta
Nível: ★★☆

Contexto: Fim do mês, a equipe do laboratório sai para almoçar. A conta vem sem a taxa
de serviço e alguém precisa calcular quanto cada um paga.

Tarefa:
1. `valor_por_pessoa(total, pessoas, servico_pct)` devolve quanto cada pessoa paga:
   o total acrescido de `servico_pct` por cento, dividido pelo número de pessoas,
   arredondado com round() para 2 casas.
   Se `pessoas` for 0, deixe o próprio Python levantar ZeroDivisionError (não trate).
2. `resumo_conta(total, pessoas, servico_pct)` devolve o texto:
   Total com <servico_pct>% de serviço: R$ <total com serviço> | Por pessoa: R$ <valor>
   com os dois valores em 2 casas decimais (formato :.2f).

Exemplos:
    >>> valor_por_pessoa(150.0, 4, 10)
    41.25
    >>> resumo_conta(100.0, 3, 10)
    'Total com 10% de serviço: R$ 110.00 | Por pessoa: R$ 36.67'

Dica: acrescentar 10% é multiplicar por (1 + 10 / 100).

Teste com:  python curso.py testar 01 ex07
"""


def valor_por_pessoa(total: float, pessoas: int, servico_pct: int) -> float:
    """Devolve o valor que cada pessoa paga, com serviço, em 2 casas."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def resumo_conta(total: float, pessoas: int, servico_pct: int) -> str:
    """Devolve o resumo da conta em uma linha de texto."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
