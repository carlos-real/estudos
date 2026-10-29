"""Relatório de estabilidade por linha de produção (exemplo "No mundo real").

Lê o CSV de ensaios do laboratório (padrão Excel BR: ';' e vírgula decimal), filtra
por ensaio e período, calcula média, desvio padrão e CV% por linha e conta as
reprovações. Devolve código de saída 1 se alguma linha passar do CV máximo.

Rode com (na pasta curso-python):
    python 07-modulos-e-biblioteca-padrao/exemplos/12_relatorio_linhas.py
    python 07-modulos-e-biblioteca-padrao/exemplos/12_relatorio_linhas.py --ensaio gramatura
    python 07-modulos-e-biblioteca-padrao/exemplos/12_relatorio_linhas.py --desde 01/10/2026 --ate 15/10/2026
"""

import argparse
import csv
import os
import statistics
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

PASTA_DADOS = Path(__file__).resolve().parent.parent / "dados"
ARQUIVO_PADRAO = PASTA_DADOS / "ensaios_linhas.csv"


def data_br(texto: str) -> date:
    """Tipo para o argparse: '29/10/2026' -> date. Erro vira mensagem amigável."""
    try:
        return datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"data inválida: {texto!r} (use dd/mm/aaaa)") from None


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="relatorio_linhas",
        description="Estatística de ensaios por linha de produção.",
    )
    parser.add_argument("arquivo", nargs="?", type=Path, default=ARQUIVO_PADRAO)
    parser.add_argument("--ensaio", default="espessura", choices=["espessura", "gramatura", "cof"])
    parser.add_argument("--linha", type=str.upper, choices=["A", "B", "C", "D"])
    parser.add_argument("--desde", type=data_br, help="data inicial (dd/mm/aaaa)")
    parser.add_argument("--ate", type=data_br, help="data final (dd/mm/aaaa)")
    padrao_cv = float(os.environ.get("LAB_CV_MAX", "5.0"))
    parser.add_argument("--cv-max", type=float, default=padrao_cv, help="CV%% máximo")
    return parser


def ler_ensaios(caminho: Path) -> list[dict]:
    """Lê o CSV e já converte data e valor para os tipos certos."""
    registros = []
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        for linha in csv.DictReader(arquivo, delimiter=";"):
            registros.append(
                {
                    "data": datetime.strptime(linha["data"], "%d/%m/%Y").date(),
                    "op": linha["op"],
                    "linha": linha["linha"],
                    "ensaio": linha["ensaio"],
                    "valor": float(linha["valor"].replace(",", ".")),
                    "resultado": linha["resultado"],
                }
            )
    return registros


def no_periodo(registro: dict, desde: date | None, ate: date | None) -> bool:
    if desde and registro["data"] < desde:
        return False
    if ate and registro["data"] > ate:
        return False
    return True


def main(argv: list[str] | None = None) -> int:
    args = criar_parser().parse_args(argv)
    try:
        registros = ler_ensaios(args.arquivo)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {args.arquivo}", file=sys.stderr)
        return 2

    filtrados = [
        r
        for r in registros
        if no_periodo(r, args.desde, args.ate) and (args.linha is None or r["linha"] == args.linha)
    ]
    valores_por_linha = defaultdict(list)
    for r in filtrados:
        if r["ensaio"] == args.ensaio:
            valores_por_linha[r["linha"]].append(r["valor"])
    reprovacoes = Counter(r["linha"] for r in filtrados if r["resultado"] == "reprovado")

    if not valores_por_linha:
        print("Nenhum registro encontrado com esses filtros.", file=sys.stderr)
        return 2

    datas = [r["data"] for r in filtrados]
    print(f"Ensaio: {args.ensaio} | período: {min(datas):%d/%m/%Y} a {max(datas):%d/%m/%Y}")
    print(f"{'Linha':<6}{'n':>3}{'Média':>9}{'Desvio':>8}{'CV%':>7}  Situação")
    alertas = 0
    for linha in sorted(valores_por_linha):
        valores = valores_por_linha[linha]
        media = statistics.mean(valores)
        desvio = statistics.stdev(valores) if len(valores) > 1 else 0.0
        cv = desvio / media * 100
        situacao = "ALERTA: CV alto" if cv > args.cv_max else "estável"
        if cv > args.cv_max:
            alertas += 1
        print(f"{linha:<6}{len(valores):>3}{media:>9.2f}{desvio:>8.2f}{cv:>7.2f}  {situacao}")

    print("\nReprovações no período (todos os ensaios):")
    for linha, quantidade in reprovacoes.most_common():
        print(f"  Linha {linha}: {quantidade}")
    if not reprovacoes:
        print("  nenhuma")
    return 1 if alertas else 0


if __name__ == "__main__":
    sys.exit(main())
