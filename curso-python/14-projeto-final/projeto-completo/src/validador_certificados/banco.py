"""Leitura do banco de regras (SQLite).

O banco é só lido aqui. Quem cadastra regras usa um editor como o DB Browser for
SQLite, ou um script próprio. O schema está em sql/schema.sql.
"""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

from .modelos import Especificacao, Tolerancia

logger = logging.getLogger(__name__)


def carregar_especificacoes(conexao: sqlite3.Connection) -> dict[str, Especificacao]:
    """Lê especificações e tolerâncias e devolve {titulo: Especificacao}."""
    especificacoes: dict[str, Especificacao] = {}
    for titulo, texto, linha in conexao.execute(
        "SELECT titulo, texto, linha FROM especificacao ORDER BY titulo"
    ):
        especificacoes[titulo] = Especificacao(titulo=titulo, texto=texto, linha=linha or "")
    consulta = """
        SELECT titulo, caracteristica, tipo, minimo, maximo, percentual
        FROM tolerancia
        ORDER BY titulo, caracteristica
    """
    for titulo, caracteristica, tipo, minimo, maximo, percentual in conexao.execute(consulta):
        especificacoes[titulo].tolerancias[caracteristica] = Tolerancia(
            caracteristica=caracteristica,
            tipo=tipo,
            minimo=minimo,
            maximo=maximo,
            percentual=percentual,
        )
    return especificacoes


def abrir_somente_leitura(caminho: Path) -> sqlite3.Connection:
    """Abre o banco só para leitura.

    sqlite3.connect("caminho_errado.db") CRIA um banco vazio sem avisar. Com
    mode=ro, um caminho errado vira erro na hora, com mensagem clara.
    """
    caminho = Path(caminho)
    if not caminho.is_file():
        raise FileNotFoundError(f"banco de regras não encontrado: {caminho}")
    return sqlite3.connect(f"{caminho.resolve().as_uri()}?mode=ro", uri=True)


def carregar_do_arquivo(caminho: Path) -> dict[str, Especificacao]:
    """Abre o arquivo .db, carrega as especificações e fecha a conexão."""
    conexao = abrir_somente_leitura(caminho)
    try:
        especificacoes = carregar_especificacoes(conexao)
    finally:
        conexao.close()
    logger.info("regras: %d especificações carregadas de %s", len(especificacoes), caminho)
    return especificacoes
