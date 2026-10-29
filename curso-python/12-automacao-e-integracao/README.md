# Módulo 12 — Automação e integração

> **Tempo estimado:** 14 a 18 horas · **Pré-requisitos:** módulos 00 a 11 · **Nível:** intermediário

## O que você vai aprender

- Explicar o que acontece numa requisição HTTP: método, URL, cabeçalhos, corpo e status.
- Consultar uma API com `requests` usando `params`, `json`, `timeout`,
  `raise_for_status()` e `Session`.
- Tratar falhas de rede (`Timeout`, `ConnectionError`, `HTTPError`) e repetir com
  espera crescente.
- Testar código que usa a rede **sem internet**, com injeção de dependência e
  `monkeypatch`.
- Organizar centenas de arquivos com `pathlib` e `shutil`, primeiro em modo ensaio.
- Gerar um relatório Excel com estilos, largura de coluna, filtro, painel congelado e
  formatação condicional usando `openpyxl`.
- Montar e salvar um e-mail com anexo (`email.message`) e ler arquivos `.eml`.
- Escolher o caminho certo para ler o Outlook: clássico (`win32com`), Novo Outlook,
  Microsoft Graph ou Power Automate.
- Agendar um script no Agendador de Tarefas do Windows.
- Escrever um robô web com Playwright no Edge: seletores robustos, esperas, prints de
  tela, log, modo ensaio e idempotência.

## Por que isso importa

Todo dia alguém no laboratório copia número de uma tela para outra. Abre o e-mail da
expedição, procura a OP, abre o Protheus, digita, confere, imprime, responde. São
minutos por pedido, horas por semana, e um erro de digitação vira certificado errado.

Automação é a área de Python que mais rápido gera valor dentro de uma empresa. Também é
uma porta de entrada no mercado: vagas de "analista de automação", "RPA" e "engenheiro
de dados" pedem exatamente APIs, arquivos, Excel, e-mail e robôs.

Este módulo é a ponte do projeto final com o mundo: o núcleo (regras, tolerâncias,
fila) está nos módulos anteriores. Aqui você aprende a **ler** pedidos de e-mail,
**gerar** relatórios e **operar** a tela do ERP com um robô que não faz besteira.

## 1. O mapa da automação: API, arquivo ou tela?

Antes de escrever código, pergunte **por onde** os dados entram e saem. Existem três
caminhos, do melhor para o pior:

```text
  MAIS ROBUSTO                                              MAIS FRÁGIL
  ┌──────────────┐     ┌───────────────────┐     ┌──────────────────────┐
  │ 1. API       │     │ 2. Arquivo        │     │ 3. Tela (robô/RPA)   │
  │ HTTP + JSON  │ --> │ Excel, CSV, .eml, │ --> │ clicar e digitar no  │
  │ do sistema   │     │ PDF numa pasta    │     │ navegador como gente │
  └──────────────┘     └───────────────────┘     └──────────────────────┘
  rápido, testável     simples, depende de       quebra quando a tela
  e estável            quem gera o arquivo       muda; último recurso
```

- **API**: o sistema oferece uma "porta" para programas. É o caminho profissional.
- **Arquivo**: alguém (ou outro programa) gera um arquivo; seu script lê ou escreve.
- **Tela**: o robô imita uma pessoa. Funciona com qualquer sistema, mas é frágil.

> 💡 **Dica:** antes de fazer um robô para o TOTVS Protheus, pergunte à TI se existe
> integração por API REST ou outra rotina de importação. O Protheus tem recursos de
> integração; quem decide se estão liberados é a TI. Se a resposta for "não", o robô
> de tela é a saída, e vamos fazê-lo direito.

## 2. HTTP em 10 minutos

HTTP é a "língua" que navegadores e programas usam para conversar com servidores. É
como o balcão do laboratório: alguém faz um **pedido** e recebe uma **resposta**.

Um pedido (requisição) tem quatro partes:

```text
GET /tolerancias?linha=A HTTP/1.1          <- MÉTODO, CAMINHO (com parâmetros) e versão
Host: api.lab.local                        <- CABEÇALHOS: informações sobre o pedido
Accept: application/json
Authorization: Bearer abc123
                                           <- linha em branco
(corpo vazio: GET não leva corpo)          <- CORPO: os dados enviados (POST, PUT...)
```

E a resposta volta assim:

```text
HTTP/1.1 200 OK                            <- STATUS: deu certo?
Content-Type: application/json; charset=utf-8
Content-Length: 120

{"linha": "A", "itens": [{"ensaio": "espessura", "minimo": 18.0, "maximo": 22.0}]}
```

### Métodos

| Método | Para quê | Exemplo |
|---|---|---|
| `GET` | Ler, sem mudar nada | consultar tolerâncias da linha A |
| `POST` | Criar algo novo | registrar uma medição |
| `PUT` | Substituir algo inteiro | trocar a regra de COF da linha B |
| `PATCH` | Mudar parte de algo | corrigir só o valor de uma medição |
| `DELETE` | Apagar | excluir uma medição lançada errada |

`GET`, `PUT` e `DELETE` são **idempotentes**: repetir o mesmo pedido deixa o servidor no
mesmo estado. `POST` não: dois `POST` iguais criam duas medições. Guarde essa palavra;
ela volta na seção 12.

### Códigos de status

O primeiro dígito diz a família:

| Família | Significado | Os mais comuns |
|---|---|---|
| 2xx | Sucesso | `200 OK`, `201 Created`, `204 No Content` |
| 3xx | Redirecionamento | `301`, `302` (vá para outro endereço) |
| 4xx | Erro **seu** (cliente) | `400` pedido malformado, `401` sem login, `403` sem permissão, `404` não existe, `422` dados inválidos, `429` devagar! |
| 5xx | Erro **do servidor** | `500` erro interno, `502`/`504` problema no caminho, `503` fora do ar |

### JSON

JSON é o formato de texto mais usado em APIs. Ele mapeia quase direto para Python:
objeto `{}` vira `dict`, lista `[]` vira `list`, `true/false/null` viram
`True/False/None`. Você já usou o módulo `json` no módulo 06.

## 3. requests: conversando com APIs

O `requests` é a biblioteca mais usada para HTTP em Python. Já está no
`requirements.txt` do curso. Se precisar: `python -m pip install requests`.

Para treinar sem depender da internet, o exemplo 01 sobe uma pequena "API de treino"
no seu próprio computador (endereço `127.0.0.1`, que significa "esta máquina"). O
trecho que importa é este:

```python
resposta = requests.get(f"{base}/tolerancias", params={"linha": "A"}, timeout=5)
print("URL montada:", resposta.url)
print("Status:", resposta.status_code, resposta.reason)
print("Content-Type:", resposta.headers["Content-Type"])
dados = resposta.json()  # texto JSON -> dict do Python
```

Rode `python exemplos/01_http_basico.py`:

```text
1) GET com parâmetros de consulta
   URL montada: <base>/tolerancias?linha=A
   Status: 200 OK
   Content-Type: application/json; charset=utf-8
   espessura   18.0 a 22.0
   cof          0.2 a 0.3
2) Um pedido que dá errado (404)
   Status: 404 | ok? False
   Corpo: {'erro': "Linha 'Z' não encontrada"}
   raise_for_status levantou HTTPError 404
3) POST enviando JSON
   Status: 201 Created
   Corpo: {'id': 1, 'op': '123456', 'ensaio': 'cof', 'valor': 0.25}
```

(`<base>` é o endereço do servidor de treino; a porta muda a cada execução.)

O que cada peça faz:

- `params={"linha": "A"}` monta a query string `?linha=A` e codifica acentos e espaços.
- `timeout=5` desiste depois de 5 segundos sem resposta. **Sempre** passe timeout.
- `resposta.status_code` é o número; `resposta.ok` é `True` para status abaixo de 400.
- `resposta.json()` converte o corpo JSON em `dict`/`list`.
- `resposta.raise_for_status()` levanta `requests.HTTPError` se o status for 4xx ou 5xx.
- `requests.post(url, json=dados)` envia `dados` como JSON (e põe o cabeçalho certo).

> ⚠️ **Erro comum:** achar que um 404 ou 500 levanta exceção sozinho. Não levanta! Para
> o `requests`, receber uma resposta é sucesso, mesmo que a resposta diga "erro". Chame
> `raise_for_status()` logo depois de cada chamada.

> 🔮 **Preveja antes de rodar:** que URL o `requests` monta aqui?
>
> ```python
> import requests
>
> pedido = requests.Request(
>     "GET", "https://api.lab.local/medicoes",
>     params={"linha": "A", "op": None, "ensaio": "tração"},
> ).prepare()
> print(pedido.url)
> ```

<details><summary>Resposta</summary>

