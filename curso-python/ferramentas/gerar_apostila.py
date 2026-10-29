"""Gera a apostila do curso em PDF (versão A4 e versão para celular).

Junta, em ordem, a aula (README.md), os enunciados dos exercícios, o desafio e o
quiz de cada módulo, converte para HTML com o pandoc e imprime em PDF com um
navegador Chromium (Chrome, Edge ou Chromium) em modo headless.

Uso (na pasta curso-python):
    python ferramentas/gerar_apostila.py

Requisitos: pandoc instalado e um navegador Chromium. Se o navegador não for
encontrado sozinho, informe o caminho na variável de ambiente APOSTILA_NAVEGADOR.
"""

from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "apostila"
PADRAO_MODULO = re.compile(r"^(\d{2})-(.+)$")

NAVEGADORES = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "chromium",
    "chromium-browser",
    "google-chrome",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

FORMATOS = {
    "a4": {
        "arquivo": "apostila-curso-python.pdf",
        "pagina": "A4",
        "margem": "16mm 15mm",
        "fonte": "10.5pt",
    },
    "celular": {
        "arquivo": "apostila-curso-python-celular.pdf",
        "pagina": "100mm 178mm",
        "margem": "6mm 5mm",
        "fonte": "9.5pt",
    },
}


def achar_navegador() -> str:
    escolhido = os.environ.get("APOSTILA_NAVEGADOR")
    if escolhido:
        return escolhido
    for candidato in NAVEGADORES:
        if Path(candidato).exists() or shutil.which(candidato):
            return candidato
    sys.exit("Navegador Chromium não encontrado. Defina APOSTILA_NAVEGADOR.")


def rebaixar_titulos(texto: str, niveis: int = 1) -> str:
    """Acrescenta '#' aos títulos Markdown (fora de blocos de código)."""
    linhas = []
    em_codigo = False
    for linha in texto.splitlines():
        if linha.lstrip().startswith(("```", "~~~")):
            em_codigo = not em_codigo
        if not em_codigo and re.match(r"^#{1,5} ", linha):
            linha = "#" * niveis + linha
        linhas.append(linha)
    return "\n".join(linhas)


def remover_links_locais(texto: str) -> str:
    """Links para arquivos do repositório não funcionam no PDF: vira só o texto."""
    return re.sub(r"\[([^\]]+)\]\((?!https?://|#|mailto:)[^)]+\)", r"\1", texto)


def enunciados_dos_exercicios(modulo: Path) -> str:
    pasta = modulo / "exercicios"
    if not pasta.exists():
        return ""
    partes = ["## Enunciados dos exercícios", ""]
    for arquivo in sorted(pasta.glob("ex*.py")):
        try:
            docstring = ast.get_docstring(ast.parse(arquivo.read_text(encoding="utf-8")))
        except SyntaxError:
            docstring = None
        if not docstring:
            continue
        primeira, _, resto = docstring.strip().partition("\n")
        partes += [f"### {primeira.strip()}", "", f"Arquivo: `exercicios/{arquivo.name}`", ""]
        partes += ["```text", resto.strip(), "```", ""]
    return "\n".join(partes)


def montar_markdown() -> str:
    blocos = []
    leia_me = RAIZ / "README.md"
    if leia_me.exists():
        blocos.append(leia_me.read_text(encoding="utf-8"))
    modulos = sorted(p for p in RAIZ.iterdir() if p.is_dir() and PADRAO_MODULO.match(p.name))
    for modulo in modulos:
        aula = modulo / "README.md"
        if aula.exists():
            blocos.append(aula.read_text(encoding="utf-8"))
        enunciados = enunciados_dos_exercicios(modulo)
        if enunciados:
            blocos.append(enunciados)
        for extra in (modulo / "desafio" / "README.md", modulo / "quiz.md"):
            if extra.exists():
                blocos.append(rebaixar_titulos(extra.read_text(encoding="utf-8")))
    carreira = RAIZ / "carreira"
    for nome in ("README.md", "recursos.md"):
        if (carreira / nome).exists():
            blocos.append((carreira / nome).read_text(encoding="utf-8"))
    texto = "\n\n".join(blocos)
    texto = remover_links_locais(texto)
    # Respostas escondidas em <details> precisam aparecer no papel
    return texto.replace("<details>", "<details open>")


