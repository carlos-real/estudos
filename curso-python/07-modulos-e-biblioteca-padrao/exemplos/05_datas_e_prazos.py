"""Datas e prazos com datetime: validade de laudo e dias úteis.

Rode com:  python exemplos/05_datas_e_prazos.py
"""

from datetime import date, datetime, timedelta

DIAS_DA_SEMANA = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]

# --- Criar e formatar -------------------------------------------------------
emissao = date(2026, 10, 29)
print("Emissão:", emissao.strftime("%d/%m/%Y"), "-", DIAS_DA_SEMANA[emissao.weekday()])

# --- Ler texto no formato brasileiro ---------------------------------------
coleta = datetime.strptime("28/10/2026 14:30", "%d/%m/%Y %H:%M")
print("Coleta:", coleta)

# --- Validade do laudo: 180 dias -------------------------------------------
vencimento = emissao + timedelta(days=180)
print("Vence em:", f"{vencimento:%d/%m/%Y}")

hoje = date(2027, 4, 20)  # fixo para o exemplo ser reproduzível; no dia a dia: date.today()
restam = (vencimento - hoje).days
print("Dias até vencer (em 20/04/2027):", restam)
print("Laudo válido?", hoje <= vencimento)


# --- Prazo em dias úteis ----------------------------------------------------
def somar_dias_uteis(inicio: date, dias: int, feriados: set[date] | None = None) -> date:
    """Anda `dias` dias úteis a partir de `inicio` (o próprio início não conta)."""
    feriados = feriados or set()
    atual = inicio
    contados = 0
    while contados < dias:
        atual += timedelta(days=1)
        if atual.weekday() < 5 and atual not in feriados:
            contados += 1
    return atual


nf_emitida = date(2026, 10, 29)  # quinta-feira
feriados_2026 = {date(2026, 11, 2), date(2026, 11, 15), date(2026, 11, 20)}
prazo = somar_dias_uteis(nf_emitida, 5, feriados_2026)
print("Certificado até:", f"{prazo:%d/%m/%Y}", "-", DIAS_DA_SEMANA[prazo.weekday()])

# --- Diferença entre dois instantes ----------------------------------------
inicio_ensaio = datetime(2026, 10, 29, 8, 15)
fim_ensaio = datetime(2026, 10, 29, 11, 40)
duracao = fim_ensaio - inicio_ensaio
print("Duração do ensaio:", duracao, "=", duracao.total_seconds() / 60, "minutos")
