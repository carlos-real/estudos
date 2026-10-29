"""Exemplo 07 — A API do laboratório organizada em módulos (pasta api_laboratorio/).

Este script usa um banco TEMPORÁRIO (variável de ambiente API_LAB_BANCO), faz
algumas requisições e mostra as respostas. Para subir o servidor de verdade,
de dentro da pasta exemplos:
    uvicorn api_laboratorio.main:app --reload
e abra http://127.0.0.1:8000/docs

Rode com:  python exemplos/07_api_organizada.py
"""

import os
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient


def demonstrar() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["API_LAB_BANCO"] = str(Path(tmp) / "lab.db")
        from api_laboratorio.main import app  # importado depois de configurar o banco

        cliente = TestClient(app)
        print("GET /linhas/B/tolerancias")
        for tol in cliente.get("/linhas/B/tolerancias").json():
            print(f"   {tol['ensaio']:<10} {tol['tipo']:<8} {tol['minimo']} a {tol['maximo']}")

        print("POST /medicoes")
        for corpo in [
            {"op": "123789", "linha": "B", "ensaio": "Espessura", "valor": 41.2},
            {"op": "123789", "linha": "B", "ensaio": "gramatura", "valor": 39.9},
            {"op": "123789", "linha": "B", "ensaio": "cof", "valor": 0.25},
        ]:
            resposta = cliente.post("/medicoes", json=corpo)
            dados = resposta.json()
            resumo = dados.get("aprovado", dados.get("detail"))
            print(f"   {corpo['ensaio']:<10} {corpo['valor']:>5} -> {resposta.status_code} {resumo}")

        print("GET /ops/123789/situacao ->", cliente.get("/ops/123789/situacao").json())
        print("GET /ops/999999/situacao ->", cliente.get("/ops/999999/situacao").status_code)

        rotas = cliente.get("/openapi.json").json()["paths"]
        print("Rotas:", ", ".join(rotas))
        del os.environ["API_LAB_BANCO"]


if __name__ == "__main__":
    demonstrar()
