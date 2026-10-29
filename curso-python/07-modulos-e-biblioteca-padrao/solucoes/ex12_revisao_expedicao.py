"""
Exercício 07.12 — Revisão: o e-mail da expedição com datas e agrupamento
Nível: ★★★

Revisão de: módulo 05 (regex e números brasileiros), módulo 03 (listas, tuplas e
dicionários) e módulo 04 (funções pequenas que se reaproveitam), junto com datetime
e defaultdict deste módulo.

Contexto: A expedição manda um e-mail assim:

    Bom dia! Segue a programação.
    Data de embarque: 05/11/2026
    OP 245101 - NF 123456 - Peso: 1.250,5 kg
    op 245102 - nf 123456 - peso: 980,00 kg
    OP 245107 - NF 123460 - Peso: 2.010,75 kg
    Att., Expedição

Os certificados precisam estar prontos ANTES do embarque.

Tarefa:
1. `extrair_itens(texto)` devolve uma lista de tuplas (op, nf, peso_kg), na ordem do
   e-mail: op no formato "OP245101" (sempre "OP" maiúsculo + dígitos), nf só com os
   dígitos ("123456") e peso como float (o texto usa formato brasileiro: "1.250,5").
   Não diferencie maiúsculas/minúsculas e aceite espaços variados em volta do "-".
2. `extrair_data_embarque(texto)` devolve a date de "Data de embarque: dd/mm/aaaa"
   (sem diferenciar maiúsculas) ou None se não houver.
3. `prazo_certificado(texto, dias_antes=2)` devolve a data limite para emitir os
   certificados: embarque − dias_antes dias corridos. Se cair num sábado ou domingo,
   recue até a sexta-feira anterior. Sem data de embarque, devolva None.
4. `total_por_nf(texto)` devolve {nf: peso total} (round(..., 2)), na ordem em que as
   NFs aparecem.

Exemplos (com o e-mail acima na variável `email`):
    extrair_itens(email)[1]        -> ("OP245102", "123456", 980.0)
    extrair_data_embarque(email)   -> date(2026, 11, 5)
    prazo_certificado(email)       -> date(2026, 11, 3)
    prazo_certificado(email, 4)    -> date(2026, 10, 30)   (01/11 é domingo)
    total_por_nf(email)            -> {"123456": 2230.5, "123460": 2010.75}

Dica: monte o padrão do item aos poucos, testando no REPL (como no módulo 05).
re.findall com 3 grupos devolve uma lista de tuplas de 3 textos.

Teste com:  python curso.py testar 07 ex12
"""

import re
from collections import defaultdict
from datetime import date, datetime, timedelta

# Padrões compilados uma vez (módulo 05). \s* aceita espaços variados; [\d.,]+ pega
# o número brasileiro inteiro ("2.010,75"); re.IGNORECASE aceita "op", "Nf", "PESO".
PADRAO_ITEM = re.compile(
    r"OP\s*(\d+)\s*-\s*NF\s*(\d+)\s*-\s*Peso\s*:?\s*([\d.,]+)\s*kg", re.IGNORECASE
)
PADRAO_EMBARQUE = re.compile(r"embarque\s*:\s*(\d{2}/\d{2}/\d{4})", re.IGNORECASE)


def numero_br(texto: str) -> float:
    """'1.250,5' -> 1250.5 (tira o ponto de milhar, troca a vírgula por ponto)."""
    return float(texto.replace(".", "").replace(",", "."))


def extrair_itens(texto: str) -> list[tuple[str, str, float]]:
    """Itens (op, nf, peso_kg) do e-mail, na ordem."""
    return [(f"OP{op}", nf, numero_br(peso)) for op, nf, peso in PADRAO_ITEM.findall(texto)]


def extrair_data_embarque(texto: str) -> date | None:
    """Data de embarque do e-mail, ou None."""
    achado = PADRAO_EMBARQUE.search(texto)
    if achado is None:  # retorno antecipado (módulo 04)
        return None
    return datetime.strptime(achado.group(1), "%d/%m/%Y").date()


def prazo_certificado(texto: str, dias_antes: int = 2) -> date | None:
    """Data limite para emitir os certificados (nunca em fim de semana)."""
    embarque = extrair_data_embarque(texto)
    if embarque is None:
        return None
    prazo = embarque - timedelta(days=dias_antes)
    # weekday(): 5 = sábado, 6 = domingo. Recua um dia por vez até cair num dia útil.
    while prazo.weekday() >= 5:
        prazo -= timedelta(days=1)
    return prazo


def total_por_nf(texto: str) -> dict[str, float]:
    """Peso total de cada NF, na ordem em que aparecem."""
    totais = defaultdict(float)
    for _op, nf, peso in extrair_itens(texto):  # reaproveita a função 1
        totais[nf] += peso
    return {nf: round(total, 2) for nf, total in totais.items()}