```text
https://api.lab.local/medicoes?linha=A&ensaio=tra%C3%A7%C3%A3o
```

Parâmetros com valor `None` são ignorados, e o `ç`/`ã` viram códigos `%XX`. O
`Request(...).prepare()` monta o pedido sem enviar: ótimo truque para conferir a URL no
REPL sem internet.

</details>

> 🔧 **Modifique:** no exemplo 01, peça a linha `"B"` e acrescente um segundo
> parâmetro, `"ensaio": "espessura"`. Veja a URL mudar. O servidor de treino ignora o
> parâmetro extra; uma API real poderia filtrar por ele.

### Sessão: configurar uma vez, usar sempre

Quando você faz várias chamadas para a mesma API, use `requests.Session()`. Ela guarda
cabeçalhos (como o token de acesso) e reaproveita a conexão, o que é mais rápido.

```python
with requests.Session() as sessao:
    sessao.headers.update(
        {"User-Agent": "robo-laboratorio/1.0", "Authorization": "Bearer abc123"}
    )
    for rota in ["/status", "/linhas"]:
        print(sessao.get(base + rota, timeout=5).json())
```

Saída (parte do exemplo 02):

```text
1) Sessão: cabeçalhos configurados uma vez, usados em todas as chamadas
   {'rota': '/status', 'user_agent': 'robo-laboratorio/1.0', 'autorizacao': 'Bearer abc123'}
   {'rota': '/linhas', 'user_agent': 'robo-laboratorio/1.0', 'autorizacao': 'Bearer abc123'}
```

> ⚠️ **Erro comum:** escrever o token ou a senha no código. Ele vai parar no Git e no
> e-mail de alguém. Leia de uma variável de ambiente:
> `token = os.environ["API_LAB_TOKEN"]`. No PowerShell, para a sessão atual:
> `$env:API_LAB_TOKEN = "abc123"`.

### Tente você

Usando `requests.Request(...).prepare()`, descubra que URL sai de
`params={"ops": ["123456", "123789"], "limite": 10}`.

<details><summary>Resposta</summary>

`?ops=123456&ops=123789&limite=10`. Uma lista vira a mesma chave repetida.

</details>

## 4. Falhas de rede: timeout, erros e novas tentativas

A rede da fábrica cai. O servidor reinicia na hora do almoço. O Wi-Fi do laboratório
some. Um robô profissional espera por isso.

As exceções do `requests` formam uma família. Todas herdam de `RequestException`:

```text
RequestException
 ├── ConnectionError        não conseguiu nem conversar com o servidor
 │    └── ConnectTimeout    (também é Timeout) demorou para conectar
 ├── Timeout
 │    └── ReadTimeout       conectou, mas a resposta não veio a tempo
 ├── HTTPError              raise_for_status() viu um 4xx ou 5xx
 └── JSONDecodeError        .json() recebeu algo que não é JSON
```

O exemplo 02 provoca as duas primeiras de propósito. Rode
`python exemplos/02_sessao_e_falhas.py` e veja o final:

```text
2) Timeout: o servidor demora 2 s, mas só aceitamos esperar 0,5 s
   ReadTimeout depois de 0.5 s
3) Ninguém escutando na porta: ConnectionError
   ConnectionError
4) A família de exceções do requests
   Timeout é RequestException? True
   HTTPError é RequestException? True
```

> 🔮 **Preveja antes de rodar:** o que este laço imprime para cada exceção?
>
> ```python
> import requests
>
> for erro in [requests.ReadTimeout("x"), requests.ConnectTimeout("x"), requests.HTTPError("x")]:
>     try:
>         raise erro
>     except requests.ConnectionError:
>         print("conexão")
>     except requests.Timeout:
>         print("timeout")
>     except requests.RequestException:
>         print("genérico")
> ```

<details><summary>Resposta</summary>

```text
timeout
conexão
genérico
```

O Python testa os `except` de cima para baixo e entra no **primeiro** que combina.
`ReadTimeout` é só `Timeout`. `ConnectTimeout` é `ConnectionError` **e** `Timeout`, e o
primeiro `except` já o pega. `HTTPError` só combina com a mãe de todas.

</details>

### Exemplo resolvido: tentar de novo com espera fixa

**Problema:** a consulta às vezes falha por queda de rede. Quero tentar até 3 vezes.

**Como pensei:**

1. Preciso repetir, então é um laço. Sei quantas vezes: `for` com `range`.
2. Dentro do laço, tento a chamada. Deu certo? `return` e acabou.
3. Deu `ConnectionError`? Aviso, espero e deixo o laço tentar de novo.
4. Se foi a **última** tentativa, não adianta esperar: relanço o erro com `raise`.
5. Para não amarrar a função a uma consulta específica, recebo a consulta como
   **função** (módulo 04: funções são valores).

```python
import time
import requests

def tentar_varias_vezes(funcao, tentativas=3, espera=2.0):
    for numero in range(1, tentativas + 1):
        try:
            return funcao()
        except requests.ConnectionError as erro:
            print(f"tentativa {numero} falhou: {erro}")
            if numero == tentativas:
                raise
            time.sleep(espera)

# Uma consulta "de mentira" que falha duas vezes e depois funciona:
falhas = [requests.ConnectionError("rede caiu"), requests.ConnectionError("rede caiu")]

def consultar():
    if falhas:
        raise falhas.pop()
    return {"linha": "A", "itens": []}

print(tentar_varias_vezes(consultar, espera=0.1))
```

Saída:

```text
tentativa 1 falhou: rede caiu
tentativa 2 falhou: rede caiu
{'linha': 'A', 'itens': []}
```

No exercício 04 você vai evoluir esta ideia: espera que **dobra** a cada falha
(*backoff exponencial*), `Timeout` também repetido, e um `dormir` injetável para o teste
não esperar de verdade.

> 💡 **Dica:** nunca repita um `HTTPError` 400, 401, 403 ou 404. Repetir não conserta um
> pedido errado, uma senha errada ou um endereço que não existe. Só vale repetir falhas
> passageiras: rede, timeout, 429, 500, 502, 503 e 504.

## 5. Testar sem internet: injeção de dependência e monkeypatch

Teste que depende da internet é teste ruim: fica lento, falha quando a API cai e não
consegue simular erros. Existem duas técnicas para isolar a rede.

**Técnica 1 — injeção de dependência.** A função **recebe** a sessão como parâmetro. No
programa real, você passa `requests.Session()`. No teste, um objeto falso (um *dublê*).

```python
def buscar_feriados(ano: int, sessao: requests.Session | None = None) -> list[str]:
    if sessao is None:
        sessao = requests.Session()
    resposta = sessao.get(URL_FERIADOS.format(ano=ano), timeout=10)
    resposta.raise_for_status()
    feriados = []
    for item in resposta.json():
        _, mes, dia = item["date"].split("-")
        feriados.append(f"{dia}/{mes} - {item['name']}")
    return feriados
```

O dublê só precisa ter os métodos que a função usa. Python não confere o tipo: se tem
`.get()`, serve (isso se chama *duck typing*: "se anda como pato...").

```python
class RespostaFalsa:
    def __init__(self, dados, status_code=200):
        self.dados = dados
        self.status_code = status_code

    def json(self):
        return self.dados

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Error")


class SessaoFalsa:
    def __init__(self, resposta):
        self.resposta = resposta
        self.chamadas = []          # o teste pode conferir o que foi pedido

    def get(self, url, **kwargs):
        self.chamadas.append((url, kwargs))
        return self.resposta


def test_formata_os_feriados():
    dados = [{"date": "2026-04-21", "name": "Tiradentes"}]
    sessao = SessaoFalsa(RespostaFalsa(dados))
    assert buscar_feriados(2026, sessao) == ["21/04 - Tiradentes"]
```

**Técnica 2 — monkeypatch.** Quando a função chama `requests.get` direto, o teste troca
`requests.get` por uma função falsa, só durante o teste. O pytest desfaz a troca no fim.

```python
def test_cidade_do_cep_com_monkeypatch(monkeypatch):
    def get_falso(url, timeout):
        assert url == "https://viacep.com.br/ws/01001000/json/"
        return RespostaFalsa({"localidade": "São Paulo", "uf": "SP"})

    monkeypatch.setattr(requests, "get", get_falso)
    assert cidade_do_cep("01001-000") == "São Paulo/SP"
```

O exemplo 03 tem as duas técnicas completas. Rode `python exemplos/03_cliente_testavel.py`:

```text
exemplos/03_cliente_testavel.py::test_formata_os_feriados PASSED         [ 20%]
exemplos/03_cliente_testavel.py::test_monta_a_url_e_usa_timeout PASSED   [ 40%]
exemplos/03_cliente_testavel.py::test_erro_http_nao_e_engolido PASSED    [ 60%]
exemplos/03_cliente_testavel.py::test_cidade_do_cep_com_monkeypatch PASSED [ 80%]
exemplos/03_cliente_testavel.py::test_cep_inexistente PASSED             [100%]

============================== 5 passed in 0.03s ===============================
```

