from pathlib import Path

import pytest
from openpyxl import Workbook

from _curso import carregar

ex = carregar(__file__, "ex07_ler_planilha")

PLANILHA_EXEMPLO = Path(__file__).resolve().parent.parent / "dados" / "planilha_valores.xlsx"

CABECALHO = [
    "OP",
    "Data",
    "Linha",
    "Produto",
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
    """Cria um .xlsx com as abas pedidas ({nome: [linha, linha, ...]})."""
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
        ("Espessura (um)", "espessura"),
        ("  OBSERVAÇÃO ", "observacao"),
        ("Tração (MPa)", "tracao"),
        ("Gramatura nominal (g/m²)", "gramatura_nominal"),
        (None, ""),
    ],
)
def test_chave_coluna(cabecalho, esperado):
    assert ex.chave_coluna(cabecalho) == esperado


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [(41, 41.0), (0.22, 0.22), ("41,2", 41.2), (" 41.2 ", 41.2)],
)
def test_numero_celula_converte(valor, esperado):
    resultado = ex.numero_celula(valor)
    assert isinstance(resultado, float)
    assert resultado == pytest.approx(esperado)


@pytest.mark.parametrize("valor", [None, "", "   ", "n/d", True])
def test_numero_celula_vazio_ou_invalido(valor):
    assert ex.numero_celula(valor) is None


def test_le_uma_aba(tmp_path):
    caminho = criar_planilha(
        tmp_path / "valores.xlsx",
        {
            "Linha A": [
                CABECALHO,
                [24518, None, "A", "Filme PE", None, 40, 41.2, 37, 37.9, 0.22, 24.5, 9.8,
                 "COF: liberado"],
            ]
        },
    )  # fmt: skip
    medicoes = ex.ler_planilha(caminho)
    assert len(medicoes) == 1
    m = medicoes[0]
    assert isinstance(m, ex.Medicao)
    assert (m.op, m.aba, m.linha, m.linha_excel) == ("24518", "Linha A", "A", 2)
    assert m.valores == pytest.approx(
        {"espessura": 41.2, "gramatura": 37.9, "cof": 0.22, "tracao": 24.5, "selagem": 9.8}
    )
    assert m.nominais == pytest.approx({"espessura": 40.0, "gramatura": 37.0})
    assert (m.especificacao, m.observacao, m.produto) == ("", "COF: liberado", "Filme PE")


def test_pula_linha_vazia_e_ignora_aba_que_nao_e_de_linha(tmp_path):
    caminho = criar_planilha(
        tmp_path / "valores.xlsx",
        {
            "Instruções": [["Uma linha por OP"]],
            "Linha B": [
                CABECALHO,
                [24527, None, "B", "", "", 35, 35.4, 32.4, 32.0, 0.30, 19.5, 6.8, "x"],
                [None] * len(CABECALHO),
                [24528, None, "b", "", "ESP-0412", 35, "34,0", 32.4, None, 0.27, 20.1,
                 "n/d", None],
            ],
        },
    )  # fmt: skip
    medicoes = ex.ler_planilha(caminho)
    assert [m.op for m in medicoes] == ["24527", "24528"]
    segunda = medicoes[1]
    assert segunda.linha_excel == 4, "a linha vazia (3) conta na numeração do Excel"
    assert segunda.valores == pytest.approx({"espessura": 34.0, "cof": 0.27, "tracao": 20.1})
    assert segunda.especificacao == "ESP-0412"
    assert segunda.observacao == ""


def test_coluna_faltando_levanta_planilha_invalida(tmp_path):
    sem_cof = [c for c in CABECALHO if c != "COF"]
    caminho = criar_planilha(tmp_path / "valores.xlsx", {"Linha C": [sem_cof]})
    with pytest.raises(ex.PlanilhaInvalida, match="cof"):
        ex.ler_planilha(caminho)


def test_fecha_o_arquivo(tmp_path):
    caminho = criar_planilha(tmp_path / "valores.xlsx", {"Linha D": [CABECALHO]})
    assert ex.ler_planilha(caminho) == []
    caminho.unlink()  # no Windows, falharia se o arquivo continuasse aberto
    assert not caminho.exists()


def test_planilha_de_exemplo_do_modulo():
    medicoes = ex.ler_planilha(PLANILHA_EXEMPLO)
    assert len(medicoes) == 16
    assert [m.aba for m in medicoes].count("Linha B") == 4
    linha_divergente = next(m for m in medicoes if m.op == "24533")
    assert (linha_divergente.aba, linha_divergente.linha) == ("Linha B", "C")
    sem_selagem = next(m for m in medicoes if m.op == "24560")
    assert "selagem" not in sem_selagem.valores
