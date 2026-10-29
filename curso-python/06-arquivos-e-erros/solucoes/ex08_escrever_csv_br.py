"""
Exercício 06.08 — Gerar CSV que abre certo no Excel
Nível: ★★☆

Contexto: O resultado da conferência vai para o pessoal da qualidade, que abre
tudo no Excel com um duplo clique. Para as colunas e os acentos aparecerem
certos no Excel em português, o arquivo precisa de ";", vírgula decimal e
UTF-8 com BOM.

Tarefa: implemente `escrever_csv_br(caminho, linhas, casas=2)`:
- `linhas` é uma lista de dicionários; o cabeçalho são as chaves do PRIMEIRO
  dicionário, na mesma ordem;
- grave com csv.DictWriter, delimiter=";", encoding "utf-8-sig" e newline="";
- valores float viram texto com vírgula decimal e `casas` casas, SEM separador
  de milhar (1250.5 vira "1250,50");
- None vira célula vazia; os outros valores (str, int) vão como estão;
- devolva quantas linhas de dados foram gravadas;
- se `linhas` estiver vazia, levante ValueError("nada para gravar") SEM criar
  o arquivo.

Exemplos:
    >>> escrever_csv_br(Path("saida.csv"), [{"lote": "A-0153", "espessura": 25.4}])
    1
    >>> Path("saida.csv").read_bytes()
    b'\\xef\\xbb\\xbflote;espessura\\r\\nA-0153;25,40\\r\\n'

Repare nos 3 bytes do BOM no começo e no "\\r\\n" (o fim de linha padrão do
csv e do Windows).

Dica: prepare uma CÓPIA de cada dicionário com os valores já formatados e só
depois chame `writerow`.

Teste com:  python curso.py testar 06 ex08
"""

import csv
from pathlib import Path


def formatar_celula(valor, casas: int) -> str:
    """Converte um valor para o texto que vai na célula do CSV."""
    if valor is None:
        return ""
    if isinstance(valor, float):
        # Sem milhar de propósito: "1250,50" o Excel entende como número;
        # "1.250,50" também, mas outros programas podem se confundir.
        return f"{valor:.{casas}f}".replace(".", ",")
    return str(valor)  # texto continua igual; inteiro 3 vira "3"


def escrever_csv_br(caminho: Path, linhas: list[dict], casas: int = 2) -> int:
    """Grava as linhas num CSV no padrão do Excel brasileiro."""
    # Validamos ANTES de abrir: abrir em "w" já cria (ou apaga!) o arquivo.
    if not linhas:
        raise ValueError("nada para gravar")
    colunas = list(linhas[0])  # as chaves, na ordem em que foram criadas
    with open(caminho, "w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas, delimiter=";")
        escritor.writeheader()
        for linha in linhas:
            escritor.writerow({chave: formatar_celula(v, casas) for chave, v in linha.items()})
    return len(linhas)

    # Sem newline="", no Windows cada linha ganharia um "\r" a mais e o Excel
    # mostraria uma linha em branco entre cada linha de dados.
