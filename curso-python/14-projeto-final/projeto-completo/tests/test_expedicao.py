import pytest

from validador_certificados.expedicao import ler_email, ler_pasta_emails, separar_emails
from validador_certificados.modelos import PedidoInvalido


@pytest.mark.parametrize(
    ("texto", "op", "nf", "peso"),
    [
        ("OP: 24518\nNF: 123456\nPeso: 1.250,5 kg", "24518", "123456", 1250.5),
        ("Certificado da OP 24519.\nNF 123457 - peso 980,0 kg", "24519", "123457", 980.0),
        (
            "OP nº 24541\nNF-e nº 123.789\nPeso líquido: 2.310,75 kg",
            "24541",
            "123789",
            2310.75,
        ),
        ("OP: 24527\nNota fiscal: 123460\nPESO: 2.040 KG", "24527", "123460", 2040.0),
    ],
)
def test_formatos_aceitos(texto, op, nf, peso):
    pedido = ler_email(texto, origem="email.txt")
    assert (pedido.op, pedido.nf, pedido.origem) == (op, nf, "email.txt")
    assert pedido.peso_kg == pytest.approx(peso)


def test_lista_todos_os_problemas():
    with pytest.raises(PedidoInvalido) as erro:
        ler_email("A carga da OP 24555 (1.500 kg) está pronta. A NF sai amanhã.")
    assert str(erro.value) == "NF não encontrada; peso não encontrado"


def test_duas_ops_nunca_escolhe_uma():
    texto = "OP 24520 - 1.700 kg\nOP 24521 - 1.500 kg\nNF: 123805\nPeso: 3.200 kg"
    with pytest.raises(PedidoInvalido, match=r"mais de uma OP no e-mail \(24520, 24521\)"):
        ler_email(texto)


def test_separar_emails():
    pedidos, fora = separar_emails({"a.txt": "OP 24518 NF 1 Peso: 10 kg", "b.txt": "oi"})
    assert [p.origem for p in pedidos] == ["a.txt"]
    assert fora == {"b.txt": "OP não encontrada; NF não encontrada; peso não encontrado"}


def test_le_pasta_com_arquivo_cp1252(tmp_path):
    (tmp_path / "1.txt").write_text("OP 24518 NF 1 Peso: 10 kg", encoding="utf-8")
    (tmp_path / "2.txt").write_text("Expedição: OP 24519 NF 2 Peso: 5 kg", encoding="cp1252")
    (tmp_path / "ignorar.eml").write_text("não é .txt", encoding="utf-8")
    emails = ler_pasta_emails(tmp_path)
    assert list(emails) == ["1.txt", "2.txt"]
    assert emails["2.txt"].startswith("Expedição")


def test_emails_de_exemplo(pasta_dados):
    pedidos, fora = separar_emails(ler_pasta_emails(pasta_dados / "emails"))
    assert len(pedidos) == 6
    assert sorted(fora) == ["email_07_sem_nf.txt", "email_08_duas_ops.txt"]
