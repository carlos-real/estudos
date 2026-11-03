"""Exemplo 09 — No mundo real: conferência das medições de uma linha de produção.

Lê o CSV exportado do Excel (UTF-8 com BOM ou cp1252), as regras de tolerância em
JSON, confere cada lote e grava o resultado num CSV que abre certo no Excel.

Rode na pasta curso-python:
    python 06-arquivos-e-erros/exemplos/09_conferencia_da_linha.py
"""

import csv
import json
from pathlib import Path

DADOS = Path(__file__).resolve().parent.parent / "dados"
SAIDA = Path(__file__).resolve().parent / "saida"
ENSAIOS = ("espessura", "gramatura", "cof")


class ErroDeQualidade(Exception):
    """Base dos erros do sistema de qualidade."""


class ArquivoInvalido(ErroDeQualidade):
    """O arquivo existe, mas não está no formato esperado."""


def numero_br(texto):
    return float(texto.strip().replace(".", "").replace(",", "."))


def ler_texto_excel(caminho):
    try:
        return caminho.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return caminho.read_text(encoding="cp1252")


def carregar_regras(caminho):
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError as erro:
        raise ArquivoInvalido(f"{caminho.name}: JSON inválido (linha {erro.lineno})") from erro


def faixa(regra):
    """Converte a regra do JSON em (mínimo, máximo): nominal ± % ou mín/máx fixos."""
    if "nominal" in regra:
        variacao = regra["nominal"] * regra["tolerancia_pct"] / 100
        return regra["nominal"] - variacao, regra["nominal"] + variacao
    return regra["min"], regra["max"]


def ler_medicoes(caminho):
    linhas = list(csv.reader(ler_texto_excel(caminho).splitlines(), delimiter=";"))
    if not linhas:
        raise ArquivoInvalido(f"{caminho.name}: arquivo vazio")
    cabecalho = [nome.strip().lower() for nome in linhas[0]]
    faltando = {"lote", "linha", *ENSAIOS} - set(cabecalho)
    if faltando:
        raise ArquivoInvalido(f"{caminho.name}: faltam as colunas {sorted(faltando)}")
    medicoes = []
    for numero, valores in enumerate(linhas[1:], start=2):
        registro = dict(zip(cabecalho, valores, strict=False))
        try:
            for ensaio in ENSAIOS:
                registro[ensaio] = numero_br(registro[ensaio])
        except ValueError as erro:
            raise ArquivoInvalido(f"{caminho.name}, linha {numero}: {erro}") from erro
        medicoes.append(registro)
    return medicoes


def conferir(medicao, regras_da_linha):
    problemas = []
    for ensaio in ENSAIOS:
        minimo, maximo = faixa(regras_da_linha[ensaio])
        if not minimo <= medicao[ensaio] <= maximo:
            problemas.append(
                f"{ensaio} {medicao[ensaio]} fora de [{minimo:.2f}, {maximo:.2f}]"
            )
    return problemas


def main():
    regras = carregar_regras(DADOS / "regras_tolerancia.json")
    medicoes = ler_medicoes(DADOS / "medicoes_linha_a.csv")
    SAIDA.mkdir(exist_ok=True)
    destino = SAIDA / "conferencia_linha_a.csv"
    with open(destino, "w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["lote", "status", "motivo"])
        for medicao in medicoes:
            problemas = conferir(medicao, regras[medicao["linha"]])
            status = "REPROVADO" if problemas else "APROVADO"
            escritor.writerow([medicao["lote"], status, "; ".join(problemas)])
            print(f"{medicao['lote']}: {status:<9} {'; '.join(problemas)}".rstrip())
    print(f"Resultado gravado em {destino.name}")


# Roda main() só quando o arquivo é executado diretamente (detalhes no módulo 07).
if __name__ == "__main__":
    main()
