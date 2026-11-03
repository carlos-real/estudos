"""
Solução — Exercício 04.13 — Revisão: pipeline de limpeza de códigos

Ideia central: funções são valores. compor recebe várias funções (*args),
guarda-as e devolve uma função nova (closure) que as aplica em sequência.
Cada etapa da limpeza é pequena e testável; a ORDEM das etapas fica num só
lugar, fácil de ler e de mudar.
"""

from collections.abc import Callable


def compor(*funcoes: Callable) -> Callable:
    """Devolve uma função que aplica as funções da esquerda para a direita."""

    def aplicar(valor):
        resultado = valor  # acumulador: começa com o valor original
        for funcao in funcoes:  # "funcoes" é lembrada (closure)
            resultado = funcao(resultado)
        return resultado

    # Sem funções, o for não roda e aplicar devolve o próprio valor:
    # a "identidade" sai de graça, sem if.
    return aplicar


def trocar_espacos_por_hifen(texto: str) -> str:
    """Troca cada espaço por hífen."""
    return texto.replace(" ", "-")


def limpar_codigos(codigos: list[str]) -> list[str]:
    """Limpa os códigos (strip, upper, espaço -> hífen), sem vazios nem repetidos."""
    # Métodos de str também são funções: str.strip(texto) == texto.strip().
    limpar = compor(str.strip, str.upper, trocar_espacos_por_hifen)

    vistos: set[str] = set()
    resultado: list[str] = []
    for codigo in codigos:
        limpo = limpar(codigo)
        if not limpo or limpo in vistos:  # vazio ou repetido: pula
            continue
        vistos.add(limpo)
        resultado.append(limpo)
    return resultado
