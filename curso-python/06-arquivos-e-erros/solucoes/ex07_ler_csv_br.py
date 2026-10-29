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

import csv
from pathlib import Path


def numero_br(texto: str) -> float:
    """ "1.250,5" -> 1250.5 (módulo 05)."""
    return float(texto.replace(".", "").replace(",", "."))


def ler_csv_br(caminho: Path, colunas_numericas: list[str]) -> list[dict]:
    """Lê um CSV do Excel brasileiro e converte as colunas numéricas."""
    resultado = []
    # newline="" é a recomendação da documentação do csv: o próprio módulo
    # cuida das quebras de linha (inclusive as que ficam dentro de aspas).
    with open(caminho, encoding="utf-8-sig", newline="") as arquivo:
        for linha in csv.DictReader(arquivo, delimiter=";"):
            limpa = {}
            for coluna, valor in linha.items():
                coluna = coluna.strip()
                valor = valor.strip()
                if coluna in colunas_numericas:
                    # Expressão condicional: vazio vira None; o resto, float.
                    valor = numero_br(valor) if valor else None
                limpa[coluna] = valor
            resultado.append(limpa)
    return resultado
