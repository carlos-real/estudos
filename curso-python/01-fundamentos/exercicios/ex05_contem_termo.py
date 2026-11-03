"""
Exercício 01.05 — Procurar um termo na observação
Nível: ★☆☆

Contexto: Na planilha de resultados, a coluna de observação traz textos como
"COF: liberado" ou "Tração: OK". O sistema do projeto final precisa saber se um termo
aparece ali, sem se importar com maiúsculas e minúsculas.

Tarefa: implemente `contem_termo(texto, termo)`, que devolve True se `termo` aparece
dentro de `texto` e False caso contrário.
- Ignore a diferença entre maiúsculas e minúsculas ("COF" e "cof" são iguais).
- Ignore espaços no começo e no fim de `termo` ("  liberado " vale como "liberado").

Exemplos:
    >>> contem_termo("COF: liberado", "cof")
    True
    >>> contem_termo("Tração: OK", "COF")
    False
    >>> contem_termo("cof: LIBERADO", "  liberado ")
    True

Dica: o operador `in` já devolve True ou False. Você não precisa de if.

Teste com:  python curso.py testar 01 ex05
"""


def contem_termo(texto: str, termo: str) -> bool:
    """Diz se o termo aparece no texto, sem diferenciar maiúsculas de minúsculas."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
