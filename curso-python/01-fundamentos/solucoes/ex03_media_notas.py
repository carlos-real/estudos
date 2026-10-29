"""
Exercício 01.03 — Média de notas
Nível: ★☆☆

Contexto: Clássico de todo curso: calcular a média de um aluno. É o lugar perfeito para
cair (ou não) na armadilha da precedência dos operadores.

Tarefa:
1. `calcular_media(nota1, nota2, nota3)` devolve a média aritmética das três notas.
2. `calcular_media_ponderada(nota1, peso1, nota2, peso2)` devolve a média ponderada:
   (nota1 * peso1 + nota2 * peso2) / (peso1 + peso2).
Não arredonde os resultados.

Exemplos:
    >>> calcular_media(7, 8, 9)
    8.0
    >>> calcular_media_ponderada(8, 2, 5, 1)
    7.0

Dica: o que o Python calcula primeiro em 7 + 8 + 9 / 3? Teste no REPL.

Teste com:  python curso.py testar 01 ex03
"""


def calcular_media(nota1: float, nota2: float, nota3: float) -> float:
    """Devolve a média aritmética de três notas."""
    # Os parênteses são obrigatórios: sem eles, o Python faria nota3 / 3 primeiro
    # (divisão vem antes da soma) e somaria o resultado às outras notas.
    return (nota1 + nota2 + nota3) / 3


def calcular_media_ponderada(nota1: float, peso1: float, nota2: float, peso2: float) -> float:
    """Devolve a média ponderada de duas notas."""
    # Separar numerador e denominador em variáveis deixa a fórmula legível e facilita
    # conferir cada parte no REPL se algo der errado.
    soma_ponderada = nota1 * peso1 + nota2 * peso2  # * vem antes de +: sem parênteses
    soma_dos_pesos = peso1 + peso2
    return soma_ponderada / soma_dos_pesos
