"""
Solução — Exercício 04.01 — Dividir o lote em bobinas

Ideias centrais: devolver vários valores numa tupla, retorno antecipado para o
caso inválido, e uma função usando a outra.
"""


def dividir_em_bobinas(
    peso_total_kg: float, peso_bobina_kg: float
) -> tuple[int, float] | None:
    """Devolve (bobinas cheias, sobra em kg) ou None se o peso da bobina for inválido."""
    # Retorno antecipado (guard clause): trata o caso ruim logo na entrada e
    # sai. O resto da função pode assumir que o peso da bobina é válido.
    if peso_bobina_kg <= 0:
        return None

    bobinas = int(peso_total_kg // peso_bobina_kg)  # // com float devolve float (4.0)
    # round: % com float tem ruído (1000.3 % 250 dá 0.2999999999999545).
    # float(): se vierem dois int (900 e 300), o resto seria o int 0, e
    # queremos sempre 0.0 na tupla.
    sobra = round(float(peso_total_kg % peso_bobina_kg), 2)
    return bobinas, sobra  # a vírgula cria a tupla; os parênteses são opcionais

    # Alternativa: divmod(a, b) devolve (a // b, a % b) de uma vez:
    #     inteiras, resto = divmod(peso_total_kg, peso_bobina_kg)


def descrever_divisao(peso_total_kg: float, peso_bobina_kg: float) -> str:
    """Descreve a divisão em texto, usando dividir_em_bobinas."""
    resultado = dividir_em_bobinas(peso_total_kg, peso_bobina_kg)
    if resultado is None:
        return "peso da bobina inválido"

    # Desempacotar dá nome às posições: bem melhor que resultado[0].
    bobinas, sobra = resultado
    return f"{bobinas} bobinas de {peso_bobina_kg:.1f} kg + sobra de {sobra:.1f} kg"
