"""Solução de referência — Desafio 06: conferência de laudos em lote.

Lê as regras de tolerância (JSON) e todos os CSVs de laudo da pasta
dados/laudos/, confere cada lote, respeita a observação de liberação
("COF: liberado") e grava, em desafio/saida/:
    resultado.csv  -> para o Excel (";", vírgula decimal, UTF-8 com BOM)
    resumo.json    -> números da conferência (gravação atômica)
    erros.log      -> um registro por arquivo recusado (acrescentado a cada execução)

Uso (na pasta curso-python):
    python 06-arquivos-e-erros/desafio/solucao_referencia.py
"""

import csv
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

PASTA_MODULO = Path(__file__).resolve().parent.parent
PASTA_LAUDOS = PASTA_MODULO / "dados" / "laudos"
ARQUIVO_REGRAS = PASTA_MODULO / "dados" / "regras_tolerancia.json"
PASTA_SAIDA = Path(__file__).resolve().parent / "saida"

ENSAIOS = ("espessura", "gramatura", "cof")
OBRIGATORIAS = {"lote", "linha", *ENSAIOS}
COLUNAS_SAIDA = ["arquivo", "lote", "linha", *ENSAIOS, "status", "motivo"]


# ------------------------------------------------------------- exceções ----
class ErroDeQualidade(Exception):
    """Base dos erros do sistema de qualidade."""


class ArquivoInvalido(ErroDeQualidade):
    """O arquivo existe, mas não está no formato esperado."""


class RegraAusente(ErroDeQualidade):
    """Não há regra de tolerância para a linha de produção ou o ensaio."""


# ----------------------------------------------------------- utilidades ----
def sem_acento(texto: str) -> str:
    decomposto = unicodedata.normalize("NFD", texto)
    return "".join([c for c in decomposto if not unicodedata.combining(c)])


def numero_br(texto: str) -> float:
    return float(texto.strip().replace(".", "").replace(",", "."))


def para_br(valor: float, casas: int = 2) -> str:
    return f"{valor:.{casas}f}".replace(".", ",")


def ler_texto_excel(caminho: Path) -> str:
    try:
        return caminho.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return caminho.read_text(encoding="cp1252")


# --------------------------------------------------------------- regras ----
def carregar_regras(caminho: Path) -> dict:
    """Regras quebradas impedem a conferência inteira: aqui o programa PARA."""
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            regras = json.load(arquivo)
    except json.JSONDecodeError as erro:
        raise ArquivoInvalido(f"{caminho.name}: JSON inválido (linha {erro.lineno})") from erro
    if not isinstance(regras, dict):
        raise ArquivoInvalido(f"{caminho.name}: esperado um objeto JSON")
    return regras


def faixa(regras: dict, linha: str, ensaio: str) -> tuple[float, float]:
    """(mínimo, máximo) do ensaio na linha: nominal ± % ou mín/máx fixos."""
    try:
        regra = regras[linha][ensaio]
    except KeyError as erro:
        raise RegraAusente(f"sem regra para linha {linha}, ensaio {ensaio}") from erro
    if "nominal" in regra:
        variacao = regra["nominal"] * regra["tolerancia_pct"] / 100
        return regra["nominal"] - variacao, regra["nominal"] + variacao
    return regra["min"], regra["max"]


# --------------------------------------------------------------- laudos ----
def ler_laudo(caminho: Path) -> list[dict]:
    """Lê e valida UM arquivo. Qualquer problema vira ArquivoInvalido."""
    linhas = list(csv.reader(ler_texto_excel(caminho).splitlines(), delimiter=";"))
    if not linhas:
        raise ArquivoInvalido("arquivo vazio")
    cabecalho = [sem_acento(nome).strip().lower() for nome in linhas[0]]
    faltando = OBRIGATORIAS - set(cabecalho)
    if faltando:
        raise ArquivoInvalido(f"colunas ausentes: {', '.join(sorted(faltando))}")

    lotes = []
    for numero, valores in enumerate(linhas[1:], start=2):
        if not any(v.strip() for v in valores):
            continue
        registro = dict(zip(cabecalho, [v.strip() for v in valores], strict=False))
        for ensaio in ENSAIOS:
            texto = registro.get(ensaio, "")
            try:
                registro[ensaio] = numero_br(texto)
            except ValueError as erro:
                raise ArquivoInvalido(
                    f"linha {numero}: valor inválido em {ensaio}: {texto!r}"
                ) from erro
        registro["linha"] = registro["linha"].upper()
        registro.setdefault("observacao", "")
        lotes.append(registro)
    return lotes


