import pytest

from _curso import carregar

ex = carregar(__file__, "ex13_revisao_ler_medicoes")


def gravar(tmp_path, texto, encoding="utf-8-sig", nome="medicoes.csv"):
    caminho = tmp_path / nome
    caminho.write_bytes(texto.replace("\n", "\r\n").encode(encoding))
    return caminho


def test_arquivo_utf8_com_bom(tmp_path):
    caminho = gravar(tmp_path, "lote;linha;espessura;gramatura\nA-0153;A;25,4;23,1\n")
    assert ex.ler_medicoes(caminho) == [
        {"lote": "A-0153", "linha": "A", "espessura": 25.4, "gramatura": 23.1}
    ]


def test_arquivo_cp1252_com_colunas_a_mais(tmp_path):
    texto = (
        "Lote;Linha;Espessura;Gramatura;Observação\n"
        "B-0201;B;50,2;46,0;Liberação parcial\n"
        'B-0202; b ;1.049,1;45,2;"COF: liberado; ok"\n'
    )
    caminho = gravar(tmp_path, texto, encoding="cp1252")
    medicoes = ex.ler_medicoes(caminho)
    assert [m["linha"] for m in medicoes] == ["B", "B"]
    assert medicoes[1]["espessura"] == pytest.approx(1049.1)
    assert set(medicoes[0]) == {"lote", "linha", "espessura", "gramatura"}


def test_nomes_de_coluna_variados(tmp_path):
    caminho = gravar(tmp_path, "  LOTE ;Linha; Espessura ;GRAMATURA\nC-1;c;20,1;18,4\n")
    assert ex.ler_medicoes(caminho)[0]["linha"] == "C"


def test_pula_linhas_vazias(tmp_path):
    caminho = gravar(tmp_path, "lote;linha;espessura;gramatura\n;;;\nD-1;D;35;32,2\n\n")
    assert len(ex.ler_medicoes(caminho)) == 1


def test_arquivo_vazio(tmp_path):
    caminho = gravar(tmp_path, "")
    with pytest.raises(ex.ArquivoInvalido, match="arquivo vazio"):
        ex.ler_medicoes(caminho)


def test_colunas_ausentes(tmp_path):
    caminho = gravar(tmp_path, "lote;linha;cof\nA-1;A;0,2\n")
    with pytest.raises(ex.ArquivoInvalido, match="^colunas ausentes: espessura, gramatura$"):
        ex.ler_medicoes(caminho)


def test_numero_invalido_informa_linha_e_coluna(tmp_path):
    texto = "lote;linha;espessura;gramatura\nC-1;C;20,3;18,5\nC-2;C;2O,1;18,2\n"
    caminho = gravar(tmp_path, texto)
    with pytest.raises(
        ex.ArquivoInvalido, match="linha 3: valor inválido em espessura: '2O,1'"
    ) as info:
        ex.ler_medicoes(caminho)
    assert isinstance(info.value.__cause__, ValueError), "Use 'raise ... from erro'."


def test_linha_de_producao_invalida(tmp_path):
    caminho = gravar(tmp_path, "lote;linha;espessura;gramatura\nE-1;E;20;18\n")
    with pytest.raises(ex.ArquivoInvalido, match="linha 2: linha de produção inválida: 'E'"):
        ex.ler_medicoes(caminho)


def test_numeros_sao_float(tmp_path):
    caminho = gravar(tmp_path, "lote;linha;espessura;gramatura\nA-1;A;25;23\n")
    medicao = ex.ler_medicoes(caminho)[0]
    assert isinstance(medicao["espessura"], float) and isinstance(medicao["gramatura"], float)
