"""Solução de referência do desafio: a API do Validador (FastAPI).

A API é só mais uma porta de entrada para o MESMO núcleo do projeto-completo:
não reescreve regra nenhuma, só traduz HTTP <-> objetos do domínio.

Rode (na pasta curso-python):
    python 14-projeto-final/desafio/solucao_referencia.py            # demonstração
    python 14-projeto-final/desafio/solucao_referencia.py --servir   # abre em :8000

Com --servir, abra http://127.0.0.1:8000/docs no navegador.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

MODULO = Path(__file__).resolve().parent.parent
# No seu projeto: pip install -e . e pronto. Aqui, para rodar sem instalar:
sys.path.insert(0, str(MODULO / "projeto-completo" / "src"))

from validador_certificados.banco import carregar_do_arquivo  # noqa: E402
from validador_certificados.modelos import EspecificacaoDesconhecida, Medicao  # noqa: E402
from validador_certificados.regras import (  # noqa: E402
    escolher_especificacao,
    validar_medicao,
)
from validador_certificados.texto import esta_liberado  # noqa: E402

BANCO_PADRAO = MODULO / "dados" / "regras.db"


# ------------------------------------------------------------------ esquemas (Pydantic)
class ToleranciaSaida(BaseModel):
    caracteristica: str
    tipo: str
    minimo: float | None = None
    maximo: float | None = None
    percentual: float | None = None


class EspecificacaoSaida(BaseModel):
    titulo: str
    texto: str
    linha: str
    tolerancias: list[ToleranciaSaida] = []


class PedidoValidacao(BaseModel):
    op: str = Field(min_length=4, max_length=6, pattern=r"^\d+$", examples=["24518"])
    linha: str = Field(pattern=r"^[A-D]$", examples=["A"])
    especificacao: str = Field(default="", examples=[""])
    valores: dict[str, float] = Field(
        examples=[{"espessura": 41.2, "gramatura": 37.9, "cof": 0.22, "tracao": 24.5,
                   "selagem": 9.8}]
    )  # fmt: skip
    nominais: dict[str, float] = Field(
        default_factory=dict, examples=[{"espessura": 40, "gramatura": 37}]
    )
    observacao: str = Field(default="", examples=["COF: liberado"])


class ResultadoSaida(BaseModel):
    op: str
    especificacao: str
    aprovado: bool
    liberado: bool
    pode_emitir: bool
    motivos: list[str]


# ------------------------------------------------------------------ aplicação
def criar_app(caminho_regras: Path = BANCO_PADRAO) -> FastAPI:
    """Cria a API com as regras carregadas UMA vez (o banco é só leitura)."""
    especificacoes = carregar_do_arquivo(caminho_regras)
    app = FastAPI(
        title="Validador de Certificados",
        version="0.1.0",
        description="Consulta especificações e valida uma OP contra as regras.",
    )

    def para_saida(especificacao) -> EspecificacaoSaida:
        return EspecificacaoSaida(
            titulo=especificacao.titulo,
            texto=especificacao.texto,
            linha=especificacao.linha,
            tolerancias=[
                ToleranciaSaida(**vars(t)) for t in especificacao.tolerancias.values()
            ],
        )

    @app.get("/saude")
    def saude() -> dict[str, object]:
        return {"status": "ok", "especificacoes": len(especificacoes)}

    @app.get("/especificacoes")
    def listar(linha: str | None = None) -> list[EspecificacaoSaida]:
        """Todas as especificações; ?linha=A filtra o padrão daquela linha."""
        escolhidas = [
            e for e in especificacoes.values() if linha is None or e.linha == linha.upper()
        ]
        return [para_saida(e) for e in escolhidas]

    @app.get("/especificacoes/{titulo}")
    def detalhar(titulo: str) -> EspecificacaoSaida:
        por_chave = {t.upper(): e for t, e in especificacoes.items()}
        especificacao = por_chave.get(titulo.strip().upper())
        if especificacao is None:
            raise HTTPException(404, detail=f"especificação {titulo!r} não cadastrada")
        return para_saida(especificacao)

    @app.post("/validar")
    def validar(pedido: PedidoValidacao) -> ResultadoSaida:
        """Valida uma OP: tolerâncias + observação de liberação."""
        try:
            especificacao = escolher_especificacao(
                pedido.especificacao, pedido.linha, especificacoes
            )
        except EspecificacaoDesconhecida as erro:
            raise HTTPException(422, detail=str(erro)) from erro
        medicao = Medicao(
            op=pedido.op,
            aba=f"Linha {pedido.linha}",
            linha=pedido.linha,
            valores=pedido.valores,
            nominais=pedido.nominais,
            especificacao=pedido.especificacao,
            observacao=pedido.observacao,
        )
        resultado = validar_medicao(medicao, especificacao)
        liberado = esta_liberado(pedido.observacao)
        return ResultadoSaida(
            op=pedido.op,
            especificacao=especificacao.titulo,
            aprovado=resultado.aprovado,
            liberado=liberado,
            pode_emitir=resultado.aprovado and liberado,
            motivos=resultado.motivos,
        )

    return app


# ------------------------------------------------------------------ demonstração
def demonstrar() -> None:
    """Faz algumas requisições com o TestClient (sem abrir servidor)."""
    cliente = TestClient(criar_app())
    base = {
        "op": "24518",
        "linha": "A",
        "valores": {"espessura": 41.2, "gramatura": 37.9, "cof": 0.22, "tracao": 24.5,
                    "selagem": 9.8},
        "nominais": {"espessura": 40, "gramatura": 37},
        "observacao": "COF: liberado",
    }  # fmt: skip
    chamadas = [
        ("GET", "/saude", None),
        ("GET", "/especificacoes/esp-0412", None),
        ("GET", "/especificacoes/ESP-9999", None),
        ("POST", "/validar", base),
        ("POST", "/validar", {**base, "op": "24519",
                              "valores": {**base["valores"], "espessura": 44.8}}),
        ("POST", "/validar", {**base, "especificacao": "ESP-9999"}),
        ("POST", "/validar", {**base, "linha": "E"}),
    ]  # fmt: skip
    for metodo, rota, corpo in chamadas:
        resposta = cliente.request(metodo, rota, json=corpo)
        dados = resposta.json()
        if rota.startswith("/especificacoes/") and resposta.status_code == 200:
            dados = {"titulo": dados["titulo"], "tolerancias": len(dados["tolerancias"])}
        if resposta.status_code == 422 and isinstance(dados.get("detail"), list):
            dados = {"erro_de_validacao_no_campo": dados["detail"][0]["loc"][-1]}
        print(f"{metodo:4} {rota:28} -> {resposta.status_code} {dados}")


def main() -> None:
    parser = argparse.ArgumentParser(description="API do Validador de Certificados")
    parser.add_argument("--servir", action="store_true", help="sobe o servidor uvicorn")
    parser.add_argument("--porta", type=int, default=8000)
    args = parser.parse_args()
    if args.servir:
        import uvicorn

        uvicorn.run(criar_app(), host="127.0.0.1", port=args.porta)
    else:
        demonstrar()


if __name__ == "__main__":
    main()
