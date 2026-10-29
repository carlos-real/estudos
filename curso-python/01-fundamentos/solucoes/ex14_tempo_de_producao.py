"""
Exercício 01.14 — Tempo de produção
Nível: ★★★

Contexto: O PCP pergunta ao laboratório quando a OP vai terminar para agendar a
coleta de amostras. Você sabe quantos metros faltam produzir e a velocidade da
máquina (metros por minuto).

Tarefa:
1. `minutos_de_producao(metros, velocidade_m_min)` devolve quantos minutos INTEIROS
   a máquina precisa. Qualquer fração de minuto conta como um minuto a mais
   (83,3 minutos viram 84). Use math.ceil.
2. `tempo_de_producao(metros, velocidade_m_min)` devolve esse tempo no formato
   "<horas>h<minutos>min", com os minutos SEMPRE em 2 dígitos: "1h24min", "0h05min".
3. `horario_termino(hora_inicio, minuto_inicio, metros, velocidade_m_min)` devolve o
   horário de término no formato "HH:MM" (2 dígitos cada). Se passar da meia-noite,
   volte a contar do zero: 22:50 + 84 minutos = "00:14".

Exemplos:
    >>> minutos_de_producao(12500, 150)
    84
    >>> tempo_de_producao(12500, 150)
    '1h24min'
    >>> horario_termino(22, 50, 12500, 150)
    '00:14'

Dica: converta tudo para minutos desde a meia-noite, some, e use // e % para voltar
a horas e minutos. Para "dar a volta" no relógio, % 24 nas horas resolve.
Lembre do `import math` no topo do arquivo.

Teste com:  python curso.py testar 01 ex14
"""

import math


def minutos_de_producao(metros: float, velocidade_m_min: float) -> int:
    """Devolve os minutos inteiros (arredondados para cima) de produção."""
    # math.ceil arredonda SEMPRE para cima: 83.33 -> 84. round() daria 83 e a coleta
    # seria agendada antes da máquina terminar.
    return math.ceil(metros / velocidade_m_min)


def tempo_de_producao(metros: float, velocidade_m_min: float) -> str:
    """Devolve o tempo de produção no formato '1h24min'."""
    total = minutos_de_producao(metros, velocidade_m_min)
    horas = total // 60  # quantas horas cheias cabem
    minutos = total % 60  # o que sobra depois das horas cheias
    # :02d preenche com zero à esquerda até 2 dígitos: 5 -> "05".
    return f"{horas}h{minutos:02d}min"


def horario_termino(
    hora_inicio: int, minuto_inicio: int, metros: float, velocidade_m_min: float
) -> str:
    """Devolve o horário de término no formato 'HH:MM'."""
    # Ideia central: transformar o horário num número só (minutos desde 00:00),
    # somar, e depois voltar para horas e minutos.
    inicio = hora_inicio * 60 + minuto_inicio
    fim = inicio + minutos_de_producao(metros, velocidade_m_min)
    # % 24 faz o relógio "dar a volta": 24 -> 0, 25 -> 1.
    horas = fim // 60 % 24
    minutos = fim % 60
    return f"{horas:02d}:{minutos:02d}"
