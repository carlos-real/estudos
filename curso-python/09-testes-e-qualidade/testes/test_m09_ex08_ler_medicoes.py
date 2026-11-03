import pytest

from _curso import carregar

ex = carregar(__file__, "ex08_ler_medicoes")


@pytest.fixture
def criar_arquivo(tmp_path):
    """Fábrica de arquivos: criar_arquivo("conteúdo") devolve o caminho criado."""

    def _criar(conteudo, nome="medicoes.txt"):
        caminho = tmp_path / nome
        caminho.write_text(conteudo, encoding="utf-8")
        return caminho

    return _criar


def test_le_valores_com_ponto(criar_arquivo):
    caminho = criar_arquivo("25.4\n25.1\n24.9\n")
    assert ex.ler_medicoes(caminho) == pytest.approx([25.4, 25.1, 24.9])


def test_aceita_virgula_decimal(criar_arquivo):
    caminho = criar_arquivo("25,4\n25.1\n24,9\n")
    assert ex.ler_medicoes(caminho) == pytest.approx([25.4, 25.1, 24.9])


def test_remove_espacos_em_volta(criar_arquivo):
    caminho = criar_arquivo("  25,4  \n\t25,1\n")
    assert ex.ler_medicoes(caminho) == pytest.approx([25.4, 25.1])


def test_ignora_linhas_vazias_e_comentarios(criar_arquivo):
    caminho = criar_arquivo("# espessura OP 123\n\n25,4\n   \n# pausa\n25,0\n")
    assert ex.ler_medicoes(caminho) == pytest.approx([25.4, 25.0])


def test_arquivo_vazio_devolve_lista_vazia(criar_arquivo):
    caminho = criar_arquivo("")
    assert ex.ler_medicoes(caminho) == []


def test_linha_invalida_informa_o_numero_da_linha(criar_arquivo):
    caminho = criar_arquivo("25,4\n\nabc\n25,1\n")
    with pytest.raises(ValueError, match="linha 3") as excinfo:
        ex.ler_medicoes(caminho)
    assert str(excinfo.value) == "linha 3: valor inválido 'abc'"


def test_mensagem_mostra_a_linha_sem_espacos(criar_arquivo):
    caminho = criar_arquivo("# cabeçalho\n  12,5 mm  \n")
    with pytest.raises(ValueError) as excinfo:
        ex.ler_medicoes(caminho)
    assert str(excinfo.value) == "linha 2: valor inválido '12,5 mm'"


def test_arquivo_inexistente_levanta_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        ex.ler_medicoes(tmp_path / "nao_existe.txt")
