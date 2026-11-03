"""Exemplo 04 — Ler e gravar arquivos de texto com with/open (seção 6).

Grava na pasta exemplos/saida/ (criada se não existir).

Rode na pasta curso-python:
    python 06-arquivos-e-erros/exemplos/04_arquivos_texto.py
"""

from pathlib import Path

SAIDA = Path(__file__).resolve().parent / "saida"
SAIDA.mkdir(exist_ok=True)
laudo = SAIDA / "laudo.txt"

with open(laudo, "w", encoding="utf-8") as arquivo:  # "w": começa do zero
    arquivo.write("Lote: L001\n")
    arquivo.write("Espessura: 25,4 µm\n")

with open(laudo, "a", encoding="utf-8") as arquivo:  # "a": acrescenta no fim
    arquivo.write("Observação: COF liberado\n")

with open(laudo, encoding="utf-8") as arquivo:  # leitura linha a linha
    for numero, linha in enumerate(arquivo, start=1):
        rotulo, _, valor = linha.strip().partition(":")
        print(f"{numero}: {rotulo:<11} = {valor.strip()}")

try:
    with open(laudo, "x", encoding="utf-8") as arquivo:  # "x": não sobrescreve
        arquivo.write("isto não vai ser gravado")
except FileExistsError:
    print(f"\n{laudo.name} já existe: o modo 'x' protegeu o arquivo.")
