# Módulo 13 — APIs web com FastAPI

> **Tempo estimado:** 12 a 16 horas · **Pré-requisitos:** módulos 00 a 12 · **Nível:** intermediário

## O que você vai aprender

- Explicar o que é uma API REST: recursos, métodos, códigos de status e JSON.
- Criar uma API com FastAPI, rodar com `uvicorn` e usar a documentação automática `/docs`.
- Testar rotas com `TestClient`, sem subir servidor.
- Receber parâmetros de caminho e de consulta, com tipos e validação (`Query`, `Enum`).
- Receber e validar o corpo de uma requisição com Pydantic v2 (`BaseModel`, `Field`,
  `Literal`, `field_validator`, `model_validator`) e controlar o que sai (modelo de
  resposta).
- Responder com o código de status certo e levantar `HTTPException`.
- Organizar a API em módulos com `APIRouter`.
- Usar dependências (`Depends`) para chave de acesso e para a conexão com o banco, e
  trocá-las nos testes com `dependency_overrides`.
- Guardar os dados em SQLite com uma dependência que abre e fecha a conexão.
- Consumir a sua API com `requests`, como um robô ou outro sistema faria.

## Por que isso importa

No módulo 12 você foi **cliente**: chamou APIs dos outros. Agora você vai ser o
**servidor**: a regra de tolerância do laboratório vira um serviço que qualquer programa
pode consultar. O robô de certificados pergunta "a OP 123456 está liberada?", o Power BI
puxa as medições, a TI integra com o ERP. Todos usando a **mesma** regra, num lugar só.

FastAPI é um dos frameworks web mais usados em Python, especialmente em dados,
automação e aprendizado de máquina. Vagas de backend Python citam FastAPI com
frequência. E ele ensina boas práticas de graça: tipos, validação, documentação e testes.

No projeto final, a API é uma das extensões: o núcleo do Validador de Certificados
(módulos anteriores) ganha uma "porta" HTTP.

## 1. O que é uma API REST

Uma API web é um programa que fica esperando pedidos HTTP e responde, quase sempre, com
JSON. REST é um **estilo** de organizar esses pedidos. A ideia central: o endereço diz
**qual recurso** e o método diz **o que fazer** com ele.

```text
  MÉTODO   CAMINHO                     SIGNIFICADO
  GET      /linhas/B/tolerancias       ler as tolerâncias da linha B
  POST     /medicoes                   registrar uma medição nova
  GET      /medicoes/15                ler a medição 15
  PUT      /regras/B/espessura         criar ou trocar a regra de espessura da linha B
  PATCH    /ocorrencias/3/encerrar     mudar parte de uma ocorrência
  DELETE   /amostras/7                 apagar a amostra 7
```

Convenções que você vai ver em toda API bem feita:

- Caminhos com **substantivos no plural** (`/medicoes`), não verbos (`/registrarMedicao`).
- O **método** carrega a ação. `GET` nunca altera nada.
- O **status** conta o resultado: 200 deu certo, 201 criou, 404 não existe, 422 dados
  inválidos (a tabela completa está no módulo 12, seção 2).
- Erros também respondem JSON, com uma mensagem útil.

Uma analogia: a API é o **balcão do laboratório**. Quem chega não entra na sala dos
equipamentos. Faz um pedido no formato combinado ("quero o laudo da OP 123456") e recebe
a resposta no formato combinado. O que acontece lá dentro (planilha, banco, cálculo) pode
mudar sem que o cliente perceba.

## 2. A primeira API

Instale (já está no `requirements.txt` do curso):

```text
python -m pip install fastapi uvicorn httpx
```

- `fastapi`: o framework.
- `uvicorn`: o servidor que recebe as conexões HTTP e entrega ao FastAPI.
- `httpx`: usado pelo `TestClient` nos testes.

O menor programa útil:

```python
from fastapi import FastAPI

app = FastAPI(title="API do Laboratório", version="0.1.0")


@app.get("/")
def raiz() -> dict:
    return {"mensagem": "API do laboratório no ar"}


@app.get("/saude")
def saude() -> dict:
    return {"status": "ok"}
```

Leia assim: `@app.get("/saude")` **registra** a função logo abaixo. Quando chegar um
`GET /saude`, o FastAPI chama `saude()` e converte o dicionário devolvido em JSON. O
`@` é um **decorador**: um jeito curto de dizer "passe esta função para o app guardar".

Para subir o servidor, na pasta do arquivo:

```text
uvicorn 01_primeira_api:app --reload
```

`01_primeira_api` é o nome do arquivo (sem `.py`), `app` é a variável com o `FastAPI()`
e `--reload` reinicia sozinho quando você salva. Saída típica:

```text
INFO:     Started server process [880]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:39330 - "GET / HTTP/1.1" 200 OK
```

Abra `http://127.0.0.1:8000/saude` no navegador e veja o JSON. Depois abra
`http://127.0.0.1:8000/docs`: uma página interativa com todas as rotas, gerada
automaticamente. Clique numa rota, em **Try it out** e em **Execute**. Para parar o
servidor: `Ctrl+C` no terminal.

> 💡 **Dica:** os exemplos deste módulo têm dois modos. `python exemplos/01_primeira_api.py`
> faz uma **demonstração** sem servidor; com `--servir`, sobem o uvicorn em
> `http://127.0.0.1:8000`.

> 🔮 **Preveja antes de rodar:** além de `GET /` e `GET /saude`, o exemplo 01 faz
> `GET /nada` e `POST /`. Que status cada um recebe?

<details><summary>Resposta</summary>

Saída de `python exemplos/01_primeira_api.py`:

```text
GET  /       -> 200 {'mensagem': 'API do laboratório no ar'}
GET  /saude  -> 200 {'status': 'ok'}
GET  /nada   -> 404 {'detail': 'Not Found'}
POST /       -> 405 {'detail': 'Method Not Allowed'}
Título na documentação: API do Laboratório 0.1.0
Rotas documentadas: ['/', '/saude']
```

