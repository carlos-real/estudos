"""
Exercício 12.10 — Montar o e-mail do certificado (SOLUÇÃO)
"""

import mimetypes
from email.message import EmailMessage
from pathlib import Path

MODELO_CORPO = (
    "Olá,\n"
    "\n"
    "Segue o certificado de qualidade referente à OP {op} (NF {nf}).\n"
    "\n"
    "Atenciosamente,\n"
    "Laboratório de Qualidade\n"
)


def montar_email_certificado(
    remetente: str, destinatarios: list[str], op: str, nf: str, anexo: Path | None = None
) -> EmailMessage:
    """Monta (sem enviar) o e-mail com o certificado da OP."""
    if not destinatarios:
        raise ValueError("Informe pelo menos um destinatário")

    msg = EmailMessage()
    # Os cabeçalhos funcionam como um dicionário. Acentos são codificados
    # automaticamente no padrão dos e-mails (aquele "=?utf-8?...").
    msg["From"] = remetente
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = f"Certificado de qualidade - OP {op} / NF {nf}"
    msg.set_content(MODELO_CORPO.format(op=op, nf=nf))

    if anexo is not None:
        # guess_type olha só a EXTENSÃO e devolve (tipo, codificação).
        tipo, _ = mimetypes.guess_type(anexo.name)
        if tipo is None:
            tipo = "application/octet-stream"  # "bytes quaisquer"
        principal, secundario = tipo.split("/", 1)
        msg.add_attachment(
            anexo.read_bytes(),  # anexos são bytes, não texto
            maintype=principal,
            subtype=secundario,
            filename=anexo.name,
        )
        # Ao anexar, a mensagem vira multipart/mixed sozinha: o texto vira a
        # primeira parte e o arquivo, a segunda. Não precisamos montar isso.
    return msg

    # Para ENVIAR de verdade (quando a TI liberar um servidor SMTP):
    #     import smtplib
    #     with smtplib.SMTP("smtp.empresa.example", 587, timeout=30) as smtp:
    #         smtp.starttls()
    #         smtp.login(usuario, senha)  # senha vinda de variável de ambiente!
    #         smtp.send_message(msg)
