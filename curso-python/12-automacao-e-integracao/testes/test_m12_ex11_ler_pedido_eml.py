from email.message import EmailMessage
from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex11_ler_pedido_eml")

PASTA_EMAILS = Path(__file__).resolve().parent.parent / "dados" / "emails"


def eml(corpo, assunto="Pedido de certificado", html=False, alternativa_html=None):
    """Monta um e-mail de teste e devolve os bytes (como um .eml salvo)."""
    msg = EmailMessage()
    msg["From"] = "Carla Souza - Expedição <expedicao@embalagens.example>"
    msg["To"] = "laboratorio@embalagens.example"
    msg["Subject"] = assunto
    msg.set_content(corpo, subtype="html" if html else "plain")
    if alternativa_html:
        msg.add_alternative(alternativa_html, subtype="html")
    return bytes(msg)


def test_texto_puro():
    conteudo = eml("Bom dia!\nOP: 123456\nNF: 98765\nPeso: 1.250,5 kg\nObrigada")
    assert ex.ler_pedido(conteudo) == {
        "remetente": "expedicao@embalagens.example",
        "assunto": "Pedido de certificado",
        "op": "123456",
        "nf": "98765",
        "peso_kg": pytest.approx(1250.5),
    }


def test_assunto_com_acentos_e_travessao():
    conteudo = eml(
        "OP 123789 NF 98766 Peso 980,25 kg", assunto="Certificado urgente — OP 123789"
    )
    pedido = ex.ler_pedido(conteudo)
    assert pedido["assunto"] == "Certificado urgente — OP 123789"
    assert pedido["peso_kg"] == pytest.approx(980.25)


def test_minusculas_e_sem_dois_pontos():
    pedido = ex.ler_pedido(eml("op 124050\nnf 1234\npeso 640 kg"))
    assert (pedido["op"], pedido["nf"], pedido["peso_kg"]) == ("124050", "1234", 640.0)


def test_corpo_somente_html():
    html = "<p>OP:<b>124001</b><br>NF:<b>98770</b><br>Peso:<b>2.310,0 kg</b></p>"
    pedido = ex.ler_pedido(eml(html, html=True))
    assert pedido["op"] == "124001"
    assert pedido["nf"] == "98770"
    assert pedido["peso_kg"] == pytest.approx(2310.0)


def test_prefere_texto_puro_quando_ha_os_dois():
    conteudo = eml(
        "OP: 111111\nNF: 1\nPeso: 10 kg",
        alternativa_html="<p>OP: 222222 NF: 2 Peso: 20 kg</p>",
    )
    assert ex.ler_pedido(conteudo)["op"] == "111111"


@pytest.mark.parametrize(
    ("corpo", "campo"),
    [
        ("NF: 98765\nPeso: 10 kg", "OP"),
        ("OP: 12345\nNF: 98765\nPeso: 10 kg", "OP"),  # só 5 dígitos
        ("OP: 123456\nNF: a confirmar\nPeso: 10 kg", "NF"),
        ("OP: 123456\nNF: 98765", "peso"),
    ],
)
def test_campo_faltando(corpo, campo):
    with pytest.raises(ValueError, match=f"Campo não encontrado: {campo}"):
        ex.ler_pedido(eml(corpo))


def test_arquivos_de_exemplo_do_modulo():
    pedido = ex.ler_pedido((PASTA_EMAILS / "pedido_003.eml").read_bytes())
    assert (pedido["op"], pedido["nf"]) == ("124001", "98770")
    with pytest.raises(ValueError, match="NF"):
        ex.ler_pedido((PASTA_EMAILS / "pedido_004.eml").read_bytes())