`/nada` não existe: 404. O caminho `/` existe, mas só para `GET`: 405, "método não
permitido". Esses dois erros o FastAPI gera sozinho.

</details>

> 🔧 **Modifique:** acrescente ao exemplo 01 uma rota `GET /versao` que devolve
> `{"versao": "0.1.0"}`. Rode com `--servir` e confira no `/docs` que ela apareceu.

> 💡 **Dica:** você vai ver `async def` em muitos tutoriais. Use `def` comum, como neste
> curso, sempre que a rota usar bibliotecas "normais" (SQLite, arquivos, pandas). O
> FastAPI roda essas funções em threads e tudo funciona. `async def` só faz sentido com
> bibliotecas assíncronas, assunto para depois do curso.

## 3. Testando com TestClient

Subir o servidor e clicar no `/docs` é ótimo para explorar, mas não para conferir 30 casos
toda vez que você muda algo. O `TestClient` é um "navegador de mentira": conversa com o
`app` direto, sem rede e sem servidor.

```python
from fastapi.testclient import TestClient

cliente = TestClient(app)
resposta = cliente.get("/saude")
print(resposta.status_code, resposta.json())
```

```text
200 {'status': 'ok'}
```

A resposta tem a mesma "cara" da resposta do `requests` (módulo 12): `.status_code`,
`.json()`, `.text`, `.headers`. Para enviar dados: `cliente.post("/medicoes",
json={...})`, `cliente.get("/bobinas", params={"linha": "C"})`,
`cliente.get("/eu", headers={"X-Chave": "lab-123"})`.

### Exemplo resolvido: o teste de uma rota

**Problema:** quero garantir que `GET /saude` responde `{"status": "ok"}`.

**Como pensei:** todo teste tem três partes (módulo 09, padrão AAA):

1. **Arrange (preparar):** criar o cliente.
2. **Act (agir):** fazer a requisição.
3. **Assert (conferir):** primeiro o status, depois o corpo. Conferir o status antes
   dá uma mensagem de erro muito mais clara quando a rota nem existe.

```python
from fastapi.testclient import TestClient

from main import app

cliente = TestClient(app)


def test_saude():
    resposta = cliente.get("/saude")                 # agir
    assert resposta.status_code == 200               # conferir o status
    assert resposta.json() == {"status": "ok"}       # conferir o corpo
```

É exatamente o molde dos testes dos exercícios deste módulo. Abra
`testes/test_m13_ex01_ola_api.py` e compare.

## 4. Parâmetros de caminho

Um pedaço do endereço pode ser variável: `/bobinas/3`, `/linhas/B/tolerancias`. Você
marca o pedaço com chaves e recebe um parâmetro com o **mesmo nome**:

```python
@app.get("/bobinas/{numero}")
def ver_bobina(numero: int) -> dict:
    for bobina in BOBINAS:
        if bobina["numero"] == numero:
            return bobina
    return {"aviso": f"bobina {numero} não existe (no exemplo 04 isso vira um 404)"}
```

O type hint `int` não é enfeite. O FastAPI usa o tipo para **converter** (`"3"` vira `3`)
e para **validar** (`"tres"` é recusado com 422, sem nem chamar a sua função).

> 🔮 **Preveja antes de rodar:** e se você esquecer o tipo?
>
> ```python
> @app.get("/dobro/{numero}")
> def dobro(numero):
>     return {"dobro": numero * 2}
>
> print(TestClient(app).get("/dobro/21").json())
> ```

<details><summary>Resposta</summary>

```text
{'dobro': '2121'}
```

Sem tipo, tudo que vem do endereço é **texto**. E `"21" * 2` repete o texto (módulo 01).
Com `numero: int`, a resposta seria `{'dobro': 42}`.

</details>

Para aceitar só alguns valores, use um `Enum` (módulo 08). O `/docs` até mostra uma lista
de escolha:

```python
class Linha(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


@app.get("/linhas/{linha}/tolerancias")
def tolerancias_da_linha(linha: Linha) -> dict:
    return {"linha": linha.value, "tolerancias": TOLERANCIAS[linha.value]}
```

Herdar de `str` faz cada membro do Enum se comportar como texto (e sair como texto no
JSON). Rode `python exemplos/02_parametros.py`. As primeiras linhas:

```text
GET /linhas/B/tolerancias
    200 {'linha': 'B', 'tolerancias': {'espessura': [38.0, 42.0], 'gramatura': [36.5, 39.5]}}
GET /linhas/E/tolerancias
    422 {'detail': [{'type': 'enum', 'loc': ['path', 'linha'], 'msg': "Input should be 'A', 'B', 'C' or 'D'", 'input': 'E', 'ctx': {'expected': "'A', 'B', 'C' or 'D'"}}]}
GET /bobinas/3
    200 {'numero': 3, 'op': '123789', 'linha': 'B', 'peso_kg': 640.0}
GET /bobinas/tres
    422 {'detail': [{'type': 'int_parsing', 'loc': ['path', 'numero'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': 'tres'}]}
```

Aprenda a ler o 422: `loc` diz **onde** (`path`, `query` ou `body`, e o nome do campo),
`msg` diz **o quê**, `input` mostra o valor recebido.

> 💡 **Dica:** uma alternativa mais leve ao `Enum` é `typing.Literal["A", "B", "C", "D"]`:
> mesmo efeito, sem criar classe. Usamos os dois neste módulo.

## 5. Parâmetros de consulta

Parâmetro da função que **não** aparece no caminho vira parâmetro de consulta (a parte
depois do `?`). Com valor padrão, é opcional:

