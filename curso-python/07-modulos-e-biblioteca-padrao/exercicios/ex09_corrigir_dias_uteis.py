"""
Exercício 07.09 — Leitura de código: o prazo que caía no sábado
Nível: ★★☆

Contexto: Um colega escreveu funções para calcular o prazo de emissão do certificado
(N dias úteis depois da NF). O sistema marcou um prazo para um SÁBADO. Seu trabalho:
ler o código, prever o que ele faz e corrigir os defeitos.

Código do colega (com 3 defeitos):

    from datetime import date, timedelta

    def eh_dia_util(dia, feriados=set()):
        return dia.weekday() <= 5 and dia not in feriados

    def somar_dias_uteis(inicio, dias, feriados=set()):
        atual = inicio
        contados = 0
        while contados < dias:
            if eh_dia_util(atual, feriados):
                contados += 1
            atual = atual + timedelta(days=1)
        return atual

    def dias_uteis_entre(inicio, fim, feriados=set()):
        total = 0
        atual = inicio
        while atual <= fim:
            if eh_dia_util(atual, feriados):
                total += 1
            atual = atual + timedelta(days=1)
        return total

Regras CORRETAS:
- Dia útil: segunda a sexta (weekday() de 0 a 4) e fora da lista de feriados.
- somar_dias_uteis(inicio, dias, feriados): o próprio dia `inicio` NÃO conta. Ande
  um dia de cada vez e conte só os dias úteis até completar `dias`. Com dias=0,
  devolva o próprio `inicio`.
- dias_uteis_entre(inicio, fim, feriados): quantos dias úteis existem DEPOIS de
  `inicio` até `fim` (inclusive). Se fim <= inicio, devolva 0.
- `feriados` pode ser None (sem feriados). Troque o default `set()` por None: default
  mutável é uma armadilha (módulo 04), mesmo quando não causa erro aqui.

Tarefa:
1. ANTES de corrigir, preveja: o que a versão do colega devolve para
   `somar_dias_uteis(date(2026, 10, 29), 2)`? (29/10/2026 é uma quinta.) Escreva sua
   previsão como retorno de `previsao_versao_com_defeito()`. Depois rode o código do
   colega para conferir (PRIMM: preveja, rode, investigue).
2. Copie as três funções para baixo, corrija os defeitos e mantenha as assinaturas.

Exemplos (versão corrigida):
    >>> from datetime import date
    >>> eh_dia_util(date(2026, 10, 31))  # sábado
    False
    >>> somar_dias_uteis(date(2026, 10, 29), 2)
    datetime.date(2026, 11, 2)
    >>> somar_dias_uteis(date(2026, 10, 29), 2, {date(2026, 11, 2)})  # Finados
    datetime.date(2026, 11, 3)
    >>> dias_uteis_entre(date(2026, 10, 29), date(2026, 11, 5))
    5

Teste com:  python curso.py testar 07 ex09
"""

from datetime import date


def previsao_versao_com_defeito() -> date:
    """Sua previsão para somar_dias_uteis(date(2026, 10, 29), 2) na versão com defeito."""
    # Escreva seu código aqui (devolva a data que você prevê, ex.: date(2026, 1, 1))
    raise NotImplementedError("Implemente esta função")


def eh_dia_util(dia: date, feriados: set[date] | None = None) -> bool:
    """True se `dia` for de segunda a sexta e não for feriado."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def somar_dias_uteis(inicio: date, dias: int, feriados: set[date] | None = None) -> date:
    """Data que fica `dias` dias úteis depois de `inicio`."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def dias_uteis_entre(inicio: date, fim: date, feriados: set[date] | None = None) -> int:
    """Quantidade de dias úteis em (inicio, fim]."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
