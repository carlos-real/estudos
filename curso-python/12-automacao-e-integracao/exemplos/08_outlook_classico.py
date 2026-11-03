"""Exemplo 08 — Ler a caixa de entrada do Outlook CLÁSSICO via win32com (só Windows).

ATENÇÃO:
- Funciona apenas no Windows, com o Outlook clássico (o "Outlook" do Office,
  aquele com Arquivo > Opções) instalado e aberto com a sua conta.
- NÃO funciona com o "Novo Outlook" (o app novo/web), que não tem a interface
  COM. Para ele, veja a seção sobre Microsoft Graph na aula.
- Precisa de:  pip install pywin32

Em outros sistemas (ou sem pywin32), o script só explica isso e termina.

Rode com:  python exemplos/08_outlook_classico.py
"""

import sys
from datetime import datetime, timedelta

PASTA_CAIXA_DE_ENTRADA = 6  # constante olFolderInbox do Outlook
CLASSE_EMAIL = 43  # constante olMail: ignora convites de reunião, recibos etc.


def pedidos_recentes(dias: int = 1, palavra: str = "certificado") -> list[dict]:
    """Devolve os e-mails dos últimos `dias` cujo assunto contém `palavra`."""
    import win32com.client  # importado aqui: só existe no Windows com pywin32

    outlook = win32com.client.Dispatch("Outlook.Application")
    caixa = outlook.GetNamespace("MAPI").GetDefaultFolder(PASTA_CAIXA_DE_ENTRADA)
    itens = caixa.Items
    itens.Sort("[ReceivedTime]", True)  # True = mais recentes primeiro

    # Restrict filtra no próprio Outlook (rápido). O formato da data segue o
    # Windows: em português é dd/mm/aaaa; num Windows em inglês, mm/dd/aaaa.
    desde = (datetime.now() - timedelta(days=dias)).strftime("%d/%m/%Y %H:%M")
    recentes = itens.Restrict(f"[ReceivedTime] >= '{desde}'")

    encontrados = []
    for msg in recentes:
        if msg.Class != CLASSE_EMAIL:
            continue
        if palavra.lower() not in msg.Subject.lower():
            continue
        encontrados.append(
            {
                "assunto": msg.Subject,
                "remetente": msg.SenderEmailAddress,  # veja o "Erro comum" na aula
                "recebido": msg.ReceivedTime,
                "corpo": msg.Body,  # texto puro; msg.HTMLBody tem o HTML
            }
        )
    return encontrados


def main() -> int:
    if sys.platform != "win32":
        print("Este exemplo só roda no Windows com o Outlook clássico.")
        print("Leia o código para entender a ideia; na aula há a alternativa com .eml.")
        return 0
    try:
        pedidos = pedidos_recentes(dias=2)
    except ImportError:
        print("Instale o pywin32 primeiro:  pip install pywin32")
        return 0
    for pedido in pedidos:
        print(pedido["recebido"], "|", pedido["assunto"])
    print(f"{len(pedidos)} e-mail(s) encontrados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
