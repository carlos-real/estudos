"""Exemplo 09 — validação de dados antes de usar.

Rode com:  python exemplos/09_validacao.py
"""


def eh_inteiro_positivo(texto: str) -> bool:
    """True se o texto (sem espaços nas pontas) tem só dígitos e não é zero."""
    limpo = texto.strip()
    if not limpo:  # texto vazio é falsy
        return False
    for caractere in limpo:
        if caractere not in "0123456789":
            return False  # basta UM caractere ruim para reprovar
    return int(limpo) > 0


def validar_quantidade(texto: str) -> str:
    """Valida a quantidade de bobinas digitada para um palete."""
    if not eh_inteiro_positivo(texto):
        return f"{texto!r}: digite um número inteiro maior que zero"
    quantidade = int(texto)  # seguro: já sabemos que só tem dígitos
    if quantidade > 12:
        return f"{texto!r}: um palete leva no máximo 12 bobinas"
    return f"{texto!r}: OK, {quantidade} bobinas"


for entrada in ["8", " 12 ", "abc", "", "7.5", "0", "15", "-3"]:
    print(validar_quantidade(entrada))
