"""Desafio 13 — API de Certificados do laboratório (solução de referência).

Uso (na pasta curso-python):
    python 13-apis-com-fastapi/desafio/solucao_referencia.py            # demonstração
    python 13-apis-com-fastapi/desafio/solucao_referencia.py --servir   # servidor + /docs

A demonstração usa um banco temporário. O servidor usa desafio/saida/certificados.db
(ou o caminho da variável de ambiente CERTIFICADOS_BANCO).
"""

from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Annotated, Literal

import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field, field_validator, model_validator

BANCO_PADRAO = Path(__file__).resolve().parent / "saida" / "certificados.db"
CHAVES = {"lab-123": "escrita", "bi-789": "leitura"}  # na vida real: variável de ambiente

Linha = Literal["A", "B", "C", "D"]

ESQUEMA = """
CREATE TABLE IF NOT EXISTS regras (
    linha TEXT NOT NULL, ensaio TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('faixa', 'nominal')),
    minimo REAL, maximo REAL, nominal REAL, percentual REAL,
    PRIMARY KEY (linha, ensaio)
);
CREATE TABLE IF NOT EXISTS medicoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    op TEXT NOT NULL, linha TEXT NOT NULL, ensaio TEXT NOT NULL,
    valor REAL NOT NULL, aprovado INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS certificados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    op TEXT NOT NULL, nf TEXT NOT NULL, peso_kg REAL NOT NULL,
    emitido_em TEXT NOT NULL,
    UNIQUE (op, nf)
);
"""

REGRAS_INICIAIS = [
    ("A", "espessura", "nominal", None, None, 20.0, 10.0),
    ("A", "cof", "faixa", 0.20, 0.30, None, None),
    ("B", "espessura", "nominal", None, None, 40.0, 5.0),
    ("B", "gramatura", "nominal", None, None, 38.0, 4.0),
    ("C", "tracao", "faixa", 25.0, 40.0, None, None),
    ("D", "selagem", "faixa", 1.5, 3.0, None, None),
]


# ----------------------------------------------------------------------------
# Banco
# ----------------------------------------------------------------------------
def caminho_banco() -> Path:
    return Path(os.environ.get("CERTIFICADOS_BANCO", BANCO_PADRAO))


def obter_conexao():
    caminho = caminho_banco()
    caminho.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(caminho, check_same_thread=False)
    con.row_factory = sqlite3.Row
    try:
        con.executescript(ESQUEMA)
        if con.execute("SELECT COUNT(*) FROM regras").fetchone()[0] == 0:
            with con:
                con.executemany(
                    "INSERT INTO regras VALUES (?, ?, ?, ?, ?, ?, ?)", REGRAS_INICIAIS
                )
        yield con
    finally:
        con.close()


Conexao = Annotated[sqlite3.Connection, Depends(obter_conexao)]


def perfil_atual(x_chave: Annotated[str | None, Header()] = None) -> str:
    if x_chave not in CHAVES:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Chave inválida ou ausente")
    return CHAVES[x_chave]


def exigir_escrita(perfil: Annotated[str, Depends(perfil_atual)]) -> None:
    if perfil != "escrita":
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Sem permissão de escrita")


# ----------------------------------------------------------------------------
# Regras de negócio (funções puras)
# ----------------------------------------------------------------------------
def limites(tipo, minimo, maximo, nominal, percentual) -> tuple[float, float]:
    if tipo == "faixa":
        return minimo, maximo
    folga = nominal * percentual / 100
    return round(nominal - folga, 4), round(nominal + folga, 4)


# ----------------------------------------------------------------------------
# Modelos
# ----------------------------------------------------------------------------
class Regra(BaseModel):
    tipo: Literal["faixa", "nominal"]
    minimo: float | None = None
    maximo: float | None = None
    nominal: float | None = None
    percentual: float | None = None

    @model_validator(mode="after")
    def conferir(self) -> Regra:
        if self.tipo == "faixa":
            if self.minimo is None or self.maximo is None or self.minimo > self.maximo:
                raise ValueError("faixa exige minimo <= maximo")
        elif not (
            self.nominal and self.nominal > 0 and self.percentual and self.percentual > 0
        ):
            raise ValueError("nominal exige nominal > 0 e percentual > 0")
        return self


class RegraCalculada(BaseModel):
    linha: Linha
    ensaio: str
    tipo: str
    minimo: float
    maximo: float


