"""
Exercício 14.02 — Carregar as regras do banco SQLite
Nível: ★★☆

Contexto: As especificações e tolerâncias ficam num banco SQLite (schema em SCHEMA,
logo abaixo). Padrões de linha têm a coluna `linha` preenchida ('A'..'D');
especificações de cliente têm `linha` NULL. O resto do sistema não quer saber de SQL:
quer um dicionário de objetos Especificacao prontos.

Tarefa: implemente `carregar_especificacoes(conexao)`.
- Devolva {titulo: Especificacao} com TODAS as linhas da tabela especificacao.
- `linha` NULL no banco vira "" no objeto.
- Cada Especificacao recebe em `tolerancias` um dicionário
  {caracteristica: Tolerancia} com as linhas da tabela tolerancia daquele título
  (minimo, maximo e percentual NULL viram None).
- Especificação sem nenhuma tolerância fica com o dicionário vazio.
- Banco sem especificações -> {}.
- Não feche a conexão: ela é de quem chamou.
- Se o banco tiver uma tolerância sem sentido (ex.: 'fixa' sem mínimo e sem máximo),
  deixe o ValueError da Tolerancia subir: regra quebrada não pode ser ignorada.

Exemplos:
    >>> especificacoes = carregar_especificacoes(conexao)
    >>> sorted(especificacoes)
    ['ESP-0412', 'PADRAO-A']
    >>> especificacoes["PADRAO-A"].linha, especificacoes["ESP-0412"].linha
    ('A', '')
    >>> especificacoes["ESP-0412"].tolerancias["cof"]
    Tolerancia(caracteristica='cof', tipo='fixa', minimo=0.18, maximo=0.25, percentual=None)

Dica: duas consultas resolvem: primeiro SELECT nas especificações (monte o dicionário),
depois SELECT nas tolerâncias (pendure cada uma na especificação do seu título).
`for a, b, c in conexao.execute(sql):` desempacota cada linha.

Teste com:  python curso.py testar 14 ex02
"""

import sqlite3
from dataclasses import dataclass, field

# ============================================================================
# PEÇAS PRONTAS (etapas anteriores) — não precisa mexer
# ============================================================================

SCHEMA = """
CREATE TABLE IF NOT EXISTS linha (
    codigo    TEXT PRIMARY KEY CHECK (codigo IN ('A', 'B', 'C', 'D')),
    descricao TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS especificacao (
    titulo TEXT PRIMARY KEY,
    texto  TEXT NOT NULL DEFAULT '',
    linha  TEXT REFERENCES linha (codigo)
);
CREATE TABLE IF NOT EXISTS tolerancia (
    titulo         TEXT NOT NULL REFERENCES especificacao (titulo),
    caracteristica TEXT NOT NULL,
    tipo           TEXT NOT NULL CHECK (tipo IN ('fixa', 'nominal')),
    minimo         REAL,
    maximo         REAL,
    percentual     REAL,
    PRIMARY KEY (titulo, caracteristica)
);
"""


@dataclass(frozen=True)
class Tolerancia:
    caracteristica: str
    tipo: str  # "fixa" ou "nominal"
    minimo: float | None = None
    maximo: float | None = None
    percentual: float | None = None

    def __post_init__(self) -> None:
        if self.tipo not in ("fixa", "nominal"):
            raise ValueError(f"tipo de tolerância inválido: {self.tipo!r}")
        if self.tipo == "fixa" and self.minimo is None and self.maximo is None:
            raise ValueError(f"{self.caracteristica}: tolerância fixa sem mínimo e máximo")
        if self.tipo == "nominal" and (self.percentual is None or self.percentual <= 0):
            raise ValueError(f"{self.caracteristica}: percentual deve ser > 0")


@dataclass
class Especificacao:
    titulo: str
    texto: str = ""
    linha: str = ""  # preenchida só nos padrões de linha
    tolerancias: dict[str, Tolerancia] = field(default_factory=dict)


# ============================================================================
# SUA PARTE
# ============================================================================


def carregar_especificacoes(conexao: sqlite3.Connection) -> dict[str, Especificacao]:
    """Lê especificações e tolerâncias e devolve {titulo: Especificacao}."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
