import pytest

from _curso import carregar

ex = carregar(__file__, "ex11_especificacao_linha")
T = ex.Tolerancia


def criar_padrao():
    return ex.Especificacao(
        "Filme PE 25 µm",
        {"espessura": T(22.5, 27.5), "gramatura": T(20.7, 25.3)},
        "Padrão da linha B",
    )


def criar_linha():
    return ex.LinhaDeProducao("B", {"cof": T(0.10, 0.30)}, criar_padrao())


MEDIDAS = {"espessura": 25.4, "gramatura": 26.0, "cof": 0.22, "tracao": 30.0}


def test_especificacao_guarda_dados_e_copia_o_dicionario():
    tolerancias = {"espessura": T(22.5, 27.5)}
    espec = ex.Especificacao("Título", tolerancias, "Texto livre")
    tolerancias["cof"] = T(0, 1)
    assert espec.titulo == "Título"
    assert espec.texto == "Texto livre"
    assert list(espec.tolerancias) == ["espessura"], "Guarde uma CÓPIA: dict(tolerancias)"
    assert ex.Especificacao("Sem texto", {}).texto == ""


def test_especificacao_avaliar_na_ordem_e_ignorando_extras():
    resultado = criar_padrao().avaliar(MEDIDAS)
    assert resultado == {"espessura": True, "gramatura": False}
    assert list(resultado) == ["espessura", "gramatura"]


def test_especificacao_aprova():
    espec = criar_padrao()
    assert espec.aprova(MEDIDAS) is False
    assert espec.aprova({"espessura": 25.0, "gramatura": 23.0}) is True


def test_especificacao_ensaio_faltando_gera_key_error():
    with pytest.raises(KeyError):
        criar_padrao().avaliar({"espessura": 25.0})


def test_linha_usa_padrao_sem_especificacao_propria():
    linha = criar_linha()
    assert linha.nome == "B"
    assert linha.tem_especificacao_propria("OP1") is False
    assert linha.especificacao_para("OP1") is linha.padrao


def test_linha_cadastrar_especificacao_da_op():
    linha = criar_linha()
    propria = ex.Especificacao("Cliente X", {"espessura": T(24.0, 26.0)}, "Pedido especial")
    linha.cadastrar("OP245110", propria)
    assert linha.tem_especificacao_propria("OP245110") is True
    assert linha.especificacao_para("OP245110") is propria
    assert linha.especificacao_para("OP245111") is linha.padrao


def test_tolerancias_para_junta_fixas_e_especificacao():
    linha = criar_linha()
    assert linha.tolerancias_para("OP1") == {
        "cof": T(0.10, 0.30),
        "espessura": T(22.5, 27.5),
        "gramatura": T(20.7, 25.3),
    }
    linha.cadastrar("OP2", ex.Especificacao("X", {"cof": T(0.10, 0.40)}))
    assert linha.tolerancias_para("OP2") == {"cof": T(0.10, 0.40)}, (
        "Se o ensaio aparece nas duas, vale a especificação"
    )


def test_linha_avaliar():
    linha = criar_linha()
    resultado = linha.avaliar("OP1", {"espessura": 25.4, "gramatura": 23.0, "cof": 0.33})
    assert resultado == {"cof": False, "espessura": True, "gramatura": True}
    assert list(resultado) == ["cof", "espessura", "gramatura"]


def test_linha_avaliar_com_especificacao_propria_e_ensaio_faltando():
    linha = criar_linha()
    linha.cadastrar("OP3", ex.Especificacao("Y", {"espessura": T(24.0, 26.0)}))
    assert linha.avaliar("OP3", {"espessura": 26.5, "cof": 0.2}) == {
        "cof": True,
        "espessura": False,
    }
    with pytest.raises(KeyError):
        linha.avaliar("OP3", {"espessura": 25.0})


def test_fixas_sao_copiadas():
    fixas = {"cof": T(0.10, 0.30)}
    linha = ex.LinhaDeProducao("A", fixas, criar_padrao())
    fixas["tracao"] = T(20, 100)
    assert "tracao" not in linha.tolerancias_para("OP1")
