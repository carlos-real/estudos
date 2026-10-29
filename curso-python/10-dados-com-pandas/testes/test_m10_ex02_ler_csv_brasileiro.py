import pytest

from _curso import carregar

ex = carregar(__file__, "ex02_ler_csv_brasileiro")

MEDICOES = (
    "data;op;bobina;espessura_um;peso_kg;observacao\n"
    "03/07/2026;024412;024412-01;38,1;1.558,5;\n"
    "05/07/2026;024412;024412-02;36,4;956,0;COF: liberado\n"
    "09/07/2026;024420;024420-01;69,8;1.012,3;\n"
)

OPS = (
    "op;cliente;produto;quantidade_kg\n"
    "024412;Torrefação Serra Ltda;PE-40;4.500,0\n"
    "024413;Laticínios Serra Azul;PE-35;3.250,5\n"
)


@pytest.fixture
def arquivo_medicoes(tmp_path):
    caminho = tmp_path / "medicoes.csv"
    caminho.write_text(MEDICOES, encoding="utf-8-sig")
    return caminho


@pytest.fixture
def arquivo_ops(tmp_path):
    caminho = tmp_path / "ops.csv"
    caminho.write_text(OPS, encoding="cp1252")
    return caminho


def test_medicoes_tem_colunas_e_linhas_certas(arquivo_medicoes):
    df = ex.ler_medicoes(arquivo_medicoes)
    assert df.shape == (3, 6), "o separador é ';' (sep=';')"
    assert list(df.columns) == [
        "data",
        "op",
        "bobina",
        "espessura_um",
        "peso_kg",
        "observacao",
    ]


def test_op_mantem_zero_a_esquerda(arquivo_medicoes):
    df = ex.ler_medicoes(arquivo_medicoes)
    assert df["op"].tolist() == ["024412", "024412", "024420"], "use dtype={'op': str}"


def test_virgula_decimal_e_ponto_de_milhar_viram_numero(arquivo_medicoes):
    df = ex.ler_medicoes(arquivo_medicoes)
    assert df["espessura_um"].tolist() == pytest.approx([38.1, 36.4, 69.8])
    assert df["peso_kg"].tolist() == pytest.approx([1558.5, 956.0, 1012.3]), (
        "o peso tem ponto de milhar: use thousands='.'"
    )


def test_texto_com_acento_e_vazio(arquivo_medicoes):
    df = ex.ler_medicoes(arquivo_medicoes)
    assert df.loc[1, "observacao"] == "COF: liberado"
    assert df["observacao"].isna().sum() == 2


def test_ops_do_erp_em_cp1252(arquivo_ops):
    ops = ex.ler_ops_erp(arquivo_ops)
    assert ops["cliente"].tolist() == ["Torrefação Serra Ltda", "Laticínios Serra Azul"]
    assert ops["op"].tolist() == ["024412", "024413"]
    assert ops["quantidade_kg"].tolist() == pytest.approx([4500.0, 3250.5])
