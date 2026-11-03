"""Exemplo 06 — Montar um e-mail com anexo usando email.message (sem enviar).

Gera saida/certificado_123456.eml. Dê dois cliques nele no Windows: o Outlook
(ou outro leitor de e-mail) abre a mensagem pronta, com o anexo.

Rode com:  python exemplos/06_email_montar.py
"""

import mimetypes
from email.message import EmailMessage
from pathlib import Path

SAIDA = Path(__file__).resolve().parent / "saida"


def criar_pdf_de_mentira(caminho: Path) -> Path:
    """Só para o exemplo ter um anexo. Na vida real o PDF vem do ERP."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(b"%PDF-1.4\n% certificado de exemplo\n%%EOF\n")
    return caminho


def montar_email(op: str, nf: str, anexo: Path) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = "Laboratório de Qualidade <laboratorio@embalagens.example>"
    msg["To"] = "Expedição <expedicao@embalagens.example>"
    msg["Cc"] = "qualidade@embalagens.example"
    msg["Subject"] = f"Certificado de qualidade - OP {op} / NF {nf}"
    msg.set_content(
        f"Olá,\n\nSegue o certificado de qualidade da OP {op} (NF {nf}).\n\n"
        "Atenciosamente,\nLaboratório de Qualidade\n"
    )
    # Versão HTML opcional: leitores que entendem HTML mostram esta
    msg.add_alternative(
        f"<p>Olá,</p><p>Segue o certificado de qualidade da <b>OP {op}</b> (NF {nf}).</p>",
        subtype="html",
    )
    # Descobre o tipo do arquivo pela extensão: .pdf -> application/pdf
    tipo, _ = mimetypes.guess_type(anexo.name)
    principal, secundario = (tipo or "application/octet-stream").split("/")
    msg.add_attachment(
        anexo.read_bytes(), maintype=principal, subtype=secundario, filename=anexo.name
    )
    return msg


def main() -> None:
    pdf = criar_pdf_de_mentira(SAIDA / "certificado_123456.pdf")
    msg = montar_email("123456", "98765", pdf)

    print("Assunto:", msg["Subject"])
    print("Para:", msg["To"])
    print("Estrutura da mensagem:")
    for parte in msg.walk():
        nome = parte.get_filename() or ""
        print("  ", parte.get_content_type(), nome)

    texto = msg.get_body(preferencelist=("plain",)).get_content()
    print("Primeira linha do texto:", texto.splitlines()[0])
    anexos = [a.get_filename() for a in msg.iter_attachments()]
    print("Anexos:", anexos)

    destino = SAIDA / "certificado_123456.eml"
    destino.write_bytes(bytes(msg))  # bytes(msg) = o e-mail no formato padrão
    print("Salvo em:", destino.name)


if __name__ == "__main__":
    main()
