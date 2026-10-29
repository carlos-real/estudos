"""Fixtures compartilhadas pelos testes."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent

# Com `pip install -e .` (ou pelo `pythonpath = ["src"]` do pyproject) isto não é
# necessário. Fica aqui para os testes rodarem também a partir da raiz do curso.
if str(RAIZ / "src") not in sys.path:
    sys.path.insert(0, str(RAIZ / "src"))

from validador_certificados.modelos import Especificacao, Medicao, Tolerancia  # noqa: E402


@pytest.fixture
def pasta_dados() -> Path:
    return RAIZ / "dados"


@pytest.fixture
def conexao_regras():
    """Banco em memória com o schema real e duas especificações."""
    conexao = sqlite3.connect(":memory:")
    conexao.executescript((RAIZ / "sql" / "schema.sql").read_text(encoding="utf-8"))
    conexao.executemany(
        "INSERT INTO linha VALUES (?, ?)", [("A", "Extrusora 1"), ("C", "Coextrusora")]
    )
    conexao.executemany(
        "INSERT INTO especificacao VALUES (?, ?, ?)",
        [("PADRAO-A", "Padrão A", "A"), ("ESP-0412", "Café 250 g", None)],
    )
    conexao.executemany(
        "INSERT INTO tolerancia VALUES (?, ?, ?, ?, ?, ?)",
        [
            ("PADRAO-A", "espessura", "nominal", None, None, 10.0),
            ("PADRAO-A", "cof", "fixa", 0.15, 0.35, None),
            ("PADRAO-A", "selagem", "fixa", 8.0, None, None),
            ("ESP-0412", "cof", "fixa", 0.18, 0.25, None),
        ],
    )
    yield conexao
    conexao.close()


@pytest.fixture
def especificacoes() -> dict[str, Especificacao]:
    """Padrões das linhas A e C + uma especificação de cliente."""
    return {
        "PADRAO-A": Especificacao(
            "PADRAO-A",
            linha="A",
            tolerancias={
                "espessura": Tolerancia("espessura", "nominal", percentual=10.0),
                "cof": Tolerancia("cof", "fixa", minimo=0.15, maximo=0.35),
                "selagem": Tolerancia("selagem", "fixa", minimo=8.0),
            },
        ),
        "PADRAO-C": Especificacao(
            "PADRAO-C",
            linha="C",
            tolerancias={
                "espessura": Tolerancia("espessura", "nominal", percentual=8.0),
                "cof": Tolerancia("cof", "fixa", minimo=0.10, maximo=0.30),
                "selagem": Tolerancia("selagem", "fixa", minimo=10.0),
            },
        ),
        "ESP-0412": Especificacao(
            "ESP-0412",
            texto="Café 250 g",
            tolerancias={
                "cof": Tolerancia("cof", "fixa", minimo=0.18, maximo=0.25),
                "selagem": Tolerancia("selagem", "fixa", minimo=12.0),
            },
        ),
    }


@pytest.fixture
def nova_medicao():
    """Fábrica de Medicao válida (linha A, aprovada e liberada); mude só o que precisar."""

    def fabricar(**mudancas) -> Medicao:
        dados = {
            "op": "24518",
            "aba": "Linha A",
            "linha": "A",
            "valores": {"espessura": 41.2, "cof": 0.22, "selagem": 9.8},
            "nominais": {"espessura": 40.0},
            "especificacao": "",
            "observacao": "COF: liberado",
        }
        dados.update(mudancas)
        return Medicao(**dados)

    return fabricar
