"""
Exercício 13.10 — Leitura de código: preveja as respostas da API do colega
Nível: ★★☆

Contexto: um colega escreveu a API abaixo (ela está pronta, logo depois deste
enunciado) e pediu sua revisão. Antes de rodar qualquer coisa, LEIA o código
e preveja o que cada requisição devolve. É assim que se pega defeito em
revisão de código: pensando, não chutando.

Tarefa:
1. Sem rodar, preencha prever_status() com o código de status que você
   espera para cada requisição (as chaves do dicionário já estão escritas).
2. Preencha prever_json_tolerancias_a() com o JSON (como dict do Python) que
   GET /tolerancias/A devolve. Atenção aos tipos!
3. Só então confira: num arquivo de rascunho, faça
       from fastapi.testclient import TestClient
       cliente = TestClient(app, raise_server_exceptions=False)
   e envie as requisições. Errou alguma? Descubra por quê antes de corrigir.
   (raise_server_exceptions=False faz o TestClient devolver 500 em vez de
   estourar a exceção do servidor no seu terminal.)
4. Não altere a API do colega: os testes conferem as suas previsões contra
   ela.

Exemplos:
    >>> prever_status()["1: GET /tolerancias/A"]
    200

Dica: pense em cada etapa: existe rota para esse caminho? E para esse método?
Os dados passam na validação do Pydantic (lembre que ele converte tipos)? O
código da função pode levantar alguma exceção que ninguém trata?

Teste com:  python curso.py testar 13 ex10
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ----------------------------------------------------------------------------
# A API do colega (NÃO altere)
# ----------------------------------------------------------------------------
TOLERANCIAS = {
    "A": {"espessura": (18.0, 22.0), "cof": (0.2, 0.3)},
    "B": {"espessura": (38.0, 42.0)},
}

app = FastAPI()


class Medicao(BaseModel):
    ensaio: str
    valor: float = Field(gt=0)


@app.get("/tolerancias/{linha}")
def ver_tolerancias(linha: str):
    if linha not in TOLERANCIAS:
        raise HTTPException(status_code=404, detail="Linha não encontrada")
    return TOLERANCIAS[linha]


@app.post("/tolerancias/{linha}/validar")
def validar(linha: str, medicao: Medicao):
    minimo, maximo = TOLERANCIAS[linha][medicao.ensaio]
    return {"aprovado": minimo <= medicao.valor <= maximo}


@app.get("/bobinas")
def listar_bobinas(limite: int = 10):
    return [{"numero": n} for n in range(1, limite + 1)]


# ----------------------------------------------------------------------------
# Suas previsões
# ----------------------------------------------------------------------------
def prever_status() -> dict[str, int]:
    """Código de status previsto para cada requisição."""
    # Escreva seu código aqui: devolva o dicionário com os números preenchidos.
    #   "1: GET /tolerancias/A": ...,
    #   "2: GET /tolerancias/a": ...,
    #   "3: GET /tolerancias": ...,
    #   "4: DELETE /tolerancias/A": ...,
    #   "5: POST /tolerancias/A/validar com {'ensaio': 'cof', 'valor': 0}": ...,
    #   "6: POST /tolerancias/A/validar com {'ensaio': 'espessura', 'valor': '20'}": ...,
    #   "7: POST /tolerancias/B/validar com {'ensaio': 'cof', 'valor': 0.25}": ...,
    #   "8: GET /bobinas?limite=abc": ...,
    #   "9: GET /bobinas?limite=-1": ...,
    raise NotImplementedError("Implemente esta função")


def prever_json_tolerancias_a() -> dict:
    """O JSON (como dict) devolvido por GET /tolerancias/A."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
