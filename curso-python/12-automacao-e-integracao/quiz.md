# Quiz — Módulo 12: Automação e integração

Responda sem consultar a aula. Depois confira no gabarito, no fim da página.

---

**1.** A API do laboratório recebeu um `POST /medicoes` e gravou a medição nova. Qual
código de status é o mais adequado na resposta?

a) 200  b) 201  c) 204  d) 302

---

**2.** O que este código imprime?

```python
import requests

pedido = requests.Request(
    "GET", "https://api.lab.local/bobinas", params={"linha": ["A", "B"], "limite": 5}
).prepare()
print(pedido.url)
```

---

**3.** Onde está o problema deste trecho de um robô que roda sozinho de madrugada?

```python
resposta = requests.get("https://api.lab.local/tolerancias", params={"linha": "A"})
dados = resposta.json()
```

---

**4.** O servidor respondeu `500 Internal Server Error`. O que este código imprime?

```python
try:
    resposta = requests.get(url, timeout=10)
    print("deu certo:", resposta.status_code)
except requests.RequestException:
    print("deu erro")
```

a) `deu erro`  b) `deu certo: 500`  c) nada, o programa trava  d) `deu certo: 200`

---

**5.** Por que a função abaixo é fácil de testar sem internet?

```python
def buscar_tolerancias(sessao, base_url, linha, timeout=10):
    resposta = sessao.get(f"{base_url}/tolerancias", params={"linha": linha}, timeout=timeout)
    ...
```

---

**6.** O que este código imprime?

```python
from pathlib import Path

p = Path("laudo_123456_B.PDF")
print(p.suffix, p.suffix.lower() in {".pdf"}, p.stem)
```

---

**7.** Você roda `shutil.move(origem, destino)` e já existe um arquivo com o mesmo nome
em `destino`. O que pode acontecer, e como o robô deveria se proteger?

---

**8.** O que este código imprime?

```python
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "teste"
msg.set_content("Olá")
print(msg.get_content_type())
msg.add_attachment(b"%PDF", maintype="application", subtype="pdf", filename="c.pdf")
print(msg.get_content_type(), len(list(msg.iter_attachments())))
```

---

**9.** Sua empresa migrou todo mundo para o **Novo Outlook**. O script com
`win32com.client.Dispatch("Outlook.Application")` parou de achar os e-mails. Qual
alternativa NÃO resolve?

a) Microsoft Graph com um aplicativo registrado pela TI.
b) Um fluxo do Power Automate que salva os e-mails numa pasta do OneDrive.
c) Instalar o pywin32 de novo.
d) Voltar a usar o Outlook clássico naquela máquina, se a empresa permitir.

---

**10.** Por que `time.sleep(5)` depois de clicar em "Confirmar" é uma má ideia num robô
Playwright? O que usar no lugar?

---

**11.** A tela tem os botões "Confirmar" e "Cancelar". O que acontece com
`page.get_by_role("button").click()`?

a) Clica no primeiro botão.
b) Clica nos dois.
c) Levanta um erro de *strict mode violation*.
d) Não faz nada e segue.

---

**12.** O robô rodou às 7h e emitiu 10 certificados. Às 13h o Agendador roda de novo com
os mesmos e-mails na pasta. O que significa dizer que o robô é **idempotente**?

---

**13.** O script funciona quando você roda no terminal, mas no Agendador de Tarefas falha
com `FileNotFoundError: 'dados/ops.csv'`. Qual a causa mais provável e duas formas de
corrigir?

---

**14.** O que é o "modo ensaio" de um robô e por que ele deve ser o padrão?

---

## Gabarito

<details><summary>Ver respostas</summary>

**1.** b) `201 Created`. `200` é o "OK" genérico; `204` é sucesso sem corpo (comum em
DELETE); `302` é redirecionamento.

**2.** `https://api.lab.local/bobinas?linha=A&linha=B&limite=5`. Uma lista vira a
mesma chave repetida, que é o jeito padrão de mandar vários valores.

**3.** Falta `timeout=`. Sem ele, se a API não responder, o robô fica esperando para
sempre. Também falta `resposta.raise_for_status()` antes do `.json()`: um 404 ou 500
passaria em silêncio.

**4.** b) `deu certo: 500`. Para o requests, receber uma resposta (mesmo de erro) não é
exceção. Só `raise_for_status()` transforma 4xx/5xx em `HTTPError`.

**5.** Porque a sessão é **injetada**: o teste passa um objeto falso com um método
`get` que devolve uma resposta pronta. Nada sai do computador. É injeção de
dependência; a outra técnica é `monkeypatch`.

**6.** `.PDF True laudo_123456_B`. `.suffix` mantém as maiúsculas do nome; por isso
comparamos com `.lower()`.

**7.** O arquivo existente pode ser **sobrescrito sem aviso** (a documentação do
`shutil.move` diz que isso depende do sistema). Antes de mover, verifique
`destino.exists()` e pule, ou escolha outro nome (`relatorio (2).xlsx`, exercício 06).

**8.** `text/plain`, depois `multipart/mixed 1`. Ao anexar, a mensagem vira
"multipart" sozinha: o texto vira uma parte e o PDF, outra.

**9.** c). O Novo Outlook não tem a interface COM que o `win32com` usa. Reinstalar o
pywin32 não muda isso.

**10.** Às vezes 5 s é pouco (o ERP estava lento e o robô segue errado), às vezes é
demais (robô lento à toa). Use as esperas do Playwright: as ações já esperam o
elemento ficar pronto, e `expect(...).to_have_text(...)` espera até a condição ser
verdadeira, com limite de tempo.

**11.** c). Locators do Playwright são "estritos": se a busca encontrar mais de um
elemento para uma ação, ele recusa em vez de chutar. Seja específico:
`get_by_role("button", name="Confirmar")`.

**12.** Rodar de novo não muda o resultado: nenhum certificado é emitido em dobro.
O robô consulta um registro (CSV, banco) do que já fez antes de agir, e anota logo
depois de agir.

**13.** O Agendador começa em outra pasta (normalmente `C:\Windows\System32`), e o
caminho relativo `dados/ops.csv` é procurado lá. Correções: no `.bat`, entrar na pasta
do projeto (`cd /d C:\robos\...`) ou preencher "Iniciar em"; no código, montar caminhos
a partir do script: `Path(__file__).resolve().parent / "dados" / "ops.csv"`.

**14.** É o modo em que o robô faz tudo (lê, valida, preenche, tira print), menos o
passo irreversível (Confirmar). Deve ser o padrão para que um esquecimento (rodar sem
pensar) nunca emita nada; emitir de verdade exige um pedido explícito (`--confirmar`).

</details>