```python
@app.get("/bobinas")
def listar_bobinas(
    linha: Linha | None = None,                          # opcional
    peso_min: Annotated[float, Query(ge=0)] = 0,         # ge = maior ou igual
    limite: Annotated[int, Query(ge=1, le=100)] = 10,    # entre 1 e 100
) -> list[dict]:
    resultado = [
        b for b in BOBINAS
        if (linha is None or b["linha"] == linha.value) and b["peso_kg"] >= peso_min
    ]
    return resultado[:limite]
```

`Annotated[tipo, Query(...)]` junta o tipo com regras extras. As mais usadas: `ge`, `gt`,
`le`, `lt` para números; `min_length`, `max_length` e `pattern` para textos. O resto do
exemplo 02:

```text
GET /bobinas?linha=C
    200 [{'numero': 4, 'op': '124001', 'linha': 'C', 'peso_kg': 1210.0}, {'numero': 5, 'op': '124001', 'linha': 'C', 'peso_kg': 1100.0}]
GET /bobinas?peso_min=500&limite=2
    200 [{'numero': 3, 'op': '123789', 'linha': 'B', 'peso_kg': 640.0}, {'numero': 4, 'op': '124001', 'linha': 'C', 'peso_kg': 1210.0}]
GET /bobinas?limite=0
    422 {'detail': [{'type': 'greater_than_equal', 'loc': ['query', 'limite'], 'msg': 'Input should be greater than or equal to 1', 'input': '0', 'ctx': {'ge': 1}}]}
```

> ⚠️ **Erro comum:** declarar `linha: str` sem valor padrão achando que é opcional. Sem
> padrão, o parâmetro é **obrigatório**: chamar `/bobinas` sem `?linha=` dá 422. Para
> opcional: `linha: str | None = None`.

> 🔮 **Preveja antes de rodar:** o que acontece com o parâmetro `extra`?
>
> ```python
> @app.get("/x/{linha}")
> def x(linha: str, limite: int = 10):
>     return {"linha": linha, "limite": limite}
>
> print(TestClient(app).get("/x/A?limite=3&extra=1").json())
> ```

<details><summary>Resposta</summary>

```text
{'linha': 'A', 'limite': 3}
```

Parâmetros de consulta que a função não declara são simplesmente ignorados. Não dá erro,
o que também significa que um erro de digitação (`?limte=3`) passa em silêncio e o
padrão 10 é usado. Teste os nomes!

</details>

> 🔧 **Modifique:** acrescente ao exemplo 02 um filtro opcional `op` (texto) em
> `/bobinas`. Teste `/bobinas?op=124001` e `/bobinas?op=124001&limite=1`.

## 6. Corpo com Pydantic

Dados maiores (uma medição, um pedido de certificado) vão no **corpo** da requisição, em
JSON. Você descreve o formato com uma classe Pydantic. O FastAPI entende: parâmetro cujo
tipo é um `BaseModel` vem do corpo.

```python
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Medicao(BaseModel):
    op: str = Field(pattern=r"^\d{6}$", examples=["123456"])
    linha: Literal["A", "B", "C", "D"]
    ensaio: str = Field(min_length=2)
    valor: float = Field(gt=0)
    unidade: str = "µm"                        # com padrão: opcional

    @field_validator("ensaio")
    @classmethod
    def padronizar_ensaio(cls, valor: str) -> str:
        return valor.strip().lower()           # " Espessura " -> "espessura"


@app.post("/medicoes/avaliar")
def avaliar(medicao: Medicao) -> Resultado:
    ...
```

O que cada peça faz:

- **Tipo** (`str`, `float`, `Literal[...]`): o Pydantic converte e valida.
- **`Field(...)`**: regras extras (`gt`, `ge`, `min_length`, `pattern`) e metadados
  (`examples`, que aparecem no `/docs`).
- **Valor padrão**: torna o campo opcional.
- **`@field_validator("campo")`**: sua própria regra para um campo. Pode transformar o
  valor (devolve o novo) ou recusar (levanta `ValueError`). Por padrão roda **depois**
  da conversão de tipo; com `mode="before"`, recebe o dado cru (útil para aceitar
  `"1.250,5"`, exercício 12).
- **`@model_validator(mode="after")`**: regra que envolve **vários** campos ao mesmo
  tempo, como "mínimo não pode ser maior que máximo". Recebe o objeto pronto (`self`) e
  deve terminar com `return self`.

O modelo funciona sozinho, fora da API. Isso é ótimo para testar e para usar no resto do
projeto (o robô do módulo 12 poderia validar os pedidos com ele). Saída da primeira parte
de `python exemplos/03_corpo_pydantic.py`:

```text
1) O modelo funciona sozinho, sem API:
   Medicao(op='123456', linha='A', ensaio='espessura', valor=20.4, unidade='µm')
   model_dump(): {'op': '123456', 'linha': 'A', 'ensaio': 'espessura', 'valor': 20.4, 'unidade': 'µm'}
   ValidationError com 3 erros:
    - ('op',) String should match pattern '^\d{6}$'
    - ('linha',) Input should be 'A', 'B', 'C' or 'D'
    - ('valor',) Input should be greater than 0
```

Repare: `valor="20.4"` (texto) virou `20.4`, e `"  Espessura "` virou `"espessura"`. E o
Pydantic lista **todos** os erros de uma vez, não só o primeiro.

> 🔮 **Preveja antes de rodar:** o que sai deste `model_dump()`?
>
> ```python
> class M(BaseModel):
>     op: str
>     valor: float = Field(gt=0)
>
> print(M(op="123456", valor=1, cor="azul").model_dump())
> ```

<details><summary>Resposta</summary>

```text
{'op': '123456', 'valor': 1.0}
```

Campos que o modelo não conhece (`cor`) são ignorados, e o `1` inteiro vira `1.0`
porque o campo é `float`. Se quiser **recusar** campos desconhecidos, acrescente
`model_config = ConfigDict(extra="forbid")` na classe.

</details>

