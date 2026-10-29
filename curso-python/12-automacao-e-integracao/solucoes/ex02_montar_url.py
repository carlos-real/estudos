"""
Exercício 12.02 — Montar a URL de uma consulta (SOLUÇÃO)
"""

from urllib.parse import urlencode


def montar_url(base: str, caminho: str, params: dict | None = None) -> str:
    """Junta base + caminho e acrescenta a query string (sem valores None)."""
    # Normalizar as pontas resolve os 4 casos de uma vez:
    # "api/" + "/x", "api" + "x", "api/" + "x" e "api" + "/x".
    url = base.rstrip("/") + "/" + caminho.lstrip("/")

    # `params or {}` trata o caso params=None sem precisar de um if separado.
    # A compreensão de dicionário (módulo 03) filtra os valores None.
    filtrados = {chave: valor for chave, valor in (params or {}).items() if valor is not None}
    if not filtrados:
        return url

    # urlencode faz a parte chata: espaço -> "+", "ç" -> "%C3%A7", "&" dentro
    # de um valor -> "%26". Montar com f-string quebraria nesses casos.
    return f"{url}?{urlencode(filtrados)}"

    # No dia a dia com requests você nem precisa disso:
    #     requests.get(url, params=filtrados)
    # monta a query string sozinho (e também ignora valores None).
