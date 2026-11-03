import json

import pytest

from _curso import carregar

ex = carregar(__file__, "ex10_carregar_config")

PADRAO = {"casas": 2, "liberacao": "COF: liberado", "pasta": "laudos"}


def test_arquivo_inexistente_devolve_copia_do_padrao(tmp_path):
    config = ex.carregar_config(tmp_path / "config.json", PADRAO)
    assert config == PADRAO
    assert config is not PADRAO, "Devolva uma cópia, não o próprio dicionário padrão."


def test_arquivo_completa_e_sobrescreve_o_padrao(tmp_path):
    caminho = tmp_path / "config.json"
    caminho.write_text('{"casas": 3, "novo": true}', encoding="utf-8")
    config = ex.carregar_config(caminho, PADRAO)
    assert config == {
        "casas": 3,
        "liberacao": "COF: liberado",
        "pasta": "laudos",
        "novo": True,
    }


def test_padrao_nao_e_alterado(tmp_path):
    caminho = tmp_path / "config.json"
    caminho.write_text('{"casas": 4}', encoding="utf-8")
    copia = dict(PADRAO)
    ex.carregar_config(caminho, PADRAO)
    assert copia == PADRAO


def test_json_quebrado_vira_arquivo_invalido(tmp_path):
    caminho = tmp_path / "config.json"
    caminho.write_text('{\n  "casas": 3\n  "pasta": "x"\n}', encoding="utf-8")
    with pytest.raises(
        ex.ArquivoInvalido, match=r"config\.json: JSON inválido \(linha 3\)"
    ) as info:
        ex.carregar_config(caminho, PADRAO)
    assert isinstance(info.value.__cause__, json.JSONDecodeError), "Use 'raise ... from erro'."


def test_json_que_nao_e_objeto(tmp_path):
    caminho = tmp_path / "config.json"
    caminho.write_text("[1, 2, 3]", encoding="utf-8")
    with pytest.raises(ex.ArquivoInvalido, match="esperado um objeto JSON"):
        ex.carregar_config(caminho, PADRAO)


def test_salvar_com_acentos_legiveis_e_indentado(tmp_path):
    caminho = tmp_path / "config.json"
    ex.salvar_config(caminho, {"liberacao": "Liberação"})
    texto = caminho.read_text(encoding="utf-8")
    assert "Liberação" in texto, "Use ensure_ascii=False."
    assert texto == '{\n  "liberacao": "Liberação"\n}'


def test_salvar_cria_pastas_e_ida_e_volta(tmp_path):
    caminho = tmp_path / "robo" / "config" / "config.json"
    ex.salvar_config(caminho, {"casas": 3, "pasta": "C:/Laudos"})
    assert ex.carregar_config(caminho, PADRAO) == {
        "casas": 3,
        "liberacao": "COF: liberado",
        "pasta": "C:/Laudos",
    }
