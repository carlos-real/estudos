"""Conversões de texto no formato brasileiro."""

from datetime import date, datetime


def numero_br(texto: str) -> float:
    """Converte '1.250,5' em 1250.5."""
    return float(texto.strip().replace(".", "").replace(",", "."))


def data_br(texto: str) -> date:
    """Converte '29/10/2026' em date(2026, 10, 29)."""
    return datetime.strptime(texto.strip(), "%d/%m/%Y").date()
