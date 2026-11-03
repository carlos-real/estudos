"""Funções de apoio usadas pelos exemplos do módulo 11.

abrir_banco_exemplo()  cria o banco do laboratório NA MEMÓRIA (a partir de
                       dados/laboratorio.sql). Cada exemplo começa do zero.
mostrar(conexao, sql)  roda uma consulta e imprime o resultado como tabela.

Rode este arquivo para ver um exemplo:
    python 11-banco-de-dados-e-sql/exemplos/utilitarios.py
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

DADOS = Path(__file__).resolve().parent.parent / "dados"


def abrir_banco_exemplo(script: str = "laboratorio.sql") -> sqlite3.Connection:
    """Devolve uma conexão com o banco de exemplo montado na memória."""
    conexao = sqlite3.connect(":memory:")
    conexao.executescript((DADOS / script).read_text(encoding="utf-8"))
    return conexao


def formatar(valor: object) -> str:
    if valor is None:
        return "NULL"
    if isinstance(valor, float):
        return f"{valor:g}"
    return str(valor)


def mostrar(conexao: sqlite3.Connection, sql: str, parametros: tuple | dict = ()) -> None:
    """Executa a consulta e imprime as linhas alinhadas, com o cabeçalho."""
    cursor = conexao.execute(sql, parametros)
    nomes = [coluna[0] for coluna in cursor.description]
    linhas = [[formatar(v) for v in linha] for linha in cursor.fetchall()]
    larguras = [
        max([len(nome), *(len(linha[i]) for linha in linhas)]) for i, nome in enumerate(nomes)
    ]
    print(" | ".join(n.ljust(w) for n, w in zip(nomes, larguras, strict=True)).rstrip())
    print("-+-".join("-" * largura for largura in larguras))
    for linha in linhas:
        print(" | ".join(v.ljust(w) for v, w in zip(linha, larguras, strict=True)).rstrip())
    print(f"({len(linhas)} linha{'s' if len(linhas) != 1 else ''})\n")


if __name__ == "__main__":
    banco = abrir_banco_exemplo()
    mostrar(banco, "SELECT codigo, descricao FROM linha")
    banco.close()
