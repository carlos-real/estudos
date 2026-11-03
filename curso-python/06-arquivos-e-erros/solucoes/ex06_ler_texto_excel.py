"""
Exercício 06.06 — Ler arquivo vindo do Excel
Nível: ★★☆

Contexto: Os CSVs chegam de computadores diferentes. Uns foram salvos como
"CSV UTF-8" (UTF-8 com BOM), outros como "CSV (separado por vírgulas)" (cp1252),
e alguns vieram de sistemas que gravam UTF-8 sem BOM. O programa precisa ler
todos e dizer como cada um foi lido.

Tarefa: implemente `ler_texto_excel(caminho)`, que devolve uma tupla
(texto, encoding):
- se o arquivo começa com o BOM (os bytes b"\\xef\\xbb\\xbf"), leia como
  "utf-8-sig" e devolva o encoding "utf-8-sig";
- senão, tente ler como "utf-8" e devolva "utf-8";
- se a leitura em UTF-8 der UnicodeDecodeError, leia como "cp1252" e devolva
  "cp1252";
- o texto devolvido nunca contém o BOM;
- se o arquivo não existir, deixe o FileNotFoundError acontecer.

Exemplos:
    >>> Path("a.csv").write_bytes("lote;observação".encode("cp1252"))
    15
    >>> ler_texto_excel(Path("a.csv"))
    ('lote;observação', 'cp1252')

Dica: `caminho.read_bytes()` lê os bytes uma vez só; depois é só usar
`dados.startswith(...)` e `dados.decode(...)` dentro de um try/except.

Teste com:  python curso.py testar 06 ex06
"""

from pathlib import Path

BOM_UTF8 = b"\xef\xbb\xbf"


def ler_texto_excel(caminho: Path) -> tuple[str, str]:
    """Lê o arquivo como UTF-8 (com ou sem BOM) ou cp1252: (texto, encoding)."""
    # Lemos os bytes UMA vez e decodificamos na memória: evita abrir o arquivo
    # duas ou três vezes.
    dados = caminho.read_bytes()
    if dados.startswith(BOM_UTF8):
        return dados.decode("utf-8-sig"), "utf-8-sig"
    try:
        return dados.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        # Bytes cp1252 com acento quase nunca formam UTF-8 válido. Se não é
        # UTF-8, apostamos no padrão antigo do Windows.
        return dados.decode("cp1252"), "cp1252"

    # Versão "clássica", reabrindo o arquivo (também correta):
    #     try:
    #         return caminho.read_text(encoding="utf-8-sig"), ...
    #     except UnicodeDecodeError:
    #         return caminho.read_text(encoding="cp1252"), "cp1252"
