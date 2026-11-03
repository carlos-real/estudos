"""Exemplo 08 — Gravação segura e processamento em lote sem parar (seções 11 e 12).

Rode na pasta curso-python:
    python 06-arquivos-e-erros/exemplos/08_escrita_segura.py
"""

import csv
import json
from pathlib import Path

DADOS = Path(__file__).resolve().parent.parent / "dados"
SAIDA = Path(__file__).resolve().parent / "saida"


def gravar_json_seguro(caminho, dados):
    """Temporário primeiro; troca no final. Em erro, o original fica intacto."""
    temporario = caminho.with_name(caminho.name + ".tmp")
    try:
        temporario.write_text(
            json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception:
        temporario.unlink(missing_ok=True)
        raise
    temporario.replace(caminho)


def contar_lotes(caminho):
    """Conta os lotes de um CSV de laudo; levanta erro se faltar coluna."""
    try:
        texto = caminho.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        texto = caminho.read_text(encoding="cp1252")
    linhas = list(csv.DictReader(texto.splitlines(), delimiter=";"))
    colunas = {nome.strip().lower() for nome in linhas[0]} if linhas else set()
    if "cof" not in colunas:
        raise KeyError("cof")
    return len(linhas)


SAIDA.mkdir(exist_ok=True)
resumo = {"lotes_por_arquivo": {}, "erros": {}}
for caminho in sorted((DADOS / "laudos").glob("*.csv")):
    try:
        resumo["lotes_por_arquivo"][caminho.name] = contar_lotes(caminho)
    except KeyError as erro:
        resumo["erros"][caminho.name] = f"falta a coluna {erro}"

destino = SAIDA / "resumo_lotes.json"
gravar_json_seguro(destino, resumo)
print(destino.read_text(encoding="utf-8"))

try:
    gravar_json_seguro(destino, {"linhas": {"A", "B"}})  # set: não vira JSON
except TypeError as erro:
    print("\nErro ao gravar:", erro)
    print(
        "O arquivo anterior continua inteiro?",
        json.loads(destino.read_text(encoding="utf-8")) == resumo,
    )
