"""
Exercício 13.03 — Linhas de produção e o erro 404 (SOLUÇÃO)
"""

from fastapi import FastAPI, HTTPException

LINHAS = {
    "A": {"nome": "Extrusora A", "produto": "Filme PP 20 µm"},
    "B": {"nome": "Extrusora B", "produto": "Filme PE 40 µm"},
    "C": {"nome": "Laminadora C", "produto": "Laminado PET/PE"},
    "D": {"nome": "Extrusora D", "produto": "Filme PE 60 µm"},
}

app = FastAPI()


@app.get("/linhas")
def listar_linhas() -> list[str]:
    return sorted(LINHAS)  # sorted de um dict ordena as CHAVES


@app.get("/linhas/{codigo}")
def ver_linha(codigo: str) -> dict:
    codigo = codigo.upper()  # normaliza antes de procurar
    if codigo not in LINHAS:
        # raise interrompe a função e o FastAPI monta a resposta de erro:
        # status 404 e corpo {"detail": "..."}.
        raise HTTPException(status_code=404, detail=f"Linha {codigo} não encontrada")
    # ** "desempacota" o dicionário da linha dentro do novo (módulo 03/04).
    return {"codigo": codigo, **LINHAS[codigo]}