**Modelo de resposta.** O tipo de retorno da rota (`-> Resultado`) é o **contrato de
saída**: o FastAPI valida o que sai e **remove** o que não está no modelo. No exemplo 03,
a função devolve um campo `uso_interno` que nunca chega ao cliente:

```text
2) Pela API:
   200 {'op': '123456', 'ensaio': 'cof', 'valor': 0.31, 'minimo': 0.2, 'maximo': 0.3, 'aprovado': False}
   422 [['body', 'ensaio'], ['body', 'valor']]
```

Isso protege você de vazar sem querer um campo interno (uma senha, um custo). O segundo
pedido mandou só `op` e `linha`: o 422 aponta os dois campos obrigatórios que faltaram.

> 💡 **Dica:** o Pydantic v2 usa `model_dump()` e `model_validate()`. Tutoriais antigos
> (Pydantic v1) usam `.dict()` e `parse_obj()`; se você encontrar isso, traduza.

## 7. Códigos de status e HTTPException

Por padrão, toda resposta de sucesso é 200. Para dizer outra coisa:

| Situação | Status | Como |
|---|---|---|
| Criou algo novo | 201 | `@app.post(..., status_code=201)` |
| Apagou, nada a devolver | 204 | `@app.delete(..., status_code=204)` e a função devolve `None` |
| Não existe | 404 | `raise HTTPException(status_code=404, detail="...")` |
| Conflita com o estado atual | 409 | `raise HTTPException(status_code=409, detail="...")` |
| Sem chave / chave inválida | 401 | idem |
| Sem permissão | 403 | idem |
| Dados inválidos | 422 | automático (Pydantic) |

O módulo `fastapi.status` tem nomes para os números (`status.HTTP_201_CREATED`,
`status.HTTP_404_NOT_FOUND`), que deixam o código mais legível.

`HTTPException` é uma exceção: `raise` interrompe a função na hora, em qualquer
profundidade, e o FastAPI monta a resposta `{"detail": "..."}` com o status escolhido.

> 🔮 **Preveja antes de rodar:** um colega escreveu `return` em vez de `raise`. Que
> status o cliente recebe para `/linhas/Z`?
>
> ```python
> @app.get("/linhas/{codigo}")
> def ver(codigo: str):
>     if codigo != "A":
>         return HTTPException(status_code=404, detail="Linha não encontrada")
>     return {"codigo": "A"}
> ```

<details><summary>Resposta</summary>

```text
200 {"status_code":404,"detail":"Linha não encontrada","headers":null}
```

**200!** Com `return`, a exceção vira um objeto comum, que o FastAPI converte em JSON e
devolve como sucesso. O cliente que só olha o status acha que deu certo. Exceção se
**levanta** (`raise`), não se devolve.

</details>

### Exemplo resolvido: um cadastro com os status certos

**Problema:** cadastro de amostras em memória: criar, ver, listar e apagar, cada operação
com o status que conta o que aconteceu.

**Como pensei:**

1. Separei o que o cliente **envia** (`AmostraEntrada`: código, OP, descrição) do que a
   API **devolve** (`Amostra`: tudo isso mais o `id`). Herança (módulo 08) evita repetir.
2. Três rotas precisam de "ache a amostra ou responda 404". Virou uma função auxiliar,
   `buscar_ou_404`, que levanta a `HTTPException`. A exceção "sobe" pela rota que chamou.
3. Código repetido não é erro de dados, é **conflito** com o que já existe: 409.
4. O novo id é o maior existente + 1 (`max(AMOSTRAS, default=0) + 1`; o `default` evita
   erro com o dicionário vazio).

```python
def buscar_ou_404(id_amostra: int) -> Amostra:
    if id_amostra not in AMOSTRAS:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Amostra {id_amostra} não existe")
    return AMOSTRAS[id_amostra]


@app.post("/amostras", status_code=status.HTTP_201_CREATED)
def criar_amostra(entrada: AmostraEntrada) -> Amostra:
    if any(a.codigo == entrada.codigo for a in AMOSTRAS.values()):
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail=f"Já existe amostra com código {entrada.codigo}"
        )
    novo_id = max(AMOSTRAS, default=0) + 1
    amostra = Amostra(id=novo_id, **entrada.model_dump())
    AMOSTRAS[novo_id] = amostra
    return amostra


@app.delete("/amostras/{id_amostra}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_amostra(id_amostra: int) -> None:
    buscar_ou_404(id_amostra)
    del AMOSTRAS[id_amostra]
```

Saída de `python exemplos/04_status_e_erros.py`:

```text
POST   /amostras    -> 201 {'codigo': 'AM-001', 'op': '123456', 'descricao': 'Bobina 3', 'id': 1}
POST   /amostras    -> 201 {'codigo': 'AM-002', 'op': '123789', 'descricao': '', 'id': 2}
POST   /amostras    -> 409 {'detail': 'Já existe amostra com código AM-001'}
GET    /amostras/2  -> 200 {'codigo': 'AM-002', 'op': '123789', 'descricao': '', 'id': 2}
DELETE /amostras/2  -> 204 (sem corpo)
DELETE /amostras/2  -> 404 {'detail': 'Amostra 2 não existe'}
GET    /amostras    -> 200 [{'codigo': 'AM-001', 'op': '123456', 'descricao': 'Bobina 3', 'id': 1}]
```

> 🔧 **Modifique:** acrescente uma rota `PATCH /amostras/{id_amostra}/descricao` que recebe
> `{"descricao": "..."}` e troca só a descrição. Que status ela deve devolver quando a
> amostra não existe? (O exercício 07 pratica `PATCH` com outra regra de negócio.)

> ⚠️ **Erro comum:** guardar dados num dicionário global e esperar que eles fiquem lá. Eles
> **somem** quando o servidor reinicia (e o `--reload` reinicia a cada vez que você salva).
> Para dados de verdade, banco: seção 10.

## 8. Organizando em módulos

