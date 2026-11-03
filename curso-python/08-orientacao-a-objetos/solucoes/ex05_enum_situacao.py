"""
Exercício 08.05 — Situação de liberação com Enum
Nível: ★☆☆

Contexto: Na planilha, a observação de liberação vem como texto livre:
"COF: liberado", "tração: REPROVADO", "Espessura : pendente ". Guardar a situação
como texto deixa o programa frágil ("liberado" ≠ "Liberado" ≠ "liberada"). Uma
Enum define o conjunto FECHADO de situações possíveis.

A Enum `Situacao` já está pronta abaixo, com três membros. Tarefa:
1. `Situacao.de_texto(texto)` (classmethod): ignora espaços nas pontas e
   maiúsculas e devolve o membro correspondente ("  LIBERADO " -> Situacao.LIBERADO).
   Texto desconhecido: levante ValueError com uma mensagem em português.
2. `pode_emitir` (property): True só para Situacao.LIBERADO.
3. `interpretar_observacao(texto)`: separa no PRIMEIRO ":" e devolve uma tupla
   (ensaio em maiúsculas e sem espaços, Situacao). Sem ":", levante ValueError.

Exemplos:
    >>> Situacao.de_texto(" Reprovado ")
    <Situacao.REPROVADO: 'reprovado'>
    >>> Situacao.LIBERADO.pode_emitir
    True
    >>> interpretar_observacao("COF: liberado")
    ('COF', <Situacao.LIBERADO: 'liberado'>)

Dica: Situacao("liberado") já procura o membro pelo valor (e levanta ValueError
se não achar). Dentro do classmethod, use cls(...).

Teste com:  python curso.py testar 08 ex05
"""

from enum import Enum


class Situacao(Enum):
    """Situação de liberação de um ensaio."""

    LIBERADO = "liberado"
    REPROVADO = "reprovado"
    PENDENTE = "pendente"

    @classmethod
    def de_texto(cls, texto: str) -> "Situacao":
        """Converte texto livre no membro da Enum."""
        try:
            # cls(valor) procura o membro pelo VALOR ("liberado" -> LIBERADO).
            return cls(texto.strip().lower())
        except ValueError:
            # Trocamos a mensagem em inglês por uma em português, com o texto original.
            raise ValueError(f"Situação desconhecida: {texto!r}") from None

    @property
    def pode_emitir(self) -> bool:
        """Só ensaio liberado permite emitir o certificado."""
        # Membros de Enum são únicos: compare com "is".
        return self is Situacao.LIBERADO


def interpretar_observacao(texto: str) -> tuple[str, Situacao]:
    """'COF: liberado' -> ('COF', Situacao.LIBERADO)."""
    if ":" not in texto:
        raise ValueError(f"Observação sem ':': {texto!r}")
    ensaio, situacao = texto.split(":", 1)  # maxsplit=1: só o primeiro ":"
    return ensaio.strip().upper(), Situacao.de_texto(situacao)
