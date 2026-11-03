# Quiz — Módulo 13: APIs com FastAPI

Responda sem consultar a aula. Depois confira no gabarito, no fim da página.

---

**1.** Numa API REST, qual combinação de método e caminho é a mais adequada para
**registrar** uma medição nova?

a) `GET /medicoes/nova`  b) `POST /medicoes`  c) `PUT /medicao`  d) `DELETE /medicoes`

---

**2.** O que estas duas requisições devolvem?

```python
@app.get("/itens/{n}")
def item(n: int):
    return {"n": n}

@app.get("/busca")
def busca(q: str, limite: int = 5):
    return {"q": q, "limite": limite}

cliente = TestClient(app)
print(cliente.get("/itens/07").json(), cliente.get("/busca?q=cof").json())
print(cliente.get("/busca").status_code)
```

---

**3.** Como o FastAPI decide se um parâmetro da função vem do **caminho**, da
**consulta** (query string) ou do **corpo**?

---

**4.** Qual a diferença entre um 404 e um 422 numa API FastAPI? Dê um exemplo de cada no
contexto do laboratório.

---

**5.** O que este código imprime?

```python
from pydantic import BaseModel, Field

class M(BaseModel):
    valor: float = Field(gt=0)
    nome: str = "x"

print(M(valor="3").model_dump())
```

---

**6.** Uma rota levanta `KeyError` sem tratamento. Qual status o cliente recebe, e como
transformar isso numa resposta útil?

a) 404, automático  b) 422  c) 500; levantar `HTTPException(404, ...)` quando a chave
não existir  d) 200 com `null`

---

**7.** O que este código imprime?

```python
@app.get("/linha/{codigo}")
def ver(codigo: str):
    return {"codigo": codigo}

@app.get("/linha/especial")
def especial():
    return {"especial": True}

print(TestClient(app).get("/linha/especial").json())
```

---

**8.** Qual a diferença entre 401 e 403?

---

**9.** Para que serve `app.dependency_overrides` nos testes?

---

**10.** Por que usamos `sqlite3.connect(..., check_same_thread=False)` numa dependência do
FastAPI, e por que cada requisição deve abrir e fechar a sua conexão?

---

**11.** Onde está o problema?

```python
@app.get("/medicoes")
def listar(con: Conexao, op: str):
    return con.execute(f"SELECT * FROM medicoes WHERE op = '{op}'").fetchall()
```

---

**12.** Qual comando sobe a API do arquivo `main.py` (com `app = FastAPI()` dentro) e
recarrega sozinho quando você salva o arquivo? Em que endereço fica a documentação?

---

**13.** A rota é `@app.delete("/amostras/{id}", status_code=204)`. O que a função deve
devolver, e o que o cliente recebe no corpo?

---

## Gabarito

<details><summary>Ver respostas</summary>

**1.** b) `POST /medicoes`. Em REST o caminho nomeia o recurso (substantivo, no plural)
e o método diz a ação. `GET` não deve criar nada.

**2.** `{'n': 7} {'q': 'cof', 'limite': 5}` e depois `422`. O `"07"` vira o inteiro 7;
`limite` usa o padrão 5; sem `q` (obrigatório, sem valor padrão) a validação falha.

**3.** Pelo nome e pelo tipo: se o nome aparece entre chaves no caminho, é de caminho; se
o tipo é um modelo Pydantic (`BaseModel`), é o corpo; os demais (tipos simples) são de
consulta. `Query()`, `Path()`, `Header()` e `Body()` deixam isso explícito.

**4.** 404: o recurso não existe (`GET /linhas/Z`, OP sem medições). 422: o pedido chegou
com dados inválidos (`valor` negativo, OP com 5 dígitos, `limite=abc`). O 422 o FastAPI
gera sozinho a partir dos tipos; o 404 de "não achei" é você quem levanta.

**5.** `{'valor': 3.0, 'nome': 'x'}`. No modo padrão, o Pydantic converte o texto `"3"`
em `3.0` e preenche o valor padrão de `nome`.

**6.** c). Exceção não tratada vira `500 Internal Server Error`, que não explica nada ao
cliente. Procure com `.get()` (ou `in`) e levante `HTTPException(404, detail=...)`.

**7.** `{'codigo': 'especial'}`. As rotas são testadas **na ordem em que foram
declaradas**, e `/linha/{codigo}` aceita qualquer texto. Declare as rotas fixas antes
das rotas com parâmetro.

**8.** 401: "não sei quem você é" (chave ausente ou inválida). 403: "sei quem você é,
mas você não tem permissão" (chave de leitura tentando alterar uma regra).

**9.** Para trocar uma dependência por outra durante o teste, sem mexer nas rotas: por
exemplo, a conexão com o banco de verdade por um banco em memória, ou as regras reais
por regras de teste. Lembre de limpar (`app.dependency_overrides.clear()`) no fim.

**10.** O FastAPI pode preparar a dependência numa thread e executar a rota em outra; sem
`check_same_thread=False`, o `sqlite3` recusa. Abrir e fechar por requisição (dependência
com `yield` e `finally`) evita compartilhar uma conexão entre requisições simultâneas e
garante que ela é fechada mesmo quando a rota dá erro.

**11.** SQL montado com f-string: **SQL injection**. Um `op` como `' OR '1'='1` devolve
a tabela inteira (ou pior). Use parâmetros:
`con.execute("SELECT * FROM medicoes WHERE op = ?", (op,))`.

**12.** `uvicorn main:app --reload`, rodado na pasta do `main.py`. A documentação
interativa fica em `http://127.0.0.1:8000/docs` (e a alternativa em `/redoc`).

**13.** A função devolve `None` (ou nada), e o cliente recebe o status 204 **sem corpo**.
204 significa "deu certo e não há conteúdo para mostrar".

</details>
