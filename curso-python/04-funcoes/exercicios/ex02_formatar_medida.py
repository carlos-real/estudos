"""
Exercício 04.02 — Formatar medidas para o laudo
Nível: ★☆☆

Contexto: O laudo mostra medidas de vários tipos: espessura em µm (1 casa),
gramatura em g/m², COF sem unidade (2 ou 3 casas), peso em kg. Às vezes o
cliente quer vírgula decimal. Em vez de uma função para cada caso, você vai
escrever UMA função com valores padrão.

Tarefa: implemente `formatar_medida(valor, unidade="µm", casas=1, decimal=".")`.
- Formate o valor com `casas` casas decimais.
- Se `decimal` for ",", troque o ponto decimal por vírgula.
- Se `unidade` não for vazia, acrescente um espaço e a unidade.
  Se for vazia (""), devolva só o número, sem espaço no fim.

Exemplos:
    >>> formatar_medida(50.24)
    '50.2 µm'
    >>> formatar_medida(46, "g/m²")
    '46.0 g/m²'
    >>> formatar_medida(0.2234, unidade="", casas=3)
    '0.223'
    >>> formatar_medida(1250.5, unidade="kg", decimal=",")
    '1250,5 kg'

Dica: o número de casas pode vir de uma variável dentro da f-string:
f"{valor:.{casas}f}" (seção 3 da aula).

Teste com:  python curso.py testar 04 ex02
"""


def formatar_medida(
    valor: float, unidade: str = "µm", casas: int = 1, decimal: str = "."
) -> str:
    """Formata o valor com casas decimais, separador e unidade."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
