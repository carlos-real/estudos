"""Depuração com breakpoint(): a média de COF está saindo errada. Por quê?

Rode normalmente (mostra o resultado errado):
    python exemplos/04_depuracao.py

Rode com o depurador (o programa PARA no breakpoint e abre o pdb):
    python exemplos/04_depuracao.py --depurar

Comandos do pdb: n (próxima linha), s (entra na função), p expr (mostra valor),
l (mostra o código), c (continua), q (sai). Veja a seção 18 da aula.
"""

import sys

DEPURAR = "--depurar" in sys.argv


def converter(texto: str) -> float:
    """Converte '0,32' em 0.32."""
    return float(texto.replace(",", "."))


def media_cof(leituras: list[str]) -> float:
    """Média das leituras de COF (coeficiente de atrito) de uma bobina."""
    if DEPURAR:
        breakpoint()  # o programa para aqui e abre o depurador
    total = 0.0
    for leitura in leituras:
        valor = converter(leitura)
        total = valor  # BUG de propósito: deveria ser total += valor
    return total / len(leituras)


def main() -> None:
    leituras = ["0,32", "0,35", "0,30"]
    resultado = media_cof(leituras)
    print(f"Leituras: {leituras}")
    print(f"Média calculada: {resultado:.4f}")
    print("Média esperada:  0.3233  (0,32 + 0,35 + 0,30) / 3")


if __name__ == "__main__":
    main()
