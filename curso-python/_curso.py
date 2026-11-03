"""Funções de apoio usadas pelos testes do curso.

Você não precisa mexer neste arquivo. Ele decide se os testes vão conferir
o SEU código (pasta `exercicios/`) ou as soluções oficiais (pasta `solucoes/`).
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from types import ModuleType


def pasta_alvo() -> str:
    """Retorna 'solucoes' quando CURSO_SOLUCOES=1, senão 'exercicios'."""
    return "solucoes" if os.environ.get("CURSO_SOLUCOES") == "1" else "exercicios"


def carregar(arquivo_teste: str, nome: str) -> ModuleType:
    """Carrega o arquivo `<modulo>/<exercicios|solucoes>/<nome>.py`.

    `arquivo_teste` é o `__file__` do teste que está pedindo o exercício.
    """
    pasta_modulo = Path(arquivo_teste).resolve().parent.parent
    sub = pasta_alvo()
    caminho = pasta_modulo / sub / f"{nome}.py"
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo do exercício não encontrado: {caminho}")
    nome_unico = f"curso_{pasta_modulo.name}_{sub}_{nome}".replace("-", "_")
    spec = importlib.util.spec_from_file_location(nome_unico, caminho)
    modulo = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(modulo)
    return modulo
