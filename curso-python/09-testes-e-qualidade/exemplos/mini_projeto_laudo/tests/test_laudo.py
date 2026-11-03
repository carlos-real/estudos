"""Testes do módulo laudo.py — rode com: python -m pytest -v (na pasta do mini projeto)."""

import pytest

import laudo
from laudo import avaliar, calcular_limites, conferir_op, ler_medicoes, media


def test_limites_com_tolerancia_de_5_porcento():
    # Arrange (preparar): os dados de entrada
    nominal, tolerancia = 20.0, 5.0
    # Act (agir): chama UMA vez o que está sendo testado
    minimo, maximo = calcular_limites(nominal, tolerancia)
    # Assert (conferir): o resultado é o esperado?
    assert minimo == pytest.approx(19.0)
    assert maximo == pytest.approx(21.0)


def test_limites_com_tolerancia_negativa_levanta_erro():
    with pytest.raises(ValueError, match="negativa"):
        calcular_limites(20.0, -1.0)


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (19.0, "APROVADO"),  # na borda inferior
        (20.0, "APROVADO"),
        (21.0, "APROVADO"),  # na borda superior
        (18.99, "REPROVADO"),
        (21.01, "REPROVADO"),
    ],
)
def test_avaliar_respeita_as_bordas(valor, esperado):
    assert avaliar(valor, 19.0, 21.0) == esperado


def test_media_de_tres_medicoes(medicoes_espessura):
    assert media(medicoes_espessura) == pytest.approx(20.1)


def test_media_de_lista_vazia_levanta_erro():
    with pytest.raises(ValueError, match="vazia"):
        media([])


def test_ler_medicoes_aceita_virgula_decimal(arquivo_medicoes, medicoes_espessura):
    assert ler_medicoes(arquivo_medicoes) == medicoes_espessura


def test_ler_medicoes_ignora_linhas_vazias(tmp_path):
    arquivo = tmp_path / "com_buracos.txt"
    arquivo.write_text("20,1\n\n   \n19,8\n", encoding="utf-8")
    assert ler_medicoes(arquivo) == [20.1, 19.8]


def test_conferir_op_sem_acessar_o_erp(monkeypatch, capsys, medicoes_espessura):
    # Troca a consulta ao ERP por uma função falsa que responde na hora
    monkeypatch.setattr(laudo, "buscar_nominal_no_erp", lambda op: 20.0)

    resultado = conferir_op("12345", medicoes_espessura, 5.0)

    assert resultado == "APROVADO"
    saida = capsys.readouterr().out
    assert saida == "OP 12345: média 20.10 em [19.00, 21.00] -> APROVADO\n"