Qual usar? Prefira **injeção**: a dependência fica visível na assinatura e o teste não
precisa saber como a função foi escrita por dentro. Use `monkeypatch` para código que
você não pode (ou não quer) mudar.

> 💡 **Dica:** com internet, experimente em casa as APIs públicas do exemplo 03, sem
> teste: `requests.get("https://viacep.com.br/ws/01001000/json/", timeout=10).json()`
> devolve um dicionário com `'localidade': 'São Paulo'` e `'uf': 'SP'`, entre outros.

## 6. Arquivos e pastas em lote (pathlib + shutil)

Você já usou `pathlib` no módulo 06. Agora o foco é **lote**: centenas de arquivos de uma
vez. No REPL do Windows:

```python
>>> from pathlib import Path
>>> arquivo = Path("C:/laboratorio/laudos") / "laudo_123456_B_2026-03-10.pdf"
>>> arquivo
WindowsPath('C:/laboratorio/laudos/laudo_123456_B_2026-03-10.pdf')
>>> print(arquivo)
C:\laboratorio\laudos\laudo_123456_B_2026-03-10.pdf
>>> arquivo.name, arquivo.stem, arquivo.suffix
('laudo_123456_B_2026-03-10.pdf', 'laudo_123456_B_2026-03-10', '.pdf')
>>> arquivo.parent.name
'laudos'
>>> arquivo.with_suffix(".xlsx").name
'laudo_123456_B_2026-03-10.xlsx'
```

(No Linux/macOS aparece `PosixPath` e as barras são `/`.)

Para listar e mover:

| O que fazer | Código |
|---|---|
| Itens da pasta (1 nível) | `pasta.iterdir()` |
| Por padrão | `pasta.glob("*.pdf")` |
| Também nas subpastas | `pasta.rglob("*.pdf")` |
| Criar pasta (e as de cima) | `pasta.mkdir(parents=True, exist_ok=True)` |
| Copiar mantendo a data | `shutil.copy2(origem, destino)` |
| Mover ou renomear | `shutil.move(origem, destino)` |
| Copiar uma árvore | `shutil.copytree(origem, destino)` |
| Compactar uma pasta | `shutil.make_archive("backup", "zip", pasta)` |
| Apagar uma árvore (cuidado!) | `shutil.rmtree(pasta)` |

> ⚠️ **Erro comum:** confiar que `shutil.move` avisa quando o destino já existe. Ele
> pode **sobrescrever** o arquivo sem perguntar (depende do sistema). Antes de mover,
> verifique `destino.exists()`.

> 🔮 **Preveja antes de rodar:** em que ordem saem estes nomes?
>
> ```python
> print(sorted(["laudo_b.pdf", "Laudo_a.pdf", "laudo_A.pdf", "10.pdf", "9.pdf"]))
> ```

<details><summary>Resposta</summary>

```text
['10.pdf', '9.pdf', 'Laudo_a.pdf', 'laudo_A.pdf', 'laudo_b.pdf']
```

`sorted` compara texto caractere por caractere pela tabela Unicode: dígitos vêm antes
de maiúsculas, que vêm antes de minúsculas. Por isso `"10"` vem antes de `"9"` (o `1` é
menor que o `9`) e `"Laudo"` antes de `"laudo"`. Para ordem "humana" de letras use
`sorted(nomes, key=str.lower)`; para números, nomeie os arquivos com zeros à esquerda
(`009`, `010`).

</details>

### Exemplo resolvido: organizar laudos por linha

**Problema:** a pasta `entrada` tem laudos como `laudo_123456_A.pdf` misturados com
outros arquivos. Quero cada laudo em `laudos/linha_A/`, `laudos/linha_B/`...

**Como pensei:**

1. O nome do arquivo tem tudo que preciso. Uma regex (módulo 05) separa OP e linha.
2. Mover arquivos é perigoso. Então separo em duas funções: `planejar` (decide, não
   mexe em nada) e `executar` (mexe, ou só mostra, conforme o modo).
3. O modo **ensaio** mostra o plano. Só depois de conferir eu rodo de verdade.
4. Nunca sobrescrevo: se o destino existe, pulo e aviso.

```python
PADRAO_LAUDO = re.compile(r"laudo_(\d{6})_([A-D])\.pdf", re.IGNORECASE)

def planejar(origem: Path, destino: Path) -> list[tuple[Path, Path]]:
    plano = []
    for arquivo in sorted(origem.iterdir()):
        achado = PADRAO_LAUDO.fullmatch(arquivo.name)
        if arquivo.is_file() and achado:
            linha = achado.group(2).upper()
            plano.append((arquivo, destino / f"linha_{linha}" / arquivo.name))
    return plano

def executar(plano: list[tuple[Path, Path]], ensaio: bool) -> None:
    for origem, destino in plano:
        if ensaio:
            print(f"   [ENSAIO] {origem.name} -> {destino.parent.name}/")
            continue
        if destino.exists():
            print(f"   [PULADO] {destino.name} já existe no destino")
            continue
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(origem, destino)
        print(f"   [MOVIDO] {origem.name} -> {destino.parent.name}/")
```

O exemplo 04 cria uma pasta temporária com arquivos de mentira e roda tudo. Saída de
`python exemplos/04_arquivos_em_lote.py`:

```text
1) Modo ensaio (nada é movido):
   [ENSAIO] LAUDO_124001_b.PDF -> linha_B/
   [ENSAIO] laudo_123456_A.pdf -> linha_A/
   [ENSAIO] laudo_123789_B.pdf -> linha_B/
   [ENSAIO] laudo_124050_D.pdf -> linha_D/
2) Agora de verdade:
   [MOVIDO] LAUDO_124001_b.PDF -> linha_B/
   [MOVIDO] laudo_123456_A.pdf -> linha_A/
   [MOVIDO] laudo_123789_B.pdf -> linha_B/
   [MOVIDO] laudo_124050_D.pdf -> linha_D/
3) Como ficou:
   entrada/anotacoes.txt
   entrada/~$relatorio.xlsx
   laudos/linha_A/laudo_123456_A.pdf
   laudos/linha_B/LAUDO_124001_b.PDF
   laudos/linha_B/laudo_123789_B.pdf
   laudos/linha_D/laudo_124050_D.pdf
```

Repare: o `~$relatorio.xlsx` ficou para trás. É o arquivo de trava que o Excel cria
enquanto uma planilha está aberta. Robôs devem ignorá-lo (exercício 05).

> 🔧 **Modifique:** no exemplo 04, mude o padrão para aceitar só linhas `A` e `B`
> (`[AB]`) e rode de novo. Quais arquivos ficam em `entrada`? Depois crie um laudo
> repetido dentro de `criar_bagunca` já no destino e veja o `[PULADO]` aparecer.

## 7. Relatórios Excel com openpyxl

No módulo 10 você exportou DataFrames com `to_excel`. Para controlar a **aparência**
(cores, larguras, filtros), usamos o `openpyxl` direto. O vocabulário:

```text
Workbook (o arquivo .xlsx)
 └── Worksheet (uma aba: wb.active, wb["Medições"], wb.create_sheet("Resumo"))
      └── Cell (uma célula: ws["A1"], ws.cell(row=1, column=1))
           ├── .value          o conteúdo
           ├── .font           Font(bold=True, color="FFFFFF")
           ├── .fill           PatternFill("solid", start_color="1F4E78")
           ├── .alignment      Alignment(horizontal="center")
           └── .number_format  "0.00", "#,##0.00", "dd/mm/yyyy"
```

O exemplo 05 monta um relatório completo em seis passos. Os pontos-chave:

```python
wb = Workbook()
ws = wb.active
ws.title = "Medições"

ws.append(CABECALHO)                         # 1) uma linha inteira por vez
for m in MEDICOES:
    ws.append([m["op"], m["linha"], m["ensaio"], m["valor"], m["min"], m["max"], status(m)])

for celula in ws[1]:                         # 2) ws[1] = a linha 1
    celula.font = Font(bold=True, color="FFFFFF")
    celula.fill = PatternFill("solid", start_color="1F4E78")

for linha in ws.iter_rows(min_row=2, min_col=4, max_col=6):
    for celula in linha:                     # 3) formato numérico
        celula.number_format = "0.00"

for indice, coluna in enumerate(ws.iter_cols(), start=1):      # 4) larguras
    maior = max(len(str(c.value)) for c in coluna if c.value is not None)
    ws.column_dimensions[get_column_letter(indice)].width = maior + 2

ws.freeze_panes = "A2"                       # 5) congela o cabeçalho
ws.auto_filter.ref = ws.dimensions           #    e liga o filtro

ws.conditional_formatting.add(               # 6) REPROVADO em vermelho
    f"G2:G{ws.max_row}",
    CellIsRule(operator="equal", formula=['"REPROVADO"'],
               font=Font(color="9C0006"),
               fill=PatternFill("solid", start_color="FFC7CE", end_color="FFC7CE")),
)
wb.save(caminho)
```

