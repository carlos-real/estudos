from _curso import carregar

ex = carregar(__file__, "ex01_apresentacao")


def test_apresentacao_basica():
    resultado = ex.apresentar("Ana", 28, "Joinville")
    assert resultado == "Meu nome é Ana, tenho 28 anos e moro em Joinville.", (
        f"Sua função devolveu {resultado!r}. Confira espaços, vírgulas e o ponto final."
    )


def test_nome_e_cidade_com_espacos():
    resultado = ex.apresentar("Carlos Souza", 41, "São Bento do Sul")
    assert resultado == "Meu nome é Carlos Souza, tenho 41 anos e moro em São Bento do Sul."


def test_idade_entra_como_numero_no_texto():
    resultado = ex.apresentar("Bia", 19, "Itajaí")
    assert "tenho 19 anos" in resultado


def test_devolve_texto_e_nao_imprime(capsys):
    resultado = ex.apresentar("Rui", 35, "Blumenau")
    saida = capsys.readouterr().out
    assert isinstance(resultado, str), "A função precisa DEVOLVER o texto com return."
    assert saida == "", "Não use print nesta função: use return."
