from email.message import EmailMessage
from pathlib import Path

from _curso import carregar

ex = carregar(__file__, "ex14_revisao_resumo_por_dia")

PASTA_EMAILS = Path(__file__).resolve().parent.parent / "dados" / "emails"


def eml(data, corpo, html=False):
    msg = EmailMessage()
    msg["From"] = "expedicao@embalagens.example"
    msg["Subject"] = "Pedido de certificado"
    msg["Date"] = data
    msg.set_content(corpo, subtype="html" if html else "plain")
    return bytes(msg)


SEG_8H = "Mon, 09 Mar 2026 08:12:00 -0300"
SEG_15H = "Mon, 09 Mar 2026 15:40:00 -0300"
TER_9H = "Tue, 10 Mar 2026 09:00:00 -0300"


def test_agrupa_por_dia_em_ordem():
    emails = [
        eml(TER_9H, "OP: 124001\nNF: 98770\nPeso: 2.310,0 kg"),
        eml(SEG_8H, "OP: 123456\nNF: 98765\nPeso: 1.250,5 kg"),
        eml(SEG_15H, "OP: 123789\nNF: 98766\nPeso: 980,25 kg"),
    ]
    assert ex.resumir_por_dia(emails) == [
        "09/03/2026: 2 pedidos, 2.230,75 kg",
        "10/03/2026: 1 pedido, 2.310,00 kg",
    ]


def test_ignora_emails_sem_peso_ou_sem_texto_puro():
    emails = [
        eml(SEG_8H, "OP: 123456\nPeso: 640 kg"),
        eml(SEG_8H, "OP: 123457\nPeso: a confirmar"),
        eml(SEG_8H, "<p>Peso: 999 kg</p>", html=True),
    ]
    assert ex.resumir_por_dia(emails) == ["09/03/2026: 1 pedido, 640,00 kg"]


def test_peso_em_minusculas_e_sem_dois_pontos():
    emails = [eml(SEG_8H, "peso 1.000 kg"), eml(SEG_15H, "PESO: 12.345,678 kg")]
    assert ex.resumir_por_dia(emails) == ["09/03/2026: 2 pedidos, 13.345,68 kg"]


def test_usa_a_data_do_fuso_do_cabecalho():
    # 23h30 em Brasília (-0300) já é dia 10 em UTC, mas o resumo é do dia 9.
    emails = [eml("Mon, 09 Mar 2026 23:30:00 -0300", "Peso: 100 kg")]
    assert ex.resumir_por_dia(emails) == ["09/03/2026: 1 pedido, 100,00 kg"]


def test_sem_emails():
    assert ex.resumir_por_dia([]) == []


def test_arquivos_de_exemplo_do_modulo():
    emails = [caminho.read_bytes() for caminho in sorted(PASTA_EMAILS.glob("*.eml"))]
    # pedido_003 só tem HTML e é ignorado; 001, 002 e 004 são do dia 09/03.
    assert ex.resumir_por_dia(emails) == [
        "09/03/2026: 3 pedidos, 2.870,75 kg",
        "10/03/2026: 1 pedido, 500,00 kg",
    ]