Rode `python exemplos/05_relatorio_excel.py`. Ele gera o arquivo e depois o **reabre**
para conferir (é assim que os testes dos exercícios fazem):

```text
Gerado: relatorio_medicoes.xlsx
Planilha: Medições | dimensões: A1:G6
Cabeçalho negrito? True | cor: 001F4E78
Largura da coluna C: 11.0
Congelado em: A2 | filtro: A1:G6
Regra condicional: G2:G6 equal ['"REPROVADO"']
OPs com reprovação: ['123789', '124001']
```

O arquivo fica em `exemplos/saida/relatorio_medicoes.xlsx`. Abra no Excel e teste o
filtro. Repare: a cor `1F4E78` volta como `001F4E78` (o openpyxl acrescenta o canal de
transparência na frente).

**Formatação condicional ou pintar a célula direto?** Pintar direto (`celula.fill = ...`)
é fixo. A formatação condicional é uma **regra** que o Excel reavalia: se alguém mudar
o texto para `APROVADO`, a cor some sozinha. Para relatórios que as pessoas editam,
prefira a regra.

> ⚠️ **Erro comum:** `formula=["REPROVADO"]` sem as aspas internas. O Excel entende
> `REPROVADO` como nome de uma célula ou intervalo e a regra nunca dispara. O certo é
> `formula=['"REPROVADO"']`: aspas simples do Python por fora, duplas do Excel por dentro.

> 🔮 **Preveja antes de rodar:** quanto vale `ws.max_row` em cada `print`?
>
> ```python
> from openpyxl import Workbook
>
> ws = Workbook().active
> ws.append(["OP", "Valor"])
> ws.append(["123456", 20.4])
> print(ws.max_row)
> ws.cell(row=10, column=1)
> print(ws.max_row, ws.dimensions)
> ```

<details><summary>Resposta</summary>

```text
2
10 A1:B10
```

Só **olhar** uma célula com `ws.cell(...)` (ou `ws["A10"]`) já a cria, vazia. Com isso
a planilha "cresce" e o `max_row` passa a ser 10. Cuidado ao usar `ws.max_row` para
saber onde estão os dados: acesse células só onde precisa escrever.

</details>

**Lendo uma planilha existente:**

```python
from openpyxl import load_workbook

wb = load_workbook("resultados.xlsx", data_only=True)   # data_only: valor, não a fórmula
ws = wb["Linha A"]
for op, espessura, cof in ws.iter_rows(min_row=2, max_col=3, values_only=True):
    print(op, espessura, cof)
```

> 💡 **Dica:** para análise (filtros, médias, groupby), leia com pandas (módulo 10).
> Para escrever com estilo, use openpyxl. Dá para juntar: `df.to_excel(...)` e depois
> `load_workbook` para formatar.

> 🔧 **Modifique:** no exemplo 05, acrescente uma segunda regra condicional que pinte
> `APROVADO` de verde (`fill` `C6EFCE`, fonte `006100`). Depois crie uma aba "Resumo"
> com `wb.create_sheet("Resumo")` e escreva nela quantas medições foram reprovadas.

## 8. E-mail: montar, salvar e ler mensagens

Um e-mail é um **arquivo de texto** com cabeçalhos (`From`, `To`, `Subject`, `Date`...) e
um corpo, que pode ter várias partes (texto, HTML, anexos). O formato se chama MIME, e a
biblioteca padrão do Python sabe montar e ler.

### Montar (sem enviar)

```python
from email.message import EmailMessage

msg = EmailMessage()
msg["From"] = "Laboratório de Qualidade <laboratorio@embalagens.example>"
msg["To"] = "Expedição <expedicao@embalagens.example>"
msg["Subject"] = f"Certificado de qualidade - OP {op} / NF {nf}"
msg.set_content(f"Olá,\n\nSegue o certificado de qualidade da OP {op} (NF {nf}).\n")
msg.add_attachment(pdf.read_bytes(), maintype="application", subtype="pdf",
                   filename=pdf.name)
caminho_eml.write_bytes(bytes(msg))     # salva no formato padrão .eml
```

O exemplo 06 faz isso (com uma versão HTML opcional) e mostra a estrutura. Saída de
`python exemplos/06_email_montar.py`:

```text
Assunto: Certificado de qualidade - OP 123456 / NF 98765
Para: Expedição <expedicao@embalagens.example>
Estrutura da mensagem:
   multipart/mixed
   multipart/alternative
   text/plain
   text/html
   application/pdf certificado_123456.pdf
Primeira linha do texto: Olá,
Anexos: ['certificado_123456.pdf']
Salvo em: certificado_123456.eml
```

Dê dois cliques no `.eml` gerado em `exemplos/saida/`: o Outlook abre a mensagem pronta.
Esse é um ótimo **modo ensaio** para e-mails: o robô monta, uma pessoa confere.

> 🔮 **Preveja antes de rodar:** o que acontece na segunda atribuição?
>
> ```python
> from email.message import EmailMessage
>
> msg = EmailMessage()
> msg["Subject"] = "Certificado OP 123456"
> msg["Subject"] = "Certificado OP 999999"
> ```

<details><summary>Resposta</summary>

```text
ValueError: There may be at most 1 Subject headers in a message
```

Cabeçalhos de e-mail **não** funcionam como um dicionário comum: atribuir de novo
acrescentaria um segundo `Subject`, e o `EmailMessage` recusa. Para trocar, apague antes:
`del msg["Subject"]` e depois atribua.

</details>

### Enviar: smtplib (conceito)

Enviar depende de um servidor SMTP liberado pela TI. O código tem esta forma:

```python
import os
import smtplib

with smtplib.SMTP("smtp.empresa.example", 587, timeout=30) as smtp:
    smtp.starttls()                                   # conexão criptografada
    smtp.login(os.environ["SMTP_USUARIO"], os.environ["SMTP_SENHA"])
    smtp.send_message(msg)
```

Em empresas com Microsoft 365 é comum o envio por usuário e senha estar **bloqueado**
por segurança. Não tente contornar: converse com a TI (as saídas oficiais são o
Microsoft Graph, a seção 9, ou um servidor de envio interno).

O mesmo vale para **ler** por IMAP (`imaplib`): no Microsoft 365 o acesso exige OAuth
(login moderno), não só senha. Na prática, para ler o Outlook corporativo, veja a
próxima seção.

### Ler arquivos .eml

Um `.eml` salvo vira bytes, e os bytes viram uma mensagem:

```python
from email import policy
from email.parser import BytesParser

msg = BytesParser(policy=policy.default).parsebytes(caminho.read_bytes())
corpo = msg.get_body(preferencelist=("plain", "html"))   # prefere texto puro
texto = corpo.get_content()
```

Use **sempre** `policy=policy.default`: ela decodifica os acentos dos cabeçalhos
(`=?utf-8?q?Expedi=C3=A7=C3=A3o?=` vira `Expedição`) e oferece `get_body` e
`get_content`. Sem ela, você cai na API antiga, bem mais trabalhosa.

### Exemplo resolvido: de onde vem cada pedido?

**Problema:** na pasta `dados/emails/` há 5 pedidos da expedição. Quero ver, para cada
um, o remetente, a data, o assunto e a OP.

**Como pensei:**

1. Ler cada `.eml` com `BytesParser` (acima).
2. O remetente vem como `Nome <endereco>`. `email.utils.parseaddr` separa as partes.
3. A data vem como texto (`Mon, 09 Mar 2026 08:12:00 -0300`).
   `email.utils.parsedate_to_datetime` devolve um `datetime` (módulo 07).
4. Alguns e-mails só têm HTML (`OP: <b>124001</b>`). Minha regex aceita um `<b>`
   opcional, só para este exemplo; no exercício 11 você vai remover as tags.

```python
for caminho in sorted(PASTA_EMAILS.glob("*.eml")):
    msg = ler_eml(caminho)
    nome, endereco = parseaddr(msg["From"])
    quando = parsedate_to_datetime(msg["Date"])
    corpo = msg.get_body(preferencelist=("plain", "html"))
    texto = corpo.get_content()
    op = re.search(r"OP:?\s*(?:<b>)?(\d{6})", texto)
    print(caminho.name)
    print("   de:", endereco, "| em:", quando.strftime("%d/%m/%Y %H:%M"))
    print("   assunto:", msg["Subject"])
    print("   corpo:", corpo.get_content_type(), "| OP:", op.group(1) if op else "?")
```

