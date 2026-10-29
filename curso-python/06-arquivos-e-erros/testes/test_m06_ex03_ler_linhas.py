import pytest

from _curso import carregar

ex = carregar(__file__, "ex03_ler_linhas")


def test_le_linhas_ignorando_vazias_e_comentarios(tmp_path):
    arquivo = tmp_path / "ops.txt"
    arquivo.write_text(
        "# OPs de hoje\nOP 123456\n\n  OP 123457  \n   # outro\n", encoding="utf-8"
    )
    assert ex.ler_linhas(arquivo) == ["OP 123456", "OP 123457"]


def test_acentos_em_utf8(tmp_path):
    arquivo = tmp_path / "obs.txt"
    arquivo.write_text("Liberação parcial\nCOF: liberado\n", encoding="utf-8")
    assert ex.ler_linhas(arquivo) == ["Liberação parcial", "COF: liberado"]


def test_quebras_de_linha_do_windows(tmp_path):
    arquivo = tmp_path / "windows.txt"
    arquivo.write_bytes(b"OP 1\r\nOP 2\r\n")
    assert ex.ler_linhas(arquivo) == ["OP 1", "OP 2"]


def test_so_comentarios_devolve_lista_vazia(tmp_path):
    arquivo = tmp_path / "vazio.txt"
    arquivo.write_text("# nada\n\n", encoding="utf-8")
    assert ex.ler_linhas(arquivo) == []


def test_arquivo_inexistente_levanta_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        ex.ler_linhas(tmp_path / "nao_existe.txt")