Uma API real tem dezenas de rotas. Tudo num arquivo vira bagunça. A ferramenta é o
`APIRouter`: um "mini-app" por assunto, que depois é plugado no app principal.

```python
# rotas/tolerancias.py
from fastapi import APIRouter

router = APIRouter(prefix="/linhas", tags=["tolerâncias"])


@router.get("/{linha}/tolerancias", summary="Tolerâncias de uma linha")
def listar_tolerancias(linha: Linha, con: Conexao) -> list[Tolerancia]:
    ...
```

```python
# main.py
from fastapi import FastAPI

from .rotas import medicoes, tolerancias

app = FastAPI(title="API do Laboratório de Qualidade", version="1.0.0")
app.include_router(tolerancias.router)
app.include_router(medicoes.router)
```

`prefix` é colado na frente de todas as rotas do router; `tags` agrupa as rotas no
`/docs`. O exemplo 07 tem uma API completa organizada assim:

```text
exemplos/api_laboratorio/
  __init__.py
  main.py            cria o app e inclui os routers
  banco.py           conexão SQLite, tabelas e dados iniciais
  modelos.py         modelos Pydantic (o que entra e o que sai)
  regras.py          lógica pura de tolerância (sem FastAPI, sem banco)
  rotas/
    __init__.py
    tolerancias.py   GET /linhas/{linha}/tolerancias
    medicoes.py      POST /medicoes e GET /ops/{op}/situacao
```

Repare em `regras.py`: a regra de negócio (faixa ou nominal ± %) não sabe que existe
FastAPI nem banco. É a mesma ideia do robô do módulo 12: o núcleo puro no meio, as
"bordas" (HTTP, banco) em volta. Assim a regra pode ser testada e reaproveitada.

Dentro do pacote, os imports são **relativos** (`from ..banco import Conexao`: dois
pontos = "o pacote de cima"). Para subir o servidor, de dentro de `exemplos`:

```text
uvicorn api_laboratorio.main:app --reload
```

> ⚠️ **Erro comum:** declarar `@app.get("/linha/{codigo}")` **antes** de
> `@app.get("/linha/especial")`. As rotas são testadas na ordem em que foram declaradas,
> e `{codigo}` aceita qualquer texto, inclusive `especial`. Declare as rotas fixas antes
> das rotas com parâmetro.

## 9. Dependências

Várias rotas precisam da mesma coisa antes de começar: conferir a chave de acesso, abrir
a conexão com o banco, carregar as regras. Repetir esse código em cada rota é pedir para
esquecer em uma. A solução do FastAPI é a **injeção de dependência** com `Depends`, a
mesma ideia do módulo 12 ("receba a sessão como parâmetro"), só que automática.

```python
CHAVES = {"lab-123": "Ana (laboratório)", "exp-456": "Carla (expedição)"}


def usuario_atual(x_chave: Annotated[str | None, Header()] = None) -> str:
    if x_chave not in CHAVES:
        raise HTTPException(status_code=401, detail="Chave de acesso inválida ou ausente")
    return CHAVES[x_chave]


def obter_tolerancias() -> dict:
    return TOLERANCIAS


Usuario = Annotated[str, Depends(usuario_atual)]
Tolerancias = Annotated[dict, Depends(obter_tolerancias)]


@app.get("/tolerancias/{linha}")
def ver_tolerancias(linha: str, usuario: Usuario, tolerancias: Tolerancias) -> dict:
    ...
```

Como funciona: antes de chamar `ver_tolerancias`, o FastAPI chama `usuario_atual` e
`obter_tolerancias` e passa os resultados. Se `usuario_atual` levantar 401, a rota nem
roda. `Header()` lê um cabeçalho HTTP; o nome `x_chave` vira o cabeçalho `x-chave` (o
FastAPI troca `_` por `-`).

O melhor vem nos testes: `app.dependency_overrides` troca uma dependência por outra
sem tocar nas rotas. Saída de `python exemplos/05_dependencias.py`:

```text
sem chave     -> {'detail': 'Chave de acesso inválida ou ausente'}
chave errada  -> 401
chave certa   -> {'usuario': 'Carla (expedição)'}
tolerâncias A -> {'linha': 'A', 'consultado_por': 'Ana (laboratório)', 'tolerancias': {'espessura': [18.0, 22.0]}}
com override  -> {'espessura': [19.0, 21.0]}
```

A última linha veio de:

```python
app.dependency_overrides[obter_tolerancias] = lambda: {"A": {"espessura": [19.0, 21.0]}}
...
app.dependency_overrides.clear()   # sempre desfaça no fim
```

> ⚠️ **Erro comum:** confundir 401 com 403. **401**: "não sei quem você é" (sem chave ou
> chave inválida). **403**: "sei quem você é, mas você não pode fazer isso" (chave só de
> leitura tentando alterar regra). O exercício 09 pratica os dois.

> 💡 **Dica:** chave no cabeçalho é um bom começo para uma API interna. Para usuários de
> verdade, o FastAPI tem suporte a OAuth2 e tokens JWT (veja "Security" na documentação).
> E chaves nunca ficam no código: leia de variável de ambiente.

## 10. Persistência com SQLite

Para os dados sobreviverem ao reinício, banco. Você já sabe SQLite (módulo 11). A
pergunta é: **como a rota recebe a conexão?** Resposta: uma dependência com `yield`.

### Exemplo resolvido: a conexão como dependência

**Como pensei:**

1. Cada requisição deve ter a **sua** conexão: abrir no começo, fechar no fim, mesmo se
   a rota der erro. Isso é um `try/finally` (módulo 06).
2. Uma dependência com `yield` faz exatamente isso: o código **antes** do `yield` roda
   antes da rota; o `finally` roda **depois** que a resposta foi montada.
