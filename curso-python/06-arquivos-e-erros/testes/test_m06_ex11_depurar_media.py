import pytest

from _curso import carregar

ex = carregar(__file__, "ex11_depurar_media")


def test_previsao_a_arquivo_normal():
    assert ex.previsoes()[0] == pytest.approx(26.0)


@pytest.mark.parametrize(
    ("indice", "caso"), [(1, "vírgula decimal"), (2, "vazio"), (3, "inexistente")]
)
def test_previsoes_b_c_d_tudo_vira_zero(indice, caso):
    assert ex.previsoes()[indice] == 0, (
        f"Arquivo {caso}: o except pega-tudo engole o erro e devolve 0."
    )


def test_media_com_virgula_e_linhas_em_branco(tmp_path):
    arquivo = tmp_path / "espessuras.txt"
    arquivo.write_text("25,4\n\n26,0\n  \n", encoding="utf-8")
    assert ex.media_do_arquivo(arquivo) == pytest.approx(25.7)


def test_media_com_milhar(tmp_path):
    arquivo = tmp_path / "pesos.txt"
    arquivo.write_text("1.250,5\n749,5\n", encoding="utf-8")
    assert ex.media_do_arquivo(arquivo) == pytest.approx(1000.0)


def test_valor_invalido_informa_a_linha(tmp_path):
    arquivo = tmp_path / "espessuras.txt"
    arquivo.write_text("25,4\n2O,1\n26,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match=r"linha 2: valor inválido '2O,1'") as info:
        ex.media_do_arquivo(arquivo)
    assert info.value.__cause__ is not None, "Encadeie com 'raise ... from erro'."


def test_linha_em_branco_conta_na_numeracao(tmp_path):
    arquivo = tmp_path / "espessuras.txt"
    arquivo.write_text("25,4\n\nabc\n", encoding="utf-8")
    with pytest.raises(ValueError, match="linha 3"):
        ex.media_do_arquivo(arquivo)


def test_arquivo_sem_valores(tmp_path):
    arquivo = tmp_path / "vazio.txt"
    arquivo.write_text("\n\n", encoding="utf-8")
    with pytest.raises(ValueError, match="arquivo sem valores"):
        ex.media_do_arquivo(arquivo)


def test_arquivo_inexistente_nao_e_escondido(tmp_path):
    with pytest.raises(FileNotFoundError):
        ex.media_do_arquivo(tmp_path / "nao_existe.txt")
