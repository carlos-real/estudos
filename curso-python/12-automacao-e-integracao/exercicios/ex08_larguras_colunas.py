"""
Exercício 12.08 — Calcular a largura das colunas de um relatório
Nível: ★☆☆

Contexto: planilha gerada por robô com colunas estreitas (aquele "#####" no
lugar do número) passa impressão de desleixo. Antes de mexer no openpyxl,
vamos resolver a parte de lógica: qual largura cada coluna precisa ter.

Tarefa: implemente calcular_larguras(linhas, minimo=8, maximo=50).
- `linhas` é uma lista de linhas; cada linha é uma lista de valores
  (a primeira costuma ser o cabeçalho).
- Para cada coluna, a largura é o tamanho do MAIOR texto da coluna
  (len(str(valor))) mais 2 de folga.
- None conta como texto vazio ("").
- Linhas podem ter tamanhos diferentes: a quantidade de colunas é a da linha
  mais comprida; células que faltam contam como vazias.
- Limite cada largura entre `minimo` e `maximo`.
- Sem linhas, devolva [].

Exemplos:
    >>> calcular_larguras([["OP", "Ensaio"], ["123456", "Espessura"]])
    [8, 11]
    >>> calcular_larguras([["Observação"], ["x" * 80]])
    [50]

Dica: monte primeiro uma lista de zeros com o número de colunas e vá
atualizando o máximo de cada posição. max() e min() ajudam a limitar.

Teste com:  python curso.py testar 12 ex08
"""


def calcular_larguras(linhas: list[list], minimo: int = 8, maximo: int = 50) -> list[int]:
    """Largura ideal de cada coluna (maior texto + 2, entre mínimo e máximo)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
