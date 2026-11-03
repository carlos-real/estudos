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
from collections.abc import Mapping
from pathlib import Path


def ler_registros(caminho: Path) -> list[dict]:
    """Lê o CSV de ensaios e converte data e valor."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def criar_parser(ambiente: Mapping[str, str] | None = None) -> argparse.ArgumentParser:
    """Parser do relatório; o CV máximo padrão vem do ambiente."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def main(argv: list[str] | None = None, ambiente: Mapping[str, str] | None = None) -> int:
    """Roda o relatório e devolve o código de saída (0, 1 ou 2)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
