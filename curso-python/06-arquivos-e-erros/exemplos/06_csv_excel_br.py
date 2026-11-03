"""Exemplo 06 — CSV no padrão do Excel brasileiro (seções 8 e 9).

Lê dois CSVs (um "CSV UTF-8" e um "CSV separado por vírgulas" em cp1252) e grava
um resumo que abre certo no Excel, em exemplos/saida/.

Rode na pasta curso-python:
    python 06-arquivos-e-erros/exemplos/06_csv_excel_br.py
"""

import csv
from pathlib import Path

DADOS = Path(__file__).resolve().parent.parent / "dados"
SAIDA = Path(__file__).resolve().parent / "saida"


def ler_texto_excel(caminho):
    try:
        return caminho.read_text(encoding="utf-8-sig"), "utf-8-sig"
    except UnicodeDecodeError:
        return caminho.read_text(encoding="cp1252"), "cp1252"


def numero_br(texto):
    return float(texto.replace(".", "").replace(",", "."))


medicoes = []
for nome in ["medicoes_linha_a.csv", "medicoes_linha_b_cp1252.csv"]:
    texto, encoding = ler_texto_excel(DADOS / nome)
    leitor = csv.DictReader(texto.splitlines(), delimiter=";")
    linhas = [
        {chave.strip().lower(): valor for chave, valor in linha.items()} for linha in leitor
    ]
    print(f"{nome} ({encoding}): colunas {list(linhas[0])}")
    medicoes.extend(linhas)

SAIDA.mkdir(exist_ok=True)
destino = SAIDA / "espessuras.csv"
with open(destino, "w", encoding="utf-8-sig", newline="") as arquivo:
    escritor = csv.DictWriter(
        arquivo, fieldnames=["lote", "linha", "espessura"], delimiter=";"
    )
    escritor.writeheader()
    for medicao in medicoes:
        espessura = numero_br(medicao["espessura"])
        escritor.writerow(
            {
                "lote": medicao["lote"],
                "linha": medicao["linha"],
                "espessura": f"{espessura:.2f}".replace(".", ","),
            }
        )

print(f"\n{destino.name} (como o Excel vai receber):")
print(destino.read_bytes()[:60], "...")