Saída de `python exemplos/07_email_ler.py` (os dois primeiros e o terceiro, só HTML):

```text
pedido_001.eml
   de: expedicao@embalagens.example | em: 09/03/2026 08:12
   assunto: Pedido de certificado - OP 123456
   corpo: text/plain | OP: 123456
pedido_002.eml
   de: expedicao@embalagens.example | em: 09/03/2026 09:40
   assunto: Certificado urgente — OP 123789
   corpo: text/plain | OP: 123789
pedido_003.eml
   de: expedicao@embalagens.example | em: 09/03/2026 10:05
   assunto: Pedido de certificado - OP 124001
   corpo: text/html | OP: 124001
```

O `pedido_002` tem texto **e** HTML (`multipart/alternative`); o `get_body` escolheu o
texto puro, como pedimos.

## 9. Outlook no Windows: clássico, novo e Microsoft Graph

Na empresa, os pedidos chegam no Outlook, não numa pasta de `.eml`. Existem dois
"Outlooks" no Windows hoje, e isso muda tudo:

| | Outlook clássico | Novo Outlook |
|---|---|---|
| Como reconhecer | Faz parte do Office; tem menu **Arquivo > Opções** | App novo, parecido com o Outlook na web |
| Automação local (COM/`win32com`) | **Sim** | **Não** |
| Macros VBA | Sim | Não |
| Caminho para Python | `win32com` (só Windows) | Microsoft Graph ou Power Automate |

**Outlook clássico com `win32com`.** O pacote `pywin32` (`pip install pywin32`) deixa o
Python "pilotar" o Outlook aberto na sua máquina. O exemplo 08 lê a caixa de entrada:

```python
import win32com.client

outlook = win32com.client.Dispatch("Outlook.Application")
caixa = outlook.GetNamespace("MAPI").GetDefaultFolder(6)   # 6 = Caixa de Entrada
itens = caixa.Items
itens.Sort("[ReceivedTime]", True)                          # mais recentes primeiro
for msg in itens.Restrict("[ReceivedTime] >= '09/03/2026 00:00'"):
    if msg.Class == 43 and "certificado" in msg.Subject.lower():   # 43 = e-mail
        print(msg.ReceivedTime, msg.Subject)
        print(msg.Body[:200])                                       # texto puro
```

Outras ações úteis: `anexo.SaveAsFile(caminho)` para cada item de `msg.Attachments`,
`msg.Move(pasta)` para arquivar e, para responder, `novo = outlook.CreateItem(0)`
seguido de `novo.Display()`. O `Display()` **abre a janela** com o e-mail pronto para
você conferir e clicar em Enviar: é o modo ensaio do Outlook. `novo.Send()` envia direto.

> ⚠️ **Erro comum:** `msg.SenderEmailAddress` de um colega da mesma empresa às vezes
> volta como `/O=EXCHANGELABS/OU=...` em vez do e-mail. Para remetentes internos use
> `msg.Sender.GetExchangeUser().PrimarySmtpAddress`.

O exemplo 08 só funciona no Windows com o Outlook clássico. Em outros casos ele explica
isso e termina.

**Novo Outlook: Microsoft Graph.** O Graph é a API oficial da Microsoft para e-mail,
calendário, OneDrive e Teams. É HTTP + JSON, exatamente o que você aprendeu nas seções
2 a 4. A parte difícil não é o código, é a **permissão**: a TI precisa registrar um
aplicativo no Microsoft Entra ID e liberar a permissão `Mail.Read`. Com isso, o login é
feito pela biblioteca `msal`, que entrega um token. A chamada em si tem esta cara
(conceito, não roda sem essa configuração):

```python
resposta = requests.get(
    "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages",
    headers={"Authorization": f"Bearer {token}"},
    params={"$select": "subject,from,receivedDateTime,body", "$top": 25,
            "$orderby": "receivedDateTime desc"},
    timeout=30,
)
resposta.raise_for_status()
for mensagem in resposta.json()["value"]:
    print(mensagem["receivedDateTime"], mensagem["subject"])
```

**Sem TI disponível? Power Automate.** Um fluxo de nuvem "Quando um novo email chegar"
pode filtrar pelo assunto e salvar a mensagem (há ação para exportar no formato `.eml`)
numa pasta do OneDrive ou SharePoint. O OneDrive sincroniza a pasta no seu computador e
o Python lê os `.eml`, como na seção 8. Simples e sem `win32com`.

> 💡 **Dica:** separe **de onde vem** o e-mail de **o que fazer** com ele. Escreva o
> processamento recebendo bytes de `.eml` (exercícios 11 e 14). Hoje os bytes vêm de uma
> pasta; amanhã, do Graph. O resto do programa não muda.

## 10. Agendamento: o Agendador de Tarefas do Windows

Um robô que você precisa lembrar de rodar não é um robô. O Windows já tem um agendador.

**Passo 1 — um lançador `.bat`.** O exemplo `exemplos/11_rodar_robo.bat` mostra o modelo:

```text
@echo off
set PASTA=C:\robos\curso-python
set SCRIPT=12-automacao-e-integracao\exemplos\09_robo_certificados.py
cd /d "%PASTA%"
if not exist logs mkdir logs
".venv\Scripts\python.exe" "%SCRIPT%" >> "logs\agendador.log" 2>&1
exit /b %ERRORLEVEL%
```

Três detalhes que evitam 90% dos problemas:

1. `cd /d` entra na pasta do projeto. O Agendador começa em `C:\Windows\System32`, e
   caminhos relativos como `dados\ops.csv` quebrariam.
2. Chama o `python.exe` **do venv** direto. Não precisa "ativar" nada.
3. `>> logs\agendador.log 2>&1` guarda tudo que o script imprimiria, inclusive erros.

**Passo 2 — criar a tarefa.** Pelo menu Iniciar, abra "Agendador de Tarefas":

1. **Criar Tarefa...** (a versão completa, não a "Básica").
2. Aba **Geral**: nome `Robo Certificados`. Se o robô abre o navegador visível, marque
   "Executar somente quando o usuário estiver conectado".
3. Aba **Disparadores**: Novo > Semanalmente, de segunda a sexta, 07:30.
4. Aba **Ações**: Novo > Iniciar um programa > o caminho do `.bat`. Em "Iniciar em",
   a pasta do projeto.
5. Aba **Configurações**: "Interromper a tarefa se for executada por mais de" 1 hora.

Ou, no PowerShell, a mesma tarefa em uma linha (e comandos para testar e remover):

```text
schtasks /Create /TN "Robo Certificados" /TR "C:\robos\curso-python\12-automacao-e-integracao\exemplos\11_rodar_robo.bat" /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST 07:30
schtasks /Run /TN "Robo Certificados"
schtasks /Query /TN "Robo Certificados" /V /FO LIST
schtasks /Delete /TN "Robo Certificados" /F
```

Na coluna "Resultado da Última Execução", `0x0` é sucesso e `0x1` significa que o
script terminou com `sys.exit(1)`. Por isso nossos scripts devolvem 1 quando algo falha:
o Agendador (e você) ficam sabendo.

No Linux/macOS o equivalente é o `cron`:
`30 7 * * 1-5 cd /home/voce/curso-python && .venv/bin/python script.py >> logs/cron.log 2>&1`.

## 11. Automação web com Playwright

O **Playwright** controla um navegador de verdade: abre páginas, preenche campos, clica,
espera e tira prints. A Microsoft mantém o projeto, e ele funciona muito bem com o Edge.

Por que Playwright e não "gravar cliques na tela" (como o `pyautogui`)? Porque ele
encontra os elementos **pelo significado** (o campo chamado "OP", o botão "Confirmar"),
não pela posição do mouse. Se a janela mudar de tamanho, o robô continua funcionando.

### Instalação (uma vez)

Com o ambiente virtual ativado:

```text
pip install playwright
```

Pronto. Não é preciso baixar navegador: usamos o **Microsoft Edge já instalado** no
Windows, com `channel="msedge"`. (Em Linux/macOS sem Edge, rode
`python -m playwright install chromium` e lance sem o `channel`.)

### O primeiro robô

O simulador `dados/simulador_certificados.html` é uma página de **treino** que imita a
tela de emissão de um ERP (OP, NF, peso, linha, observação, Confirmar e Cancelar). Ela
até demora um pouco para responder, como um sistema real.

