from email import policy
from email.message import EmailMessage
from email.parser import BytesParser

import pytest

from _curso import carregar

ex = carregar(__file__, "ex10_montar_email")

REMETENTE = "Laboratório <laboratorio@embalagens.example>"
DESTINOS = ["expedicao@embalagens.example", "faturamento@embalagens.example"]
CORPO = (
    "Olá,\n\nSegue o certificado de qualidade referente à OP 123456 (NF 98765).\n\n"
    "Atenciosamente,\nLaboratório de Qualidade\n"
)


def test_cabecalhos():
    msg = ex.montar_email_certificado(REMETENTE, DESTINOS, "123456", "98765")
    assert isinstance(msg, EmailMessage)
    assert msg["From"] == REMETENTE
    assert msg["To"] == "expedicao@embalagens.example, faturamento@embalagens.example"
    assert msg["Subject"] == "Certificado de qualidade - OP 123456 / NF 98765"


def test_corpo_em_texto_puro():
    msg = ex.montar_email_certificado(REMETENTE, DESTINOS[:1], "123456", "98765")
    assert msg.get_content_type() == "text/plain"
    assert msg.get_content() == CORPO


def test_anexo_pdf(tmp_path):
    pdf = tmp_path / "certificado_123456.pdf"
    pdf.write_bytes(b"%PDF-1.4 conteudo")
    msg = ex.montar_email_certificado(REMETENTE, DESTINOS, "123456", "98765", anexo=pdf)

    assert msg.get_body(preferencelist=("plain",)).get_content() == CORPO
    anexos = list(msg.iter_attachments())
    assert len(anexos) == 1
    assert anexos[0].get_filename() == "certificado_123456.pdf"
    assert anexos[0].get_content_type() == "application/pdf"
    assert anexos[0].get_content() == b"%PDF-1.4 conteudo"


def test_anexo_de_tipo_desconhecido(tmp_path):
    arquivo = tmp_path / "medicoes.lab42"
    arquivo.write_bytes(b"\x00\x01")
    msg = ex.montar_email_certificado(REMETENTE, DESTINOS, "1", "2", anexo=arquivo)
    anexo = next(msg.iter_attachments())
    assert anexo.get_content_type() == "application/octet-stream"
    assert anexo.get_filename() == "medicoes.lab42"


def test_sobrevive_ida_e_volta_em_bytes(tmp_path):
    pdf = tmp_path / "cert.pdf"
    pdf.write_bytes(b"%PDF")
    msg = ex.montar_email_certificado(REMETENTE, DESTINOS, "124001", "98770", anexo=pdf)
    relido = BytesParser(policy=policy.default).parsebytes(bytes(msg))
    assert relido["Subject"] == "Certificado de qualidade - OP 124001 / NF 98770"
    assert relido["From"] == REMETENTE


def test_sem_destinatarios():
    with pytest.raises(ValueError):
        ex.montar_email_certificado(REMETENTE, [], "123456", "98765")
