"""Gera INDICE.md: o mapa detalhado do curso (seções das aulas e exercícios).

Lê direto dos arquivos, então o índice nunca fica desatualizado. Rode de novo sempre
que uma aula ou exercício mudar:
    python ferramentas/gerar_indice.py
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PADRAO_MODULO = re.compile(r"^(\d{2})-(.+)$")
SECOES_FIXAS = {
    "O que você vai aprender",
    "Por que isso importa",
    "Boas práticas",
    "No mundo real",
    "Resumo",
    "Exercícios",
    "Desafio do módulo",
    "Quiz",
    "Para ir além",
}


def secoes_da_aula(aula: Path) -> list[str]:
    secoes = []
    em_codigo = False
    for linha in aula.read_text(encoding="utf-8").splitlines():
        if linha.lstrip().startswith(("```", "~~~")):
            em_codigo = not em_codigo
        if em_codigo or not linha.startswith("## "):
            continue
        titulo = linha[3:].strip()
        if titulo not in SECOES_FIXAS:
            secoes.append(titulo)
    return secoes


def resumo_exercicio(arquivo: Path) -> tuple[str, str, str]:
    """(título, nível, primeira frase da tarefa)."""
    docstring = ast.get_docstring(ast.parse(arquivo.read_text(encoding="utf-8"))) or ""
    linhas = docstring.strip().splitlines()
    titulo = linhas[0].split("—", 1)[-1].strip() if linhas else arquivo.stem
    nivel = next(
        (linha.split(":", 1)[1].strip() for linha in linhas if linha.startswith("Nível")), ""
    )
    tarefa = ""
    # "Tarefa:", "Tarefa 1:" ou "Tarefa (observação):" seguido do texto até a linha em branco
    achado = re.search(r"Tarefa[^\n:]*:\s*(.+?)(?:\n\s*\n|$)", docstring, flags=re.S)
    if not achado:  # exercícios de leitura de código não têm "Tarefa": usa o contexto
        achado = re.search(r"Contexto:\s*(.+?)(?:\n\s*\n|$)", docstring, flags=re.S)
    if achado:
        tarefa = " ".join(achado.group(1).split())
        tarefa = re.split(r"(?<=[.!?:;])\s", tarefa, maxsplit=1)[0]
        tarefa = tarefa if len(tarefa) <= 220 else tarefa[:217].rstrip() + "..."
    return titulo, nivel, tarefa


def main() -> None:
    partes = [
        "# Índice detalhado do curso",
        "",
        "Gerado por `ferramentas/gerar_indice.py` a partir das aulas e dos exercícios.",
        "Use para achar em que módulo e seção cada assunto é ensinado.",
        "",
    ]
    for modulo in sorted(
        p for p in RAIZ.iterdir() if p.is_dir() and PADRAO_MODULO.match(p.name)
    ):
        aula = modulo / "README.md"
        titulo = aula.read_text(encoding="utf-8").partition("\n")[0].lstrip("# ").strip()
        partes += [
            f"## {titulo}",
            "",
            f"Pasta: `{modulo.name}/`",
            "",
            "**Seções da aula:**",
            "",
        ]
        partes += [f"- {secao}" for secao in secoes_da_aula(aula)]
        partes += [
            "",
            "**Exercícios:**",
            "",
            "| Arquivo | Título | Nível | Tarefa |",
            "|---|---|---|---|",
        ]
        for arquivo in sorted((modulo / "exercicios").glob("ex*.py")):
            nome, nivel, tarefa = resumo_exercicio(arquivo)
            tarefa = tarefa.replace("|", "\\|")
            partes.append(f"| `{arquivo.stem}` | {nome} | {nivel} | {tarefa} |")
        desafio = modulo / "desafio" / "README.md"
        if desafio.exists():
            primeira = (
                desafio.read_text(encoding="utf-8").partition("\n")[0].lstrip("# ").strip()
            )
            partes += ["", f"**Desafio:** {primeira}"]
        partes.append("")
    destino = RAIZ / "INDICE.md"
    destino.write_text("\n".join(partes), encoding="utf-8")
    print(f"Gerado: {destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
