"""Módulo com conversões no formato brasileiro.

Pode ser IMPORTADO por outro arquivo (veja 02_usando_conversoes.py) ou RODADO
direto (python exemplos/conversoes_br.py), e aí o bloco do final executa.
"""


def numero_br(texto: str) -> float:
    """Converte '1.250,5' em 1250.5."""
    return float(texto.strip().replace(".", "").replace(",", "."))


def formatar_br(valor: float, casas: int = 2) -> str:
    """Converte 1250.5 em '1.250,50'."""
    texto = f"{valor:,.{casas}f}"  # '1,250.50' (padrão americano)
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


print(f"[conversoes_br] carregado; __name__ = {__name__!r}")

if __name__ == "__main__":
    # Só roda quando o arquivo é executado diretamente: ótimo para um autoteste rápido
    print(numero_br("1.250,5"))
    print(formatar_br(1250.5))
