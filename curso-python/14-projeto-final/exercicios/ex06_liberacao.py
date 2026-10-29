r"""
Exercício 14.06 — Observação de liberação: leia, preveja e conserte
Nível: ★★☆

Contexto: Um estagiário escreveu a primeira versão da checagem de liberação do COF:

    def esta_liberado_v1(observacao):
        return "liberado" in observacao.lower()

Ela foi para produção e deu problema: OP sem liberação entrou na fila. Leia o código
com atenção antes de continuar.

Tarefa 1 (leitura de código): implemente `prever_v1()` devolvendo uma lista com o
que esta_liberado_v1 devolveria para estas observações, nesta ordem. Responda SEM
RODAR primeiro; depois confira.
    1. "COF: não liberado - refazer ensaio"
    2. "Liberado para corte; COF pendente"
    3. "COF: líberado"      (o técnico digitou um acento sem querer)
    4. None                 (célula vazia na planilha)
Use True ou False. Quando a função quebraria, use o NOME da exceção como texto
(ex.: "TypeError").

Tarefa 2: implemente `normalizar(texto)`: minúsculas, sem acento e com espaços
simples (sem espaço nas pontas e um só espaço entre palavras). None vira "".

Tarefa 3: implemente a versão correta, `esta_liberado(observacao)`. Ela devolve True
só se o texto normalizado tiver a palavra "cof" seguida de "liberado" ou "liberada"
(podendo haver ":" ou "-" e espaços no meio). "cof: nao liberado", "aguardando",
"liberado" sem "cof", texto vazio e None devolvem False.

Exemplos:
    >>> normalizar("  COF:   Não  Liberado ")
    'cof: nao liberado'
    >>> esta_liberado("COF - LIBERADO")
    True
    >>> esta_liberado("Cof: Liberado. Bobina 2 com rebarba")
    True
    >>> esta_liberado("COF: não liberado - refazer ensaio")
    False

Dica: unicodedata.normalize("NFKD", texto) separa a letra do acento ("í" vira "i" +
acento); descarte os caracteres c em que unicodedata.combining(c) é verdadeiro.
Para a marca, use re.search com: \b + cof + \s* + [:-]? + \s* + liberad[oa] + \b.

Teste com:  python curso.py testar 14 ex06
"""

import re  # noqa: F401 (você vai usar)
import unicodedata  # noqa: F401 (você vai usar)


def prever_v1() -> list[object]:
    """O que esta_liberado_v1 devolve para as 4 observações do enunciado."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def normalizar(texto: str | None) -> str:
    """Minúsculas, sem acento e com espaços simples. None vira ""."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def esta_liberado(observacao: str | None) -> bool:
    """True se a observação tem a marca "COF: liberado" (em qualquer variação)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
