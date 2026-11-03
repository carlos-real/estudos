"""
Exercício 04.08 — Filtros com **kwargs
Nível: ★★☆

Contexto: Você quer uma função de filtro flexível, como um WHERE do SQL:
filtrar_registros(amostras, linha="A", status="aprovado"). Os nomes dos
critérios não são fixos: qualquer coluna pode virar filtro.

Tarefa: implemente duas funções.
1. `criar_amostra(op, linha, **medicoes)` devolve um dicionário com "op",
   "linha" (em maiúscula e sem espaços nas pontas) e cada medição recebida
   por nome, nessa ordem.
2. `filtrar_registros(registros, **criterios)` devolve uma lista NOVA com os
   registros em que, para TODOS os critérios, registro.get(coluna) == valor.
   Sem critérios, devolve todos os registros (numa lista nova).

Exemplos:
    >>> criar_amostra("OP-4512", " a", espessura=50.2, cof=0.22)
    {'op': 'OP-4512', 'linha': 'A', 'espessura': 50.2, 'cof': 0.22}
    >>> tabela = [
    ...     {"op": "OP-1", "linha": "A", "status": "aprovado"},
    ...     {"op": "OP-2", "linha": "B", "status": "aprovado"},
    ...     {"op": "OP-3", "linha": "A", "status": "reprovado"},
    ... ]
    >>> [r["op"] for r in filtrar_registros(tabela, linha="A")]
    ['OP-1', 'OP-3']
    >>> [r["op"] for r in filtrar_registros(tabela, linha="A", status="aprovado")]
    ['OP-1']

Dica: dentro da função, `criterios` é um dicionário comum. all() com uma
expressão geradora (módulo 03) resolve o "para TODOS os critérios".

Teste com:  python curso.py testar 04 ex08
"""


def criar_amostra(op: str, linha: str, **medicoes: float) -> dict:
    """Monta o dicionário da amostra com as medições recebidas por nome."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def filtrar_registros(registros: list[dict], **criterios) -> list[dict]:
    """Devolve os registros que atendem a TODOS os critérios coluna=valor."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
