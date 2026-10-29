"""
Exercício 12.01 — Classificar códigos de status HTTP (SOLUÇÃO)

Ideia central: o primeiro dígito do código diz a família. Em vez de cinco
comparações de faixa, usamos a divisão inteira por 100 e um dicionário.
"""

FAMILIAS = {
    1: "informativo",
    2: "sucesso",
    3: "redirecionamento",
    4: "erro do cliente",
    5: "erro do servidor",
}

# Conjunto (set): a pergunta "está aqui?" é rápida e o código fica legível.
# 408 = Request Timeout, 429 = Too Many Requests (você está indo rápido demais),
# 500/502/503/504 = o servidor (ou algo no caminho) teve um problema temporário.
PASSAGEIROS = {408, 429, 500, 502, 503, 504}


def classificar_status(codigo: int) -> str:
    """Devolve a família do código de status HTTP."""
    # Primeiro barramos o que está fora da faixa: 99 // 100 seria 0 e
    # 600 // 100 seria 6, que não existem no dicionário.
    if not 100 <= codigo <= 599:
        raise ValueError(f"Código de status inválido: {codigo}")
    return FAMILIAS[codigo // 100]
    # Alternativa com if/elif (também correta, só mais longa):
    #     if 200 <= codigo <= 299:
    #         return "sucesso"
    #     elif ...


def vale_tentar_de_novo(codigo: int) -> bool:
    """True se o erro costuma ser passageiro (vale repetir a requisição)."""
    # Note o que NÃO está aqui: 400, 401, 403 e 404. Repetir não resolve um
    # pedido malformado, uma senha errada ou um endereço que não existe.
    return codigo in PASSAGEIROS
