import pytest

from _curso import carregar

ex = carregar(__file__, "ex12_emissor_ensaio")


def item(op="24518", nf="123456", situacao="emitir", peso=1250.5):
    return ex.ItemFila(op=op, nf=nf, peso_kg=peso, situacao=situacao, especificacao="PADRAO-A")


class EmissorFalso(ex.Emissor):
    """Emissor "real" de mentira: anota as chamadas e falha nas OPs pedidas."""

    def __init__(self, falhar_em=()):
        self.falhar_em = set(falhar_em)
        self.chamadas = []

    def emitir(self, item):
        self.chamadas.append((item.op, item.nf))
        if item.op in self.falhar_em:
            raise ex.ErroEmissao("tela não respondeu")
        return f"CQ-{item.op}"


class BugNoRobo(Exception):
    """Exceção que NÃO é ErroEmissao: representa um bug."""


def test_emissor_totvs_registra_o_que_faria():
    emissor = ex.EmissorTotvs()
    assert emissor.ensaio is True
    assert emissor.registro == []
    comprovante = emissor.emitir(item())
    assert comprovante == "ENSAIO-24518-123456"
    assert emissor.registro == [
        "emitiria certificado: OP 24518 | NF 123456 | 1250.50 kg | PADRAO-A"
    ]


def test_modo_real_indisponivel():
    with pytest.raises(ex.EmissaoIndisponivel):
        ex.EmissorTotvs(ensaio=False)


def test_emitir_fila_em_ensaio():
    emissor = ex.EmissorTotvs()
    resultado = ex.emitir_fila([item(), item("24541", "123789")], emissor)
    assert [(r.op, r.situacao, r.comprovante) for r in resultado] == [
        ("24518", "ensaio", "ENSAIO-24518-123456"),
        ("24541", "ensaio", "ENSAIO-24541-123789"),
    ]
    assert len(emissor.registro) == 2


def test_emissor_real_marca_emitido():
    resultado = ex.emitir_fila([item()], EmissorFalso())
    assert (resultado[0].situacao, resultado[0].comprovante) == ("emitido", "CQ-24518")


def test_falha_em_uma_op_nao_para_a_serie():
    emissor = EmissorFalso(falhar_em={"2"})
    resultado = ex.emitir_fila([item("1"), item("2"), item("3")], emissor)
    assert [r.situacao for r in resultado] == ["emitido", "falha", "emitido"]
    assert resultado[1].motivos == ["falha na emissão: tela não respondeu"]
    assert resultado[1].comprovante == ""
    assert [op for op, _ in emissor.chamadas] == ["1", "2", "3"]


def test_idempotencia_por_op_e_nf():
    emissor = EmissorFalso()
    ja_emitidas = {("1", "123456")}
    fila = [item("1"), item("2"), item("2"), item("2", nf="999")]
    resultado = ex.emitir_fila(fila, emissor, ja_emitidas)
    assert [r.situacao for r in resultado] == ["ignorado", "emitido", "ignorado", "emitido"]
    assert resultado[0].motivos == ["certificado já emitido para esta OP/NF"]
    assert emissor.chamadas == [("2", "123456"), ("2", "999")]
    assert ja_emitidas == {("1", "123456")}, "não altere o conjunto recebido"


def test_falha_nao_conta_como_emitido():
    emissor = EmissorFalso(falhar_em={"2"})
    resultado = ex.emitir_fila([item("2"), item("2")], emissor)
    assert [r.situacao for r in resultado] == ["falha", "falha"], (
        "Se a 1ª tentativa falhou, a OP/NF não foi emitida: a 2ª deve tentar de novo."
    )


def test_item_que_nao_e_emitir_volta_igual():
    bloqueado = item(situacao="bloqueado")
    emissor = EmissorFalso()
    assert ex.emitir_fila([bloqueado], emissor) == [bloqueado]
    assert emissor.chamadas == []


def test_nao_altera_os_itens_recebidos():
    original = item()
    ex.emitir_fila([original], EmissorFalso())
    assert (original.situacao, original.comprovante) == ("emitir", "")


def test_bug_no_emissor_sobe():
    class EmissorComBug(ex.Emissor):
        def emitir(self, item):
            raise BugNoRobo("seletor errado")

    with pytest.raises(BugNoRobo):
        ex.emitir_fila([item()], EmissorComBug())