class MedicaoEntrada(BaseModel):
    op: str = Field(pattern=r"^\d{6}$")
    linha: Linha
    ensaio: str = Field(min_length=2)
    valor: float = Field(gt=0)

    @field_validator("ensaio")
    @classmethod
    def minusculo(cls, valor: str) -> str:
        return valor.strip().lower()


class MedicaoAvaliada(MedicaoEntrada):
    id: int
    minimo: float
    maximo: float
    aprovado: bool


class Situacao(BaseModel):
    op: str
    medicoes: int
    reprovadas: int
    liberada: bool


class PedidoCertificado(BaseModel):
    op: str = Field(pattern=r"^\d{6}$")
    nf: str = Field(pattern=r"^\d+$")
    peso_kg: float = Field(gt=0)


class Certificado(PedidoCertificado):
    id: int
    emitido_em: str


# ----------------------------------------------------------------------------
# Rotas
# ----------------------------------------------------------------------------
app = FastAPI(
    title="API de Certificados",
    version="1.0.0",
    description="Regras de tolerância, medições e emissão de certificados de qualidade.",
)


@app.get("/saude", tags=["infra"])
def saude() -> dict:
    return {"status": "ok"}


@app.get("/linhas/{linha}/regras", tags=["regras"], summary="Regras de uma linha")
def listar_regras(linha: Linha, con: Conexao) -> list[RegraCalculada]:
    linhas = con.execute("SELECT * FROM regras WHERE linha = ? ORDER BY ensaio", (linha,))
    resultado = []
    for r in linhas:
        minimo, maximo = limites(
            r["tipo"], r["minimo"], r["maximo"], r["nominal"], r["percentual"]
        )
        resultado.append(
            RegraCalculada(
                linha=linha, ensaio=r["ensaio"], tipo=r["tipo"], minimo=minimo, maximo=maximo
            )
        )
    return resultado


@app.put(
    "/linhas/{linha}/regras/{ensaio}",
    tags=["regras"],
    summary="Cria ou troca uma regra",
    dependencies=[Depends(exigir_escrita)],
)
def gravar_regra(linha: Linha, ensaio: str, regra: Regra, con: Conexao) -> RegraCalculada:
    ensaio = ensaio.lower()
    with con:
        con.execute(
            "INSERT OR REPLACE INTO regras VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                linha,
                ensaio,
                regra.tipo,
                regra.minimo,
                regra.maximo,
                regra.nominal,
                regra.percentual,
            ),
        )
    minimo, maximo = limites(
        regra.tipo, regra.minimo, regra.maximo, regra.nominal, regra.percentual
    )
    return RegraCalculada(
        linha=linha, ensaio=ensaio, tipo=regra.tipo, minimo=minimo, maximo=maximo
    )


@app.post("/medicoes", status_code=status.HTTP_201_CREATED, tags=["medições"])
def registrar_medicao(entrada: MedicaoEntrada, con: Conexao) -> MedicaoAvaliada:
    r = con.execute(
        "SELECT * FROM regras WHERE linha = ? AND ensaio = ?", (entrada.linha, entrada.ensaio)
    ).fetchone()
    if r is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Sem regra para linha {entrada.linha} / ensaio {entrada.ensaio}",
        )
    minimo, maximo = limites(
        r["tipo"], r["minimo"], r["maximo"], r["nominal"], r["percentual"]
    )
    aprovado = minimo <= entrada.valor <= maximo
    with con:
        cursor = con.execute(
            "INSERT INTO medicoes (op, linha, ensaio, valor, aprovado) VALUES (?, ?, ?, ?, ?)",
            (entrada.op, entrada.linha, entrada.ensaio, entrada.valor, aprovado),
        )
    return MedicaoAvaliada(
        id=cursor.lastrowid,
        **entrada.model_dump(),
        minimo=minimo,
        maximo=maximo,
        aprovado=aprovado,
    )


def situacao(con: sqlite3.Connection, op: str) -> Situacao:
    total, reprovadas = con.execute(
        "SELECT COUNT(*), COALESCE(SUM(aprovado = 0), 0) FROM medicoes WHERE op = ?", (op,)
    ).fetchone()
    return Situacao(
        op=op, medicoes=total, reprovadas=reprovadas, liberada=total > 0 and not reprovadas
    )


