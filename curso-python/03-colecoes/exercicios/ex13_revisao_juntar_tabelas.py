"""
Exercício 03.13 — Revisão: juntar pedidos e resultados (o seu primeiro JOIN)
Nível: ★★★

Contexto: Este exercício mistura o módulo 03 (lista de dicionários, índice com
dicionário) com o 01 (strip, upper, replace, round) e o 02 (if/elif/else,
acumuladores). A expedição digita a OP de vários jeitos ("op-4512",
" OP 4512 "); a planilha do laboratório tem o status de cada OP.

    pedidos = [{"op": "op-4512", "nf": "123", "peso_kg": 500.0}, ...]
    resultados = [{"op": "OP-4512", "linha": "A", "status": "Aprovado"}, ...]

Tarefa: implemente quatro funções.
1. `normalizar_op(texto)`: tira espaços das pontas, passa para maiúscula e
   troca espaços internos por "-".  " op 4512 " -> "OP-4512".
2. `indexar_por_op(resultados)`: devolve um dicionário  OP normalizada ->
   resultado (o próprio dicionário). Se a OP se repetir, vale o ÚLTIMO.
3. `juntar(pedidos, resultados)`: para cada pedido, na ordem, devolve um
   dicionário NOVO com todas as chaves do pedido (com "op" normalizada) mais:
   - "linha": a linha do resultado (ou None, se não houver resultado);
   - "status": o status do resultado em minúsculas e sem espaços nas pontas
     (ou "sem resultado").
   Não altere os pedidos nem os resultados.
4. `resumo_expedicao(juntados)`: recebe a saída de `juntar` e devolve
   {"emitir": [...], "bloqueadas": [...], "sem_resultado": [...],
    "peso_emitir_kg": ...}
   - "emitir": OPs com status "aprovado"; "sem_resultado": OPs com status
     "sem resultado"; "bloqueadas": as demais (reprovado, em análise...).
   - As listas seguem a ordem dos pedidos.
   - "peso_emitir_kg": soma dos pesos das OPs a emitir, round(..., 1).

Exemplos:
    >>> normalizar_op(" op 4512 ")
    'OP-4512'
    >>> pedidos = [{"op": "op-4512", "nf": "123", "peso_kg": 500.0},
    ...            {"op": "OP-4599", "nf": "124", "peso_kg": 80.5}]
    >>> resultados = [{"op": "OP-4512", "linha": "A", "status": " Aprovado"}]
    >>> juntados = juntar(pedidos, resultados)
    >>> juntados[0]
    {'op': 'OP-4512', 'nf': '123', 'peso_kg': 500.0, 'linha': 'A', 'status': 'aprovado'}
    >>> juntados[1]["status"]
    'sem resultado'
    >>> resumo = resumo_expedicao(juntados)
    >>> resumo["emitir"], resumo["sem_resultado"], resumo["peso_emitir_kg"]
    (['OP-4512'], ['OP-4599'], 500.0)

Dica: procurar cada pedido percorrendo TODOS os resultados funciona, mas é
lento (é um laço dentro de outro). Monte o índice uma vez e use .get(op).

Teste com:  python curso.py testar 03 ex13
"""


def normalizar_op(texto: str) -> str:
    """Padroniza o código da OP: " op 4512 " -> "OP-4512"."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def indexar_por_op(resultados: list[dict]) -> dict[str, dict]:
    """Devolve OP normalizada -> resultado (o último, se houver repetição)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def juntar(pedidos: list[dict], resultados: list[dict]) -> list[dict]:
    """LEFT JOIN: cada pedido ganha "linha" e "status" do seu resultado."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def resumo_expedicao(juntados: list[dict]) -> dict:
    """Separa as OPs em emitir / bloqueadas / sem_resultado e soma o peso."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
