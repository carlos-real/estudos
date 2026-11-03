import importlib

import pytest

from validador_certificados.emissao import (
    EmissaoIndisponivel,
    Emissor,
    EmissorTotvs,
    ErroEmissao,
    emitir_fila,
)
from validador_certificados.modelos import ItemFila


def item(op="24518", nf="123456", situacao="emitir"):
    return ItemFila(op=op, nf=nf, peso_kg=100.0, situacao=situacao, especificacao="PADRAO-A")


class EmissorFalso(Emissor):
    """Emissor "real" de mentira: falha nas OPs pedidas."""

    def __init__(self, falhar_em=()):
        self.falhar_em = set(falhar_em)
        self.chamadas = []

    def emitir(self, item):
        self.chamadas.append(item.op)
        if item.op in self.falhar_em:
            raise ErroEmissao("tela travou")
        return f"CQ-{item.op}"


def test_ensaio_so_registra():
    emissor = EmissorTotvs()
    resultado = emitir_fila([item()], emissor)
    assert resultado[0].situacao == "ensaio"
    assert resultado[0].comprovante == "ENSAIO-24518-123456"
    assert emissor.registro == [
        "emitiria certificado: OP 24518 | NF 123456 | 100.00 kg | PADRAO-A"
    ]


def test_modo_real_ainda_indisponivel():
    with pytest.raises(EmissaoIndisponivel):
        EmissorTotvs(ensaio=False)


def test_falha_em_uma_op_nao_para_a_serie():
    emissor = EmissorFalso(falhar_em={"2"})
    resultado = emitir_fila([item("1"), item("2"), item("3")], emissor)
    assert [r.situacao for r in resultado] == ["emitido", "falha", "emitido"]
    assert resultado[1].motivos == ["falha na emissão: tela travou"]
    assert emissor.chamadas == ["1", "2", "3"]


def test_idempotencia_por_op_e_nf():
    emissor = EmissorFalso()
    ja_emitidas = {("1", "123456")}
    fila = [item("1"), item("2"), item("2"), item("2", nf="999")]
    resultado = emitir_fila(fila, emissor, ja_emitidas)
    assert [r.situacao for r in resultado] == ["ignorado", "emitido", "ignorado", "emitido"]
    assert emissor.chamadas == ["2", "2"]
    assert ja_emitidas == {("1", "123456")}, "não deve alterar o conjunto recebido"


def test_bug_no_emissor_sobe():
    class EmissorComBug(Emissor):
        def emitir(self, item):
            return item.nao_existe

    with pytest.raises(AttributeError):
        emitir_fila([item()], EmissorComBug())


def test_esqueleto_playwright_importa_sem_playwright():
    modulo = importlib.import_module("validador_certificados.robo_playwright")
    assert issubclass(modulo.EmissorTotvsPlaywright, Emissor)
