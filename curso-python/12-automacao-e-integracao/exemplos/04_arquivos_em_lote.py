"""Exemplo 04 — Organizar arquivos em lote com pathlib e shutil.

Cria uma pasta temporária com laudos "bagunçados", mostra o plano (modo ensaio)
e depois executa de verdade: cada laudo vai para pasta_destino/linha_X/.

Rode com:  python exemplos/04_arquivos_em_lote.py
"""

import re
import shutil
import tempfile
from pathlib import Path

PADRAO_LAUDO = re.compile(r"laudo_(\d{6})_([A-D])\.pdf", re.IGNORECASE)


def criar_bagunca(pasta: Path) -> None:
    """Cria arquivos de exemplo (vazios) para o teste."""
    nomes = [
        "laudo_123456_A.pdf",
        "laudo_123789_B.pdf",
        "LAUDO_124001_b.PDF",
        "laudo_124050_D.pdf",
        "anotacoes.txt",
        "~$relatorio.xlsx",
    ]
    for nome in nomes:
        (pasta / nome).write_text("conteúdo de exemplo", encoding="utf-8")


def planejar(origem: Path, destino: Path) -> list[tuple[Path, Path]]:
    """Decide para onde vai cada laudo. NÃO mexe em nada (função pura)."""
    plano = []
    for arquivo in sorted(origem.iterdir()):
        achado = PADRAO_LAUDO.fullmatch(arquivo.name)
        if arquivo.is_file() and achado:
            linha = achado.group(2).upper()
            plano.append((arquivo, destino / f"linha_{linha}" / arquivo.name))
    return plano


def executar(plano: list[tuple[Path, Path]], ensaio: bool) -> None:
    for origem, destino in plano:
        if ensaio:
            print(f"   [ENSAIO] {origem.name} -> {destino.parent.name}/")
            continue
        if destino.exists():
            print(f"   [PULADO] {destino.name} já existe no destino")
            continue
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(origem, destino)
        print(f"   [MOVIDO] {origem.name} -> {destino.parent.name}/")


def mostrar_arvore(raiz: Path) -> None:
    for caminho in sorted(raiz.rglob("*")):
        if caminho.is_file():
            print("  ", caminho.relative_to(raiz).as_posix())


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        origem = Path(tmp) / "entrada"
        destino = Path(tmp) / "laudos"
        origem.mkdir()
        criar_bagunca(origem)

        plano = planejar(origem, destino)
        print("1) Modo ensaio (nada é movido):")
        executar(plano, ensaio=True)

        print("2) Agora de verdade:")
        executar(plano, ensaio=False)

        print("3) Como ficou:")
        mostrar_arvore(Path(tmp))
    # Ao sair do "with", a pasta temporária é apagada sozinha.


if __name__ == "__main__":
    main()
