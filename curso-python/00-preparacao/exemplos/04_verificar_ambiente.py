"""Confere se o seu computador está pronto para o curso.

Rode na pasta curso-python, com o ambiente virtual ativado:
    python 00-preparacao/exemplos/04_verificar_ambiente.py

Você não precisa entender este código agora: ele usa recursos dos próximos módulos.
Leia as mensagens que ele imprime e corrija o que aparecer com ✘.
"""

from __future__ import annotations

import importlib.util
import platform
import re
import shutil
import sys
from pathlib import Path

# A pasta curso-python fica dois níveis acima deste arquivo:
# curso-python/00-preparacao/exemplos/04_verificar_ambiente.py
RAIZ_DO_CURSO = Path(__file__).resolve().parents[2]
REQUISITOS = RAIZ_DO_CURSO / "requirements.txt"


def pacotes_do_requirements(caminho: Path) -> list[str]:
    """Lê os nomes dos pacotes do requirements.txt (ignora comentários e versões)."""
    if not caminho.exists():
        return []
    nomes = []
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.split("#")[0].strip()
        if linha:
            # "pandas>=2.2" -> "pandas"
            nomes.append(re.split(r"[<>=!~\[ ;]", linha)[0])
    return nomes


def marca(ok: bool) -> str:
    return "✔" if ok else "✘"


def main() -> int:
    problemas = 0
    print("Verificando o ambiente do curso...\n")

    # 1) Versão do Python
    versao = platform.python_version()
    if sys.version_info >= (3, 12):
        print(f"✔ Python {versao}")
    else:
        print(f"⚠ Python {versao}: o curso pede 3.12 ou mais novo (mínimo absoluto: 3.10).")

    # 2) Ambiente virtual ativo? (dentro de um venv, sys.prefix aponta para o .venv)
    no_venv = sys.prefix != sys.base_prefix
    print(f"{marca(no_venv)} Ambiente virtual ativo")
    if not no_venv:
        print("    Ative com:  .venv\\Scripts\\Activate.ps1")
        print("    (Linux/macOS: source .venv/bin/activate)")
        problemas += 1

    # 3) Bibliotecas do requirements.txt instaladas?
    faltando = [
        nome
        for nome in pacotes_do_requirements(REQUISITOS)
        if importlib.util.find_spec(nome) is None
    ]
    print(f"{marca(not faltando)} Bibliotecas do curso instaladas")
    if faltando:
        print(f"    Faltando: {', '.join(faltando)}")
        print("    Instale com:  python -m pip install -r requirements.txt")
        problemas += 1

    # 4) Git instalado e no PATH?
    tem_git = shutil.which("git") is not None
    print(f"{marca(tem_git)} Git encontrado")
    if not tem_git:
        print("    Instale o Git for Windows e abra um terminal NOVO.")
        problemas += 1

    # 5) Rodando de dentro da pasta curso-python?
    na_pasta = Path.cwd().resolve() == RAIZ_DO_CURSO
    print(f"{marca(na_pasta)} Terminal na pasta curso-python")
    if not na_pasta:
        print(f"    Você está em: {Path.cwd()}")
        print(f"    Vá para:      cd {RAIZ_DO_CURSO}")
        problemas += 1

    print()
    if problemas == 0:
        print("Tudo pronto! Pode rodar:  python curso.py testar 00")
    else:
        print(f"Faltam {problemas} item(ns). Corrija o que tem ✘ e rode de novo.")
    # Sempre termina sem erro: o objetivo é informar, não quebrar.
    return 0


if __name__ == "__main__":
    sys.exit(main())
