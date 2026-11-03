"""
Exercício 04.12 — Revisão: validar os pedidos da expedição
Nível: ★★★

Contexto: Este exercício mistura o módulo 04 (decomposição, retorno antecipado,
funções pequenas) com o 01 (métodos de string), o 02 (validação, laços) e o 03
(dicionários, listas, enumerate). Os pedidos chegam do e-mail da expedição
assim:

    {"op": " op-45120", "nf": "000123456", "peso_kg": 1250.5}

Tarefa: implemente cinco funções. Cada validador devolve None quando está tudo
certo, ou o TEXTO do problema.
1. `validar_op(op)`: limpe com strip + upper.
   - vazia -> "OP vazia"
   - precisa começar com "OP-" e ter de 4 a 6 dígitos depois do hífen;
     senão -> "OP inválida: 'OP-12'" (com o texto já limpo entre aspas simples)
2. `validar_nf(nf)`: limpe com strip.
   - vazia -> "NF vazia"
   - só dígitos e no máximo 9 deles; senão -> "NF inválida: '12A'"
3. `validar_peso(peso_kg)`:
   - None -> "peso ausente"
   - menor ou igual a 0 -> "peso deve ser maior que zero"
   - maior que 30000 -> "peso acima de 30000 kg (confira a unidade)"
4. `validar_pedido(pedido)`: devolve a LISTA de problemas, na ordem op, nf,
   peso (lista vazia = pedido válido). Chave ausente ou com None conta como
   vazia (op, nf) ou ausente (peso).
5. `separar_pedidos(pedidos)`: devolve a tupla (validos, mensagens):
   - validos: dicionários NOVOS dos pedidos sem problema, com "op" limpa
     (strip + upper) e "nf" limpa (strip); as demais chaves ficam iguais;
   - mensagens: um texto por pedido com problema, com a posição (a partir de
     1) e os problemas unidos por "; ":
     "pedido 2: OP inválida: 'OP-12'; peso deve ser maior que zero"

Exemplos:
    >>> validar_op(" op-45120")
    >>> validar_op("OP-12")
    "OP inválida: 'OP-12'"
    >>> validar_nf("12A")
    "NF inválida: '12A'"
    >>> validar_pedido({"op": "OP-4512", "nf": "", "peso_kg": None})
    ['NF vazia', 'peso ausente']
    >>> validos, mensagens = separar_pedidos([
    ...     {"op": " op-45120", "nf": "123456", "peso_kg": 1250.5},
    ...     {"op": "OP-12", "nf": "123", "peso_kg": 0},
    ... ])
    >>> validos
    [{'op': 'OP-45120', 'nf': '123456', 'peso_kg': 1250.5}]
    >>> mensagens
    ["pedido 2: OP inválida: 'OP-12'; peso deve ser maior que zero"]

Dica: dois métodos de string ajudam (seção 11 da aula): texto.startswith("OP-")
e texto.isdigit(). Para "chave ausente ou None", use pedido.get("op") or "".

Teste com:  python curso.py testar 04 ex12
"""


def validar_op(op: str) -> str | None:
    """None se a OP é válida; senão, o texto do problema."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def validar_nf(nf: str) -> str | None:
    """None se a NF é válida; senão, o texto do problema."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def validar_peso(peso_kg: float | None) -> str | None:
    """None se o peso é válido; senão, o texto do problema."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def validar_pedido(pedido: dict) -> list[str]:
    """Lista os problemas do pedido (vazia se estiver tudo certo)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def separar_pedidos(pedidos: list[dict]) -> tuple[list[dict], list[str]]:
    """Separa (pedidos válidos já limpos, mensagens dos inválidos)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
