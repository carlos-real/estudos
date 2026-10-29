"""Exemplo 08 — Um servidor uvicorn de verdade e um cliente requests (módulo 12).

Sobe a API do laboratório (exemplo 07) numa porta livre, numa thread separada,
e conversa com ela por HTTP de verdade usando requests. É o que um robô ou outro
sistema faria do outro lado da rede.

Rode com:  python exemplos/08_cliente_requests.py
"""

import os
import socket
import tempfile
import threading
import time
from pathlib import Path

import requests
import uvicorn


def porta_livre() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["API_LAB_BANCO"] = str(Path(tmp) / "lab.db")
        from api_laboratorio.main import app

        porta = porta_livre()
        servidor = uvicorn.Server(
            uvicorn.Config(app, host="127.0.0.1", port=porta, log_level="warning")
        )
        thread = threading.Thread(target=servidor.run, daemon=True)
        thread.start()
        while not servidor.started:  # espera o servidor ficar pronto
            time.sleep(0.05)

        base = f"http://127.0.0.1:{porta}"
        with requests.Session() as sessao:
            resposta = sessao.get(f"{base}/saude", timeout=5)
            print("saúde:", resposta.status_code, resposta.json())

            medicao = {"op": "124001", "linha": "C", "ensaio": "tracao", "valor": 22.5}
            resposta = sessao.post(f"{base}/medicoes", json=medicao, timeout=5)
            resposta.raise_for_status()
            print("medição:", resposta.status_code, "aprovado =", resposta.json()["aprovado"])

            resposta = sessao.get(f"{base}/ops/124001/situacao", timeout=5)
            print("situação:", resposta.json())

            resposta = sessao.post(f"{base}/medicoes", json={"op": "1"}, timeout=5)
            try:
                resposta.raise_for_status()
            except requests.HTTPError:
                campos = [erro["loc"][-1] for erro in resposta.json()["detail"]]
                print("pedido inválido:", resposta.status_code, "campos com problema:", campos)

        servidor.should_exit = True  # pede para o uvicorn parar
        thread.join()
        del os.environ["API_LAB_BANCO"]


if __name__ == "__main__":
    main()