```python
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

pagina_treino = Path("12-automacao-e-integracao/dados/simulador_certificados.html")

with sync_playwright() as p:
    navegador = p.chromium.launch(channel="msedge", headless=False, slow_mo=300)
    page = navegador.new_page()
    page.goto(pagina_treino.resolve().as_uri())

    page.get_by_label("OP", exact=True).fill("123456")
    page.get_by_label("NF", exact=True).fill("98765")
    page.get_by_label("Peso (kg)").fill("1.250,50")
    page.get_by_label("Linha").select_option("B")
    page.screenshot(path="preenchido.png")

    page.get_by_role("button", name="Cancelar").click()   # ensaio: NÃO confirma
    expect(page.get_by_role("status")).to_have_text("Operação cancelada")
    navegador.close()
```

As peças:

- `sync_playwright()` liga o Playwright; o `with` desliga no fim.
- `p.chromium.launch(channel="msedge", ...)`: o Edge é um navegador da família Chromium.
  `headless=False` mostra a janela; `slow_mo=300` desacelera cada ação em 300 ms para
  você acompanhar com os olhos.
- `page` é a aba. `goto` abre o endereço (`as_uri()` transforma o caminho do arquivo em
  `file:///C:/...`).
- `get_by_label(...)` encontra o campo pelo **rótulo** visível; `fill` digita.
- `expect(...).to_have_text(...)` **espera** até a mensagem aparecer (ou falha depois
  do tempo limite).

### Seletores: como o robô acha as coisas

Use os localizadores na ordem desta tabela. Os de cima imitam como uma **pessoa** acha
o elemento e sobrevivem a mudanças no visual da página:

| Prioridade | Localizador | Quando usar |
|---|---|---|
| 1 | `page.get_by_role("button", name="Confirmar")` | botões, links, caixas, abas |
| 2 | `page.get_by_label("Peso (kg)")` | campos com rótulo |
| 3 | `page.get_by_placeholder("Digite a OP")` | campos sem rótulo, com texto de dica |
| 4 | `page.get_by_text("Certificado gerado")` | textos na tela |
| 5 | `page.locator("#peso")` (CSS) | quando nada acima funciona |
| 6 | XPath (`page.locator("xpath=//div[3]/input")`) | evite: quebra fácil |

`exact=True` exige o texto inteiro (sem ele, `get_by_label("OP")` também acharia um
rótulo "OP de origem"). Para descobrir os nomes, aperte **F12** no Edge e inspecione o
elemento, ou deixe o Playwright gravar por você:

```text
python -m playwright codegen --channel msedge https://endereco-da-tela
```

O **codegen** abre o Edge e uma janela que vai escrevendo o código Python enquanto você
clica. Use como ponto de partida, nunca como código final.

> 🔮 **Preveja antes de rodar:** a tela tem os botões "Confirmar" e "Cancelar". O que
> acontece com esta linha?
>
> ```python
> page.get_by_role("button").click()
> ```

<details><summary>Resposta</summary>

O Playwright recusa e levanta um erro (texto real):

```text
Error: Locator.click: Error: strict mode violation: get_by_role("button") resolved to 2 elements:
    1) <button type="button" id="confirmar">Confirmar</button> aka get_by_role("button", name="Confirmar")
    2) <button type="button" id="cancelar">Cancelar</button> aka get_by_role("button", name="Cancelar")
```

É o **modo estrito**: uma ação nunca "chuta" entre vários elementos. Ótimo para um robô
que emite certificados! A mensagem ainda sugere o seletor certo para cada um.

</details>

### Esperas: nunca `time.sleep`

A maior fonte de robôs instáveis é esperar "no chute". O Playwright tem esperas embutidas:

- **Toda ação espera sozinha.** `click()` aguarda o botão existir, estar visível,
  habilitado e parado. `fill()` aguarda o campo aceitar texto.
- **`expect(...)` espera uma condição** e tenta de novo até o limite:
  `to_be_visible()`, `to_have_text(...)`, `to_contain_text(...)`, `to_have_value(...)`,
  `to_be_empty()`. Aceita regex: `to_have_text(re.compile(r"Certificado \d+|Erro"))`.
- **Navegação:** `page.wait_for_url("**/certificados/**")` espera o endereço mudar.
- **Tempo limite padrão:** `page.set_default_timeout(10_000)` (10 s). Para um passo
  lento, `timeout=30_000` só nele.

```text
time.sleep(5)  ->  rápido demais num dia lento, lento demais num dia normal
expect(...)    ->  espera exatamente o necessário, e falha com mensagem clara
```

### Prints, trace e outros recursos

- `page.screenshot(path="tela.png", full_page=True)`: a página inteira.
- `page.get_by_role("table").screenshot(path="tabela.png")`: só um elemento.
- **Trace**: grava tudo (prints, cliques, rede) num `.zip` que você "assiste" depois.
  `contexto.tracing.start(screenshots=True, snapshots=True)` no início,
  `contexto.tracing.stop(path="trace.zip")` no fim, e
  `python -m playwright show-trace trace.zip` para ver.
- Elementos dentro de **iframe**: `page.frame_locator("iframe").get_by_label("OP")`.
- **Janelas de confirmação** do navegador (`alert`/`confirm`):
  `page.on("dialog", lambda dialogo: dialogo.accept())`.
- **Login guardado**: `p.chromium.launch_persistent_context("perfil_robo",
  channel="msedge", headless=False)` usa uma pasta de perfil própria e mantém cookies
  entre execuções (útil com login único da empresa).

### E o Protheus?

O TOTVS Protheus roda no navegador pelo **WebApp**. Do ponto de vista do robô, é uma
página web como o simulador, com algumas particularidades:

- **Telas antes da rotina:** programa inicial e ambiente, login, empresa/filial, data
  base e só então o menu. Cada uma é um passo do robô, com um `expect` confirmando que
  a tela certa abriu.
- **Componentes próprios:** a tela é desenhada com componentes web da TOTVS, muitas
  vezes dentro de *shadow DOM* (uma "subpágina" encapsulada). Os localizadores
  `get_by_role`, `get_by_label`, `get_by_text` e CSS do Playwright atravessam shadow
  DOM aberto; XPath não atravessa. Mais um motivo para fugir do XPath.
- **Lentidão variável:** use `expect` com tempo limite generoso nos passos que dependem
  do servidor, e confira a mensagem de retorno de cada operação.
- **Ambiente de teste:** peça à TI um ambiente de homologação (cópia do Protheus para
  testes). O robô aprende lá; em produção, só depois de muitos ensaios.
- **Credenciais:** usuário e senha do robô ficam em variáveis de ambiente
  (`os.environ["PROTHEUS_USUARIO"]`), nunca no código ou no Git. Combine com a TI se o
  robô terá um usuário próprio, com só as permissões necessárias.

O caminho é: treinar no simulador, gravar o fluxo real com `codegen` no ambiente de
teste, trocar os seletores gravados por `get_by_role`/`get_by_label`, e só então
encaixar no esqueleto do robô da próxima seção.

## 12. O robô de certificados: modo ensaio, log, prints e idempotência

Um robô de verdade não é só "preencher e clicar". Ele precisa de cinco proteções:

```text
 pedidos ──> [validar dados] ──> [já emitido?] ──> [plano de ações] ──> [executar na tela]
                  │ inválido          │ sim               │                  │
                  v                   v                   │ ensaio:          │ falhou:
             log + pendência     log + pula               │ Cancelar         │ print + log
                                                          v                  v
                                                    registro (CSV) <── emitido: anota
```

1. **Modo ensaio por padrão:** faz tudo, menos o passo irreversível. Emitir de verdade
   exige pedir explicitamente (`--confirmar`).
2. **Log em arquivo:** o robô roda sozinho às 7h; o log é o único jeito de saber o que
   aconteceu. Use `logging`, não `print` (módulo 09).
3. **Prints de tela:** um antes de confirmar e um em cada erro. Evidência para você e
   para a auditoria da qualidade.
4. **Idempotência:** antes de agir, pergunte a um registro se aquilo já foi feito.
   Depois de agir, anote **na hora**. Rodar de novo não duplica nada.
5. **Falhas isoladas:** um pedido com problema vira log + print e o robô segue para o
   próximo. No fim, o código de saída diz se houve falha.

### Exemplo resolvido: separar o plano da execução

**Problema:** quero testar a lógica do robô sem abrir o navegador.

**Como pensei:** a parte que **decide** (o que preencher, em que ordem, se confirma ou
cancela) não precisa da tela. Então escrevo uma função que devolve o plano como dados:

```python
def planejar(pedido: dict, ensaio: bool) -> list[tuple[str, str, str]]:
    return [
        ("preencher", "OP", pedido["op"]),
        ("preencher", "NF", pedido["nf"]),
        ("preencher", "Peso (kg)", formatar_peso(pedido["peso_kg"])),
        ("selecionar", "Linha", pedido["linha"]),
        ("print", f"antes_de_confirmar_{pedido['op']}", ""),
        ("clicar", "Cancelar" if ensaio else "Confirmar", ""),
    ]
```

