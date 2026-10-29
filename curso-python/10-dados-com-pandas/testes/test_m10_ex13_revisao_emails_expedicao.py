import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from _curso import carregar

ex = carregar(__file__, "ex13_revisao_emails_expedicao")

EMAIL_1 = """De: Marcos <expedicao@exemplo.com.br>
Assunto: Certificado - OP 24518

Bom dia! Favor emitir o certificado.

OP: 24518
NF: 123456
Peso: 1.250,5 kg
"""

EMAIL_2 = "op:24533\nnf:   000789\npeso:980 KG\nObrigado"
EMAIL_3 = "OP: 24518\nNF: 123499\nPeso: 2.000,25 kg"
EMAIL_SEM_NF = "OP: 24541\nPeso: 500,0 kg\n(NF sai à tarde)"


def test_extrai_pedido_completo():
    assert ex.extrair_pedido(EMAIL_1) == {"op": 24518, "nf": "123456", "peso_kg": 1250.5}


def test_maiusculas_minusculas_e_espacos():
    pedido = ex.extrair_pedido(EMAIL_2)
    assert pedido == {"op": 24533, "nf": "000789", "peso_kg": 980.0}, (
        "aceite 'op:' minúsculo, espaços variados e NF com zero à esquerda (texto)"
    )


@pytest.mark.parametrize("texto", [EMAIL_SEM_NF, "Bom dia, tudo bem?", ""])
def test_pedido_incompleto_devolve_none(texto):
    assert ex.extrair_pedido(texto) is None


def test_pedidos_para_tabela_ignora_incompletos():
    tabela = ex.pedidos_para_tabela([EMAIL_1, EMAIL_SEM_NF, EMAIL_2, EMAIL_3])
    esperado = pd.DataFrame(
        {
            "op": [24518, 24533, 24518],
            "nf": ["123456", "000789", "123499"],
            "peso_kg": [1250.5, 980.0, 2000.25],
        }
    )
    assert_frame_equal(tabela, esperado, check_dtype=False)


def test_tabela_vazia_tem_as_colunas():
    tabela = ex.pedidos_para_tabela([EMAIL_SEM_NF])
    assert len(tabela) == 0
    assert list(tabela.columns) == ["op", "nf", "peso_kg"]


def test_peso_por_op():
    pedidos = pd.DataFrame(
        {
            "op": [24533, 24518, 24518],
            "nf": ["000789", "123456", "123499"],
            "peso_kg": [980.0, 1250.5, 2000.25],
        }
    )
    resultado = ex.peso_por_op(pedidos)
    esperado = pd.DataFrame(
        {"op": [24518, 24533], "notas": [2, 1], "peso_total_kg": [3250.8, 980.0]}
    )
    assert_frame_equal(resultado, esperado, check_dtype=False)
