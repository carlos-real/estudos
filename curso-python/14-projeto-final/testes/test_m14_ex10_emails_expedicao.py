from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex10_emails_expedicao")

PASTA_EMAILS = Path(__file__).resolve().parent.parent / "dados" / "emails"


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [("1.250,5", 1250.5), ("2.040", 2040.0), ("980,0", 980.0), (" 15 ", 15.0)],
)
def test_numero_br(texto, esperado):
    assert ex.numero_br(texto) == pytest.approx(esperado)


@pytest.mark.parametrize(
    ("texto", "op", "nf", "peso"),
    [
        ("OP: 24518\nNF: 123456\nPeso: 1.250,5 kg", "24518", "123456", 1250.5),
        ("Certificado da OP 24519.\nNF 123457 - peso 980,0 kg", "24519", "123457", 980.0),
        ("OP nº 24541\nNF-e nº 123.789\nPeso líquido: 2.310,75 kg", "24541", "123789",
         2310.75),
        ("op: 24527\nNota fiscal: 123460.\nPESO: 2.040 KG", "24527", "123460", 2040.0),
    ],
)  # fmt: skip
def test_formatos_aceitos(texto, op, nf, peso):
    pedido = ex.ler_email(texto, origem="email.txt")
    assert isinstance(pedido, ex.Pedido)
    assert (pedido.op, pedido.nf, pedido.origem) == (op, nf, "email.txt")
    assert pedido.peso_kg == pytest.approx(peso)


def test_valor_repetido_conta_uma_vez():
    texto = "Assunto: Certificado OP 24518\n\nOP: 24518\nNF: 1\nPeso: 1.500 kg\npeso 1500 kg"
    pedido = ex.ler_email(texto)
    assert (pedido.op, pedido.peso_kg) == ("24518", 1500.0)


def test_junta_todos_os_problemas_em_ordem():
    with pytest.raises(ex.PedidoInvalido) as erro:
        ex.ler_email("A carga da OP 24555 (1.500 kg) está pronta. A NF sai amanhã.")
    assert str(erro.value) == "NF não encontrada; peso não encontrado"


def test_email_sem_nada():
    with pytest.raises(ex.PedidoInvalido) as erro:
        ex.ler_email("Bom dia!")
    assert str(erro.value) == "OP não encontrada; NF não encontrada; peso não encontrado"


def test_duas_ops_nunca_escolhe_uma():
    texto = "OP 24521 - 1.500 kg\nOP 24520 - 1.700 kg\nNF: 123805\nPeso: 3.200 kg"
    with pytest.raises(ex.PedidoInvalido) as erro:
        ex.ler_email(texto)
    assert str(erro.value) == "mais de uma OP no e-mail (24520, 24521)"


def test_duas_nfs_e_dois_pesos():
    texto = "OP 24518\nNF 2\nNF 1\nPeso: 1.700 kg\nPeso: 1.500 kg"
    with pytest.raises(ex.PedidoInvalido) as erro:
        ex.ler_email(texto)
    assert str(erro.value) == (
        "mais de uma NF no e-mail (1, 2); mais de um peso no e-mail (1500, 1700)"
    )


def test_peso_zero():
    with pytest.raises(ex.PedidoInvalido, match="peso deve ser maior que zero"):
        ex.ler_email("OP 24518 NF 1 Peso: 0 kg")


def test_separar_emails():
    emails = {
        "a.txt": "OP 24518 NF 1 Peso: 10 kg",
        "b.txt": "Bom dia",
        "c.txt": "OP 24519 NF 2 Peso: 5,5 kg",
    }
    pedidos, fora = ex.separar_emails(emails)
    assert [(p.op, p.origem) for p in pedidos] == [("24518", "a.txt"), ("24519", "c.txt")]
    assert fora == {"b.txt": "OP não encontrada; NF não encontrada; peso não encontrado"}


def test_emails_de_exemplo_do_modulo():
    emails = {}
    for arquivo in sorted(PASTA_EMAILS.glob("*.txt")):
        try:
            emails[arquivo.name] = arquivo.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            emails[arquivo.name] = arquivo.read_text(encoding="cp1252")
    pedidos, fora = ex.separar_emails(emails)
    assert [p.op for p in pedidos] == ["24518", "24519", "24527", "24541", "24546", "24533"]
    assert sorted(fora) == ["email_07_sem_nf.txt", "email_08_duas_ops.txt"]
