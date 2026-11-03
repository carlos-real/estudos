"""
Exercício 07.06 — Sorteio de bobinas para auditoria
Nível: ★★☆

Contexto: A auditoria interna pede que as bobinas reensaiadas sejam escolhidas por
SORTEIO, e que o sorteio possa ser repetido depois (para provar que não houve
escolha a dedo). Para isso usamos uma semente: mesma semente, mesmo sorteio.

Tarefa:
1. `sortear_bobinas(bobinas, quantidade, semente=None)` sorteia `quantidade` bobinas
   SEM repetição, usando EXATAMENTE `random.Random(semente).sample(bobinas, quantidade)`.
   Levante ValueError se quantidade for negativa ou maior que o número de bobinas.
2. `sortear_por_linha(bobinas_por_linha, por_linha, semente=None)` recebe um dicionário
   {linha: [bobinas]} e sorteia `por_linha` bobinas de cada linha. Regras exatas:
   - crie UM gerador: `gerador = random.Random(semente)`;
   - percorra as linhas em ordem alfabética (sorted);
   - de cada linha sorteie `gerador.sample(lista, min(por_linha, len(lista)))`;
   - devolva {linha: sorteadas}, com as linhas em ordem alfabética.
3. `embaralhar_ordem(amostras, semente=None)` devolve uma NOVA lista com as amostras
   embaralhadas (ordem em que vão para o equipamento) usando
   `random.Random(semente).shuffle(...)` numa CÓPIA. A lista original não muda.

Exemplos:
    >>> sortear_bobinas(["B01", "B02", "B03", "B04", "B05"], 2, semente=1)
    ['B02', 'B01']
    >>> sortear_bobinas(["B01", "B02"], 3)
    Traceback (most recent call last):
    ...
    ValueError: Não dá para sortear 3 de 2 bobinas

Dica: shuffle embaralha a própria lista e devolve None. Copie antes: lista[:] ou
list(lista).

Teste com:  python curso.py testar 07 ex06
"""


def sortear_bobinas(
    bobinas: list[str], quantidade: int, semente: int | None = None
) -> list[str]:
    """Sorteia bobinas sem repetição (reprodutível com a semente)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def sortear_por_linha(
    bobinas_por_linha: dict[str, list[str]], por_linha: int, semente: int | None = None
) -> dict[str, list[str]]:
    """Sorteia até `por_linha` bobinas de cada linha."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def embaralhar_ordem(amostras: list[str], semente: int | None = None) -> list[str]:
    """Nova lista com as amostras em ordem aleatória (a original não muda)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
