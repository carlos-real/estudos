"""Utilidades de texto: normalização, observação de liberação e números BR."""

from __future__ import annotations

import re
import unicodedata

# "cof", talvez ":" ou traço, e "liberado(a)" logo depois. "cof: nao liberado" não casa,
# porque depois de "cof:" vem "nao", e não "liberado".
PADRAO_LIBERACAO = re.compile(r"\bcof\s*[:\-–—]?\s*liberad[oa]\b")


def normalizar(texto: str | None) -> str:
    """Minúsculas, sem acento e com espaços simples: " COF:  Não " -> "cof: nao"."""
    if texto is None:
        return ""
    decomposto = unicodedata.normalize("NFKD", str(texto))
    sem_acento = "".join(c for c in decomposto if not unicodedata.combining(c))
    return " ".join(sem_acento.lower().split())


def esta_liberado(observacao: str | None) -> bool:
    """True se a observação tem a marca "COF: liberado" (em qualquer variação)."""
    return PADRAO_LIBERACAO.search(normalizar(observacao)) is not None


def numero_br(texto: str) -> float:
    """Converte número no formato brasileiro: "1.250,5" -> 1250.5; "2.040" -> 2040.0."""
    return float(texto.strip().replace(".", "").replace(",", "."))
