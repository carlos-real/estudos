"""ruff na prática: cria um arquivo "bagunçado" numa pasta temporária e roda o ruff nele.

Rode:  python exemplos/05_ruff_na_pratica.py
Precisa do ruff instalado (está no requirements.txt do curso).
O arquivo bagunçado é criado fora do curso, então o seu repositório continua limpo.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CONFIG_DO_CURSO = Path(__file__).resolve().parents[2] / "ruff.toml"

CODIGO_BAGUNCADO = """\
import os, sys
import json


def conferir(valores, minimo, maximo, avisos=[]):
    aprovados = []
    total = len(valores)
    for i in range(len(valores)):
        v = valores[i]
        if v >= minimo and v <= maximo:
            aprovados.append(v)
        else:
            avisos.append("fora: %s" % v)
    return len(aprovados) == len(valores)
"""

CODIGO_MAL_FORMATADO = """\
def limites(nominal,tol):
    margem=nominal*tol/100
    return (nominal-margem , nominal+margem)
"""


def comando_ruff() -> list[str] | None:
    """Descobre como chamar o ruff neste computador."""
    if shutil.which("ruff"):
        return ["ruff"]
    try:
        import ruff  # noqa: F401  (só para saber se está instalado)
    except ImportError:
        return None
    return [sys.executable, "-m", "ruff"]


def rodar(ruff: list[str], argumentos: list[str], pasta: Path) -> None:
    comando = [*ruff, *argumentos, "--config", str(CONFIG_DO_CURSO)]
    print("$ ruff " + " ".join(argumentos))
    resultado = subprocess.run(comando, cwd=pasta, capture_output=True, text=True)
    print(resultado.stdout + resultado.stderr)


def main() -> None:
    ruff = comando_ruff()
    if ruff is None:
        print("O ruff não está instalado. Rode: python -m pip install ruff")
        return
    with tempfile.TemporaryDirectory() as tmp:
        pasta = Path(tmp)
        (pasta / "conferencia.py").write_text(CODIGO_BAGUNCADO, encoding="utf-8")
        (pasta / "limites.py").write_text(CODIGO_MAL_FORMATADO, encoding="utf-8")

        print("1) LINT: procurando problemas\n")
        rodar(ruff, ["check", "--output-format", "concise", "conferencia.py"], pasta)

        print("2) FORMAT: o que mudaria (diff)\n")
        rodar(ruff, ["format", "--diff", "limites.py"], pasta)

        print("3) Aplicando a formatação e mostrando o resultado\n")
        rodar(ruff, ["format", "limites.py"], pasta)
        print((pasta / "limites.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
