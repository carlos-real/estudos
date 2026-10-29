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

# Este exercício usa o módulo csv.
# Apague o "# " do começo da linha abaixo para importá-lo:
# import csv
from pathlib import Path


def escrever_csv_br(caminho: Path, linhas: list[dict], casas: int = 2) -> int:
    """Grava as linhas num CSV no padrão do Excel brasileiro."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
