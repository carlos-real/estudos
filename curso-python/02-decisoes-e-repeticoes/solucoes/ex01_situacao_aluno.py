"""
Exercício 02.01 — Situação do aluno
Nível: ★☆☆

Contexto: O clássico dos clássicos: a escola precisa dizer se o aluno passou, ficou
de recuperação ou reprovou, a partir da média final (de 0 a 10).

Tarefa: implemente `situacao(media)`, que devolve:
- "Nota inválida" se a média for menor que 0 ou maior que 10;
- "Aprovado" se a média for 7 ou mais;
- "Recuperação" se a média for 5 ou mais (e menor que 7);
- "Reprovado" nos demais casos.

Exemplos:
    >>> situacao(7.0)
    'Aprovado'
    >>> situacao(6.9)
    'Recuperação'
    >>> situacao(11)
    'Nota inválida'

Dica: valide primeiro (nota inválida) e depois teste da maior faixa para a menor.
A ordem dos elif importa.

Teste com:  python curso.py testar 02 ex01
"""


def situacao(media: float) -> str:
    """Devolve a situação do aluno a partir da média."""
    # 1º validar: dado ruim é tratado antes de qualquer regra de negócio.
    if media < 0 or media > 10:
        return "Nota inválida"
    # 2º regras da maior faixa para a menor. Quando chegamos ao elif, já sabemos que
    # media < 7 (senão o if teria pego), então não precisamos escrever 5 <= media < 7.
    if media >= 7:
        return "Aprovado"
    elif media >= 5:
        return "Recuperação"
    else:
        return "Reprovado"

    # Armadilha: testar "media >= 5" ANTES de "media >= 7" faria um 9 cair em
    # "Recuperação", porque 9 >= 5 é verdade e o primeiro bloco verdadeiro ganha.
