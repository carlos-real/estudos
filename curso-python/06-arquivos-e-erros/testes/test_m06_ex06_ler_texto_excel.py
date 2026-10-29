import pytest

from _curso import carregar

ex = carregar(__file__, "ex06_ler_texto_excel")

TEXTO = "lote;observação\r\nA-0153;Liberação parcial\r\n"


def test_utf8_com_bom(tmp_path):
    arquivo = tmp_path / "csv_utf8.csv"
    arquivo.write_bytes(TEXTO.encode("utf-8-sig"))
    texto, encoding = ex.ler_texto_excel(arquivo)
    assert encoding == "utf-8-sig"
    assert texto.startswith("lote;"), "O BOM (\\ufeff) não pode ficar grudado no texto."
    assert "Liberação" in texto


def test_utf8_sem_bom(tmp_path):
    arquivo = tmp_path / "sistema.csv"
    arquivo.write_bytes(TEXTO.encode("utf-8"))
    assert ex.ler_texto_excel(arquivo)[1] == "utf-8"
    assert "observação" in ex.ler_texto_excel(arquivo)[0]


def test_cp1252(tmp_path):
    arquivo = tmp_path / "excel_antigo.csv"
    arquivo.write_bytes(TEXTO.encode("cp1252"))
    texto, encoding = ex.ler_texto_excel(arquivo)
    assert encoding == "cp1252"
    assert "Liberação parcial" in texto, "Os acentos precisam aparecer certos."


def test_texto_sem_acento_e_utf8(tmp_path):
    arquivo = tmp_path / "simples.csv"
    arquivo.write_bytes(b"lote;espessura\n")
    assert ex.ler_texto_excel(arquivo) == ("lote;espessura\n", "utf-8")


def test_arquivo_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        ex.ler_texto_excel(tmp_path / "nao_existe.csv")
