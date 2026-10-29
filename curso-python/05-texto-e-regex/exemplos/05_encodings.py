"""Exemplo 05 — Encodings: UTF-8, cp1252 e o BOM (seção 8).

Lê os e-mails salvos em dados/emails/ (cada um num encoding diferente) e mostra
o que acontece quando o encoding errado é usado.

Rode na pasta curso-python:
    python 05-texto-e-regex/exemplos/05_encodings.py
"""

from pathlib import Path

# Path(__file__).resolve().parent é a pasta onde ESTE arquivo está. Assim o
# exemplo acha os dados de qualquer pasta de onde você o rodar (módulo 06).
PASTA_EMAILS = Path(__file__).resolve().parent.parent / "dados" / "emails"

texto = "Expedição"
print("UTF-8 :", texto.encode("utf-8"))
print("cp1252:", texto.encode("cp1252"))
print("UTF-8 lido como cp1252 ->", texto.encode("utf-8").decode("cp1252"))
print("cp1252 lido como UTF-8 ->", texto.encode("cp1252").decode("utf-8", errors="replace"))
print("Consertando o estrago ->", "ExpediÃ§Ã£o".encode("cp1252").decode("utf-8"))


def decodificar(dados):
    """Tenta UTF-8 (sem BOM); se aparecer o losango, era cp1252."""
    texto = dados.decode("utf-8-sig", errors="replace")
    if "�" in texto:
        texto = dados.decode("cp1252")
    return texto


print()
for arquivo in sorted(PASTA_EMAILS.glob("*.txt")):
    dados = arquivo.read_bytes()  # os bytes crus, do jeito que estão no disco
    primeira_linha_utf8 = dados.decode("utf-8", errors="replace").splitlines()[0]
    primeira_linha_certa = decodificar(dados).splitlines()[0]
    tem_bom = dados.startswith(b"\xef\xbb\xbf")
    print(f"{arquivo.name}  (BOM: {'sim' if tem_bom else 'não'})")
    print(f"   lido como UTF-8: {primeira_linha_utf8!r}")
    print(f"   decodificado   : {primeira_linha_certa!r}")
