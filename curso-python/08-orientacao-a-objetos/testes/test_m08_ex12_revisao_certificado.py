import dataclasses
from datetime import date

import pytest

from _curso import carregar

ex = carregar(__file__, "ex12_revisao_certificado")
R = ex.ResultadoEnsaio
EMISSAO = date(2026, 10, 29)
APROVADOS = [R("espessura", 25.1, "µm", True), R("cof", 0.22, "", True)]


def criar(**mudancas):
    dados = {
        "op": "OP245101",
        "nf": "123456",
        "cliente": "Alimentos Bom Sabor",
        "peso_kg": 1250.5,
        "emissao": EMISSAO,
        "resultados": list(APROVADOS),
    }
    dados.update(mudancas)
    return ex.Certificado(**dados)


def test_e_dataclass_com_campos_na_ordem():
    c = criar()
    assert dataclasses.is_dataclass(c)
    nomes = [f.name for f in dataclasses.fields(c)]
    assert nomes == ["op", "nf", "cliente", "peso_kg", "emissao", "resultados"]


def test_resultados_padrao_e_lista_nova_para_cada_um():
    a = ex.Certificado("OP1", "1", "X", 10.0, EMISSAO)
    b = ex.Certificado("OP2", "2", "Y", 10.0, EMISSAO)
    a.resultados.append(APROVADOS[0])
    assert b.resultados == [], "Use field(default_factory=list)"


def test_post_init_limpa_e_valida():
    c = criar(op=" OP245101 ", nf=" 123456 ")
    assert (c.op, c.nf) == ("OP245101", "123456")
    for invalido in ({"op": "  "}, {"nf": ""}, {"peso_kg": 0}, {"peso_kg": -5}):
        with pytest.raises(ValueError):
            criar(**invalido)


def test_numero():
    assert criar().numero == "CQ-20261029-OP245101"


def test_aprovado():
    assert criar().aprovado is True
    assert criar(resultados=[R("cof", 0.35, "", False)]).aprovado is False
    assert criar(resultados=[]).aprovado is False, "Sem resultados não está aprovado"


def test_texto_exato():
    esperado = (
        "CERTIFICADO DE QUALIDADE Nº CQ-20261029-OP245101\n"
        "Cliente: Alimentos Bom Sabor\n"
        "OP: OP245101 | NF: 123456 | Peso: 1.250,50 kg\n"
        "Emissão: 29/10/2026\n"
        "Resultados:\n"
        "- espessura: 25,10 µm (aprovado)\n"
        "- cof: 0,22 (aprovado)\n"
        "Situação: APROVADO"
    )
    assert criar().texto() == esperado


def test_texto_reprovado():
    texto = criar(resultados=[R("tração", 18.0, "MPa", False)]).texto()
    linhas = texto.splitlines()
    assert linhas[-2] == "- tração: 18,00 MPa (reprovado)"
    assert linhas[-1] == "Situação: REPROVADO"


def test_salvar_cria_pasta_e_arquivo(tmp_path):
    pasta = tmp_path / "certificados" / "2026-10"
    caminho = criar().salvar(pasta)
    assert caminho == pasta / "CQ-20261029-OP245101.txt"
    assert caminho.read_text(encoding="utf-8") == criar().texto()


def test_emitir_aprovado():
    c = ex.Certificado.emitir("OP9", "777", "Cliente", 300.0, EMISSAO, APROVADOS)
    assert isinstance(c, ex.Certificado)
    assert c.resultados == APROVADOS
    assert c.aprovado is True


def test_emitir_reprovado_lista_ensaios_em_ordem():
    resultados = [
        R("espessura", 28.0, "µm", False),
        R("gramatura", 23.0, "g/m²", True),
        R("cof", 0.35, "", False),
    ]
    with pytest.raises(ex.CertificadoReprovadoError, match="OP9 reprovada em: cof, espessura"):
        ex.Certificado.emitir("OP9", "777", "Cliente", 300.0, EMISSAO, resultados)


def test_emitir_sem_resultados():
    with pytest.raises(ValueError):
        ex.Certificado.emitir("OP9", "777", "Cliente", 300.0, EMISSAO, [])
