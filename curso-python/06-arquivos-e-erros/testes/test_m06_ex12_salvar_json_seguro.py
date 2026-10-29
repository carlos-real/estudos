import json

import pytest

from _curso import carregar

ex = carregar(__file__, "ex12_salvar_json_seguro")

REGRAS = {"linha": "A", "cof": [0.15, 0.3], "obs": "Liberação"}


def test_grava_json_legivel(tmp_path):
    destino = tmp_path / "regras.json"
    ex.salvar_json_seguro(destino, REGRAS)
    texto = destino.read_text(encoding="utf-8")
    assert json.loads(texto) == REGRAS
    assert "Liberação" in texto and '\n  "linha"' in texto, (
        "Use indent=2 e ensure_ascii=False."
    )


def test_nao_sobra_temporario(tmp_path):
    ex.salvar_json_seguro(tmp_path / "regras.json", REGRAS)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["regras.json"]


def test_sobrescreve_arquivo_existente(tmp_path):
    destino = tmp_path / "regras.json"
    destino.write_text('{"versao": 1}', encoding="utf-8")
    ex.salvar_json_seguro(destino, {"versao": 2})
    assert json.loads(destino.read_text(encoding="utf-8")) == {"versao": 2}


def test_erro_mantem_o_arquivo_antigo_intacto(tmp_path):
    destino = tmp_path / "regras.json"
    destino.write_text('{"versao": 1}', encoding="utf-8")
    with pytest.raises(TypeError):
        ex.salvar_json_seguro(destino, {"linhas": {"A", "B"}})  # set não vira JSON
    assert destino.read_text(encoding="utf-8") == '{"versao": 1}'


def test_erro_nao_deixa_temporario_para_tras(tmp_path):
    destino = tmp_path / "regras.json"
    with pytest.raises(TypeError):
        ex.salvar_json_seguro(destino, {"bobina": object()})
    assert list(tmp_path.iterdir()) == [], "Apague o .tmp quando der erro."
