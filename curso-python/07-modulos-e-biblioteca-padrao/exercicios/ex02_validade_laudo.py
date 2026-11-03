"""
Exercício 07.02 — Validade do laudo
Nível: ★☆☆

Contexto: Todo laudo de qualidade tem validade (no seu laboratório, 180 dias a partir
da emissão). O cliente só aceita material com laudo válido, então a expedição precisa
saber se o laudo ainda vale e quantos dias faltam.

Tarefa:
1. `data_vencimento(emissao, dias_validade=180)` devolve a data de vencimento
   (emissão + dias_validade dias).
2. `laudo_valido(emissao, hoje, dias_validade=180)` devolve True se `hoje` for
   menor ou igual ao vencimento (no próprio dia do vencimento o laudo ainda vale).
3. `dias_para_vencer(emissao, hoje, dias_validade=180)` devolve quantos dias faltam
   até o vencimento (int). Se já venceu, o número é negativo.

Por que `hoje` é parâmetro e não date.today()? Porque assim dá para testar com
qualquer data. Quem chama a função passa date.today() no programa de verdade.

Exemplos:
    >>> from datetime import date
    >>> data_vencimento(date(2026, 10, 29))
    datetime.date(2027, 4, 27)
    >>> laudo_valido(date(2026, 10, 29), date(2027, 4, 27))
    True
    >>> dias_para_vencer(date(2026, 10, 29), date(2027, 5, 1))
    -4

Dica: subtrair duas datas dá um timedelta; o atributo .days tem o número de dias.

Teste com:  python curso.py testar 07 ex02
"""

from datetime import date


def data_vencimento(emissao: date, dias_validade: int = 180) -> date:
    """Data em que o laudo vence."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def laudo_valido(emissao: date, hoje: date, dias_validade: int = 180) -> bool:
    """True se o laudo ainda vale em `hoje` (vencimento incluso)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def dias_para_vencer(emissao: date, hoje: date, dias_validade: int = 180) -> int:
    """Dias que faltam para vencer (negativo se já venceu)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