3. O FastAPI pode preparar a dependência numa thread e rodar a rota em outra. O `sqlite3`,
   por segurança, recusa usar a conexão em outra thread. `check_same_thread=False`
   desliga essa trava, o que é seguro aqui porque cada requisição tem a sua conexão.
4. `row_factory = sqlite3.Row` faz as linhas funcionarem como dicionário
   (`linha["valor"]`), o que facilita montar os modelos.
5. Um apelido `Conexao` deixa as assinaturas das rotas curtas.

```python
def obter_conexao():
    CAMINHO_BANCO.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(CAMINHO_BANCO, check_same_thread=False)
    con.row_factory = sqlite3.Row
    try:
        criar_tabela(con)
        yield con
    finally:
        con.close()


Conexao = Annotated[sqlite3.Connection, Depends(obter_conexao)]


@app.post("/medicoes", status_code=status.HTTP_201_CREATED)
def criar_medicao(entrada: MedicaoEntrada, con: Conexao) -> Medicao:
    with con:  # transação: commit se tudo der certo, rollback se der erro
        cursor = con.execute(
            "INSERT INTO medicoes (op, ensaio, valor) VALUES (?, ?, ?)",
            (entrada.op, entrada.ensaio, entrada.valor),
        )
    return Medicao(id=cursor.lastrowid, **entrada.model_dump())
```

Saída de `python exemplos/06_sqlite.py`:

```text
POST -> 201 {'op': '123456', 'ensaio': 'espessura', 'valor': 20.4, 'id': 1}
POST -> 201 {'op': '123456', 'ensaio': 'cof', 'valor': 0.27, 'id': 2}
POST -> 201 {'op': '123789', 'ensaio': 'espessura', 'valor': 39.8, 'id': 3}
GET /medicoes?op=123456 -> [{'op': '123456', 'ensaio': 'espessura', 'valor': 20.4, 'id': 1}, {'op': '123456', 'ensaio': 'cof', 'valor': 0.27, 'id': 2}]
Depois do reinício, /medicoes/3 -> {'op': '123789', 'ensaio': 'espessura', 'valor': 39.8, 'id': 3}
GET /medicoes/99 -> 404
```

O "reinício" é um segundo `TestClient`: os dados continuam, porque estão no arquivo
`exemplos/saida/medicoes.db`. Nos testes, você troca `obter_conexao` por um banco **em
memória** com `dependency_overrides`; cada teste começa limpo e nada é gravado em disco
(exercício 11).

> ⚠️ **Erro comum:** montar o SQL com f-string: `f"SELECT * FROM medicoes WHERE op =
> '{op}'"`. Numa API isso é ainda mais grave que num script, porque **qualquer um** na
> rede pode mandar um `op` malicioso (SQL injection, módulo 11). Sempre `?` e a tupla de
> parâmetros.

> 🔧 **Modifique:** acrescente ao exemplo 06 a rota `DELETE /medicoes/{id_medicao}` (204,
> ou 404 se não existir). Dica: `cursor.rowcount` diz quantas linhas o `DELETE` apagou.

> 💡 **Dica:** quando o projeto crescer, existem bibliotecas que mapeiam tabelas para
> classes (SQLAlchemy, SQLModel, este último do mesmo autor do FastAPI). Para começar e
> para entender o que elas fazem por baixo, `sqlite3` puro é o melhor professor.

## 11. Documentação automática

O FastAPI gera, a partir do seu código, um documento padrão chamado **OpenAPI**
(`/openapi.json`) e duas telas em cima dele:

- `/docs` (Swagger UI): interativa, com **Try it out**.
- `/redoc`: só leitura, boa para imprimir ou mandar para alguém.

Tudo que você escreve vira documentação:

| No código | No /docs |
|---|---|
| `FastAPI(title=..., version=..., description=...)` | cabeçalho da página |
| `tags=["medições"]` (rota ou router) | grupos de rotas |
| `summary="Registra e avalia uma medição"` | título da rota |
| docstring da função da rota | descrição da rota |
| tipos e `Field(examples=[...])` dos modelos | esquema e exemplo do corpo |
| tipo de retorno | esquema da resposta |

Saída do final de `python exemplos/07_api_organizada.py`:

```text
Rotas: /linhas/{linha}/tolerancias, /medicoes, /ops/{op}/situacao, /saude
```

> 💡 **Dica:** mande o link do `/docs` para quem vai usar a sua API (a TI, o pessoal do
> BI). É documentação que nunca fica desatualizada, porque **é** o código.

## 12. Rodando de verdade: uvicorn e um cliente requests

Juntando com o módulo 12: o exemplo 08 sobe a API do laboratório num uvicorn **de
verdade** (numa thread, numa porta livre) e conversa com ela por HTTP com `requests`,
como o robô de certificados faria:

```python
servidor = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=porta, log_level="warning"))
threading.Thread(target=servidor.run, daemon=True).start()
...
resposta = sessao.post(f"{base}/medicoes", json=medicao, timeout=5)
resposta.raise_for_status()
```

Saída de `python exemplos/08_cliente_requests.py`:

```text
saúde: 200 {'status': 'ok'}
medição: 201 aprovado = False
situação: {'op': '124001', 'medicoes': 1, 'reprovadas': 1, 'liberada': False}
pedido inválido: 422 campos com problema: ['op', 'linha', 'ensaio', 'valor']
```

Detalhes para quando for usar no trabalho:

- `uvicorn main:app --reload` é para **desenvolver**. Em uso contínuo, rode sem
  `--reload`.
- `--host 127.0.0.1` (padrão) só aceita conexões do próprio computador. Para colegas na
  rede acessarem, `--host 0.0.0.0` e a porta liberada no firewall do Windows. Antes de
  fazer isso, converse com a TI: uma API exposta na rede precisa de chave de acesso e de
  alguém responsável por ela.
- `--port 8080` troca a porta, se a 8000 estiver ocupada.
- Com `pip install "fastapi[standard]"`, você ganha o comando `fastapi dev main.py`, um
  atalho para o uvicorn com recarga.

