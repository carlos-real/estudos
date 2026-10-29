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

import re
import unicodedata


def prever_v1() -> list[object]:
    """O que esta_liberado_v1 devolve para as 4 observações do enunciado."""
    # 1. "cof: não liberado - ..." CONTÉM "liberado" -> True (o defeito grave:
    #    o "não" é ignorado e a OP vai para a fila).
    # 2. "liberado para corte; cof pendente" também contém "liberado" -> True.
    #    A palavra está lá, mas não fala do COF.
    # 3. "cof: líberado": "lí" não é "li", então "liberado" não aparece -> False.
    #    Uma OP liberada fica bloqueada à toa.
    # 4. None.lower() -> AttributeError: 'NoneType' object has no attribute 'lower'.
    return [True, True, False, "AttributeError"]


def normalizar(texto: str | None) -> str:
    """Minúsculas, sem acento e com espaços simples. None vira ""."""
    if texto is None:
        return ""
    # NFKD decompõe "ã" em "a" + "~" (o til vira um caractere "combinante").
    decomposto = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in decomposto if not unicodedata.combining(c))
    # split() sem argumento quebra em QUALQUER espaço (inclusive \xa0 e \t) e
    # descarta os vazios; o join cola de volta com um espaço só.
    return " ".join(sem_acento.lower().split())


def esta_liberado(observacao: str | None) -> bool:
    """True se a observação tem a marca "COF: liberado" (em qualquer variação)."""
    # Normalizar ANTES da regex deixa o padrão simples: não precisa de
    # re.IGNORECASE, nem de [ií], nem de pensar em espaços duplos.
    # Por que "cof: nao liberado" não casa? Depois de "cof:" e do espaço, o padrão
    # exige "liberad", mas o texto tem "nao". Não há como pular palavras.
    padrao = r"\bcof\s*[:-]?\s*liberad[oa]\b"
    return re.search(padrao, normalizar(observacao)) is not None
