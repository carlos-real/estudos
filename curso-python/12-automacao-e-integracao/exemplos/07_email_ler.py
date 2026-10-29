"""Exemplo 07 — Ler arquivos .eml (e-mails salvos) com o módulo email.

Lê os pedidos da expedição em dados/emails/ e mostra remetente, data,
assunto, o tipo do corpo e a OP encontrada no texto.

Rode com:  python exemplos/07_email_ler.py
"""

import re
from email import policy
from email.parser import BytesParser
from email.utils import parseaddr, parsedate_to_datetime
from pathlib import Path

PASTA_EMAILS = Path(__file__).resolve().parent.parent / "dados" / "emails"


def ler_eml(caminho: Path):
    # policy.default = API moderna: decodifica acentos e devolve objetos fáceis
    return BytesParser(policy=policy.default).parsebytes(caminho.read_bytes())


def main() -> None:
    for caminho in sorted(PASTA_EMAILS.glob("*.eml")):
        msg = ler_eml(caminho)
        nome, endereco = parseaddr(msg["From"])
        quando = parsedate_to_datetime(msg["Date"])
        corpo = msg.get_body(preferencelist=("plain", "html"))
        texto = corpo.get_content()
        op = re.search(r"OP:?\s*(?:<b>)?(\d{6})", texto)

        print(caminho.name)
        print("   de:", endereco, "| em:", quando.strftime("%d/%m/%Y %H:%M"))
        print("   assunto:", msg["Subject"])
        print("   corpo:", corpo.get_content_type(), "| OP:", op.group(1) if op else "?")


if __name__ == "__main__":
    main()