## Lendo mensagens de erro deste módulo

**422 Unprocessable Content** (na resposta, não no terminal):

```text
{'detail': [{'type': 'greater_than_equal', 'loc': ['query', 'limite'],
 'msg': 'Input should be greater than or equal to 1', 'input': '0', 'ctx': {'ge': 1}}]}
```

O pedido não passou na validação. `loc` diz onde (`path`, `query`, `body` + campo),
`msg` diz o quê, `input` mostra o valor recebido. Corrija o pedido, não a API (a não ser
que a regra esteja errada).

**404 `{'detail': 'Not Found'}`** (sem a sua mensagem): não existe rota para esse caminho.
Erro de digitação, barra a mais, ou o router não foi incluído (`include_router`). Se a
resposta tem a **sua** mensagem (`'Linha Z não encontrada'`), a rota existe e foi a sua
lógica que respondeu.

**405 `{'detail': 'Method Not Allowed'}`**: o caminho existe, mas não para esse método
(`POST` numa rota `GET`). Confira o decorador.

**500 Internal Server Error**: uma exceção que ninguém tratou estourou dentro da rota. O
cliente vê só "Internal Server Error"; o traceback de verdade aparece **no terminal do
uvicorn**. Leia de baixo para cima, como no módulo 00. No `TestClient`, a exceção
original aparece direto no teste.

**Resposta fora do modelo:**

```text
fastapi.exceptions.ResponseValidationError: 1 validation error:
  {'type': 'missing', 'loc': ('response', 'aprovado'), 'msg': 'Field required', 'input': {'op': '123456'}}
```

A rota devolveu algo que não bate com o tipo de retorno (faltou `aprovado`). O cliente
recebe 500. O erro é seu: complete o que a função devolve.

**uvicorn não acha o app:**

```text
ERROR:    Error loading ASGI app. Could not import module "main".
ERROR:    Error loading ASGI app. Attribute "aplicativo" not found in module "01_primeira_api".
```

No primeiro, você está na pasta errada ou o arquivo tem outro nome. No segundo, o nome
depois dos `:` não é o da variável (`app`).

**Porta ocupada:**

```text
ERROR:    [Errno 98] error while attempting to bind on address ('127.0.0.1', 8000): [errno 98] address already in use
```

(No Windows o número é `10048`.) Outro uvicorn ainda está rodando, talvez em outro
terminal. Pare-o com `Ctrl+C` ou use `--port 8001`.

**SQLite e threads:** `sqlite3.ProgrammingError: SQLite objects created in a thread can
only be used in that same thread.` Faltou `check_same_thread=False` (seção 10).

**Sem httpx:** `RuntimeError: The starlette.testclient module requires the httpx package
to be installed.` Rode `python -m pip install httpx` (ou o `requirements.txt`).

## Boas práticas

- **Substantivos no plural nos caminhos**, método HTTP para a ação, status que conta o
  resultado.
- **Valide na entrada** com Pydantic (tipos, `Field`, validadores) e **controle a saída**
  com o tipo de retorno. Nunca confie no que o cliente mandou.
- **`raise HTTPException`**, nunca `return`. E mensagens de `detail` que ajudam quem
  chamou a corrigir o pedido.
- **Lógica de negócio fora das rotas**, em funções puras (`regras.py`). A rota só traduz
  HTTP para Python e de volta.
- **Uma conexão por requisição**, via dependência com `yield`. SQL sempre com `?`.
- **Teste com `TestClient`**, conferindo o status antes do corpo. Troque banco e
  configurações com `dependency_overrides`.
- **Configuração por variável de ambiente** (caminho do banco, chaves), não no código.
- **Rotas fixas antes das rotas com parâmetro** no mesmo prefixo.
- **Documente enquanto escreve:** `title`, `version`, `tags`, `summary`, docstrings.
- **Não exponha na rede sem combinar com a TI.**

## No mundo real

O exemplo 07 é um retrato pequeno, mas fiel, de uma API de laboratório. Rode
`python exemplos/07_api_organizada.py`:

```text
GET /linhas/B/tolerancias
   espessura  nominal  38.0 a 42.0
   gramatura  nominal  36.48 a 39.52
POST /medicoes
   Espessura   41.2 -> 201 True
   gramatura   39.9 -> 201 False
   cof         0.25 -> 404 Sem tolerância para linha B / ensaio cof
GET /ops/123789/situacao -> {'op': '123789', 'medicoes': 2, 'reprovadas': 1, 'liberada': False}
GET /ops/999999/situacao -> 404
Rotas: /linhas/{linha}/tolerancias, /medicoes, /ops/{op}/situacao, /saude
```

Repare em três decisões de "mundo real":

1. **Tolerância nominal ± %** guardada como nominal e percentual, e convertida em
   mínimo/máximo na hora (40 ± 5% → 38,0 a 42,0). Se a especificação mudar o percentual,
   muda um número no banco.
2. **`404` para ensaio sem tolerância**, em vez de aprovar ou reprovar no escuro.
   Medição sem regra é um problema de cadastro, e a API diz isso claramente.
3. **A situação da OP** junta todas as medições: uma reprovação basta para não liberar.
   É a pergunta que o robô do módulo 12 faria antes de emitir o certificado.

Como isso se encaixa na empresa:

```text
  operador (tablet) ──POST /medicoes──┐
  robô de certificados ──GET /ops/{op}/situacao──┤
  Power BI / Excel ──GET (relatórios)──┤──> API do laboratório ──> SQLite (ou o banco da TI)
  ERP (integração da TI) ──────────────┘
```

Para produção, o caminho natural é a TI hospedar a API num servidor, trocar o SQLite pelo
banco corporativo (o código das rotas quase não muda, porque o acesso ao banco está
isolado em `banco.py`) e colocar autenticação de verdade. Mas a **regra**, que é o que
você entende melhor que ninguém, já está pronta, testada e documentada.