E uma função **burra** que executa qualquer plano, com uma linha por tipo de ação:

```python
def executar(page, acoes, pasta_prints):
    for acao, alvo, valor in acoes:
        if acao == "preencher":
            page.get_by_label(alvo, exact=True).fill(valor)
        elif acao == "selecionar":
            page.get_by_label(alvo, exact=True).select_option(valor)
        elif acao == "clicar":
            page.get_by_role("button", name=alvo, exact=True).click()
        elif acao == "print":
            page.screenshot(path=pasta_prints / f"{alvo}.png")
```

Agora o teste mais importante do robô ("em ensaio, nunca clica em Confirmar") roda em
milissegundos, sem navegador. O exercício 12 é exatamente isso, com o código de um
colega cheio de defeitos para você encontrar.

### O robô completo

O `exemplos/09_robo_certificados.py` junta tudo: validação antes da tela, registro
`emitidos.csv`, log diário, pasta de prints por execução, `try/except` por pedido e
`expect` esperando sucesso **ou** erro da tela. Ele tem um pedido com OP errada de
propósito. Rode no Windows (depois do `pip install playwright`):

```text
python 12-automacao-e-integracao/exemplos/09_robo_certificados.py
```

O Edge abre, preenche cada pedido e cancela. No terminal (os horários variam):

```text
02:44:20 INFO    Início. Modo: ENSAIO
02:44:29 INFO    [ENSAIO] OP 123456 preenchida e cancelada
02:44:29 INFO    [ENSAIO] OP 123789 preenchida e cancelada
02:44:29 ERROR   OP 12400 com dados inválidos: OP inválida: '12400'
02:44:29 INFO    [ENSAIO] OP 124050 preenchida e cancelada
02:44:29 INFO    Fim. {'emitidos': 0, 'ensaiados': 3, 'pulados': 0, 'falhas': 1}
```

Com `--confirmar`, ele emite no simulador e anota no registro. Rodando **de novo**:

```text
02:44:42 INFO    Início. Modo: CONFIRMAR
02:44:43 INFO    OP 123456 / NF 98765 já emitida antes: pulando
02:44:43 INFO    OP 123789 / NF 98766 já emitida antes: pulando
02:44:43 ERROR   OP 12400 com dados inválidos: OP inválida: '12400'
02:44:43 INFO    OP 124050 / NF 98771 já emitida antes: pulando
02:44:43 INFO    Fim. {'emitidos': 0, 'ensaiados': 0, 'pulados': 3, 'falhas': 1}
```

Isso é idempotência na prática. Os prints ficam em `exemplos/saida/robo/prints_.../`.
Se o Playwright não estiver instalado, o script só explica como instalar e termina.

> 🔧 **Modifique:** no robô, troque a NF do segundo pedido por `"98x66"` e rode com
> `--confirmar --headless`. A tela recusa ("Erro: NF inválida"); veja no log o traceback,
> o print `123789_ERRO.png` e o robô seguindo para o próximo pedido. Depois acrescente a
> validação da NF em `problemas_do_pedido`, para o erro ser pego **antes** da tela.

O exemplo 10 mostra a mesma ideia de idempotência sem navegador, usando o `Message-ID`
de cada e-mail. Saída de `python exemplos/10_log_e_idempotencia.py`:

```text
--- 1ª rodada ---
INFO  Novo pedido: pedido_001.eml | Pedido de certificado - OP 123456
INFO  Novo pedido: pedido_002.eml | Certificado urgente — OP 123789
INFO  Novo pedido: pedido_003.eml | Pedido de certificado - OP 124001
INFO  Novo pedido: pedido_004.eml | Pedido de certificado - OP 124050
INFO  Novo pedido: pedido_005.eml | Pedido de certificado - OP 125310
novos: 5
--- 2ª rodada (nada mudou na pasta) ---
DEBUG pedido_001.eml já processado, pulando
DEBUG pedido_002.eml já processado, pulando
DEBUG pedido_003.eml já processado, pulando
DEBUG pedido_004.eml já processado, pulando
DEBUG pedido_005.eml já processado, pulando
novos: 0
--- o arquivo de log tem 10 linhas; a primeira é: ---
INFO  Novo pedido: pedido_001.eml | Pedido de certificado - OP 123456
```

Repare no `salvar_vistos`: ele grava num arquivo temporário e depois **troca** pelo
definitivo (`temporario.replace(caminho)`). Se o computador desligar no meio, o
registro antigo continua inteiro. Robôs gostam de arquivos que nunca ficam pela metade.

## Lendo mensagens de erro deste módulo

**Não conectou:**

```text
requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=8766):
Max retries exceeded with url: /tolerancias (Caused by NewConnectionError(...
Failed to establish a new connection: [Errno 111] Connection refused"))
```

Ninguém atendeu no endereço. No Windows aparece `[WinError 10061]`. Confira o endereço e
a porta, se o servidor está no ar e se a VPN está ligada. Com `NameResolutionError`, o
nome do servidor nem foi encontrado (erro de digitação ou rede interna fora do ar).

**Demorou demais:**

```text
requests.exceptions.ReadTimeout: HTTPConnectionPool(host='127.0.0.1', port=8765):
Read timed out. (read timeout=0.5)
```

Conectou, mas a resposta não veio a tempo. Aumente o `timeout` se a API é lenta mesmo,
ou trate com novas tentativas (seção 4).

**O servidor respondeu com erro:**

```text
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: http://127.0.0.1:8765/x
```

Veio do `raise_for_status()`. Leia o número: 4xx é pedido seu errado (endereço,
parâmetro, login); 5xx é problema do lado de lá. `erro.response.text` costuma explicar.

**Não era JSON:**

```text
requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

Você chamou `.json()` e veio HTML ou texto. Clássico: a API redirecionou para uma página
de login, ou devolveu uma página de erro. Imprima `resposta.status_code` e
`resposta.text[:300]` antes de qualquer coisa.

**Certificado SSL (rede corporativa):** `SSLError ... certificate verify failed: unable
to get local issuer certificate`. O proxy da empresa usa um certificado próprio. Peça à
TI o arquivo da autoridade certificadora e use `verify="caminho/empresa.pem"`. Nunca
"resolva" com `verify=False` em produção: isso desliga a segurança da conexão.

**Planilha aberta no Excel:** `PermissionError: [Errno 13] Permission denied:
'relatorio.xlsx'`. No Windows, o Excel trava o arquivo aberto. Feche a planilha ou salve
com outro nome (exercício 06).

**Formato antigo:** `InvalidFileException: openpyxl does not support the old .xls file
format, please use xlrd to read this file, or convert it to the more recent .xlsx file
format.` Abra no Excel e salve como `.xlsx`.

**Edge não encontrado:**

```text
Error: BrowserType.launch: Chromium distribution 'msedge' is not found at /opt/microsoft/msedge/msedge
Run "playwright install msedge"
```

Este texto veio de um Linux sem Edge. No Windows, verifique se o Edge está instalado;
em último caso rode `python -m playwright install msedge` (pede administrador) ou use
`python -m playwright install chromium` e lance sem `channel`.

**Elemento não apareceu:**

```text
playwright._impl._errors.TimeoutError: Locator.click: Timeout 3000ms exceeded.
Call log:
  - waiting for get_by_role("button", name="Gravar")
```

O robô esperou um botão "Gravar" que não existe (o nome real é "Confirmar") ou que ainda
não apareceu. O *call log* mostra exatamente qual seletor falhou. Confira o nome no F12
ou no `codegen`.

**A tela mostrou outra coisa:**

```text
AssertionError: Locator expected to have text 'Certificado'
Actual value:
Call log:
  - Expect "to_have_text" get_by_role("status") with timeout 2000ms
```

Veio de um `expect`. O "Actual value" mostra o que estava na tela. Aqui, nada: o robô
não chegou a clicar em Confirmar.

**Outlook:** `pywintypes.com_error: (-2147221005, 'Invalid class string', None, None)`
(em português a mensagem vem traduzida). O Windows não encontrou o Outlook clássico:
não está instalado ou a máquina só tem o Novo Outlook (seção 9).

## Boas práticas

- **API > arquivo > tela.** Robô de tela é o último recurso, não o primeiro.
- **Timeout em toda chamada HTTP** e `raise_for_status()` logo depois.
- **Segredos fora do código:** tokens e senhas em variáveis de ambiente. Nada de senha
  no Git, no log ou no print de tela.
- **Funções puras no núcleo** (planejar, validar, formatar) e efeitos colaterais (rede,
  disco, tela) nas bordas. O núcleo se testa sem internet e sem navegador.
- **Injete dependências** (sessão, função de emitir, função de dormir) para testar.
- **Modo ensaio como padrão** em qualquer coisa que mova, apague, envie ou emita.
- **Nunca sobrescreva** evidências: confira `exists()` ou gere um nome novo.
- **Idempotência:** registre o que foi feito e consulte antes de agir.
- **Log em arquivo** com data e hora, e código de saída 0/1 para o Agendador.
- **Caminhos a partir do script** (`Path(__file__).resolve().parent`), não da pasta
  atual.
- **Seletores por papel e rótulo** no Playwright; `expect` em vez de `sleep`.
- **Comece pequeno:** um pedido, em ensaio, com você olhando. Depois dez. Depois o dia.

## No mundo real

Uma rotina realista no laboratório, juntando as peças deste módulo:

```text
07:25  Power Automate salva os e-mails "Pedido de certificado" como .eml na pasta
       OneDrive\Robo\entrada (sincronizada no PC do laboratório).
