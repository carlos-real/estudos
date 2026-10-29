"""
Exercício 12.05 — Listar as planilhas de uma pasta (SOLUÇÃO)
"""

from pathlib import Path

EXTENSOES = {".xlsx", ".xlsm"}


def listar_planilhas(pasta: Path) -> list[str]:
    """Nomes das planilhas Excel da pasta, em ordem alfabética."""
    # iterdir() numa pasta inexistente já levantaria FileNotFoundError, mas a
    # mensagem fica mais clara se verificarmos antes (e deixamos a regra visível).
    if not pasta.is_dir():
        raise FileNotFoundError(f"Pasta não encontrada: {pasta}")

    nomes = [
        arquivo.name
        for arquivo in pasta.iterdir()  # só o primeiro nível, sem subpastas
        if arquivo.is_file()
        and arquivo.suffix.lower() in EXTENSOES  # ".XLSX" -> ".xlsx"
        and not arquivo.name.startswith("~$")  # arquivo de trava do Excel
    ]
    # Sem key=str.lower, "Linha_B" viria antes de "linha_a" ("L" < "l" na tabela
    # de caracteres). Para pessoas, a ordem "natural" ignora maiúsculas.
    return sorted(nomes, key=str.lower)

    # Alternativa com glob: pasta.glob("*.xlsx") é mais curta, mas no Linux é
    # sensível a maiúsculas (não acharia "RELATORIO.XLSX"). A comparação com
    # .suffix.lower() funciona igual em qualquer sistema.
