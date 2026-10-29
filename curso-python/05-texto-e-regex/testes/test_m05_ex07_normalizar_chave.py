import pytest

from _curso import carregar

ex = carregar(__file__, "ex07_normalizar_chave")


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("Gramatura (g/m²)", "gramatura_g_m2"),
        ("  Coeficiente de Atrito – Estático ", "coeficiente_de_atrito_estatico"),
        ("Tração MD (N/15mm)", "tracao_md_n_15mm"),
        ("Observação", "observacao"),
        ("OP", "op"),
    ],
)
def test_normaliza_nomes_de_coluna(entrada, esperado):
    assert ex.normalizar_chave(entrada) == esperado


def test_micro_vira_u():
    assert ex.normalizar_chave("Espessura (µm)") == "espessura_um", (
        "Troque 'µ' por 'u' ANTES da NFKD (ela transforma o µ em outra letra)."
    )


def test_expoente_vira_digito():
    assert ex.normalizar_chave("m²") == "m2", "Use NFKD: ela transforma '²' em '2'."


def test_sequencia_de_simbolos_vira_um_sublinhado():
    assert ex.normalizar_chave("lote -- (linha)  A") == "lote_linha_a"


@pytest.mark.parametrize("entrada", ["", "   ", "(%)"])
def test_sem_letras_nem_digitos_devolve_vazio(entrada):
    assert ex.normalizar_chave(entrada) == ""