07:30  O Agendador roda rodar_robo.bat:
         1. lê os .eml novos (Message-ID ainda não visto);
         2. extrai OP, NF e peso; e-mail incompleto vira pendência;
         3. confere a OP no banco de regras (módulo 11) e escolhe a especificação;
         4. robô Playwright no Edge: preenche a tela de certificados, tira print,
            CONFIRMA (este passo só foi ligado depois de 2 semanas de ensaio);
         5. anota cada emissão no registro (idempotência);
         6. gera fila_AAAA-MM-DD.xlsx com abas Fila e Pendências;
         7. monta o e-mail-resumo com a planilha e abre no Outlook (Display) para
            o analista conferir e enviar.
07:45  O analista lê o resumo, resolve as 2 pendências na mão e envia.
```

O ganho não é só tempo. É **rastreabilidade**: para cada certificado existe log, print
da tela antes da confirmação e registro de quando foi emitido. Numa auditoria de
cliente, isso vale ouro.

Repare também no que **não** é automático: o envio do e-mail e as pendências. Bons
robôs deixam com as pessoas as decisões que pedem julgamento.

O desafio deste módulo é construir as etapas 1, 2, 3, 5, 6 e 7 (com um emissor
simulado no lugar da tela).

## Resumo

| Assunto | Essencial |
|---|---|
| GET com parâmetros | `requests.get(url, params={...}, timeout=10)` |
| POST com JSON | `requests.post(url, json=dados, timeout=10)` |
| Conferir status | `resposta.raise_for_status()`; `resposta.status_code`; `resposta.ok` |
| Corpo | `resposta.json()`, `resposta.text`, `resposta.headers["Content-Type"]` |
| Sessão | `with requests.Session() as s: s.headers.update({...})` |
| Exceções | `RequestException` > `ConnectionError`, `Timeout`, `HTTPError` |
| Testar sem rede | receber `sessao` por parâmetro; `monkeypatch.setattr(requests, "get", falso)` |
| Arquivos em lote | `iterdir`, `glob`, `rglob`, `mkdir(parents=True, exist_ok=True)` |
| Mover/copiar | `shutil.move`, `shutil.copy2` (confira `exists()` antes) |
| Excel | `Workbook`, `ws.append`, `Font`, `PatternFill`, `number_format`, `column_dimensions[...].width` |
| Excel (extras) | `freeze_panes = "A2"`, `auto_filter.ref`, `conditional_formatting.add(..., CellIsRule(...))` |
| Montar e-mail | `EmailMessage()`, `msg["Subject"]`, `set_content`, `add_attachment`, `bytes(msg)` |
| Ler .eml | `BytesParser(policy=policy.default).parsebytes(b)`, `get_body(preferencelist=...)` |
| Outlook clássico | `win32com.client.Dispatch("Outlook.Application")` (só Windows) |
| Novo Outlook | Microsoft Graph (TI registra o app) ou Power Automate salvando `.eml` |
| Agendar | `.bat` com `cd /d` + `python.exe` do venv; `schtasks /Create ...` |
| Playwright | `sync_playwright()`, `p.chromium.launch(channel="msedge", headless=False)` |
| Localizar | `get_by_role(..., name=...)`, `get_by_label(...)`, `exact=True` |
| Esperar | ações esperam sozinhas; `expect(loc).to_have_text(...)`; sem `sleep` |
| Evidências | `page.screenshot(path=...)`, trace, `logging` em arquivo |
| Robô seguro | ensaio por padrão, validação antes da tela, registro idempotente, falha isolada |

## Você domina este módulo se...

- [ ] Explico sem consultar o que são método, status, cabeçalho e corpo numa requisição
      HTTP, e o que significam 200, 201, 404, 422 e 503.
- [ ] Escrevo uma chamada `requests` com `params`, `timeout` e `raise_for_status()` e
      sei qual exceção aparece quando a rede cai, quando demora e quando dá 404.
- [ ] Testo uma função que usa a rede sem internet, com um dublê injetado ou
      `monkeypatch`.
- [ ] Organizo uma pasta de arquivos em lote com modo ensaio e sem sobrescrever nada.
- [ ] Gero uma planilha com cabeçalho estilizado, filtro e formatação condicional, e
      confiro o resultado reabrindo com `load_workbook`.
- [ ] Monto um e-mail com anexo, salvo como `.eml` e leio de volta OP, NF e peso.
- [ ] Sei explicar por que o `win32com` não funciona no Novo Outlook e quais são as
      alternativas.
- [ ] Escrevo um robô Playwright que usa `get_by_role`/`get_by_label`, espera com
      `expect`, tira prints, roda em ensaio por padrão e não emite nada em dobro.

## Exercícios

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_classificar_status` | ★☆☆ | famílias de status HTTP, quando repetir |
| 02 | `ex02_montar_url` | ★☆☆ | juntar URL sem barra dupla, `urlencode` |
| 03 | `ex03_buscar_tolerancias` | ★★☆ | `requests` com sessão injetada, `timeout`, `raise_for_status` |
| 04 | `ex04_com_retentativas` | ★★★ | backoff exponencial, exceções de rede, `dormir` injetável |
| 05 | `ex05_listar_planilhas` | ★☆☆ | `pathlib`, extensões, arquivos `~$` do Excel |
| 06 | `ex06_nome_disponivel` | ★☆☆ | nunca sobrescrever: `nome (2).pdf` |
| 07 | `ex07_organizar_laudos` | ★★☆ | regex no nome, `shutil.move`, modo ensaio |
| 08 | `ex08_larguras_colunas` | ★☆☆ | lógica de largura de coluna (função pura) |
| 09 | `ex09_relatorio_excel` | ★★★ | `openpyxl`: estilos, formato, filtro, formatação condicional |
| 10 | `ex10_montar_email` | ★★☆ | `EmailMessage`, anexo, `mimetypes` |
| 11 | `ex11_ler_pedido_eml` | ★★☆ | ler `.eml`, HTML, regex, número brasileiro |
| 12 | `ex12_corrigir_plano_robo` | ★★☆ | leitura de código: achar os defeitos do plano do robô |
| 13 | `ex13_revisao_fila_idempotente` | ★★★ | revisão: CSV, funções como valores, exceções (módulos 03, 04, 06) |
| 14 | `ex14_revisao_resumo_por_dia` | ★★☆ | revisão: datas, regex, acumuladores, formato BR (módulos 03, 05, 07) |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar de
`raise NotImplementedError` e rode, na pasta `curso-python`:

```text
python curso.py testar 12 ex01
```

Para testar o módulo inteiro: `python curso.py testar 12`. Nenhum exercício usa
internet nem navegador: rede, tela e relógio são sempre dublês nos testes.

## Desafio do módulo

**Robô da expedição (modo ensaio).** Um programa de linha de comando que lê os pedidos
de certificado em `.eml`, confere as OPs no cadastro, monta a fila com plano de ações,
"emite" com registro idempotente, gera o relatório Excel com abas Fila e Pendências e
salva o e-mail-resumo para o supervisor. Enunciado completo em
[desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou: [quiz.md](quiz.md).

## Para ir além

- `urllib.parse` (montar e desmontar URLs): https://docs.python.org/pt-br/3/library/urllib.parse.html
- `pathlib`: https://docs.python.org/pt-br/3/library/pathlib.html
- `shutil`: https://docs.python.org/pt-br/3/library/shutil.html
- `email` (exemplos de mensagens): https://docs.python.org/pt-br/3/library/email.examples.html
- `logging` (guia básico): https://docs.python.org/pt-br/3/howto/logging.html
- requests: https://requests.readthedocs.io/
- openpyxl (estilos e formatação condicional): https://openpyxl.readthedocs.io/
- Playwright para Python (comece por "Locators" e "Auto-waiting"):
  https://playwright.dev/python/docs/intro
- Microsoft Graph, API de e-mail:
  https://learn.microsoft.com/graph/api/resources/mail-api-overview
