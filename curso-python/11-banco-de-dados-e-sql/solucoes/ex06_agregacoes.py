"""
Exercício 11.06 — Funções de agregação (SOLUÇÃO)
"""

import sqlite3


def resumo_caracteristica(conexao: sqlite3.Connection, caracteristica: str) -> dict:
    """Quantidade, média, mínimo e máximo dos valores medidos."""
    sql = """
        SELECT COUNT(valor), ROUND(AVG(valor), 2), MIN(valor), MAX(valor)
        FROM ensaio
        WHERE caracteristica = ?
    """
    # Sem GROUP BY, a agregação devolve exatamente UMA linha, mesmo sem dados:
    # COUNT dá 0 e AVG/MIN/MAX dão NULL (None no Python). Já é o que queremos.
    n, media, minimo, maximo = conexao.execute(sql, (caracteristica,)).fetchone()
    return {"n": n, "media": media, "minimo": minimo, "maximo": maximo}


def peso_expedido(conexao: sqlite3.Connection, op: int | None = None) -> float:
    """Peso total expedido (de todas as OPs ou de uma)."""
    # Truque para filtro opcional sem montar SQL com if: quando o parâmetro é
    # NULL, a condição "? IS NULL" é verdadeira e o filtro some.
    sql = """
        SELECT COALESCE(SUM(peso_kg), 0)
        FROM expedicao
        WHERE (? IS NULL OR op = ?)
    """
    (total,) = conexao.execute(sql, (op, op)).fetchone()
    return float(total)  # COALESCE(..., 0) devolve o inteiro 0; float() padroniza
    # Alternativa: TOTAL(peso_kg), que é o SUM do SQLite que devolve 0.0 em vez de NULL.
