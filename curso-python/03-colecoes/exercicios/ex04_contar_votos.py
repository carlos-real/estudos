"""
Exercício 03.04 — Enquete do refeitório
Nível: ★☆☆

Contexto: O RH fez uma enquete para escolher o prato da sexta-feira. Cada pessoa
digitou o voto à mão, então vieram votos como "Feijoada", "feijoada " e "FEIJOADA".

Tarefa: implemente duas funções.
1. `contar_votos(votos)` devolve um dicionário  prato -> quantidade de votos.
   - Normalize cada voto: tire espaços das pontas e passe para minúscula.
   - Ignore votos vazios (que ficam "" depois de limpar).
   - As chaves aparecem na ordem do primeiro voto de cada prato.
2. `vencedor(contagem)` recebe o dicionário de contagem e devolve o prato com
   mais votos. Em caso de empate, vale o que aparece primeiro no dicionário.
   Dicionário vazio: devolva None.

Exemplos:
    >>> contagem = contar_votos(["Feijoada", "lasanha ", "FEIJOADA", "", "strogonoff"])
    >>> contagem
    {'feijoada': 2, 'lasanha': 1, 'strogonoff': 1}
    >>> vencedor(contagem)
    'feijoada'
    >>> print(vencedor({}))
    None

Dica: o padrão de contagem é  contagem[chave] = contagem.get(chave, 0) + 1.
Para o vencedor, max() aceita key= (seção 11 da aula).

Teste com:  python curso.py testar 03 ex04
"""


def contar_votos(votos: list[str]) -> dict[str, int]:
    """Conta os votos depois de normalizar (strip + lower), ignorando vazios."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def vencedor(contagem: dict[str, int]) -> str | None:
    """Devolve o prato mais votado (o primeiro, em caso de empate) ou None."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
