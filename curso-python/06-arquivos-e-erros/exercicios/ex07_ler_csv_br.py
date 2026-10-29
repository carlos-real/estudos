"""
Exercício 06.07 — Ler CSV do Excel brasileiro
Nível: ★★☆

Contexto: A planilha de medições é exportada pelo Excel como "CSV UTF-8":
separador ";", vírgula decimal e BOM no começo. Você quer cada linha como um
dicionário, com os números já em float.

    lote;linha;espessura;observacao
    A-0153;A;25,4;COF: liberado
    A-0154;A;;"Selagem; refazer"

Tarefa: implemente `ler_csv_br(caminho, colunas_numericas)`:
- abra com encoding "utf-8-sig" e newline="" e use csv.DictReader com
  delimiter=";";
- tire os espaços das pontas dos nomes das colunas e dos valores;
- nas colunas listadas em `colunas_numericas`, converta o número brasileiro
  para float; célula vazia vira None;
- as outras colunas continuam como texto;
- devolva a lista de dicionários, um por linha de dados.

Exemplos (com o arquivo acima):
    >>> linhas = ler_csv_br(Path("medicoes.csv"), ["espessura"])
    >>> linhas[0]
    {'lote': 'A-0153', 'linha': 'A', 'espessura': 25.4, 'observacao': 'COF: liberado'}
    >>> linhas[1]["espessura"], linhas[1]["observacao"]
    (None, 'Selagem; refazer')

Dica: monte um dicionário novo para cada linha, percorrendo `linha.items()`.
Repare que o csv já cuida do ";" que está entre aspas.

Teste com:  python curso.py testar 06 ex07
"""

# Este exercício usa o módulo csv.
# Apague o "# " do começo da linha abaixo para importá-lo:
# import csv
from pathlib import Path


def ler_csv_br(caminho: Path, colunas_numericas: list[str]) -> list[dict]:
    """Lê um CSV do Excel brasileiro e converte as colunas numéricas."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
