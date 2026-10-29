"""Fixtures compartilhadas por todos os testes do mini projeto.

O pytest carrega este arquivo sozinho, antes dos testes. Toda fixture definida
aqui pode ser pedida por qualquer teste da pasta tests/, sem import.
"""

import sys
from pathlib import Path

import pytest

# Coloca a pasta do projeto no caminho de importação, para que `import laudo`
# funcione nos testes de qualquer pasta de onde o pytest for chamado.
sys.path.insert(0, str(Path(__file__).resolve().parent))


@pytest.fixture
def medicoes_espessura() -> list[float]:
    """Três medições de espessura (µm) de uma bobina com nominal de 20 µm."""
    return [20.1, 19.8, 20.4]


@pytest.fixture
def arquivo_medicoes(tmp_path: Path, medicoes_espessura: list[float]) -> Path:
    """Cria um arquivo de medições numa pasta temporária e devolve o caminho."""
    caminho = tmp_path / "medicoes.txt"
    linhas = [str(valor).replace(".", ",") for valor in medicoes_espessura]
    caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return caminho
