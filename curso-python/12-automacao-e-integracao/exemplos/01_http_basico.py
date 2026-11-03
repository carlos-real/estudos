"""Exemplo 01 — HTTP na prática com requests, sem depender da internet.

O script sobe uma "API de treino" no seu próprio computador (endereço 127.0.0.1),
faz requisições com requests e mostra status, cabeçalhos e JSON.

Rode com:  python exemplos/01_http_basico.py
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import requests

TOLERANCIAS = {
    "A": [
        {"ensaio": "espessura", "minimo": 18.0, "maximo": 22.0},
        {"ensaio": "cof", "minimo": 0.2, "maximo": 0.3},
    ],
    "B": [
        {"ensaio": "espessura", "minimo": 38.0, "maximo": 42.0},
        {"ensaio": "gramatura", "minimo": 36.5, "maximo": 39.5},
    ],
}


class ApiDeTreino(BaseHTTPRequestHandler):
    """Um servidor HTTP mínimo. Você não precisa entender cada linha dele agora."""

    def _responder(self, status: int, dados: dict) -> None:
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self) -> None:  # nome exigido pela biblioteca http.server
        url = urlparse(self.path)
        if url.path != "/tolerancias":
            self._responder(404, {"erro": "Rota não encontrada"})
            return
        linha = parse_qs(url.query).get("linha", [""])[0]
        if linha in TOLERANCIAS:
            self._responder(200, {"linha": linha, "itens": TOLERANCIAS[linha]})
        else:
            self._responder(404, {"erro": f"Linha {linha!r} não encontrada"})

    def do_POST(self) -> None:
        tamanho = int(self.headers["Content-Length"])
        dados = json.loads(self.rfile.read(tamanho))
        self._responder(201, {"id": 1, **dados})

    def log_message(self, *args) -> None:
        pass  # silencia o log que o servidor imprime a cada requisição


def subir_servidor() -> ThreadingHTTPServer:
    """Sobe o servidor numa porta livre (porta 0 = 'escolha uma para mim')."""
    servidor = ThreadingHTTPServer(("127.0.0.1", 0), ApiDeTreino)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor


def main() -> None:
    servidor = subir_servidor()
    base = f"http://127.0.0.1:{servidor.server_port}"

    print("1) GET com parâmetros de consulta")
    resposta = requests.get(f"{base}/tolerancias", params={"linha": "A"}, timeout=5)
    print("   URL montada:", resposta.url.replace(base, "<base>"))
    print("   Status:", resposta.status_code, resposta.reason)
    print("   Content-Type:", resposta.headers["Content-Type"])
    dados = resposta.json()  # texto JSON -> dict do Python
    for item in dados["itens"]:
        print(f"   {item['ensaio']:<10} {item['minimo']:>5} a {item['maximo']}")

    print("2) Um pedido que dá errado (404)")
    resposta = requests.get(f"{base}/tolerancias", params={"linha": "Z"}, timeout=5)
    print("   Status:", resposta.status_code, "| ok?", resposta.ok)
    print("   Corpo:", resposta.json())
    try:
        resposta.raise_for_status()
    except requests.HTTPError as erro:
        print("   raise_for_status levantou", type(erro).__name__, erro.response.status_code)

    print("3) POST enviando JSON")
    medicao = {"op": "123456", "ensaio": "cof", "valor": 0.25}
    resposta = requests.post(f"{base}/medicoes", json=medicao, timeout=5)
    print("   Status:", resposta.status_code, resposta.reason)
    print("   Corpo:", resposta.json())

    servidor.shutdown()


if __name__ == "__main__":
    main()
