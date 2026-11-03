"""
Exercício 11.12 — O banco de regras do projeto final (SOLUÇÃO)

Decomposição: cada função resolve um pedaço e a próxima reaproveita a anterior.
  especificacao_da_op  -> "qual especificação vale?" (e erro claro se não houver)
  tolerancias_efetivas -> "quais tolerâncias valem?" (padrão + cliente por cima)
  limites              -> "qual a faixa numérica?" (pura, sem banco: fácil de testar)
"""

import sqlite3

COLUNAS = ("tipo", "minimo", "maximo", "percentual")


def _padrao_da_linha(conexao: sqlite3.Connection, linha: str) -> tuple[str, str]:
    linha_banco = conexao.execute(
        "SELECT titulo, texto FROM especificacao WHERE linha = ?", (linha,)
    ).fetchone()
    if linha_banco is None:
        raise LookupError(f"linha {linha!r} sem especificação padrão cadastrada")
    return linha_banco


def especificacao_da_op(
    conexao: sqlite3.Connection, linha: str, titulo: str | None = None
) -> tuple[str, str]:
    """(titulo, texto) da especificação que vale para a OP."""
    if titulo is None or not titulo.strip():
        return _padrao_da_linha(conexao, linha)
    # Comparação "tolerante" feita pelo próprio banco: sem maiúsculas e sem espaços
    # nas pontas. O título continua sendo parâmetro (?), nunca f-string.
    linha_banco = conexao.execute(
        "SELECT titulo, texto FROM especificacao WHERE UPPER(TRIM(titulo)) = UPPER(TRIM(?))",
        (titulo,),
    ).fetchone()
    if linha_banco is None:
        raise LookupError(f"especificação {titulo.strip()!r} não cadastrada")
    return linha_banco


def _tolerancias_do_titulo(conexao: sqlite3.Connection, titulo: str) -> dict[str, dict]:
    sql = """
        SELECT caracteristica, tipo, minimo, maximo, percentual
        FROM tolerancia
        WHERE titulo = ?
    """
    resultado = {}
    for caracteristica, *valores in conexao.execute(sql, (titulo,)):
        resultado[caracteristica] = dict(zip(COLUNAS, valores, strict=True))
        resultado[caracteristica]["origem"] = titulo
    return resultado


def tolerancias_efetivas(
    conexao: sqlite3.Connection, linha: str, titulo: str | None = None
) -> dict[str, dict]:
    """Tolerâncias do padrão da linha, sobrescritas pelas da especificação."""
    titulo_padrao, _ = _padrao_da_linha(conexao, linha)
    efetivas = _tolerancias_do_titulo(conexao, titulo_padrao)
    if titulo is not None and titulo.strip():
        titulo_cliente, _ = especificacao_da_op(conexao, linha, titulo)  # LookupError
        # dict.update: as características da especificação "vencem" as do padrão
        efetivas.update(_tolerancias_do_titulo(conexao, titulo_cliente))
    return efetivas
    # Alternativa numa consulta só (veja a aula): as do cliente UNION ALL as do
    # padrão cuja característica NOT IN (as do cliente).


def limites(
    tolerancia: dict, nominal: float | None = None
) -> tuple[float | None, float | None]:
    """(minimo, maximo) de uma tolerância fixa ou nominal ± %."""
    if tolerancia["tipo"] == "fixa":
        return tolerancia["minimo"], tolerancia["maximo"]
    if nominal is None or nominal <= 0:
        raise ValueError("tolerância nominal precisa de um valor nominal maior que zero")
    folga = nominal * tolerancia["percentual"] / 100
    # round(…, 4) evita 27.599999999999998 no relatório
    return round(nominal - folga, 4), round(nominal + folga, 4)
