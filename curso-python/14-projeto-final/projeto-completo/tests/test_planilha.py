import pytest
from openpyxl import Workbook

from validador_certificados.modelos import PlanilhaInvalida
from validador_certificados.planilha import (
    chave_coluna,
    conferir_linha,
    ler_planilha,
    normalizar_linha,
    numero_celula,
    texto_celula,
)

CABECALHO = [
    "OP",
    "Linha",
    "Especificação",
    "Espessura nominal (µm)",
    "Espessura (µm)",
    "Gramatura nominal (g/m²)",
    "Gramatura (g/m²)",
    "COF",
    "Tração (MPa)",
    "Selagem (N/15mm)",
    "Observação",
]


def criar_planilha(caminho, abas):
    pasta_trabalho = Workbook()
    pasta_trabalho.remove(pasta_trabalho.active)
    for nome, linhas in abas.items():
        aba = pasta_trabalho.create_sheet(nome)
        for linha in linhas:
            aba.append(linha)
    pasta_trabalho.save(caminho)
    return caminho


@pytest.mark.parametrize(
    ("cabecalho", "esperado"),
    [
        ("Espessura nominal (µm)", "espessura_nominal"),
        ("  OBSERVAÇÃO ", "observacao"),
        ("Tração (MPa)", "tracao"),
        (None, ""),
    ],
)
def test_chave_coluna(cabecalho, esperado):
    assert chave_coluna(cabecalho) == esperado


def test_celulas():
    assert texto_celula(24518.0) == "24518"
    assert texto_celula(None) == ""
    assert numero_celula("41,2") == pytest.approx(41.2)
    assert numero_celula("n/d") is None
    assert numero_celula(None) is None


def test_le_abas_de_linha_e_ignora_o_resto(tmp_path):
    caminho = criar_planilha(
        tmp_path / "valores.xlsx",
        {
            "Linha A": [
                CABECALHO,
                [24518, "A", None, 40, 41.2, 37, 37.9, 0.22, 24.5, 9.8, "COF: liberado"],
                [None] * len(CABECALHO),
                [24519, "a", "ESP-0533", 40, "44,8", 37, None, 0.24, 23.9, 9.1, None],
            ],
            "Instruções": [["Preencha uma linha por OP"]],
        },
    )
    medicoes = ler_planilha(caminho)
    assert [m.op for m in medicoes] == ["24518", "24519"]
    primeira, segunda = medicoes
    assert primeira.aba == "Linha A"
    assert primeira.linha_excel == 2
    assert primeira.valores["cof"] == pytest.approx(0.22)
    assert primeira.nominais == {"espessura": 40.0, "gramatura": 37.0}
    assert segunda.linha_excel == 4
    assert segunda.valores["espessura"] == pytest.approx(44.8)
    assert "gramatura" not in segunda.valores
    assert segunda.especificacao == "ESP-0533"
    assert segunda.observacao == ""


def test_coluna_faltando_e_erro_claro(tmp_path):
    caminho = criar_planilha(tmp_path / "valores.xlsx", {"Linha B": [CABECALHO[:-1]]})
    with pytest.raises(PlanilhaInvalida, match="observacao"):
        ler_planilha(caminho)


def test_planilha_de_exemplo(pasta_dados):
    medicoes = ler_planilha(pasta_dados / "planilha_valores.xlsx")
    assert len(medicoes) == 16
    assert {m.aba for m in medicoes} == {"Linha A", "Linha B", "Linha C", "Linha D"}


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [("Linha A", "A"), (" linha  b ", "B"), ("c", "C"), ("Linha E", None), ("", None)],
)
def test_normalizar_linha(texto, esperado):
    assert normalizar_linha(texto) == esperado


def test_conferir_linha():
    assert conferir_linha("Linha B", "b") is None
    assert conferir_linha("Linha B", "C") == "linha informada C diferente da aba Linha B"
    assert conferir_linha("Linha B", None) == "linha não informada ou inválida: ''"
    assert "não corresponde" in conferir_linha("Resumo", "A")
