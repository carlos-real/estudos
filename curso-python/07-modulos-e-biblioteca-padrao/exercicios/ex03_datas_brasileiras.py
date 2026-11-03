"""
Exercício 07.03 — Datas no formato brasileiro
Nível: ★☆☆

Contexto: Na planilha do laboratório e nos e-mails da expedição as datas vêm como
texto "29/10/2026" ou "29/10/2026 14:30". O Python precisa de objetos date/datetime
para fazer contas, e os relatórios precisam do texto de volta.

Tarefa:
1. `ler_data_br(texto)` converte "dd/mm/aaaa" em date. Ignore espaços nas pontas.
   Texto inválido (ex.: "31/02/2026" ou "2026-10-29") deve gerar ValueError
   (o strptime já faz isso por você).
2. `formatar_data_br(data)` faz o caminho contrário: date → "dd/mm/aaaa".
3. `ler_data_hora_br(texto)` converte "dd/mm/aaaa hh:mm" em datetime.
4. `dia_da_semana(data)` devolve o nome do dia em português, em minúsculas e sem
   "-feira": "segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo".

Exemplos:
    >>> from datetime import date
    >>> ler_data_br(" 29/10/2026 ")
    datetime.date(2026, 10, 29)
    >>> formatar_data_br(date(2026, 3, 5))
    '05/03/2026'
    >>> ler_data_hora_br("29/10/2026 14:30")
    datetime.datetime(2026, 10, 29, 14, 30)
    >>> dia_da_semana(date(2026, 10, 29))
    'quinta'

Dica: datetime.strptime(texto, "%d/%m/%Y") devolve um datetime; o método .date()
pega só a data. Para o dia da semana, .weekday() devolve 0 (segunda) a 6 (domingo).
Não use "%A": ele depende do idioma do computador.

Teste com:  python curso.py testar 07 ex03
"""

from datetime import date, datetime


def ler_data_br(texto: str) -> date:
    """Converte 'dd/mm/aaaa' em date."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def formatar_data_br(data: date) -> str:
    """Converte date em 'dd/mm/aaaa'."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def ler_data_hora_br(texto: str) -> datetime:
    """Converte 'dd/mm/aaaa hh:mm' em datetime."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def dia_da_semana(data: date) -> str:
    """Nome do dia da semana em português ('segunda' ... 'domingo')."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
