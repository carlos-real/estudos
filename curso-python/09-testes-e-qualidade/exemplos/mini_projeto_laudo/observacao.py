"""Leitura da observação de liberação da planilha (ex.: "COF: liberado").

Este código nasceu com TDD: veja a seção 13 da aula do módulo 09.
"""

STATUS_VALIDOS = {"liberado": True, "reprovado": False}


def _ler_item(item: str) -> tuple[str, bool]:
    """Converte 'COF: liberado' em ('COF', True)."""
    ensaio, status = item.split(":")
    status = status.strip()
    if status not in STATUS_VALIDOS:
        raise ValueError(f"status desconhecido: {status!r}")
    return ensaio.strip().upper(), STATUS_VALIDOS[status]


def ler_liberacoes(observacao: str) -> dict[str, bool]:
    """Converte 'COF: liberado; Selagem: reprovado' em {'COF': True, 'SELAGEM': False}."""
    return dict(_ler_item(item) for item in observacao.split(";"))
