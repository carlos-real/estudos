"""
Exercício 07.11 — Programa de terminal completo: relatório de CV por linha
Nível: ★★★

Contexto: Você quer rodar, todo fim de turno,
    python relatorio.py ensaios.csv --ensaio espessura --cv-max 5
e ver se alguma linha está instável. O CV máximo padrão pode vir de uma variável de
ambiente (LAB_CV_MAX), para cada computador do laboratório ter o seu.

O CSV (separador ";", vírgula decimal, UTF-8) tem as colunas:
    data;op;linha;ensaio;valor
    01/10/2026;OP245101;A;espessura;20,4
(pode ter colunas a mais, como "resultado": ignore-as.)

Tarefa:
1. `ler_registros(caminho)` lê o CSV e devolve uma lista de dicionários com
   "data" (date), "op" (str), "linha" (str), "ensaio" (str) e "valor" (float).
   Se o arquivo não existir, deixe o FileNotFoundError acontecer.
2. `criar_parser(ambiente=None)` devolve um ArgumentParser (prog="relatorio") com:
   - `arquivo`: posicional, type=Path;
   - `--ensaio`: texto, padrão "espessura";
   - `--cv-max`: float; o padrão é float(ambiente["LAB_CV_MAX"]) se essa chave
     existir, senão 5.0. Se `ambiente` for None, use os.environ.
3. `main(argv=None, ambiente=None)` junta tudo:
   - arquivo inexistente: escreva "Arquivo não encontrado: <arquivo>" no sys.stderr
     e devolva 2;
   - nenhum registro do ensaio pedido: escreva "Nenhum registro de <ensaio>" no
     sys.stderr e devolva 2;
   - para cada linha (em ordem alfabética), imprima EXATAMENTE:
       Linha A: n=3 média=20.10 desvio=0.30 CV=1.49%
     (desvio amostral; com 1 valor só, desvio e CV valem 0.0) e acrescente
     " ALERTA" no fim quando o CV passar de cv_max (maior estrito);
   - devolva 1 se houve algum ALERTA, senão 0.

Exemplo de execução:
    > python relatorio.py ensaios.csv --cv-max 2
    Linha A: n=3 média=20.10 desvio=0.30 CV=1.49%
    Linha C: n=2 média=42.00 desvio=2.83 CV=6.73% ALERTA

Dica: termine o arquivo com o bloco abaixo; ele não roda nos testes (que chamam
main direto), só quando o arquivo é executado no terminal:
    if __name__ == "__main__":
        sys.exit(main())

Teste com:  python curso.py testar 07 ex11
"""

import argparse
import csv
import os
import statistics
import sys
from collections import defaultdict
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path


def ler_registros(caminho: Path) -> list[dict]:
    """Lê o CSV de ensaios e converte data e valor."""
    registros = []
    # newline="" é a recomendação do módulo csv (módulo 06); encoding explícito sempre.
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        for linha in csv.DictReader(arquivo, delimiter=";"):
            registros.append(
                {
                    "data": datetime.strptime(linha["data"], "%d/%m/%Y").date(),
                    "op": linha["op"],
                    "linha": linha["linha"],
                    "ensaio": linha["ensaio"],
                    "valor": float(linha["valor"].replace(".", "").replace(",", ".")),
                }
            )
    return registros


def criar_parser(ambiente: Mapping[str, str] | None = None) -> argparse.ArgumentParser:
    """Parser do relatório; o CV máximo padrão vem do ambiente."""
    # Injetar o ambiente (em vez de ler os.environ lá dentro) deixa a função testável:
    # o teste passa um dicionário; o programa de verdade usa o os.environ.
    if ambiente is None:
        ambiente = os.environ
    padrao_cv = float(ambiente.get("LAB_CV_MAX", "5.0"))

    parser = argparse.ArgumentParser(prog="relatorio", description="CV% por linha.")
    parser.add_argument("arquivo", type=Path, help="CSV de ensaios (; e vírgula decimal)")
    parser.add_argument("--ensaio", default="espessura", help="ensaio a analisar")
    # "--cv-max" vira args.cv_max (o hífen troca por sublinhado)
    parser.add_argument("--cv-max", type=float, default=padrao_cv, help="CV%% máximo")
    return parser


def main(argv: list[str] | None = None, ambiente: Mapping[str, str] | None = None) -> int:
    """Roda o relatório e devolve o código de saída (0, 1 ou 2)."""
    args = criar_parser(ambiente).parse_args(argv)

    try:
        registros = ler_registros(args.arquivo)
    except FileNotFoundError:
        # Mensagens de erro vão para o stderr; o stdout fica só com o relatório.
        print(f"Arquivo não encontrado: {args.arquivo}", file=sys.stderr)
        return 2

    valores_por_linha: dict[str, list[float]] = defaultdict(list)
    for registro in registros:
        if registro["ensaio"] == args.ensaio:
            valores_por_linha[registro["linha"]].append(registro["valor"])

    if not valores_por_linha:
        print(f"Nenhum registro de {args.ensaio}", file=sys.stderr)
        return 2

    houve_alerta = False
    for linha in sorted(valores_por_linha):
        valores = valores_por_linha[linha]
        media = statistics.mean(valores)
        # stdev exige 2 valores: com 1 só, não há variação para medir.
        desvio = statistics.stdev(valores) if len(valores) > 1 else 0.0
        cv = desvio / media * 100 if media else 0.0
        texto = (
            f"Linha {linha}: n={len(valores)} média={media:.2f} "
            f"desvio={desvio:.2f} CV={cv:.2f}%"
        )
        if cv > args.cv_max:
            texto += " ALERTA"
            houve_alerta = True
        print(texto)

    # Código de saída: o Agendador de Tarefas (ou outro script) sabe se deu alerta.
    return 1 if houve_alerta else 0


if __name__ == "__main__":
    sys.exit(main())