CSS = """
@page { size: %(pagina)s; margin: %(margem)s; }
html { font-size: %(fonte)s; }
body { font-family: Inter, 'Segoe UI', 'DejaVu Sans', sans-serif, 'Noto Color Emoji';
       color: #1b2330; line-height: 1.5; max-width: none; margin: 0; padding: 0; }
h1 { font-size: 1.9em; color: #0d4a6b; border-bottom: 3px solid #0d4a6b;
     padding-bottom: .2em; break-before: page; margin-top: 0; }
h2 { font-size: 1.35em; color: #0d4a6b; margin-top: 1.6em; break-after: avoid; }
h3 { font-size: 1.12em; margin-top: 1.3em; break-after: avoid; }
h4, h5 { font-size: 1em; break-after: avoid; }
p, li { orphans: 3; widows: 3; }
a { color: #0b6e99; text-decoration: none; }
code { font-family: 'JetBrains Mono', Consolas, 'DejaVu Sans Mono', monospace;
       font-size: .86em; background: #eef2f5; padding: .05em .3em; border-radius: 3px; }
pre { background: #f5f7f9; border: 1px solid #d9e0e6; border-left: 4px solid #0d4a6b;
      padding: .6em .8em; border-radius: 4px; white-space: pre-wrap; word-break: break-word;
      font-size: .92em; line-height: 1.35; }
pre code { background: none; padding: 0; font-size: 1em; }
blockquote { margin: 1em 0; padding: .5em .9em; background: #f3f8fb;
             border-left: 4px solid #4c9bc4; color: #24323f; }
blockquote p { margin: .3em 0; }
table { border-collapse: collapse; width: 100%%; margin: 1em 0; font-size: .92em; }
th, td { border: 1px solid #cfd8df; padding: .35em .5em; text-align: left;
         vertical-align: top; }
th { background: #e6eef3; }
tr { break-inside: avoid; }
details { margin: .6em 0; padding: .4em .7em; border: 1px dashed #9db4c4;
          border-radius: 4px; }
summary { font-weight: 600; }
nav#TOC { break-after: page; }
nav#TOC ul { list-style: none; padding-left: 1em; }
nav#TOC > ul { padding-left: 0; }
nav#TOC > ul > li { margin-top: .5em; font-weight: 600; }
nav#TOC > ul > li li { font-weight: 400; }
header#title-block-header { break-after: page; text-align: center; padding-top: 30%%; }
header#title-block-header h1 { border: none; font-size: 2.6em; break-before: auto; }
header#title-block-header .subtitle { font-size: 1.3em; color: #4a5b6a; }
"""


def gerar(formato: str, html_base: Path, navegador: str, tmp: Path) -> Path:
    config = FORMATOS[formato]
    css = tmp / f"estilo-{formato}.css"
    css.write_text(CSS % config, encoding="utf-8")
    html = tmp / f"apostila-{formato}.html"
    conteudo = html_base.read_text(encoding="utf-8").replace(
        "</head>", f'<link rel="stylesheet" href="{css.name}">\n</head>'
    )
    html.write_text(conteudo, encoding="utf-8")
    destino = SAIDA / config["arquivo"]
    subprocess.run(
        [
            navegador,
            "--headless",
            "--no-sandbox",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={destino}",
            html.as_uri(),
        ],
        check=True,
        capture_output=True,
    )
    return destino


def main() -> int:
    if shutil.which("pandoc") is None:
        sys.exit("pandoc não encontrado. Instale em https://pandoc.org/installing.html")
    navegador = achar_navegador()
    SAIDA.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as pasta:
        tmp = Path(pasta)
        fonte = tmp / "apostila.md"
        fonte.write_text(montar_markdown(), encoding="utf-8")
        html_base = tmp / "base.html"
        subprocess.run(
            [
                "pandoc",
                str(fonte),
                "-f",
                "gfm+attributes",
                "-t",
                "html5",
                "--standalone",
                "--toc",
                "--toc-depth=2",
                "--highlight-style=tango",
                "--metadata",
                "title=Curso de Python",
                "--metadata",
                "subtitle=Do zero ao primeiro sistema profissional",
                "--metadata",
                "lang=pt-BR",
                "-o",
                str(html_base),
            ],
            check=True,
        )
        for formato in FORMATOS:
            destino = gerar(formato, html_base, navegador, tmp)
            print(f"Gerado: {destino.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
