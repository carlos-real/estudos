"""Conferência de medições: versão refatorada do legado_conferencia.py.

Solução de referência do desafio do módulo 09. O que mudou em relação ao legado:
  - funções pequenas, com nomes que dizem o que fazem e type hints;
  - regras (limites) separadas da lógica, prontas para virem de um banco;
  - logging no lugar dos prints de aviso, com arquivo de log opcional;
  - regra nova, feita com TDD: medição FORA com observação "<ENSAIO>: liberado"
    vira LIBERADO (a liberação técnica do laboratório);
  - testes em test_solucao_referencia.py.

Uso (na pasta do módulo):
    python desafio/solucao_referencia.py
    python desafio/solucao_referencia.py --arquivo outra_planilha.csv --log conferencia.log
"""

import argparse
import csv
import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger("conferencia")

ARQUIVO_PADRAO = Path(__file__).resolve().parent / "dados" / "medicoes_exemplo.csv"

# (linha, ensaio) -> (mínimo, máximo). No projeto final, isso vem do SQLite.
LIMITES: dict[tuple[str, str], tuple[float, float]] = {
    ("A", "espessura"): (19.0, 21.0),
    ("A", "gramatura"): (18.2, 19.0),
    ("A", "cof"): (0.20, 0.35),
    ("B", "espessura"): (23.75, 26.25),
    ("B", "gramatura"): (21.5, 22.5),
    ("B", "cof"): (0.20, 0.35),
    ("C", "espessura"): (28.5, 31.5),
    ("C", "cof"): (0.25, 0.40),
    ("D", "espessura"): (14.25, 15.75),
    ("D", "gramatura"): (13.8, 14.6),
}

OK, FORA, LIBERADO, SEM_REGRA = "OK", "FORA", "LIBERADO", "SEM REGRA"


@dataclass(frozen=True)
class Medicao:
    op: str
    linha: str
    ensaio: str
    valor: float
    observacao: str = ""


def converter_numero_br(texto: str) -> float:
    """'1.250,5' -> 1250.5. Levanta ValueError se não for número."""
    return float(texto.strip().replace(".", "").replace(",", "."))


def formatar_br(valor: float, casas: int = 2) -> str:
    """0.38 -> '0,38' (sem separador de milhar: os valores do laudo são pequenos)."""
    return f"{valor:.{casas}f}".replace(".", ",")


def ler_medicoes(caminho: Path) -> list[Medicao]:
    """Lê o CSV (separador ';', padrão Excel BR). Linhas com valor inválido são
    registradas no log e ignoradas, como no legado."""
    medicoes = []
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        # start=2: a linha 1 do arquivo é o cabeçalho
        for numero, linha in enumerate(csv.DictReader(arquivo, delimiter=";"), start=2):
            try:
                valor = converter_numero_br(linha["valor"])
            except ValueError:
                logger.warning("linha %d ignorada, valor: %s", numero, linha["valor"])
                continue
            medicoes.append(
                Medicao(
                    op=linha["op"].strip(),
                    linha=linha["linha"].strip().upper(),
                    ensaio=linha["ensaio"].strip().lower(),
                    valor=valor,
                    observacao=(linha.get("observacao") or "").strip(),
                )
            )
    logger.info("%d medições lidas de %s", len(medicoes), Path(caminho).name)
    return medicoes


def ensaios_liberados(observacao: str) -> set[str]:
    """'COF: liberado; Selagem: reprovado' -> {'cof'}. Itens sem ':' são ignorados."""
    liberados = set()
    for item in observacao.split(";"):
        ensaio, separador, status = item.partition(":")
        if separador and status.strip().lower() == "liberado":
            liberados.add(ensaio.strip().lower())
    return liberados


def classificar(medicao: Medicao, limites: dict[tuple[str, str], tuple[float, float]]) -> str:
    """Devolve OK, FORA, LIBERADO ou SEM REGRA para uma medição."""
    regra = limites.get((medicao.linha, medicao.ensaio))
    if regra is None:
        return SEM_REGRA
    minimo, maximo = regra
    if minimo <= medicao.valor <= maximo:
        return OK
    if medicao.ensaio in ensaios_liberados(medicao.observacao):
        return LIBERADO
    return FORA


def resumir(classificadas: list[tuple[Medicao, str]]) -> dict[str, dict[str, int]]:
    """Conta, por linha, medições com regra, quantas FORA e quantas LIBERADAS."""
    resumo: dict[str, dict[str, int]] = {}
    for medicao, situacao in classificadas:
        if situacao == SEM_REGRA:
            continue
        contagem = resumo.setdefault(medicao.linha, {"total": 0, "fora": 0, "liberadas": 0})
        contagem["total"] += 1
        if situacao == FORA:
            contagem["fora"] += 1
        elif situacao == LIBERADO:
            contagem["liberadas"] += 1
    return resumo


def montar_relatorio(classificadas: list[tuple[Medicao, str]]) -> str:
    """Monta o texto do relatório (devolver texto facilita testar)."""
    linhas = ["CONFERÊNCIA DE MEDIÇÕES"]
    for medicao, situacao in classificadas:
        linhas.append(
            f"OP {medicao.op} | linha {medicao.linha} | {medicao.ensaio} | "
            f"{formatar_br(medicao.valor)} | {situacao}"
        )
    linhas.append("RESUMO POR LINHA")
    for linha, contagem in sorted(resumir(classificadas).items()):
        percentual = formatar_br(contagem["fora"] / contagem["total"] * 100, casas=1)
        linhas.append(
            f"{linha}: {contagem['total']} medições, {contagem['fora']} fora "
            f"({percentual}%), {contagem['liberadas']} liberada(s)"
        )
    return "\n".join(linhas)


def configurar_log(arquivo_log: Path | None) -> None:
    """Avisos vão para o terminal; com --log, tudo (INFO+) vai também para o arquivo."""
    terminal = logging.StreamHandler()
    terminal.setLevel(logging.WARNING)
    handlers: list[logging.Handler] = [terminal]
    if arquivo_log is not None:
        handlers.append(logging.FileHandler(arquivo_log, encoding="utf-8"))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=handlers,
    )


def main(argumentos: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Confere medições contra os limites.")
    parser.add_argument("--arquivo", type=Path, default=ARQUIVO_PADRAO, help="CSV de medições")
    parser.add_argument("--log", type=Path, default=None, help="arquivo de log (opcional)")
    opcoes = parser.parse_args(argumentos)

    configurar_log(opcoes.log)
    medicoes = ler_medicoes(opcoes.arquivo)
    classificadas = [(medicao, classificar(medicao, LIMITES)) for medicao in medicoes]
    print(montar_relatorio(classificadas))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