def ensaios_liberados(observacao: str) -> set[str]:
    """{'cof', 'espessura'} para "COF: liberado; Espessura - liberada"."""
    texto = sem_acento(observacao).lower()
    return {
        ensaio
        for ensaio in ENSAIOS
        if re.search(rf"\b{ensaio}\s*[:-]?\s*liberad[oa]\b", texto)
    }


def conferir_lote(lote: dict, regras: dict) -> tuple[str, str]:
    """Devolve (status, motivo) do lote."""
    liberados = ensaios_liberados(lote["observacao"])
    fora, com_liberacao = [], []
    for ensaio in ENSAIOS:
        minimo, maximo = faixa(regras, lote["linha"], ensaio)
        if minimo <= lote[ensaio] <= maximo:
            continue
        texto = (
            f"{ensaio} {para_br(lote[ensaio])} fora de [{para_br(minimo)}; {para_br(maximo)}]"
        )
        (com_liberacao if ensaio in liberados else fora).append(texto)
    if fora:
        return "REPROVADO", " | ".join(fora + com_liberacao)
    if com_liberacao:
        return "APROVADO COM LIBERAÇÃO", " | ".join(com_liberacao)
    return "APROVADO", ""


# --------------------------------------------------------------- saídas ----
def gravar_json_seguro(caminho: Path, dados) -> None:
    temporario = caminho.with_name(caminho.name + ".tmp")
    try:
        temporario.write_text(
            json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception:
        temporario.unlink(missing_ok=True)
        raise
    temporario.replace(caminho)


def gravar_resultado(caminho: Path, linhas: list[dict]) -> None:
    try:
        with open(caminho, "w", encoding="utf-8-sig", newline="") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS_SAIDA, delimiter=";")
            escritor.writeheader()
            escritor.writerows(linhas)
    except PermissionError:
        print(f"Não consegui gravar {caminho.name}: feche o arquivo no Excel e rode de novo.")
        raise


def registrar_erros(caminho: Path, erros: dict[str, str]) -> None:
    # datetime (módulo 07) dá a data e a hora atuais; strftime formata como texto.
    momento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(caminho, "a", encoding="utf-8") as arquivo:
        for nome, mensagem in erros.items():
            arquivo.write(f"{momento} | {nome} | {mensagem}\n")


# ------------------------------------------------------------ principal ----
def main() -> None:
    regras = carregar_regras(ARQUIVO_REGRAS)
    resultado, erros = [], {}
    contagem = {"APROVADO": 0, "APROVADO COM LIBERAÇÃO": 0, "REPROVADO": 0}

    arquivos = sorted(p for p in PASTA_LAUDOS.iterdir() if p.suffix.lower() == ".csv")
    for caminho in arquivos:
        try:
            lotes = ler_laudo(caminho)
            linhas_do_arquivo = []
            for lote in lotes:
                status, motivo = conferir_lote(lote, regras)
                linhas_do_arquivo.append(
                    {
                        "arquivo": caminho.name,
                        "lote": lote["lote"],
                        "linha": lote["linha"],
                        **{ensaio: para_br(lote[ensaio]) for ensaio in ENSAIOS},
                        "status": status,
                        "motivo": motivo,
                    }
                )
        except ErroDeQualidade as erro:
            erros[caminho.name] = str(erro)
            print(f"[RECUSADO] {caminho.name}: {erro}")
            continue
        resultado.extend(linhas_do_arquivo)  # só entra se o arquivo inteiro deu certo
        for linha in linhas_do_arquivo:
            contagem[linha["status"]] += 1
        print(f"[OK]       {caminho.name}: {len(linhas_do_arquivo)} lotes")

    PASTA_SAIDA.mkdir(exist_ok=True)
    gravar_resultado(PASTA_SAIDA / "resultado.csv", resultado)
    resumo = {
        "arquivos_lidos": len(arquivos) - len(erros),
        "arquivos_recusados": erros,
        "lotes": len(resultado),
        "por_status": contagem,
    }
    gravar_json_seguro(PASTA_SAIDA / "resumo.json", resumo)
    if erros:
        registrar_erros(PASTA_SAIDA / "erros.log", erros)

    print()
    print(f"{'Lote':<8}{'Linha':<7}{'Status':<24}Motivo")
    for linha in resultado:
        texto = f"{linha['lote']:<8}{linha['linha']:<7}{linha['status']:<24}{linha['motivo']}"
        print(texto.rstrip())
    print()
    print(
        f"Lotes conferidos: {len(resultado)} | "
        + " | ".join(f"{k}: {v}" for k, v in contagem.items())
    )
    print(f"Arquivos gravados em: {PASTA_SAIDA.name}/ (resultado.csv, resumo.json, erros.log)")


# Roda main() só quando o arquivo é executado diretamente (detalhes no módulo 07).
if __name__ == "__main__":
    main()
