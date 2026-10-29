from _curso import carregar

ex = carregar(__file__, "ex01_ola_mundo")


def test_devolve_um_valor():
    resultado = ex.ola_mundo()
    assert resultado is not None, (
        "Sua função não devolveu nada (devolveu None). Você usou print() em vez de return?"
    )


def test_devolve_um_texto():
    resultado = ex.ola_mundo()
    assert isinstance(resultado, str), f"Era para devolver um texto (str), veio {resultado!r}."


def test_texto_exato():
    assert ex.ola_mundo() == "Olá, mundo!"


def test_tem_acento_em_ola():
    resultado = ex.ola_mundo()
    assert resultado.startswith("Olá"), "O texto deve começar com 'Olá' (com acento no á)."


def test_sem_espacos_sobrando():
    resultado = ex.ola_mundo()
    assert resultado == resultado.strip(), "Tem espaço sobrando no começo ou no fim do texto."
