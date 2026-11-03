"""Desafio do módulo 11 — Banco de regras do laboratório (solução de referência).

Uma ferramenta de linha de comando para criar, consultar e usar o banco de regras
do Validador de Certificados (o mesmo schema do projeto final).

Uso (na pasta curso-python):
    python 11-banco-de-dados-e-sql/desafio/solucao_referencia.py            (demonstração)
    python 11-banco-de-dados-e-sql/desafio/solucao_referencia.py criar
    python 11-banco-de-dados-e-sql/desafio/solucao_referencia.py listar
    python 11-banco-de-dados-e-sql/desafio/solucao_referencia.py regras --linha A \\
        --especificacao ESP-0533 --nominal espessura=60 --nominal gramatura=55.5
    python 11-banco-de-dados-e-sql/desafio/solucao_referencia.py conferir --linha A \\
        --especificacao ESP-0533 --nominal espessura=60 --valor espessura=63.4 \\
        --valor cof=0.28

O banco padrão fica em 11-banco-de-dados-e-sql/saida/regras.db (use --banco).
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

PASTA_MODULO = Path(__file__).resolve().parent.parent
SCRIPT_SQL = PASTA_MODULO / "dados" / "regras.sql"
BANCO_PADRAO = PASTA_MODULO / "saida" / "regras.db"


# --------------------------------------------------------------------------- banco
def criar_banco(conexao: sqlite3.Connection) -> None:
    conexao.executescript(SCRIPT_SQL.read_text(encoding="utf-8"))
    conexao.commit()


def abrir_existente(caminho: Path) -> sqlite3.Connection:
    """Abre só se o arquivo existir (connect() criaria um banco vazio sem avisar)."""
    if not caminho.is_file():
        raise FileNotFoundError(f"banco não encontrado: {caminho} (rode o comando 'criar')")
    return sqlite3.connect(caminho)


def listar(conexao: sqlite3.Connection) -> list[tuple[str, str, int]]:
    sql = """
        SELECT e.titulo, COALESCE(e.linha, '-') AS linha, COUNT(t.caracteristica) AS qtd
        FROM especificacao AS e
        LEFT JOIN tolerancia AS t ON t.titulo = e.titulo
        GROUP BY e.titulo, e.linha
        ORDER BY e.linha IS NULL, e.linha, e.titulo
    """
    return conexao.execute(sql).fetchall()


def especificacao(conexao: sqlite3.Connection, linha: str, titulo: str | None) -> str:
    """Título da especificação que vale (padrão da linha se titulo vier vazio)."""
    if titulo and titulo.strip():
        linha_banco = conexao.execute(
            "SELECT titulo FROM especificacao WHERE UPPER(TRIM(titulo)) = UPPER(TRIM(?))",
            (titulo,),
        ).fetchone()
        if linha_banco is None:
            raise LookupError(f"especificação {titulo.strip()!r} não cadastrada")
        return linha_banco[0]
    linha_banco = conexao.execute(
        "SELECT titulo FROM especificacao WHERE linha = ?", (linha,)
    ).fetchone()
    if linha_banco is None:
        raise LookupError(f"linha {linha!r} sem padrão cadastrado")
    return linha_banco[0]


EFETIVAS = """
    SELECT caracteristica, tipo, minimo, maximo, percentual, titulo
    FROM tolerancia
    WHERE titulo = :titulo
    UNION ALL
    SELECT t.caracteristica, t.tipo, t.minimo, t.maximo, t.percentual, t.titulo
    FROM tolerancia AS t
    JOIN especificacao AS e ON e.titulo = t.titulo
    WHERE e.linha = :linha
      AND t.caracteristica NOT IN (
          SELECT caracteristica FROM tolerancia WHERE titulo = :titulo
      )
    ORDER BY caracteristica
