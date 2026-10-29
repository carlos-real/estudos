"""Ferramenta do curso: testa seus exercícios e mostra seu progresso.

Uso (rode dentro da pasta curso-python):
    python curso.py testar 03          # testa todos os exercícios do módulo 03
    python curso.py testar 03 ex05     # testa só o exercício 05 do módulo 03
    python curso.py progresso          # mostra quantos exercícios você já resolveu
    python curso.py modulos            # lista os módulos do curso
    python curso.py solucoes [03]      # confere as soluções oficiais (quem mantém o curso)
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
PADRAO_MODULO = re.compile(r"^(\d{2})-(.+)$")


def listar_modulos() -> list[Path]:
    """Pastas de módulo (ex.: 03-colecoes), em ordem."""
    return sorted(p for p in RAIZ.iterdir() if p.is_dir() and PADRAO_MODULO.match(p.name))


def titulo(modulo: Path) -> str:
    numero, nome = PADRAO_MODULO.match(modulo.name).groups()
    return f"{numero} {nome.replace('-', ' ').title()}"


def encontrar_modulo(numero: str) -> Path:
    numero = numero.strip().zfill(2)
    for modulo in listar_modulos():
        if modulo.name.startswith(f"{numero}-"):
            return modulo
    disponiveis = ", ".join(m.name[:2] for m in listar_modulos())
    sys.exit(f"Módulo {numero} não encontrado. Módulos disponíveis: {disponiveis}")


def normalizar_exercicio(texto: str) -> str:
    """Aceita '5', '05', 'ex5' ou 'ex05' e devolve 'ex05'."""
    digitos = re.sub(r"\D", "", texto)
    if not digitos:
        sys.exit(f"Exercício inválido: {texto!r}. Use algo como ex05.")
    return f"ex{int(digitos):02d}"


def exigir_pytest() -> None:
    if importlib.util.find_spec("pytest") is None:
        sys.exit(
            "O pytest não está instalado neste Python.\n"
            "Rode: python -m pip install -r requirements.txt\n"
            "(com o ambiente virtual ativado, veja o módulo 00)."
        )


def rodar_pytest(alvos: list[Path], solucoes: bool, extra: list[str]) -> int:
    exigir_pytest()
    ambiente = os.environ.copy()
    if solucoes:
        ambiente["CURSO_SOLUCOES"] = "1"
    else:
        ambiente.pop("CURSO_SOLUCOES", None)
    comando = [sys.executable, "-m", "pytest", *map(str, alvos), *extra]
    return subprocess.run(comando, cwd=RAIZ, env=ambiente).returncode


def cmd_testar(args: argparse.Namespace) -> int:
    modulo = encontrar_modulo(args.modulo)
    pasta_testes = modulo / "testes"
    if not pasta_testes.exists():
        sys.exit(f"O módulo {modulo.name} não tem testes automáticos.")
    if args.exercicio:
        ex = normalizar_exercicio(args.exercicio)
        alvos = sorted(pasta_testes.glob(f"test_*_{ex}_*.py"))
        if not alvos:
            sys.exit(f"Não achei testes para {ex} em {modulo.name}.")
    else:
        alvos = [pasta_testes]
    codigo = rodar_pytest(alvos, solucoes=False, extra=["-v", "--tb=short", "--no-header"])
    if codigo == 0:
        print("\n✔ Tudo certo! Pode seguir para o próximo exercício.")
    else:
        print("\n✘ Ainda há testes falhando. Leia a mensagem acima: ela diz o que era")
        print("  esperado e o que seu código devolveu. Corrija e rode de novo.")
    return codigo


def coletar_resultados(modulos: list[Path]) -> dict[str, dict[str, bool]]:
    """Roda os testes em silêncio e devolve {modulo: {exercicio: passou?}}."""
    exigir_pytest()
    pastas = [m / "testes" for m in modulos if (m / "testes").exists()]
    resultados: dict[str, dict[str, bool]] = {}
    if not pastas:
        return resultados
    with tempfile.TemporaryDirectory() as tmp:
        relatorio = Path(tmp) / "resultado.xml"
        ambiente = os.environ.copy()
        ambiente.pop("CURSO_SOLUCOES", None)
        comando = [
            sys.executable,
            "-m",
            "pytest",
            *map(str, pastas),
            "-q",
            "--tb=no",
            "-p",
            "no:cacheprovider",
            f"--junitxml={relatorio}",
            "-o",
            "junit_family=xunit1",
        ]
        subprocess.run(comando, cwd=RAIZ, env=ambiente, capture_output=True)
        if not relatorio.exists():
            return resultados
        arvore = ET.parse(relatorio)
    for caso in arvore.iter("testcase"):
        arquivo = caso.get("file") or ""
        partes = Path(arquivo).parts
        if len(partes) < 3:
            continue
        modulo, nome_arquivo = partes[0], partes[-1]
        achado = re.search(r"_(ex\d+)_", nome_arquivo)
        if not achado:
            continue
        passou = not any(filho.tag in {"failure", "error", "skipped"} for filho in caso)
        exercicios = resultados.setdefault(modulo, {})
        exercicios[achado.group(1)] = exercicios.get(achado.group(1), True) and passou
    for pasta in pastas:
        exercicios = resultados.setdefault(pasta.parent.name, {})
        for arquivo in pasta.glob("test_*.py"):
            achado = re.search(r"_(ex\d+)_", arquivo.name)
            if achado:
                exercicios.setdefault(achado.group(1), False)
    return resultados


def barra(feitos: int, total: int, largura: int = 20) -> str:
    cheios = round(largura * feitos / total) if total else 0
    return "█" * cheios + "░" * (largura - cheios)


def cmd_progresso(args: argparse.Namespace) -> int:
    modulos = listar_modulos()
    print("Conferindo seus exercícios, aguarde...\n")
    resultados = coletar_resultados(modulos)
    total_feitos = total_geral = 0
    for modulo in modulos:
        exercicios = resultados.get(modulo.name, {})
        if not exercicios:
            continue
        feitos = sum(exercicios.values())
        total = len(exercicios)
        total_feitos += feitos
        total_geral += total
        marca = "✔" if feitos == total else " "
        print(f"{marca} {titulo(modulo):<34} {barra(feitos, total)} {feitos:>2}/{total}")
        if args.detalhes:
            linha = "   " + "  ".join(
                f"{ex}{'✔' if ok else '·'}" for ex, ok in sorted(exercicios.items())
            )
            print(linha)
    if total_geral:
        pct = 100 * total_feitos / total_geral
        print(f"\nTotal: {total_feitos}/{total_geral} exercícios ({pct:.0f}%)")
    return 0


def cmd_modulos(args: argparse.Namespace) -> int:
    for modulo in listar_modulos():
        testes = modulo / "testes"
        qtd = len(list(testes.glob("test_*.py"))) if testes.exists() else 0
        print(f"{titulo(modulo):<36} {qtd:>2} exercícios")
    return 0


def cmd_solucoes(args: argparse.Namespace) -> int:
    modulos = [encontrar_modulo(args.modulo)] if args.modulo else listar_modulos()
    alvos = [m / "testes" for m in modulos if (m / "testes").exists()]
    if not alvos:
        sys.exit("Nenhum teste encontrado.")
    return rodar_pytest(alvos, solucoes=True, extra=["-q"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Ferramenta do Curso de Python.")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_testar = sub.add_parser("testar", help="testa os exercícios de um módulo")
    p_testar.add_argument("modulo", help="número do módulo, ex.: 03")
    p_testar.add_argument("exercicio", nargs="?", help="exercício, ex.: ex05")
    p_testar.set_defaults(func=cmd_testar)

    p_prog = sub.add_parser("progresso", help="mostra seu progresso no curso")
    p_prog.add_argument("-d", "--detalhes", action="store_true", help="mostra cada exercício")
    p_prog.set_defaults(func=cmd_progresso)

    p_mod = sub.add_parser("modulos", help="lista os módulos")
    p_mod.set_defaults(func=cmd_modulos)

    p_sol = sub.add_parser("solucoes", help="confere as soluções oficiais")
    p_sol.add_argument("modulo", nargs="?", help="número do módulo (opcional)")
    p_sol.set_defaults(func=cmd_solucoes)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
