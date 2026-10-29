"""
Exercício 12.07 — Organizar laudos em pastas (SOLUÇÃO)

Raciocínio:
1. Decidir O QUE fazer com cada arquivo (o "plano") não depende do modo.
2. O modo ensaio só decide se o plano é EXECUTADO.
Separar as duas coisas faz o ensaio mostrar exatamente o que aconteceria.
"""

import re
import shutil
from pathlib import Path

# Grupos: 1 = OP, 2 = linha, 3 = ano-mês (o dia não importa para a pasta).
PADRAO = re.compile(r"laudo_(\d{6})_([A-D])_(\d{4}-\d{2})-\d{2}\.pdf")


def organizar_laudos(origem: Path, destino: Path, ensaio: bool = True) -> list[tuple[str, str]]:
    """Planeja (e, fora do ensaio, executa) a organização dos laudos."""
    resultado = []
    # sorted() já deixa a lista final em ordem alfabética pelo nome.
    for arquivo in sorted(origem.iterdir(), key=lambda p: p.name):
        achado = PADRAO.fullmatch(arquivo.name)  # fullmatch: o nome INTEIRO
        if not arquivo.is_file() or achado is None:
            continue

        linha, ano_mes = achado.group(2), achado.group(3)
        alvo = destino / f"linha_{linha}" / ano_mes / arquivo.name

        if alvo.exists():
            continue  # nunca sobrescrever: fica na origem para alguém olhar

        if not ensaio:
            alvo.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(arquivo, alvo)

        # as_posix() garante "/" também no Windows, que usaria "\".
        resultado.append((arquivo.name, alvo.relative_to(destino).as_posix()))
    return resultado
