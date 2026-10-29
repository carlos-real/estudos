"""Núcleo puro e casca de I/O: a ideia que organiza o projeto inteiro.

O NÚCLEO decide (recebe dados, devolve resultado, não lê nem escreve nada).
A CASCA conversa com o mundo (planilha, banco, e-mail, tela) e chama o núcleo.

Rode:  python exemplos/01_nucleo_e_casca.py
"""


# ----------------------------------------------------------------- núcleo (puro)
def verificar_espessura(valor: float, nominal: float, percentual: float) -> str | None:
    """None se passou; senão, o motivo. Não sabe de onde vieram os números."""
    folga = nominal * percentual / 100
    minimo, maximo = round(nominal - folga, 4), round(nominal + folga, 4)
    if minimo <= valor <= maximo:
        return None
    return (
        f"espessura {valor:g} fora de {nominal:g} ± {percentual:g}% ({minimo:g} a {maximo:g})"
    )


# ----------------------------------------------------------------- casca (I/O)
def ler_medicoes_falsas() -> list[tuple[str, float, float]]:
    """Aqui entraria o openpyxl. Para o exemplo, uma lista fixa (OP, valor, nominal)."""
    return [("24518", 41.2, 40.0), ("24519", 44.8, 40.0), ("24520", 49.1, 50.0)]


def main() -> None:
    for op, valor, nominal in ler_medicoes_falsas():
        motivo = verificar_espessura(valor, nominal, 10)
        print(f"OP {op}: {'OK' if motivo is None else motivo}")


if __name__ == "__main__":
    main()
    # O núcleo se testa sem planilha nenhuma:
    assert verificar_espessura(44.0, 40, 10) is None
    assert verificar_espessura(44.8, 40, 10) is not None
    print("núcleo testado sem abrir arquivo nenhum")
