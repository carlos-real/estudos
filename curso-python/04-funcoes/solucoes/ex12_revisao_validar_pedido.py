"""
Solução — Exercício 04.12 — Revisão: validar os pedidos da expedição

Ideia central: um validador por campo (pequeno, testável, com retorno
antecipado) e uma função que só COMPÕE os validadores. Nenhuma delas imprime
ou altera o pedido recebido.

    separar_pedidos
    └── validar_pedido
        ├── validar_op
        ├── validar_nf
        └── validar_peso
"""

PESO_MAXIMO_KG = 30000  # um caminhão; acima disso, provavelmente digitaram em gramas


def validar_op(op: str) -> str | None:
    """None se a OP é válida; senão, o texto do problema."""
    texto = op.strip().upper()
    if not texto:
        return "OP vazia"

    numero = texto[3:]  # o que vem depois de "OP-" (fatiamento, módulo 03)
    # Cada condição numa linha, com nome claro, fica fácil de conferir.
    prefixo_ok = texto.startswith("OP-")
    numero_ok = numero.isdigit() and 4 <= len(numero) <= 6
    if not (prefixo_ok and numero_ok):
        return f"OP inválida: '{texto}'"
    return None


def validar_nf(nf: str) -> str | None:
    """None se a NF é válida; senão, o texto do problema."""
    texto = nf.strip()
    if not texto:
        return "NF vazia"
    if not texto.isdigit() or len(texto) > 9:
        return f"NF inválida: '{texto}'"
    return None


def validar_peso(peso_kg: float | None) -> str | None:
    """None se o peso é válido; senão, o texto do problema."""
    # A ordem importa: comparar None com 0 daria TypeError. Por isso o
    # "is None" vem primeiro (retorno antecipado).
    if peso_kg is None:
        return "peso ausente"
    if peso_kg <= 0:
        return "peso deve ser maior que zero"
    if peso_kg > PESO_MAXIMO_KG:
        return f"peso acima de {PESO_MAXIMO_KG} kg (confira a unidade)"
    return None


def validar_pedido(pedido: dict) -> list[str]:
    """Lista os problemas do pedido (vazia se estiver tudo certo)."""
    # "pedido.get('op') or ''" cobre chave ausente E valor None.
    resultados = [
        validar_op(pedido.get("op") or ""),
        validar_nf(pedido.get("nf") or ""),
        validar_peso(pedido.get("peso_kg")),
    ]
    # Fica só com os problemas de verdade (descarta os None).
    return [problema for problema in resultados if problema is not None]


def separar_pedidos(pedidos: list[dict]) -> tuple[list[dict], list[str]]:
    """Separa (pedidos válidos já limpos, mensagens dos inválidos)."""
    validos = []
    mensagens = []
    for posicao, pedido in enumerate(pedidos, start=1):
        problemas = validar_pedido(pedido)
        if problemas:
            mensagens.append(f"pedido {posicao}: " + "; ".join(problemas))
            continue
        # Dicionário NOVO: o pedido original continua como chegou.
        limpo = {**pedido, "op": pedido["op"].strip().upper(), "nf": pedido["nf"].strip()}
        validos.append(limpo)
    return validos, mensagens
