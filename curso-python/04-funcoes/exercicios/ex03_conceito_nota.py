"""
Exercício 04.03 — Conceito e situação do aluno
Nível: ★☆☆

Contexto: Uma escola técnica converte a nota (0 a 10) em conceito e decide a
situação final do aluno, que também depende da frequência.

Tarefa: implemente duas funções usando RETORNO ANTECIPADO (um return por caso,
sem if aninhado).
1. `conceito(nota)` devolve:
   - "inválida" se a nota for menor que 0 ou maior que 10;
   - "A" se nota >= 9;  "B" se nota >= 7;  "C" se nota >= 5;  senão "D".
2. `situacao(nota, frequencia_pct)` devolve, nesta ordem de prioridade:
   - "reprovado por falta" se a frequência for menor que 75;
   - "nota inválida" se o conceito for "inválida";
   - "aprovado" se o conceito for A, B ou C;
   - "reprovado por nota" nos demais casos.
   Use a função conceito dentro de situacao.

Exemplos:
    >>> conceito(9.5)
    'A'
    >>> conceito(7)
    'B'
    >>> conceito(11)
    'inválida'
    >>> situacao(8.0, 60)
    'reprovado por falta'
    >>> situacao(4.9, 90)
    'reprovado por nota'

Dica: com retorno antecipado, a ordem dos ifs é a regra de negócio. Escreva o
caso mais restritivo primeiro.

Teste com:  python curso.py testar 04 ex03
"""


def conceito(nota: float) -> str:
    """Converte a nota (0 a 10) em A, B, C, D ou "inválida"."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def situacao(nota: float, frequencia_pct: float) -> str:
    """Decide a situação final do aluno a partir da nota e da frequência."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
