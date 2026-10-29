"""
Solução — Exercício 04.02 — Formatar medidas para o laudo

Ideia central: valores padrão deixam o caso comum curto (formatar_medida(50.2))
e os casos especiais explícitos (formatar_medida(0.22, unidade="", casas=2)).
"""


def formatar_medida(
    valor: float, unidade: str = "µm", casas: int = 1, decimal: str = "."
) -> str:
    """Formata o valor com casas decimais, separador e unidade."""
    # {casas} dentro da especificação de formato: o Python primeiro troca
    # {casas} pelo número (ex.: 3) e depois aplica ".3f".
    numero = f"{valor:.{casas}f}"

    if decimal == ",":
        numero = numero.replace(".", ",")

    if not unidade:  # string vazia é falsy
        return numero
    return f"{numero} {unidade}"

    # Atenção: não usamos separador de milhar aqui. Com milhar, trocar "."
    # por "," exigiria trocar os dois separadores (assunto do módulo 05).
