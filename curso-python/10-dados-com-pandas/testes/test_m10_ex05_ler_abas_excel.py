import pytest
from openpyxl import Workbook

from _curso import carregar

ex = carregar(__file__, "ex05_ler_abas_excel")

CABECALHO = ["OP", "Bobina", "Espessura (µm)"]


def criar_planilha(caminho, abas):
    """abas: {nome: lista de linhas}. Abas de linha ganham título e cabeçalho."""
    livro = Workbook()
    livro.remove(livro.active)
    for nome, linhas in abas.items():
        aba = livro.create_sheet(nome)
        if nome.startswith("Linha "):
            aba.append([f"Controle de qualidade — {nome}"])
            aba.append(CABECALHO)
        for linha in linhas:
            aba.append(linha)
    livro.save(caminho)
    return caminho


@pytest.fixture
def planilha(tmp_path):
    return criar_planilha(
        tmp_path / "valores.xlsx",
        {
            "Instruções": [["Preencha uma aba por linha de produção."]],
            "Linha A": [["024412", "024412-01", 38.1], ["024412", "024412-02", 36.4]],
            "Linha B": [["024413", "024413-01", 32.9]],
            "Linha D": [["024421", "024421-01", 65.2], ["024421", "024421-02", 59.3]],
        },
    )


def test_colunas_na_ordem_pedida(planilha):
    df = ex.ler_todas_as_abas(planilha)
    assert list(df.columns) == ["linha", "op", "bobina", "espessura_um"]


def test_junta_as_abas_de_linha_e_ignora_as_outras(planilha):
    df = ex.ler_todas_as_abas(planilha)
    assert len(df) == 5, "a aba 'Instruções' não deve entrar"
    assert df["linha"].tolist() == ["A", "A", "B", "D", "D"]
    assert df["bobina"].tolist() == [
        "024412-01", "024412-02", "024413-01", "024421-01", "024421-02"
    ]  # fmt: skip


def test_op_continua_texto_com_zero(planilha):
    df = ex.ler_todas_as_abas(planilha)
    assert df["op"].tolist() == ["024412", "024412", "024413", "024421", "024421"]


def test_valores_e_indice(planilha):
    df = ex.ler_todas_as_abas(planilha)
    assert df["espessura_um"].tolist() == pytest.approx([38.1, 36.4, 32.9, 65.2, 59.3])
    assert df.index.tolist() == [0, 1, 2, 3, 4], "use ignore_index=True no concat"


def test_sem_aba_de_linha_da_value_error(tmp_path):
    caminho = criar_planilha(tmp_path / "errada.xlsx", {"Plan1": [["nada aqui"]]})
    with pytest.raises(ValueError):
        ex.ler_todas_as_abas(caminho)