O desafio deste módulo leva essa API até a emissão de certificados.

## Resumo

| Assunto | Essencial |
|---|---|
| Criar o app | `app = FastAPI(title=..., version=...)` |
| Rota | `@app.get("/caminho")`, `@app.post`, `@app.put`, `@app.patch`, `@app.delete` |
| Subir | `uvicorn main:app --reload` → `http://127.0.0.1:8000/docs` |
| Testar | `cliente = TestClient(app)`; `cliente.get(...)`, `.post(..., json=...)` |
| Caminho | `@app.get("/bobinas/{numero}")` + `def f(numero: int)` |
| Valores fixos | `class Linha(str, Enum)` ou `Literal["A", "B"]` |
| Consulta | parâmetro fora do caminho; opcional com `= None`; `Annotated[int, Query(ge=1)] = 10` |
| Corpo | `class Medicao(BaseModel)` + `def f(medicao: Medicao)` |
| Regras de campo | `Field(gt=0, min_length=2, pattern=r"...")`, `@field_validator` |
| Regra entre campos | `@model_validator(mode="after")` ... `return self` |
| Converter | `modelo.model_dump()`, `Modelo.model_validate(dict)` |
| Saída | tipo de retorno `-> Resultado` (valida e filtra) |
| Status | `status_code=201` no decorador; 204 devolve `None` |
| Erro | `raise HTTPException(status_code=404, detail="...")` |
| Organizar | `router = APIRouter(prefix=..., tags=[...])`; `app.include_router(router)` |
| Dependência | `Annotated[str, Depends(funcao)]`; `Header()` para cabeçalhos |
| Banco | dependência com `yield` + `finally: con.close()`; `check_same_thread=False` |
| Trocar no teste | `app.dependency_overrides[original] = substituta`; `.clear()` no fim |

## Você domina este módulo se...

- [ ] Explico sem consultar a diferença entre parâmetro de caminho, de consulta e corpo,
      e sei como o FastAPI decide qual é qual.
- [ ] Escolho o status certo para criar (201), apagar (204), não encontrado (404),
      conflito (409), sem chave (401), sem permissão (403) e dados inválidos (422).
- [ ] Escrevo um modelo Pydantic com `Field`, `Literal` e um validador, e leio um 422
      apontando o campo com problema.
- [ ] Testo uma rota com `TestClient`, conferindo status e corpo.
- [ ] Uso `Depends` para chave de acesso e para a conexão, e troco uma dependência no
      teste com `dependency_overrides`.
- [ ] Guardo dados em SQLite com uma dependência com `yield`, usando sempre `?` no SQL.
- [ ] Organizo uma API em `main.py`, `modelos.py`, `banco.py` e `rotas/` com `APIRouter`.
- [ ] Subo a API com uvicorn, uso o `/docs` e consumo a API com `requests`.

## Exercícios

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_ola_api` | ★☆☆ | primeiras rotas GET, JSON, 405 |
| 02 | `ex02_parametros_caminho` | ★☆☆ | parâmetros de caminho com tipo, 422 automático |
| 03 | `ex03_linhas_404` | ★☆☆ | `HTTPException` 404, normalizar entrada |
| 04 | `ex04_parametros_consulta` | ★★☆ | filtros opcionais, `Annotated` + `Query(ge, le)` |
| 05 | `ex05_modelos_pydantic` | ★☆☆ | `BaseModel`, `Field`, `Literal`, `ValidationError` |
| 06 | `ex06_validar_medicao` | ★★☆ | corpo + modelo de resposta + função pura |
| 07 | `ex07_ocorrencias` | ★★☆ | CRUD com 201, 404, 409, 204 e `PATCH` |
| 08 | `ex08_router_e_docs` | ★☆☆ | `APIRouter`, prefixo, tags, resumos, `/openapi.json` |
| 09 | `ex09_dependencias` | ★★☆ | `Depends`, `Header`, 401 x 403, `dependency_overrides` |
| 10 | `ex10_leitura_prever_status` | ★★☆ | leitura de código: prever os status da API de um colega |
| 11 | `ex11_revisao_estatisticas_sqlite` | ★★★ | revisão: SQLite, `statistics`, agrupamento (módulos 03, 07, 11) |
| 12 | `ex12_revisao_regras_tolerancia` | ★★★ | revisão: Enum, número BR, validadores (módulos 04, 05, 08) |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código e rode, na
pasta `curso-python`:

```text
python curso.py testar 13 ex01
```

Nos exercícios de API, o arquivo já cria `app = FastAPI()`: você escreve as rotas
(e os modelos e funções que o enunciado pedir, no lugar de `raise NotImplementedError`).
Para o módulo inteiro: `python curso.py testar 13`.

## Desafio do módulo

**API de Certificados do laboratório.** Regras de tolerância (faixa e nominal ± %) em
SQLite, medições avaliadas na hora, situação da OP, emissão de certificado só para OP
liberada (e sem duplicar), chave de acesso para alterar regras e `/docs` organizado.
Enunciado completo em [desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou: [quiz.md](quiz.md).

## Para ir além

- `sqlite3` (documentação oficial): https://docs.python.org/pt-br/3/library/sqlite3.html
- `enum`: https://docs.python.org/pt-br/3/library/enum.html
- `typing` (`Annotated`, `Literal`): https://docs.python.org/pt-br/3/library/typing.html
- Tutorial oficial do FastAPI (tem versão em português): https://fastapi.tiangolo.com/pt/tutorial/
- FastAPI, "Bigger Applications" (organizar em módulos):
  https://fastapi.tiangolo.com/tutorial/bigger-applications/
- Pydantic v2 (modelos e validadores): https://docs.pydantic.dev/latest/concepts/models/
- Leitura extra: os códigos de status HTTP explicados pela MDN:
  https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status
