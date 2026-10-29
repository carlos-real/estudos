import pytest

from _curso import carregar

ex = carregar(__file__, "ex01_classificar_status")


@pytest.mark.parametrize(
    ("codigo", "esperado"),
    [
        (100, "informativo"),
        (200, "sucesso"),
        (201, "sucesso"),
        (204, "sucesso"),
        (301, "redirecionamento"),
        (400, "erro do cliente"),
        (404, "erro do cliente"),
        (422, "erro do cliente"),
        (500, "erro do servidor"),
        (599, "erro do servidor"),
    ],
)
def test_classifica_familias(codigo, esperado):
    assert ex.classificar_status(codigo) == esperado


@pytest.mark.parametrize("codigo", [0, 99, 600, 1000, -200])
def test_codigo_fora_da_faixa_levanta_value_error(codigo):
    with pytest.raises(ValueError, match="Código de status inválido"):
        ex.classificar_status(codigo)


@pytest.mark.parametrize("codigo", [408, 429, 500, 502, 503, 504])
def test_erros_passageiros_valem_nova_tentativa(codigo):
    assert ex.vale_tentar_de_novo(codigo) is True


@pytest.mark.parametrize("codigo", [200, 201, 400, 401, 403, 404, 422, 501])
def test_outros_codigos_nao_valem_nova_tentativa(codigo):
    assert ex.vale_tentar_de_novo(codigo) is False, (
        f"Repetir a requisição não resolve o código {codigo}"
    )
