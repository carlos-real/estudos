"""Solução de referência do desafio do módulo 07: agenda de validade de laudos.

Rode com (na pasta curso-python):
    python 07-modulos-e-biblioteca-padrao/desafio/solucao_referencia.py --hoje 29/10/2026
    python 07-modulos-e-biblioteca-padrao/desafio/solucao_referencia.py --janela 7 --estrito
    python 07-modulos-e-biblioteca-padrao/desafio/solucao_referencia.py --help

Sem --hoje, usa a data de hoje do computador. Sem arquivo, usa dados/laudos.csv.
A janela padrão vem da variável de ambiente LAB_JANELA_DIAS (ou 30 dias).

Código de saída: 0 = ok; 2 = erro de entrada; com --estrito, 1 quando houver vencidos
(útil no Agendador de Tarefas do Windows, que marca a execução como falha).

Organização: cada bloco abaixo poderia ser um módulo de um pacote `agenda_laudos/`
(datas.py, leitura.py, relatorio.py, cli.py e __main__.py). Ficou num arquivo só
para você ler de cima para baixo.
"""

import argparse
import csv
import json
import os
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

PASTA_MODULO = Path(__file__).resolve().parent.parent
ARQUIVO_PADRAO = PASTA_MODULO / "dados" / "laudos.csv"
DIAS_DA_SEMANA = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]


# --- datas ------------------------------------------------------------------
def data_br(texto: str) -> date:
    """'29/10/2026' -> date. Serve também como type= do argparse."""
    try:
        return datetime.strptime(texto.strip(), "%d/%m/%Y").date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"data inválida: {texto!r} (use dd/mm/aaaa)"
        ) from None


def descrever_prazo(dias: int) -> str:
    """Texto amigável para a distância até o vencimento."""
    if dias == 0:
        return "hoje"
    if dias == 1:
        return "amanhã"
    if dias > 1:
        return f"em {dias} dias"
    return f"há {-dias} dia" + ("s" if dias < -1 else "")


# --- leitura ----------------------------------------------------------------
def ler_laudos(caminho: Path) -> list[dict]:
    """Lê o CSV de laudos e calcula vencimento de cada um."""
    laudos = []
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        for numero, linha in enumerate(csv.DictReader(arquivo, delimiter=";"), start=2):
            try:
                emissao = data_br(linha["emissao"])
                validade = int(linha["validade_dias"])
            except (argparse.ArgumentTypeError, ValueError) as erro:
                print(f"Linha {numero} ignorada: {erro}", file=sys.stderr)
                continue
            laudos.append(
                {
                    "op": linha["op"],
                    "cliente": linha["cliente"],
                    "produto": linha["produto"],
                    "emissao": emissao,
                    "vencimento": emissao + timedelta(days=validade),
                }
            )
    return laudos


# --- regras -----------------------------------------------------------------
def classificar(laudos: list[dict], hoje: date, janela: int) -> dict[str, list[dict]]:
    """Separa em 'vencidos', 'a_vencer' (dentro da janela) e 'em_dia'."""
    grupos = {"vencidos": [], "a_vencer": [], "em_dia": []}
    for laudo in laudos:
        dias = (laudo["vencimento"] - hoje).days
        item = {**laudo, "dias": dias}  # cópia do dicionário com a chave nova
        if dias < 0:
            grupos["vencidos"].append(item)
        elif dias <= janela:
            grupos["a_vencer"].append(item)
        else:
            grupos["em_dia"].append(item)
    for itens in grupos.values():
        itens.sort(key=lambda item: item["vencimento"])
    return grupos


# --- relatório --------------------------------------------------------------
def imprimir_relatorio(grupos: dict[str, list[dict]], hoje: date, janela: int) -> None:
    print(f"Agenda de laudos em {hoje:%d/%m/%Y} (janela: {janela} dias)\n")
    print(f"VENCIDOS ({len(grupos['vencidos'])})")
    for laudo in grupos["vencidos"]:
        print(
            f"  {laudo['op']}  {laudo['cliente']:<22} venceu em "
            f"{laudo['vencimento']:%d/%m/%Y} ({descrever_prazo(laudo['dias'])})"
        )
    print(f"\nVENCEM EM ATÉ {janela} DIAS ({len(grupos['a_vencer'])})")
    for laudo in grupos["a_vencer"]:
        dia = DIAS_DA_SEMANA[laudo["vencimento"].weekday()]
        print(
            f"  {laudo['op']}  {laudo['cliente']:<22} vence em "
            f"{laudo['vencimento']:%d/%m/%Y}, {dia} ({descrever_prazo(laudo['dias'])})"
        )
    print(f"\nEm dia: {len(grupos['em_dia'])} laudo(s)")

    vencidos = Counter(laudo["cliente"] for laudo in grupos["vencidos"])
    a_vencer = Counter(laudo["cliente"] for laudo in grupos["a_vencer"])
    clientes = sorted(set(vencidos) | set(a_vencer))
    if clientes:
        print("\nPor cliente (vencidos / a vencer):")
        for cliente in clientes:
            print(f"  {cliente:<22} {vencidos[cliente]} / {a_vencer[cliente]}")


def salvar_json(grupos: dict[str, list[dict]], caminho: Path) -> None:
    """Extra: grava o resultado em JSON (datas viram texto dd/mm/aaaa)."""
    saida = {
        nome: [
            {
                **laudo,
                "emissao": f"{laudo['emissao']:%d/%m/%Y}",
                "vencimento": f"{laudo['vencimento']:%d/%m/%Y}",
            }
            for laudo in itens
        ]
        for nome, itens in grupos.items()
    }
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(saida, arquivo, ensure_ascii=False, indent=2)


# --- linha de comando -------------------------------------------------------
def criar_parser() -> argparse.ArgumentParser:
    janela_padrao = int(os.environ.get("LAB_JANELA_DIAS", "30"))
    parser = argparse.ArgumentParser(
        prog="agenda_laudos",
        description="Mostra laudos vencidos e a vencer.",
        epilog="Código de saída: 0 ok, 1 vencidos (só com --estrito), 2 erro.",
    )
    parser.add_argument("arquivo", nargs="?", type=Path, default=ARQUIVO_PADRAO)
    parser.add_argument("--hoje", type=data_br, default=None, help="data de referência")
    parser.add_argument(
        "--janela", type=int, default=janela_padrao, help="dias de antecedência do alerta"
    )
    parser.add_argument("--cliente", help="filtra pelo nome do cliente (parte do nome)")
    parser.add_argument("--json", type=Path, help="também grava o resultado neste arquivo")
    parser.add_argument(
        "--estrito", action="store_true", help="código de saída 1 se houver vencidos"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = criar_parser().parse_args(argv)
    hoje = args.hoje or date.today()
    try:
        laudos = ler_laudos(args.arquivo)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {args.arquivo}", file=sys.stderr)
        return 2
    if args.cliente:
        filtro = args.cliente.lower()
        laudos = [laudo for laudo in laudos if filtro in laudo["cliente"].lower()]
    grupos = classificar(laudos, hoje, args.janela)
    imprimir_relatorio(grupos, hoje, args.janela)
    if args.json:
        salvar_json(grupos, args.json)
        print(f"\nJSON gravado em {args.json}")
    if args.estrito and grupos["vencidos"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
