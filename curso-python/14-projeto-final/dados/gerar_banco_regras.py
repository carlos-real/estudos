"""Gera o banco de regras de exemplo: dados/regras.db.

Uso (na pasta curso-python):
    python 14-projeto-final/dados/gerar_banco_regras.py

O schema fica em schema_regras.sql (mesma pasta). O script apaga o banco antigo e
cria tudo de novo, então pode rodar quantas vezes quiser.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

PASTA = Path(__file__).resolve().parent
SCHEMA = PASTA / "schema_regras.sql"
DESTINO = PASTA / "regras.db"

LINHAS = [
    ("A", "Extrusora 1 - filmes PE monocamada"),
    ("B", "Extrusora 2 - filmes PE finos"),
    ("C", "Coextrusora 3 camadas"),
    ("D", "Laminadora - PET/PE e BOPP/PE"),
]

# (titulo, texto, linha)  -> linha preenchida = padrão da linha
ESPECIFICACOES = [
    ("PADRAO-A", "Padrão da linha A (filmes PE monocamada).", "A"),
    ("PADRAO-B", "Padrão da linha B (filmes PE finos).", "B"),
    ("PADRAO-C", "Padrão da linha C (coextrusados 3 camadas).", "C"),
    ("PADRAO-D", "Padrão da linha D (laminados).", "D"),
    (
        "ESP-0412",
        "Torrefação Serra - embalagem de café 250 g. "
        "COF interno de 0,18 a 0,25; selagem mínima 12 N/15mm.",
        None,
    ),
    (
        "ESP-0533",
        "Agro Campo - sacaria de ração 15 kg. Espessura nominal ± 5%; tração mínima 28 MPa.",
        None,
    ),
    (
        "ESP-0618",
        "Biscoitos Aurora - filme para biscoito. COF de 0,12 a 0,22; gramatura ± 5%.",
        None,
    ),
]

# (titulo, caracteristica, tipo, minimo, maximo, percentual)
TOLERANCIAS = [
    ("PADRAO-A", "espessura", "nominal", None, None, 10.0),
    ("PADRAO-A", "gramatura", "nominal", None, None, 10.0),
    ("PADRAO-A", "cof", "fixa", 0.15, 0.35, None),
    ("PADRAO-A", "tracao", "fixa", 20.0, None, None),
    ("PADRAO-A", "selagem", "fixa", 8.0, None, None),
    ("PADRAO-B", "espessura", "nominal", None, None, 10.0),
    ("PADRAO-B", "gramatura", "nominal", None, None, 10.0),
    ("PADRAO-B", "cof", "fixa", 0.20, 0.40, None),
    ("PADRAO-B", "tracao", "fixa", 18.0, None, None),
    ("PADRAO-B", "selagem", "fixa", 6.0, None, None),
    ("PADRAO-C", "espessura", "nominal", None, None, 8.0),
    ("PADRAO-C", "gramatura", "nominal", None, None, 8.0),
    ("PADRAO-C", "cof", "fixa", 0.10, 0.30, None),
    ("PADRAO-C", "tracao", "fixa", 25.0, None, None),
    ("PADRAO-C", "selagem", "fixa", 10.0, None, None),
    ("PADRAO-D", "espessura", "nominal", None, None, 7.0),
    ("PADRAO-D", "gramatura", "nominal", None, None, 7.0),
    ("PADRAO-D", "cof", "fixa", 0.15, 0.30, None),
    ("PADRAO-D", "tracao", "fixa", 30.0, None, None),
    ("PADRAO-D", "selagem", "fixa", 12.0, None, None),
    ("ESP-0412", "cof", "fixa", 0.18, 0.25, None),
    ("ESP-0412", "selagem", "fixa", 12.0, None, None),
    ("ESP-0533", "espessura", "nominal", None, None, 5.0),
    ("ESP-0533", "tracao", "fixa", 28.0, None, None),
    ("ESP-0618", "cof", "fixa", 0.12, 0.22, None),
    ("ESP-0618", "gramatura", "nominal", None, None, 5.0),
]


def gerar(destino: Path = DESTINO) -> Path:
    """Cria o banco do zero e devolve o caminho."""
    destino.unlink(missing_ok=True)
    conexao = sqlite3.connect(destino)
    try:
        with conexao:  # commit no fim (ou rollback se der erro)
            conexao.executescript(SCHEMA.read_text(encoding="utf-8"))
            conexao.executemany("INSERT INTO linha VALUES (?, ?)", LINHAS)
            conexao.executemany("INSERT INTO especificacao VALUES (?, ?, ?)", ESPECIFICACOES)
            conexao.executemany(
                "INSERT INTO tolerancia VALUES (?, ?, ?, ?, ?, ?)", TOLERANCIAS
            )
    finally:
        conexao.close()
    return destino


if __name__ == "__main__":
    caminho = gerar()
    print(f"Banco gerado: {caminho.name}")
    print(f"  {len(LINHAS)} linhas, {len(ESPECIFICACOES)} especificações, "
          f"{len(TOLERANCIAS)} tolerâncias")
