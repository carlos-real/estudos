"""
Exercício 12.01 — Classificar códigos de status HTTP
Nível: ★☆☆

Contexto: o robô consulta uma API e precisa decidir o que fazer com cada
resposta: seguir em frente, desistir ou tentar de novo mais tarde.

Tarefa: implemente duas funções.

1. classificar_status(codigo) devolve a família do código:
   - 100 a 199 -> "informativo"
   - 200 a 299 -> "sucesso"
   - 300 a 399 -> "redirecionamento"
   - 400 a 499 -> "erro do cliente"
   - 500 a 599 -> "erro do servidor"
   Qualquer outro número levanta ValueError com a mensagem
   "Código de status inválido: <codigo>".

2. vale_tentar_de_novo(codigo) devolve True só para os códigos que costumam
   ser passageiros: 408, 429, 500, 502, 503 e 504. Para os outros, False.

Exemplos:
    >>> classificar_status(201)
    'sucesso'
    >>> classificar_status(404)
    'erro do cliente'
    >>> vale_tentar_de_novo(503)
    True
    >>> vale_tentar_de_novo(404)
    False

Dica: a divisão inteira 404 // 100 dá 4.

Teste com:  python curso.py testar 12 ex01
"""


def classificar_status(codigo: int) -> str:
    """Devolve a família do código de status HTTP."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def vale_tentar_de_novo(codigo: int) -> bool:
    """True se o erro costuma ser passageiro (vale repetir a requisição)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
