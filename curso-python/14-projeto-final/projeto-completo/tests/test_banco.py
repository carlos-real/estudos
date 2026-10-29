import pytest

from validador_certificados.banco import (
    abrir_somente_leitura,
    carregar_do_arquivo,
    carregar_especificacoes,
)


def test_carrega_especificacoes_e_tolerancias(conexao_regras):
    especificacoes = carregar_especificacoes(conexao_regras)
    assert set(especificacoes) == {"PADRAO-A", "ESP-0412"}
    padrao = especificacoes["PADRAO-A"]
    assert padrao.linha == "A"
    assert set(padrao.tolerancias) == {"espessura", "cof", "selagem"}
    assert padrao.tolerancias["selagem"].maximo is None
    assert especificacoes["ESP-0412"].linha == ""  # NULL no banco vira ""


def test_banco_inexistente_nao_e_criado(tmp_path):
    caminho = tmp_path / "nao_existe.db"
    with pytest.raises(FileNotFoundError):
        abrir_somente_leitura(caminho)
    assert not caminho.exists()


def test_banco_de_exemplo(pasta_dados):
    especificacoes = carregar_do_arquivo(pasta_dados / "regras.db")
    assert len(especificacoes) == 7
    padroes = sorted(e.linha for e in especificacoes.values() if e.linha)
    assert padroes == ["A", "B", "C", "D"]