@app.get("/ops/{op}/situacao", tags=["medições"])
def ver_situacao(op: str, con: Conexao) -> Situacao:
    resultado = situacao(con, op)
    if resultado.medicoes == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"OP {op} sem medições")
    return resultado


@app.post("/certificados", status_code=status.HTTP_201_CREATED, tags=["certificados"])
def emitir_certificado(pedido: PedidoCertificado, con: Conexao) -> Certificado:
    existente = con.execute(
        "SELECT * FROM certificados WHERE op = ? AND nf = ?", (pedido.op, pedido.nf)
    ).fetchone()
    if existente is not None:
        # Idempotência: pedir de novo devolve o MESMO certificado (com 409 para
        # o cliente saber que nada novo foi criado).
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"mensagem": "Certificado já emitido", "certificado": dict(existente)},
        )
    sit = situacao(con, pedido.op)
    if sit.medicoes == 0:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=f"OP {pedido.op} sem medições")
    if not sit.liberada:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"OP {pedido.op} com {sit.reprovadas} medição(ões) reprovada(s)",
        )
    emitido_em = datetime.now().isoformat(timespec="seconds")
    with con:
        cursor = con.execute(
            "INSERT INTO certificados (op, nf, peso_kg, emitido_em) VALUES (?, ?, ?, ?)",
            (pedido.op, pedido.nf, pedido.peso_kg, emitido_em),
        )
    return Certificado(id=cursor.lastrowid, emitido_em=emitido_em, **pedido.model_dump())


@app.get("/certificados", tags=["certificados"])
def listar_certificados(con: Conexao, op: str | None = None) -> list[Certificado]:
    if op is None:
        linhas = con.execute("SELECT * FROM certificados ORDER BY id")
    else:
        linhas = con.execute("SELECT * FROM certificados WHERE op = ? ORDER BY id", (op,))
    return [Certificado(**dict(linha)) for linha in linhas]


# ----------------------------------------------------------------------------
# Demonstração
# ----------------------------------------------------------------------------
def demonstrar() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["CERTIFICADOS_BANCO"] = str(Path(tmp) / "demo.db")
        cliente = TestClient(app)

        def mostrar(rotulo, resposta):
            corpo = resposta.json()
            if isinstance(corpo, dict) and "emitido_em" in corpo:
                corpo = {k: v for k, v in corpo.items() if k != "emitido_em"}  # hora varia
            print(f"{rotulo:<34} {resposta.status_code} {corpo}")

        print("Regras da linha B:")
        for r in cliente.get("/linhas/B/regras").json():
            print(f"   {r['ensaio']:<10} {r['minimo']} a {r['maximo']}")

        for op, ensaio, valor in [
            ("123789", "espessura", 41.2),
            ("123789", "gramatura", 38.1),
            ("123456", "espessura", 43.0),
        ]:
            corpo = {"op": op, "linha": "B", "ensaio": ensaio, "valor": valor}
            resposta = cliente.post("/medicoes", json=corpo)
            aprovado = resposta.json()["aprovado"]
            print(f"medição {op} {ensaio:<10} {valor:>5} -> aprovado={aprovado}")

        pedido = {"op": "123789", "nf": "98766", "peso_kg": 980.25}
        mostrar("POST /certificados (OP liberada)", cliente.post("/certificados", json=pedido))
        segundo = cliente.post("/certificados", json=pedido)
        print(
            f"{'POST /certificados (de novo)':<34} {segundo.status_code}",
            segundo.json()["detail"]["mensagem"],
        )
        ruim = {"op": "123456", "nf": "98765", "peso_kg": 1250.5}
        mostrar("POST /certificados (reprovada)", cliente.post("/certificados", json=ruim))
        nova = {"tipo": "faixa", "minimo": 0.2, "maximo": 0.3}
        mostrar(
            "PUT regra com chave de leitura",
            cliente.put("/linhas/B/regras/cof", json=nova, headers={"X-Chave": "bi-789"}),
        )
        mostrar(
            "PUT regra com chave de escrita",
            cliente.put("/linhas/B/regras/cof", json=nova, headers={"X-Chave": "lab-123"}),
        )
        print("Certificados emitidos:", len(cliente.get("/certificados").json()))
        del os.environ["CERTIFICADOS_BANCO"]


if __name__ == "__main__":
    if "--servir" in sys.argv:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        demonstrar()
