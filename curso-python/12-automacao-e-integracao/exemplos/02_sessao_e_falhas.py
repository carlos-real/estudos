"""Exemplo 02 — Sessão, cabeçalhos, timeout e as falhas de rede mais comuns.

Também sobe um servidor de treino local. Uma das rotas demora 2 segundos de
propósito, para você ver o timeout em ação.

Rode com:  python exemplos/02_sessao_e_falhas.py
"""

import json
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import requests


class ApiDeTreino(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/lento":
            time.sleep(2)  # simula um sistema sobrecarregado
        dados = {
            "rota": self.path,
            "user_agent": self.headers.get("User-Agent"),
            "autorizacao": self.headers.get("Authorization"),
        }
        corpo = json.dumps(dados).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, *args) -> None:
        pass


def porta_sem_ninguem() -> int:
    """Pede ao sistema uma porta livre e a devolve fechada (ninguém escutando)."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main() -> None:
    servidor = ThreadingHTTPServer(("127.0.0.1", 0), ApiDeTreino)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{servidor.server_port}"

    print("1) Sessão: cabeçalhos configurados uma vez, usados em todas as chamadas")
    with requests.Session() as sessao:
        sessao.headers.update(
            {"User-Agent": "robo-laboratorio/1.0", "Authorization": "Bearer abc123"}
        )
        for rota in ["/status", "/linhas"]:
            print("  ", sessao.get(base + rota, timeout=5).json())

        print("2) Timeout: o servidor demora 2 s, mas só aceitamos esperar 0,5 s")
        inicio = time.perf_counter()
        try:
            sessao.get(base + "/lento", timeout=0.5)
        except requests.Timeout as erro:
            gasto = time.perf_counter() - inicio
            print(f"   {type(erro).__name__} depois de {gasto:.1f} s")

    print("3) Ninguém escutando na porta: ConnectionError")
    try:
        requests.get(f"http://127.0.0.1:{porta_sem_ninguem()}/", timeout=2)
    except requests.ConnectionError as erro:
        print("  ", type(erro).__name__)

    print("4) A família de exceções do requests")
    print("   Timeout é RequestException?", issubclass(requests.Timeout, requests.RequestException))
    print("   HTTPError é RequestException?", issubclass(requests.HTTPError, requests.RequestException))

    servidor.shutdown()


if __name__ == "__main__":
    main()
