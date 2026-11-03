"""
Exercício 12.10 — Montar o e-mail do certificado (sem enviar)
Nível: ★★☆

Contexto: depois de emitir o certificado, o laboratório responde à expedição
com o PDF anexado. Montar a mensagem em Python permite salvá-la como .eml
(para conferir no Outlook) ou entregá-la a um servidor SMTP depois.

Tarefa: implemente montar_email_certificado(remetente, destinatarios, op, nf, anexo=None).
- Devolva um email.message.EmailMessage com:
  - From = remetente
  - To = os destinatários separados por ", "
  - Subject = "Certificado de qualidade - OP <op> / NF <nf>"
  - corpo em texto puro EXATAMENTE assim (com quebra de linha no fim):
        Olá,

        Segue o certificado de qualidade referente à OP <op> (NF <nf>).

        Atenciosamente,
        Laboratório de Qualidade
- Se `anexo` (um Path) for informado, anexe o conteúdo do arquivo com o nome
  original (filename) e o tipo descoberto por mimetypes.guess_type
  (.pdf -> application/pdf). Tipo desconhecido -> application/octet-stream.
- Lista de destinatários vazia -> ValueError.
- A função NÃO envia nada.

Exemplos:
    >>> msg = montar_email_certificado("lab@x.example", ["exp@x.example"], "123456", "98765")
    >>> msg["Subject"]
    'Certificado de qualidade - OP 123456 / NF 98765'

Dica: msg.set_content(texto) para o corpo; msg.add_attachment(bytes,
maintype=..., subtype=..., filename=...) para o anexo.

Teste com:  python curso.py testar 12 ex10
"""

from email.message import EmailMessage
from pathlib import Path


def montar_email_certificado(
    remetente: str, destinatarios: list[str], op: str, nf: str, anexo: Path | None = None
) -> EmailMessage:
    """Monta (sem enviar) o e-mail com o certificado da OP."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
