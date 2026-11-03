"""
Exercício 12.14 — Revisão: resumo diário dos pedidos por e-mail (SOLUÇÃO)

Decomposição em três perguntas:
1. De cada e-mail, o que eu preciso? (data, peso) -> função extrair()
2. Como acumular por dia? -> dicionário de acumuladores (módulos 03 e 07)
3. Como apresentar? -> sorted + f-string + formato brasileiro (módulo 05)
"""

import re
from collections import defaultdict
from datetime import date
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime

RE_PESO = re.compile(r"\bpeso\s*:?\s*([\d.]+(?:,\d+)?)\s*kg", re.IGNORECASE)


def numero_br(texto: str) -> float:
    return float(texto.replace(".", "").replace(",", "."))


def formatar_br(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")


def extrair(conteudo: bytes) -> tuple[date, float] | None:
    """(data, peso) do e-mail, ou None se ele não tiver peso no texto puro."""
    msg = BytesParser(policy=policy.default).parsebytes(conteudo)
    corpo = msg.get_body(preferencelist=("plain",))
    if corpo is None:
        return None
    achado = RE_PESO.search(corpo.get_content())
    if achado is None:
        return None
    # parsedate_to_datetime entende "Mon, 09 Mar 2026 08:12:00 -0300" e devolve
    # um datetime COM fuso. .date() pega o dia como está escrito no cabeçalho.
    quando = parsedate_to_datetime(msg["Date"]).date()
    return quando, numero_br(achado.group(1))


def resumir_por_dia(emails: list[bytes]) -> list[str]:
    """Uma linha por dia: data, quantidade de pedidos e peso total."""
    quantidade: defaultdict[date, int] = defaultdict(int)
    peso_total: defaultdict[date, float] = defaultdict(float)

    for conteudo in emails:
        extraido = extrair(conteudo)
        if extraido is None:
            continue  # sem peso: não entra no resumo
        dia, peso = extraido
        quantidade[dia] += 1
        peso_total[dia] += peso

    linhas = []
    for dia in sorted(quantidade):  # date ordena do mais antigo ao mais novo
        n = quantidade[dia]
        palavra = "pedido" if n == 1 else "pedidos"
        linhas.append(f"{dia:%d/%m/%Y}: {n} {palavra}, {formatar_br(peso_total[dia])} kg")
    return linhas
    # Alternativa com pandas (módulo 10), útil quando são milhares de e-mails:
    # monte um DataFrame com colunas "dia" e "peso" e faça
    #     df.groupby("dia")["peso"].agg(["count", "sum"])