"""


def tolerancias_efetivas(
    conexao: sqlite3.Connection, linha: str, titulo: str | None
) -> list[tuple[str, str, float | None, float | None, float | None, str]]:
    especificacao(conexao, linha, None)  # confere se a linha tem padrão
    escolhida = especificacao(conexao, linha, titulo)
    return conexao.execute(EFETIVAS, {"linha": linha, "titulo": escolhida}).fetchall()


def limites(
    tipo: str, minimo: float | None, maximo: float | None, percentual: float | None,
    nominal: float | None,
) -> tuple[float | None, float | None]:  # fmt: skip
    if tipo == "fixa":
        return minimo, maximo
    if nominal is None or nominal <= 0:
        return None, None  # sem nominal não dá para calcular a faixa
    folga = nominal * percentual / 100
    return round(nominal - folga, 4), round(nominal + folga, 4)


def conferir(
    conexao: sqlite3.Connection,
    linha: str,
    titulo: str | None,
    valores: dict[str, float],
    nominais: dict[str, float],
) -> list[str]:
    """Devolve a lista de motivos de reprovação (vazia = aprovada)."""
    motivos = []
    for carac, tipo, minimo, maximo, pct, _ in tolerancias_efetivas(conexao, linha, titulo):
        if carac not in valores:
            continue  # característica não medida neste lote
        valor = valores[carac]
        if tipo == "nominal" and carac not in nominais:
            motivos.append(f"{carac}: falta o valor nominal")
            continue
        lim_min, lim_max = limites(tipo, minimo, maximo, pct, nominais.get(carac))
        if lim_min is not None and valor < lim_min:
            motivos.append(f"{carac} {valor:g} abaixo do mínimo {lim_min:g}")
        if lim_max is not None and valor > lim_max:
            motivos.append(f"{carac} {valor:g} acima do máximo {lim_max:g}")
    return motivos


# --------------------------------------------------------------------------- saída
def numero(valor: float | None) -> str:
    return "-" if valor is None else f"{valor:g}".replace(".", ",")


def imprimir_regras(conexao, linha, titulo, nominais) -> None:
    print(f"Linha {linha}, especificação {especificacao(conexao, linha, titulo)}")
    print(f"{'característica':<15} {'tipo':<8} {'mínimo':>8} {'máximo':>8}  origem")
    for carac, tipo, minimo, maximo, pct, origem in tolerancias_efetivas(
        conexao, linha, titulo
    ):
        lim_min, lim_max = limites(tipo, minimo, maximo, pct, nominais.get(carac))
        if tipo == "nominal" and carac not in nominais:
            faixa = f"{'nominal ± ' + numero(pct) + '%':>17}"
        else:
            faixa = f"{numero(lim_min):>8} {numero(lim_max):>8}"
        print(f"{carac:<15} {tipo:<8} {faixa}  {origem}")


def pares(textos: list[str] | None) -> dict[str, float]:
    """['espessura=60', 'cof=0,28'] -> {'espessura': 60.0, 'cof': 0.28}"""
    resultado = {}
    for texto in textos or []:
        nome, sep, valor = texto.partition("=")
        if not sep:
            raise ValueError(f"use nome=valor, recebi {texto!r}")
        resultado[nome.strip().lower()] = float(valor.replace(",", "."))
    return resultado


# --------------------------------------------------------------------------- CLI
def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Banco de regras do laboratório.")
    parser.add_argument("--banco", type=Path, default=BANCO_PADRAO, help="arquivo .db")
    sub = parser.add_subparsers(dest="comando")
    p_criar = sub.add_parser("criar", help="cria o banco com as regras de exemplo")
    p_criar.add_argument("--forcar", action="store_true", help="apaga o banco existente")
    sub.add_parser("listar", help="lista as especificações")
    for nome in ("regras", "conferir"):
        p = sub.add_parser(nome)
        p.add_argument("--linha", required=True, choices=["A", "B", "C", "D"])
        p.add_argument("--especificacao", help="título (vazio = padrão da linha)")
        p.add_argument("--nominal", action="append", help="caracteristica=valor nominal")
        if nome == "conferir":
            p.add_argument(
                "--valor", action="append", required=True, help="caracteristica=valor"
            )
    return parser


def executar(conexao: sqlite3.Connection, args: argparse.Namespace) -> int:
    if args.comando == "listar":
        for titulo, linha, qtd in listar(conexao):
            print(f"{titulo:<10} linha {linha}  {qtd} tolerância(s)")
    elif args.comando == "regras":
        imprimir_regras(conexao, args.linha, args.especificacao, pares(args.nominal))
    elif args.comando == "conferir":
        motivos = conferir(
            conexao, args.linha, args.especificacao, pares(args.valor), pares(args.nominal)
        )
        print("REPROVADA" if motivos else "APROVADA")
        for motivo in motivos:
            print(f"  - {motivo}")
        return 2 if motivos else 0
    return 0


def demonstracao() -> None:
    """Sem argumentos: roda tudo num banco na memória, sem criar arquivos."""
    with closing(sqlite3.connect(":memory:")) as conexao:
        criar_banco(conexao)
        parser = criar_parser()
        comandos = [
            ["listar"],
            ["regras", "--linha", "A", "--especificacao", "esp-0533", "--nominal",
             "espessura=60", "--nominal", "gramatura=55,5"],
            ["conferir", "--linha", "A", "--especificacao", "ESP-0533", "--nominal",
             "espessura=60", "--valor", "espessura=63,4", "--valor", "cof=0,28"],
        ]  # fmt: skip
        for comando in comandos:
            print(f"$ ... {' '.join(comando)}")
            executar(conexao, parser.parse_args(comando))
            print()


def main(argv: list[str] | None = None) -> int:
    args = criar_parser().parse_args(argv)
    if args.comando is None:
        demonstracao()
        return 0
    try:
        if args.comando == "criar":
            if args.banco.exists() and not args.forcar:
                print(f"Erro: {args.banco} já existe (use --forcar)", file=sys.stderr)
                return 1
            args.banco.parent.mkdir(parents=True, exist_ok=True)
            args.banco.unlink(missing_ok=True)
            with closing(sqlite3.connect(args.banco)) as conexao:
                criar_banco(conexao)
            print(f"Banco criado: {args.banco}")
            return 0
        with closing(abrir_existente(args.banco)) as conexao:
            return executar(conexao, args)
    except (FileNotFoundError, LookupError, ValueError) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
