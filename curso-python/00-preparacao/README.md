# Módulo 00 — Preparação do ambiente

> **Tempo estimado:** 4 a 6 horas (divida em 3 ou 4 dias) · **Pré-requisitos:** nenhum ·
> **Nível:** iniciante

Este módulo é diferente dos outros. Quase não tem teoria de programação. Ele deixa o seu
computador pronto, ensina as ferramentas que todo profissional usa todo dia (terminal,
ambiente virtual, Git) e mostra como estudar o curso do jeito certo.

Não pule. Ambiente mal configurado é a causa número um de gente que desiste no começo.

## O que você vai aprender

- Explicar, com suas palavras, o que é um programa e o que o Python faz com o seu código.
- Instalar o Python 3.12+ no Windows com "Add python.exe to PATH" e conferir no terminal.
- Instalar o VS Code com a extensão Python e o Git for Windows.
- Andar pelas pastas no PowerShell com `cd`, `ls` e caminhos relativos e absolutos.
- Usar o REPL (`>>>`) para testar uma ideia em segundos.
- Criar e rodar um script `.py`.
- Clonar o repositório `estudos`, criar e ativar um ambiente virtual e instalar as
  bibliotecas com `pip`.
- Resolver o erro "a execução de scripts foi desabilitada neste sistema".
- Rodar os testes de um exercício com `python curso.py testar 00 ex01` e ver seu
  progresso com `python curso.py progresso`.
- Ler um traceback de baixo para cima e achar a linha do erro.
- Salvar e enviar seu trabalho com `git add`, `git commit`, `git push` e `git pull`.
- Usar IA como professor particular, e não como cola.

## Por que isso importa

Todo programador profissional, de analista de dados a desenvolvedor backend, faz isto
todos os dias: abre o terminal, ativa um ambiente virtual, roda testes e envia código para
o Git. Você vai aprender isso no primeiro dia, não no último.

Tem mais. Você já viu (ou vai ver) o problema "o script só funciona no computador do
fulano". Ambiente virtual + `requirements.txt` + Git resolvem exatamente isso. É o que
separa um script solto de um sistema que outra pessoa consegue rodar.

E o seu repositório no GitHub começa a virar portfólio hoje. O primeiro commit deste
módulo é o primeiro tijolo do projeto final (o Validador de Certificados).

---

## 1. O que é programar (e o que o Python faz com o seu código)

Programar é escrever instruções exatas para o computador seguir.

Pense num POP (procedimento operacional padrão) de ensaio de tração. Um técnico segue os
passos na ordem: corta o corpo de prova, mede a espessura, prende nas garras, roda o
ensaio, anota o resultado. Se um passo estiver ambíguo, ele usa o bom senso.

O computador também segue os passos na ordem. Mas ele **não tem bom senso nenhum**. Ele faz
exatamente o que está escrito, nem mais, nem menos. Se algo não estiver claro, ele para e
reclama. Isso parece chato, mas é uma vantagem: o erro aparece na hora, com a linha exata.

O caminho do seu código até o resultado:

```text
 você escreve           o interpretador            o computador
 ola.py  ──────────▶   python lê o arquivo  ──────▶  executa linha
 (texto)                e traduz cada linha          por linha
                                                         │
                         ┌───────────────────────────────┤
                         ▼                               ▼
                   saída na tela                 ou um ERRO, com o nome
                   (resultado)                   do arquivo e o número
                                                 da linha (traceback)
```

- **Código-fonte** é o texto que você escreve, num arquivo terminado em `.py`.
- **Interpretador** é o programa `python`. Ele lê o seu arquivo e executa as instruções,
  de cima para baixo.
- **Saída** é o que o programa mostra ou produz.

`print(...)` mostra na tela o que estiver entre os parênteses. Texto vai entre aspas.

> 🔮 **Preveja antes de rodar:** o que este programa mostra, e em que ordem?

```python
print("Pesando a bobina...")
print(4 * 250)
print("Pronto")
```

<details><summary>Resposta</summary>

```text
Pesando a bobina...
1000
Pronto
```

As linhas rodam de cima para baixo. Na segunda, `4 * 250` não está entre aspas: é uma
conta, e o Python mostra o resultado (1000), não o texto "4 * 250".

</details>

Ainda não tem Python no seu computador? Vamos instalar.

---

## 2. Instalando o Python no Windows

### 2.1 Primeiro, confira se já existe

Abra o **PowerShell**: aperte a tecla Windows, digite `PowerShell` e Enter. Digite:

```text
python --version
```

Três resultados possíveis:

| O que aparece | O que significa |
|---|---|
| `Python 3.12.x`, `3.13.x` ou `3.14.x` | Já está instalado. Pule para a seção 3. |
| A Microsoft Store abre, ou nada acontece | Não está instalado (é só um atalho do Windows). |
| `O termo 'python' não é reconhecido...` | Não está instalado ou não está no PATH. |

### 2.2 Qual versão instalar

Use **Python 3.14**: já tem um ano de correções e roda todas as bibliotecas do curso. As
versões 3.12 e 3.13 também servem. O curso exige no mínimo 3.10, mas recomenda 3.12+.

A 3.15 saiu em outubro de 2026. Pode usar, mas saiba que em versões recém-lançadas alguma
biblioteca às vezes demora a publicar o pacote pronto. Se a instalação das bibliotecas
falhar (seção 9), volte para a 3.14.

### 2.3 Passo a passo com o instalador tradicional

1. Entre em `https://www.python.org/downloads/windows/`.
2. Procure a última versão **3.14.x** e baixe **Windows installer (64-bit)**.
3. Abra o instalador. Na **primeira tela**, lá embaixo, marque
   **"Add python.exe to PATH"**. Este é o passo mais importante.
4. Clique em **Install Now** e aguarde.
5. Se no final aparecer **"Disable path length limit"**, clique nele (pede permissão de
   administrador). Isso evita erros com caminhos de pasta muito longos. É opcional.
6. **Feche o PowerShell e abra de novo.** O terminal só enxerga o PATH novo depois disso.
7. Confira:

```text
python --version
```

Deve aparecer algo como `Python 3.14.x`.

O que é **PATH**? É a lista de pastas onde o Windows procura um programa quando você digita
um comando. É como a lista de ramais da empresa: se o ramal do Python não está na lista,
o Windows responde "não conheço ninguém com esse nome".

> ⚠️ **Erro comum:** esquecer de marcar "Add python.exe to PATH". Solução: abra o
> instalador de novo, escolha **Modify**, avance e marque **"Add Python to environment
> variables"**. Depois feche e abra o terminal.

> ⚠️ **Erro comum:** digitar `python` e abrir a Microsoft Store, mesmo depois de instalar.
> São os "aliases de execução" do Windows. Abra **Configurações**, pesquise por
> **"aliases de execução de aplicativo"** e desligue os itens `python.exe` e `python3.exe`
> do "Instalador de Aplicativo".

### 2.4 Outras formas de instalar

O python.org agora recomenda, para Windows, o novo **Python install manager** (comando
`py install 3.14`; aceite quando ele perguntar se deve adicionar a pasta de comandos ao
PATH). O instalador da seção 2.3 continua disponível, mas foi marcado como obsoleto e
deixará de ser publicado a partir do Python 3.16. Outra opção é o `winget`, que já vem no
Windows 10/11: `winget install Python.Python.3.14`. Qualquer caminho serve: no fim,
`python --version` precisa responder.

> 💡 **Dica:** em computador da empresa, a TI pode bloquear instalações. Use o seu
> computador pessoal para o curso ou peça a instalação à TI.

**Linux e macOS:** no Linux o Python costuma vir instalado (comando `python3`; no
Ubuntu/Debian instale também `python3-venv`). No macOS use o instalador do python.org ou o
Homebrew. Nesses sistemas, onde o curso escrever `python`, use `python3`.

---

## 3. VS Code e a extensão Python

O **VS Code** (Visual Studio Code) é o editor onde você vai escrever código. Ele é para o
programador o que o Excel é para quem trabalha com planilhas: a ferramenta do dia a dia.

### 3.1 Instalar

1. Entre em `https://code.visualstudio.com` e baixe a versão para Windows.
2. Na tela "Selecionar tarefas adicionais", deixe marcado **"Adicionar ao PATH"** e marque
   **"Adicionar a ação 'Abrir com Code'"** (os dois menus de contexto).
3. Abra o VS Code.

### 3.2 Instalar a extensão Python

1. Aperte `Ctrl+Shift+X` (painel de extensões).
2. Pesquise **Python** e instale a da **Microsoft** (identificador `ms-python.python`).
   Ela já traz junto o Pylance (autocompletar) e o Python Debugger.

### 3.3 As partes que você vai usar

```text
┌──────────────┬─────────────────────────────────────────┐
│  EXPLORADOR  │  EDITOR                                 │
│  (arquivos)  │  aqui você escreve o código             │
│  Ctrl+Shift+E│                                         │
│              ├─────────────────────────────────────────┤
│              │  TERMINAL (PowerShell)        Ctrl+'    │
│              │  aqui você roda os comandos             │
└──────────────┴─────────────────────────────────────────┘
 barra de status: mostra qual Python está em uso (canto inferior direito)
 Paleta de comandos: Ctrl+Shift+P (procura qualquer função do VS Code)
```

> ⚠️ **Erro comum:** rodar o teste com o arquivo **não salvo**. O teste lê o arquivo do
> disco, não o que está na tela. Uma bolinha branca na aba significa "não salvo". Use
> `Ctrl+S` sempre, ou ligue **Arquivo → Salvamento Automático**.

> 💡 **Dica:** abra sempre a **pasta** do projeto (Arquivo → Abrir Pasta), não um arquivo
> solto. Assim o VS Code encontra o ambiente virtual e os testes.

---

## 4. Git for Windows: instalar e configurar

**Git** guarda o histórico do seu código. Cada **commit** é uma fotografia do projeto num
momento, com data, autor e uma mensagem. Pense nas revisões de um procedimento
controlado: rev. 00, rev. 01, rev. 02. Você sempre pode ver o que mudou e voltar atrás.

**GitHub** é um site que guarda uma cópia do seu repositório na nuvem. Serve de backup,
permite trabalhar em mais de um computador e vira o seu portfólio.

### 4.1 Instalar

1. Entre em `https://git-scm.com/downloads/win` e baixe o **Git for Windows** (64-bit).
2. Avance com as opções padrão, com três atenções:
   - **Editor padrão:** escolha "Use Visual Studio Code as Git's default editor".
   - **Nome do branch inicial:** escolha "Override the default branch name" e deixe `main`.
   - **PATH:** deixe a opção recomendada, "Git from the command line and also from
     3rd-party software".
3. Feche e abra o terminal. Confira:

```text
git --version
```

Deve aparecer algo como `git version 2.x.x.windows.1`.

### 4.2 Dizer ao Git quem é você (uma vez por computador)

Todo commit leva nome e e-mail do autor. Use o **mesmo e-mail da sua conta do GitHub**:

```text
git config --global user.name "Carlos Eduardo"
git config --global user.email "o-email-da-sua-conta@exemplo.com"
git config --global init.defaultBranch main
```

Para conferir: `git config --global --list`.

O login no GitHub acontece no primeiro `git push`: o Git for Windows abre uma janela do
navegador para você autorizar. Você não digita senha no terminal.

---

## 5. O terminal (PowerShell) sem medo

O terminal é uma janela onde você dá ordens ao computador escrevendo. Parece antigo, mas
servidores, robôs e ferramentas de dados são controlados assim. No VS Code: menu
**Terminal → Novo Terminal** (ou `Ctrl+'`). No Windows ele abre o PowerShell.

O texto antes do cursor é o **prompt**. Ele mostra em que pasta você está:

```text
PS C:\Users\carlos>
```

### 5.1 Os comandos que você vai usar

| Comando | O que faz | Exemplo |
|---|---|---|
| `pwd` | mostra a pasta atual | `pwd` |
| `ls` (ou `dir`) | lista o que tem na pasta | `ls` |
| `cd pasta` | entra numa pasta | `cd projetos` |
| `cd ..` | volta uma pasta (sobe um nível) | `cd ..` |
| `cd ~` | vai para a sua pasta de usuário | `cd ~` |
| `mkdir nome` | cria uma pasta | `mkdir projetos` |
| `cls` (ou `clear`) | limpa a tela | `cls` |
| `code .` | abre a pasta atual no VS Code | `code .` |
| `explorer .` | abre a pasta atual no Explorador de Arquivos | `explorer .` |

Três atalhos que economizam horas:

- **Tab** completa nomes de pastas e arquivos. Digite `cd proj` e aperte Tab.
- **Seta para cima** traz os comandos anteriores.
- **Ctrl+C** interrompe um programa que travou.

### 5.2 Caminhos absolutos e relativos

- **Absoluto:** o endereço completo, desde o disco. `C:\Users\carlos\projetos\estudos`.
- **Relativo:** a partir de onde você está. Se você está em `C:\Users\carlos`, então
  `projetos\estudos` leva ao mesmo lugar.
- `.` é "a pasta atual". `..` é "a pasta de cima".

```text
C:\Users\carlos
└── projetos
    └── estudos
        └── curso-python
            ├── 00-preparacao
            └── curso.py
```

> 🔮 **Preveja antes de rodar:** você está em `C:\Users\carlos\projetos\estudos\curso-python`
> e digita `cd ..\..`. Em que pasta você vai parar?

<details><summary>Resposta</summary>

Em `C:\Users\carlos\projetos`. Cada `..` sobe um nível: o primeiro sai de `curso-python`
para `estudos`, o segundo sai de `estudos` para `projetos`.

</details>

> ⚠️ **Erro comum:** caminho com espaço sem aspas. `cd C:\Meus Projetos` falha. Use
> `cd "C:\Meus Projetos"`. Melhor ainda: crie pastas sem espaço e sem acento.

> ⚠️ **Erro comum:** guardar projetos em pastas sincronizadas pelo OneDrive (em muitos PCs,
> "Documentos" e "Área de Trabalho" são). O ambiente virtual tem milhares de arquivos e a
> sincronização atrapalha. Use `C:\Users\<seu-usuario>\projetos`.

No Linux e no macOS os comandos são quase os mesmos (`pwd`, `ls`, `cd`, `mkdir`), e as
barras dos caminhos são `/` em vez de `\`.

---

## 6. O REPL: conversando com o Python

Digite `python` no terminal e aperte Enter. Aparece algo assim (a primeira linha muda
conforme a sua versão):

```text
Python 3.14.x (...) on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

O `>>>` é o **REPL** (Read-Eval-Print Loop): o Python lê o que você digita, calcula,
mostra o resultado e espera a próxima instrução. É a calculadora de bolso do programador.

```python
>>> 2 + 3
5
>>> 312.5 * 3
937.5
>>> 7 / 2
3.5
```

Para sair: digite `exit()` e Enter. (Atalho: no Windows, `Ctrl+Z` e Enter; no Linux e no
macOS, `Ctrl+D`.)

> 🔮 **Preveja antes de rodar:** qual a diferença entre as duas saídas?

```python
>>> "Olá"
>>> print("Olá")
```

<details><summary>Resposta</summary>

```python
>>> "Olá"
'Olá'
>>> print("Olá")
Olá
```

Na primeira, o REPL mostra o **valor** como o Python o enxerga: um texto, por isso as
aspas. Na segunda, o `print` mostra o texto **para humanos**, sem aspas. Guarde essa
diferença: ela volta na seção 10 (print × return).

</details>

**O REPL é o seu laboratório de hipóteses.** "Será que `7 / 2` dá 3?" Não discuta com
você mesmo: pergunte ao Python. Ele responde `3.5`, e a hipótese cai em 5 segundos.

> 💡 **Dica:** sempre que tiver dúvida sobre "o que acontece se...", abra o REPL e teste.
> É mais rápido que pesquisar e você lembra melhor do que descobriu sozinho.

---

## 7. Seu primeiro script

O REPL esquece tudo quando você sai. Um **script** é um arquivo `.py` que fica salvo e pode
rodar quantas vezes quiser.

1. No terminal, crie uma pasta de rascunho e abra no VS Code:

```text
cd ~
mkdir projetos
cd projetos
mkdir rascunho
cd rascunho
code .
```

2. No VS Code, crie o arquivo `ola.py` (ícone de novo arquivo no Explorador) e **digite**:

```python
print("Olá, mundo!")
print("Meu primeiro script")
print(250 * 4)
```

3. Salve (`Ctrl+S`). No terminal do VS Code, rode:

```text
python ola.py
```

Saída:

```text
Olá, mundo!
Meu primeiro script
1000
```

Também dá para rodar pelo botão ▷ ("Run Python File") no canto superior direito do editor.
Ele faz a mesma coisa: chama `python` com o caminho do arquivo.

> 🔧 **Modifique:** acrescente uma linha que mostre o seu nome e outra que calcule o peso de
> 3 bobinas de 312,5 kg (lembre: no código, número com vírgula se escreve com ponto,
> `312.5`). Rode de novo e confira.

> ⚠️ **Erro comum:** digitar `python ola.py` estando na pasta errada. Resultado:
> `can't open file ... [Errno 2] No such file or directory`. Confira com `ls` se o arquivo
> está na pasta atual.

---

## 8. Baixando o curso: clonar (ou atualizar) o repositório

O curso fica dentro do seu repositório `estudos`, no GitHub:
`https://github.com/carlos-real/estudos`. **Clonar** é baixar o repositório inteiro, com
todo o histórico, e deixá-lo ligado ao GitHub.

### 8.1 Se este computador ainda não tem o repositório

```text
cd ~\projetos
git clone https://github.com/carlos-real/estudos.git
cd estudos\curso-python
ls
```

O `git clone` mostra algo como `Cloning into 'estudos'...` e alguns contadores de
progresso. No fim você tem a pasta `estudos` com tudo dentro.

### 8.2 Se você já tinha clonado antes

Entre na pasta e traga as novidades:

```text
cd ~\projetos\estudos
git pull
```

### 8.3 O que tem no repositório

```text
estudos/
├── pyproject.toml     configuração do Poetry (dos seus estudos anteriores)
├── src/               seu script antigo de salários
├── arquivos/          salaries.csv (será usado no módulo 10)
└── curso-python/      O CURSO: é aqui que você vai trabalhar
    ├── curso.py       a ferramenta que testa seus exercícios
    ├── requirements.txt
    ├── 00-preparacao/
    ├── 01-.../
    └── carreira/
```

Sobre o `pyproject.toml` na raiz: ele não atrapalha. Neste curso vamos usar `venv` + `pip`
dentro de `curso-python`, que é o caminho mais simples para começar. O Poetry volta, a
fundo, no módulo 07.

Agora abra a pasta do curso no VS Code:

```text
cd ~\projetos\estudos\curso-python
code .
```

---

## 9. Ambiente virtual (venv) e pip

### 9.1 O problema

Python tem milhares de bibliotecas prontas (pandas, openpyxl, pytest...), instaladas com o
**pip**. Se você instalar tudo "no Python do computador", um dia um projeto precisa do
pandas 2 e outro do pandas 3: atualizou para um, quebrou o outro.

Pense nas bancadas do laboratório: cada linha tem o seu próprio jogo de calibradores, e
trocar um calibrador da linha A não mexe na linha B. Um **ambiente virtual** é isso: uma
pasta (`.venv`) com um Python e bibliotecas só daquele projeto.

### 9.2 Criar o ambiente virtual

No terminal, **dentro de `curso-python`**:

```text
python -m venv .venv
```

Leva alguns segundos e cria a pasta `.venv`. O `-m` significa "rode o módulo": aqui,
"Python, rode o módulo venv e crie um ambiente na pasta `.venv`". Isso se faz **uma vez**
por computador.

### 9.3 Ativar

```text
.venv\Scripts\Activate.ps1
```

Funcionou se o prompt ganhar `(.venv)` na frente:

```text
(.venv) PS C:\Users\carlos\projetos\estudos\curso-python>
```

A partir daí, `python` e `pip` são os do ambiente virtual.

No Prompt de Comando (cmd), o comando é `.venv\Scripts\activate.bat`. No Linux e no macOS:
`source .venv/bin/activate`.

### 9.4 O erro da política de execução (quase todo mundo vê)

Na primeira ativação, o PowerShell costuma recusar:

```text
.venv\Scripts\Activate.ps1 : O arquivo C:\Users\carlos\...\Activate.ps1 não pode ser
carregado porque a execução de scripts foi desabilitada neste sistema. Para obter mais
informações, consulte about_Execution_Policies em https://go.microsoft.com/fwlink/?LinkID=135170.
```

(Em inglês: `cannot be loaded because running scripts is disabled on this system`.)

**Por quê?** No Windows 10 e 11 a política padrão do PowerShell é `Restricted`: ele não
roda nenhum script `.ps1`, nem os criados no seu próprio computador. O `Activate.ps1` é um
script, então é bloqueado.

**Solução** (vale só para o seu usuário e não precisa de administrador):

```text
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Se pedir confirmação, digite `S` (Sim) e Enter. Depois rode o `Activate.ps1` de novo.

O que isso faz: `RemoteSigned` libera scripts criados no seu computador e exige assinatura
digital dos baixados da internet. É o que a documentação da Microsoft recomenda para quem
não assina scripts. Para ver a política atual: `Get-ExecutionPolicy -List`.

> ⚠️ **Erro comum:** em computador da empresa, a TI pode impor a política (Group Policy) e
> o comando não muda nada. Não tente burlar: estude no computador pessoal ou fale com a TI.
> (Se a TI liberar o Prompt de Comando, o `cmd`, a ativação nele é
> `.venv\Scripts\activate.bat`.)

### 9.5 Instalar as bibliotecas do curso

Com o `(.venv)` aparecendo no prompt:

```text
python -m pip install -r requirements.txt
```

O `-r` diz "leia a lista deste arquivo". O `requirements.txt` do curso lista pytest, ruff,
pandas, openpyxl, matplotlib, requests, fastapi, httpx e uvicorn. A instalação leva alguns
minutos e termina com uma linha `Successfully installed ...`.

Para ver o que está instalado: `python -m pip list`.

> 💡 **Dica:** prefira `python -m pip` a só `pip`. Assim você garante que está usando o pip
> do mesmo Python que vai rodar o código (o do `.venv`).

### 9.6 Ensinar o VS Code a usar o `.venv`

1. `Ctrl+Shift+P` → digite **Python: Select Interpreter** → escolha o que tem `.venv`.
2. Abra um terminal novo (`Ctrl+Shift+'`). Normalmente o VS Code já ativa o `.venv`
   sozinho e o `(.venv)` aparece.

### 9.7 Conferir tudo de uma vez

O curso tem um verificador. Na pasta `curso-python`, com o `.venv` ativo:

```text
python 00-preparacao/exemplos/04_verificar_ambiente.py
```

Saída quando está tudo certo (o número da versão será o do seu Python):

```text
Verificando o ambiente do curso...

✔ Python 3.13.16
✔ Ambiente virtual ativo
✔ Bibliotecas do curso instaladas
✔ Git encontrado
✔ Terminal na pasta curso-python

Tudo pronto! Pode rodar:  python curso.py testar 00
```

> 🔮 **Preveja antes de rodar:** você abre um PowerShell novo, fora do VS Code, vai até
> `curso-python` e roda o verificador **sem ativar** o `.venv`. Que linha vai aparecer
> com ✘?

<details><summary>Resposta</summary>

`✘ Ambiente virtual ativo`, com a dica de como ativar. Se as bibliotecas não estiverem
instaladas no Python do sistema, também aparece `✘ Bibliotecas do curso instaladas`.
Cada terminal novo começa **sem** ambiente ativo; é preciso ativar de novo (o VS Code faz
isso por você quando o interpretador está selecionado).

</details>

Para sair do ambiente virtual: `deactivate`. Deu tudo errado? Apague a pasta `.venv` e
crie de novo; não se perde nada.

> ⚠️ **Erro comum:** copiar a pasta `.venv` para outro computador ou mandar para o GitHub.
> Ela não funciona em outro lugar. O certo é recriar com os comandos acima. O curso já
> tem um `.gitignore` que impede o `.venv` de ir para o GitHub.

---

## 10. O molde dos exercícios: `def` e `return`

### 10.1 Rodando os exemplos da aula

Cada aula tem uma pasta `exemplos/` com scripts prontos. Rode sempre da pasta
`curso-python`:

```text
python 00-preparacao/exemplos/02_calculadora.py
```

> 🔮 **Preveja antes de rodar:** abra `00-preparacao/exemplos/02_calculadora.py`, leia o
> código e escreva num papel as 7 linhas que você acha que vão aparecer. Depois rode.

```python
print("Peso de 4 bobinas de 250 kg:")
print(4 * 250)

print("Média de três medições de espessura (µm):")
print((50.2 + 49.8 + 51.0) / 3)

print("Precedência: multiplicação antes da soma")
print(2 + 3 * 4)
print((2 + 3) * 4)
```

<details><summary>Resposta</summary>

```text
Peso de 4 bobinas de 250 kg:
1000
Média de três medições de espessura (µm):
50.333333333333336
Precedência: multiplicação antes da soma
14
20
```

O `50.333333333333336` costuma surpreender: o computador guarda números com vírgula em
binário e às vezes sobra um "resto" minúsculo no fim. Não é erro seu. O módulo 01 explica
e ensina a arredondar. E o 14 e o 20 seguem a matemática da escola: multiplicação antes da
soma, e parênteses mudam a ordem.

</details>

### 10.2 Função: uma máquina que recebe e devolve

Quase todo exercício do curso pede para você completar uma **função**. Pense num
equipamento de ensaio: você coloca a amostra (entrada), ele faz o trabalho e devolve um
resultado (saída). Você não precisa saber o que acontece lá dentro para usar o resultado.

```python
def peso_liquido(peso_bruto_kg: float, tara_kg: float) -> float:
    """Devolve o peso líquido (kg): peso bruto menos a tara (tubete e embalagem)."""
    return peso_bruto_kg - tara_kg
```

Peça por peça:

```text
def peso_liquido(peso_bruto_kg: float, tara_kg: float) -> float:
│   │            │                                     │       │
│   │            └── parâmetros: as entradas           │       └── dois-pontos
│   └── nome da função                                 └── tipo do resultado (anotação)
└── "vou definir uma função"

    """Devolve o peso líquido..."""  ← docstring: explica o que a função faz
    return peso_bruto_kg - tara_kg    ← return: DEVOLVE o resultado para quem chamou
^^^^
4 espaços de recuo: é assim que o Python sabe o que está "dentro" da função
```

Definir não executa nada. A função só trabalha quando é **chamada**, com valores entre
os parênteses (um para cada parâmetro, na mesma ordem):

```python
>>> peso_liquido(1050.0, 50.0)
1000.0
>>> peso_liquido(937.5, 37.5)
900.0
```

Os `: float` e `-> float` são **anotações de tipo** (type hints): avisos para
você e para o VS Code sobre o que entra e o que sai. O Python não confere. Detalhes nos
módulos 01 e 04.

> 💡 **Dica:** o recuo de 4 espaços não é enfeite. No VS Code, aperte Tab para recuar e
> Shift+Tab para voltar. Ele converte o Tab em 4 espaços.

### 10.3 `print` mostra, `return` devolve

Esta é a confusão número um de quem começa. Abra `00-preparacao/exemplos/03_molde_da_funcao.py`:

```python
def dobro(numero: float) -> float:
    """Devolve o dobro de um número."""
    return numero * 2


def mensagem_liberacao(ensaio: str) -> str:
    """Devolve a observação de liberação de um ensaio, ex.: 'COF: liberado'."""
    return ensaio + ": liberado"


def ola_com_print() -> None:
    """Só MOSTRA um texto na tela. Não devolve nada (devolve None)."""
    print("Olá (mostrado com print)")


# Chamando as funções e mostrando o que elas DEVOLVEM:
print(dobro(21))
print(dobro(2.5))
print(mensagem_liberacao("COF"))
print(mensagem_liberacao("Selagem"))

# A diferença entre print e return:
resultado = ola_com_print()
print(resultado)
```

> 🔮 **Preveja antes de rodar:** as quatro primeiras linhas da saída são fáceis. E as duas
> últimas? O que fica guardado em `resultado`?

<details><summary>Resposta</summary>

```text
42
5.0
COF: liberado
Selagem: liberado
Olá (mostrado com print)
None
```

`ola_com_print()` **mostra** o texto na tela, mas não tem `return`. Toda função sem
`return` devolve `None`, que é o jeito do Python dizer "nada". Então `resultado` guarda
`None`, e o último `print` mostra `None`.

É por isso que os testes do curso reclamam quando você usa `print` no lugar de `return`:
o teste recebe `None`, não o texto.

</details>

Duas coisas novas no exemplo, só o suficiente por agora:

- `resultado = ...` guarda um valor com um nome (uma **variável**). Módulo 01 a fundo.
- `ensaio + ": liberado"`: o `+` entre textos **junta** os textos. `"COF" + ": liberado"`
  vira `"COF: liberado"`. Outra forma, que você vai usar muito, é a f-string:
  `f"{ensaio}: liberado"` (módulo 01).

> 🔧 **Modifique:** no exemplo, crie uma função `triplo(numero)` que devolve o número vezes
> 3 e mostre `print(triplo(7))`. Depois troque o `return` de `dobro` por `print` e veja o
> que acontece com `print(dobro(21))`. (Desfaça depois.)

### 10.4 Como é um exercício do curso

Abra `00-preparacao/exercicios/ex01_ola_mundo.py`. Todo exercício tem este formato:

```python
"""
Exercício 00.01 — Olá, mundo!
Nível: ★☆☆
(... contexto, tarefa, exemplos e dica ...)
Teste com:  python curso.py testar 00 ex01
"""


def ola_mundo() -> str:
    """Devolve o texto 'Olá, mundo!'."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
```

- O texto entre `"""` no topo é o **enunciado**. Leia inteiro, inclusive os exemplos.
- `raise NotImplementedError(...)` é uma placa de "em construção": se alguém chamar a
  função, ela avisa que ainda não foi feita. **Apague essa linha** e escreva o seu código
  no lugar.
- Não mude o nome da função nem os parâmetros: os testes chamam exatamente esse nome.

### 10.5 Exemplo resolvido: a mensagem de liberação

Antes de você fazer os exercícios, veja como eu penso um problema parecido, passo a passo.

**Enunciado:** escreva `liberar(ensaio)`, que devolve a observação que vai na planilha,
no formato `"<ensaio>: liberado"`. Exemplo: `liberar("COF")` devolve `"COF: liberado"`.

**Passo 1 — entrada e saída.** Primeiro eu pensei: o que entra? Um texto (o nome do
ensaio). O que sai? Outro texto. Então a assinatura é:

```python
def liberar(ensaio: str) -> str:
```

**Passo 2 — resolver um caso concreto no REPL.** Antes de pensar em "qualquer ensaio",
resolvo para um ensaio só:

```python
>>> "COF" + ": liberado"
'COF: liberado'
```

**Passo 3 — generalizar.** Agora troco o valor fixo `"COF"` pelo parâmetro `ensaio`
(sem aspas, porque quero o conteúdo da caixa, não a palavra "ensaio"):

```python
def liberar(ensaio: str) -> str:
    """Devolve a observação de liberação do ensaio."""
    return ensaio + ": liberado"
```

**Passo 4 — testar com mais de um caso.** Inclusive um que não está no enunciado:

```python
>>> liberar("COF")
'COF: liberado'
>>> liberar("Tração")
'Tração: liberado'
```

**Passo 5 — conferir os detalhes.** O enunciado pede dois-pontos e **um** espaço. Está
certo. Pronto.

Esse roteiro (entrada/saída → caso concreto → generalizar → testar → conferir detalhes)
resolve os três exercícios deste módulo e boa parte dos próximos.

---

## 11. Seu primeiro teste: o ciclo do curso

### 11.1 Como cada módulo é organizado

```text
00-preparacao/
├── README.md      a aula (este arquivo)
├── exemplos/      scripts da aula, prontos para rodar
├── exercicios/    ONDE VOCÊ TRABALHA: complete as funções
├── testes/        os testes que corrigem seus exercícios (não mexa)
├── solucoes/      soluções oficiais comentadas (só depois de tentar!)
├── desafio/       um mini projeto
└── quiz.md        perguntas de revisão com gabarito
```

### 11.2 A ferramenta `curso.py`

Rode sempre de dentro da pasta `curso-python`, com o `.venv` ativo:

| Comando | O que faz |
|---|---|
| `python curso.py modulos` | lista os módulos e quantos exercícios cada um tem |
| `python curso.py testar 00` | testa todos os exercícios do módulo 00 |
| `python curso.py testar 00 ex01` | testa só o exercício 01 do módulo 00 |
| `python curso.py progresso` | mostra quantos exercícios você já resolveu |
| `python curso.py progresso -d` | o mesmo, com o detalhe de cada exercício |

O exercício pode ser escrito como `ex01`, `ex1`, `01` ou `1`. O `-d` também pode ser
escrito `--detalhes`.

### 11.3 Passo a passo do exercício 01

**1. Rode o teste ANTES de mexer.** Sim, ele vai falhar. Isso confirma que tudo está
ligado:

```text
python curso.py testar 00 ex01
```

Saída (trecho):

```text
collecting ... collected 5 items

00-preparacao/testes/test_m00_ex01_ola_mundo.py::test_devolve_um_valor FAILED [ 20%]
(...)
00-preparacao/testes/test_m00_ex01_ola_mundo.py::test_sem_espacos_sobrando FAILED [100%]

=================================== FAILURES ===================================
____________________________ test_devolve_um_valor _____________________________
00-preparacao/testes/test_m00_ex01_ola_mundo.py:7: in test_devolve_um_valor
    resultado = ex.ola_mundo()
                ^^^^^^^^^^^^^^
00-preparacao/exercicios/ex01_ola_mundo.py:26: in ola_mundo
    raise NotImplementedError("Implemente esta função")
E   NotImplementedError: Implemente esta função
(...)
============================== 5 failed in 0.03s ===============================

✘ Ainda há testes falhando. Leia a mensagem acima: ela diz o que era
  esperado e o que seu código devolveu. Corrija e rode de novo.
```

Como ler: são 5 testes, todos `FAILED`. A linha que começa com `E` diz o motivo:
`NotImplementedError`, ou seja, a função ainda está com a placa de "em construção".
(No Windows, as barras dos caminhos podem aparecer como `\`.)

**2. Escreva o código.** Apague o `raise NotImplementedError(...)` e escreva o `return`.

> 🔮 **Preveja antes de rodar:** suponha que, em vez de `return "Olá, mundo!"`, você
> escreva `print("Olá, mundo!")`. Quantos dos 5 testes passam?

<details><summary>Resposta</summary>

Nenhum. A função mostra o texto, mas devolve `None`. Trecho da saída real:

```text
____________________________ test_devolve_um_valor _____________________________
00-preparacao/testes/test_m00_ex01_ola_mundo.py:8: in test_devolve_um_valor
    assert resultado is not None, (
E   AssertionError: Sua função não devolveu nada (devolveu None). Você usou print() em vez de return?
E   assert None is not None
----------------------------- Captured stdout call -----------------------------
Olá, mundo!
```

Repare no "Captured stdout call": o pytest mostra o que o seu `print` escreveu na tela.
O texto apareceu, mas não foi devolvido.

</details>

**3. Se errar um detalhe, leia a diferença.** Por exemplo, sem o acento
(`return "Ola, mundo!"`), dois testes falham e um deles mostra:

```text
E   AssertionError: assert 'Ola, mundo!' == 'Olá, mundo!'
E     
E     - Olá, mundo!
E     ?   ^
E     + Ola, mundo!
E     ?   ^
```

A linha com `-` é o **esperado**, a linha com `+` é o que o **seu código devolveu**, e o
`^` aponta exatamente a letra diferente.

**4. Tudo certo.** Com o código correto e o arquivo salvo, os 5 testes aparecem como
`PASSED` e o fim da saída é:

```text
============================== 5 passed in 0.02s ===============================

✔ Tudo certo! Pode seguir para o próximo exercício.
```

**5. Compare com a solução oficial.** Só agora abra `solucoes/ex01_ola_mundo.py`. Ela traz
comentários sobre armadilhas e alternativas. Mesmo acertando, sempre dá para aprender algo.

**6. Veja o seu progresso:**

```text
python curso.py progresso -d
```

```text
Conferindo seus exercícios, aguarde...

  00 Preparacao                      ███████░░░░░░░░░░░░░  1/3
   ex01✔  ex02·  ex03·

Total: 1/3 exercícios (33%)
```

(Quando houver mais módulos no curso, cada um aparece numa linha.)

> ⚠️ **Erro comum:** rodar `python curso.py ...` fora da pasta `curso-python`. Resultado:
> `can't open file '...\curso.py': [Errno 2] No such file or directory`. Volte com
> `cd ~\projetos\estudos\curso-python`.

---

## 12. Git no dia a dia: status, add, commit, push, pull

### 12.1 O caminho de uma alteração

```text
 sua pasta            área de preparação         histórico local          GitHub
 (arquivos editados)  (o que vai no commit)      (commits)                (nuvem)
        │   git add          │    git commit           │    git push         │
        └──────────────────▶ └───────────────────────▶ └──────────────────▶  │
        ◀─────────────────────────────────────────────────────────────────── ┘
                                    git pull
```

Analogia do laboratório:

- `git add`: colocar as amostras na bandeja do que vai ser registrado.
- `git commit`: emitir o laudo, com data, responsável e descrição.
- `git push`: enviar o laudo para o arquivo central (GitHub).
- `git pull`: buscar no arquivo central o que outros (ou você, em outro computador)
  registraram.

### 12.2 Salvando o exercício 01

Depois de passar no teste, na pasta `curso-python`:

```text
git status
```

O Git mostra o que mudou (a mensagem pode aparecer em português, conforme a instalação):

```text
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   00-preparacao/exercicios/ex01_ola_mundo.py

no changes added to commit (use "git add" and/or "git commit -a")
```

Coloque o arquivo na bandeja e confira de novo:

```text
git add 00-preparacao/exercicios/ex01_ola_mundo.py
git status
```

Agora o arquivo aparece em `Changes to be committed` (vai no próximo commit). Registre e
envie:

```text
git commit -m "Resolve exercício 00.01 (olá, mundo)"
git push
```

No primeiro `push`, o navegador abre para você autorizar o acesso ao GitHub. Depois
disso, a última linha do `push` mostra algo como `main -> main`. Abra
`https://github.com/carlos-real/estudos` e veja o seu commit lá.

Para ver o histórico: `git log --oneline` (aperte `q` para sair, se a lista for longa).

> 🔮 **Preveja antes de rodar:** você resolveu o ex02, salvou e rodou direto
> `git commit -m "Resolve ex02"`, **sem** `git add`. O que acontece?

<details><summary>Resposta</summary>

Nada é registrado. O Git responde:

```text
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   00-preparacao/exercicios/ex02_saudacao.py

no changes added to commit (use "git add" and/or "git commit -a")
```

O commit só leva o que está na área de preparação. Faltou o `git add`.

</details>

### 12.3 Boas mensagens de commit

| Ruim | Boa |
|---|---|
| `ajustes` | `Resolve exercício 00.02 (saudação)` |
| `teste` | `Corrige acento na saudação do ex01` |
| `aaaa` | `Adiciona script de apresentação do desafio 00` |

Regra prática: complete a frase "Este commit...". Verbo no presente, curto, específico.

### 12.4 `git pull` no começo, `git push` no fim

Comece cada sessão com `git pull` (traz novidades do curso ou do outro computador) e
termine com `git add`, `git commit` e `git push`. O atalho `git add .` coloca na bandeja
**tudo** o que mudou na pasta atual: rode `git status` antes para conferir o que vai junto.

> ⚠️ **Erro comum:** colocar no GitHub planilhas da empresa, laudos com nome de cliente,
> senhas ou arquivos `.env`. Se o repositório for público, qualquer pessoa vê. Use dados
> fictícios nos seus projetos.

---

## 13. Como estudar este curso

### 13.1 O método, em sete passos

1. **Leia a aula com o VS Code aberto.** Não só no celular. Ler sem testar dá a falsa
   sensação de que entendeu.
2. **Digite os exemplos, não copie e cole.** Digitar obriga a reparar em cada parêntese,
   aspas e recuo. É assim que os dedos e os olhos aprendem a sintaxe.
3. **Nos blocos 🔮, preveja antes de rodar.** Escreva a previsão num papel. Depois rode e
   compare.
4. **Faça os exercícios em ordem.** Eles sobem de dificuldade de propósito.
5. **Só abra a solução depois de tentar de verdade.** Travou por mais de 30 minutos,
   seguindo o roteiro da seção 13.4? Aí sim. E depois de ver a solução, apague o seu
   código e refaça sem olhar.
6. **Faça o quiz sem consultar nada.** Só depois confira o gabarito.
7. **Faça o desafio e dê commit/push.** O desafio junta tudo num programa de verdade.

### 13.2 Por que esses métodos funcionam

O curso usa técnicas com boa base em pesquisa sobre aprendizagem e ensino de programação.
Saber o porquê ajuda a não pular etapas.

**PRIMM: Preveja, Rode, Investigue, Modifique, Crie.** Método criado por pesquisadores de
ensino de computação no Reino Unido (Sue Sentance e colegas). Primeiro você **lê** e
**prevê** o que um código faz; depois roda e confere; investiga o que não entendeu;
modifica um detalhe; e só então cria algo do zero. Prever obriga a ler com atenção e
mostra o que você *acha* que sabe. Errar a previsão é exatamente o momento em que você mais
aprende. Nas aulas, isso aparece como 🔮 **Preveja antes de rodar** e 🔧 **Modifique**.

**Exemplos resolvidos.** Para quem está começando, ver um problema parecido resolvido
passo a passo, com o raciocínio explicado, ensina mais do que se debater sozinho desde o
início. A memória de trabalho de um iniciante enche rápido (é a ideia central da teoria
da carga cognitiva, de John Sweller); o exemplo resolvido libera espaço para aprender a
*estratégia*. Por isso cada aula mostra um "Exemplo resolvido" antes dos exercícios,
como o da seção 10.5.

**Prática deliberada com feedback imediato.** Repetir o que já sabe não faz evoluir. O
que faz é praticar no limite do que você consegue, com foco num ponto e com retorno
rápido sobre o erro (ideia estudada por Anders Ericsson). Os testes são esse retorno: em
segundos você sabe o que estava esperado e o que o seu código devolveu. É como ter o
resultado do ensaio na hora, em vez de esperar a reclamação do cliente.

**Revisão espaçada e intercalada.** A partir do módulo 02, os dois últimos exercícios de
cada módulo se chamam `exNN_revisao_<tema>.py`. Eles misturam o assunto novo com
conceitos de módulos anteriores. Dois efeitos estão em jogo:

- **Espaçamento:** revisar depois de alguns dias, quando já esqueceu um pouco, fixa
  muito mais do que estudar tudo de uma vez.
- **Intercalação:** misturar tipos de problema treina a parte mais difícil: decidir
  *qual* ferramenta usar, e não só *como* usá-la.

Por isso esses exercícios parecem mais difíceis. É de propósito.

**Recuperação ativa.** Tentar lembrar fortalece a memória mais do que reler (o "efeito
de teste", estudado por Henry Roediger e Jeffrey Karpicke). Por isso o quiz é para ser
feito **sem consultar**. Errou? Ótimo diagnóstico: volte àquela seção da aula. Outra forma
simples: no começo de cada sessão, escreva de memória, em 3 linhas, o que aprendeu na
anterior.

**Projeto contínuo.** Tudo no curso converge para o Validador de Certificados (módulo 14),
um problema real do seu trabalho: planilhas das linhas A a D, tolerâncias, e-mails da
expedição, certificados. Aprender com um objetivo concreto dá contexto ("isso serve para
aquilo") e motivação, e no fim vira portfólio.

### 13.3 Rotina sugerida: 1 hora por dia

Com 1 hora por dia, 5 dias por semana, o curso leva cerca de 31 semanas (7 meses).
Constância vence intensidade: 5 horas espalhadas na semana ensinam mais que 5 horas num
sábado.

| Tempo | O que fazer |
|---|---|
| 5 min | Resumo de memória: sem olhar nada, escreva 3 coisas da última aula. `git pull`. |
| 20 min | Aula: uma ou duas seções, digitando os exemplos e fazendo os 🔮. |
| 30 min | Exercícios: um ou dois, com o ciclo testar → corrigir → passar. |
| 5 min | Diário de bordo (o que aprendeu, onde travou) e `git add`/`commit`/`push`. |

Sexta-feira é dia de revisão espaçada: refaça sem consultar o quiz do módulo anterior e
refaça do zero um exercício de 2 ou 3 módulos atrás. O calendário semana a semana, com os
marcos de portfólio, está em `PLANO-DE-ESTUDOS.md` (na pasta `curso-python`).

> 💡 **Dica:** o celular é ótimo para **reler** a aula e fazer o quiz no ônibus ou no
> intervalo. Mas exercício se faz no computador.

### 13.4 Quando travar

Siga esta ordem antes de abrir a solução:

1. Releia o enunciado inteiro, devagar. Muitas respostas estão nos exemplos dele.
2. Leia a mensagem do teste: o que era esperado e o que veio.
3. Teste um pedaço da sua ideia no REPL, com valores concretos.
4. Releia a seção da aula sobre o assunto e o exemplo resolvido.
5. Explique o problema em voz alta, linha por linha, como se fosse para um colega (ou
   para um pato de borracha: a técnica tem esse nome, "rubber duck debugging"). Muitas
   vezes a resposta aparece no meio da explicação.
6. Peça uma **dica** (não a resposta) para a IA ou para alguém.
7. Só então abra a solução. Entenda, apague, refaça sem olhar.

### 13.5 IA como professor, não como cola

Ferramentas de IA (ChatGPT, Claude, Copilot, Gemini) são excelentes professores
particulares. E péssimas colas: se a IA escreve o código, quem aprende é ela.

**Use assim:**

- "Sou iniciante, estou no módulo 00 de um curso de Python. **Não me dê a resposta.** Meu
  teste falha com `assert None == 'Olá, mundo!'`. Me dê uma dica do que pode ser."
- "Explique este traceback linha por linha, como para um iniciante: (cole o erro)."
- "Faça 5 perguntas sobre ambiente virtual, sem as respostas. Depois corrija as minhas."
- "Meu código já passa nos testes. O que um programador experiente faria diferente? Explique o porquê."
- "Explique a diferença entre `print` e `return` com uma analogia de laboratório."

**Não use assim:**

- Colar o enunciado e pedir o código pronto.
- Aceitar código que você não sabe explicar linha por linha. Regra: **se você não
  consegue explicar, o código não é seu.**
- Colar dados da empresa (planilhas reais, nomes de clientes, NFs, laudos). Além da
  política interna, existe a LGPD. Use dados inventados.

E lembre: a IA erra com toda a confiança do mundo. Confira sempre rodando o código.

### 13.6 Como pesquisar

1. Copie a **última linha** do erro (sem os seus caminhos de pasta) e pesquise junto com
   a palavra `python`. Ex.: `python NameError: name 'pritn' is not defined`. Tente também
   em inglês: há muito mais conteúdo.
2. Prefira fontes confiáveis: a documentação oficial (`docs.python.org/pt-br/3/`), o
   Stack Overflow, a documentação da biblioteca.
3. Confira a data e a versão: resposta de 2012 pode ser de Python 2.

### 13.7 Como pedir ajuda (e ser respondido)

Quem pergunta bem recebe resposta rápida. Use este modelo, em comunidades ou com colegas:

```text
O que estou tentando fazer: resolver o exercício 00.02 (saudação).
O que eu esperava: saudar("Ana") devolver "Olá, Ana!".
O que aconteceu: o teste diz  assert 'Olá, nome!' == 'Olá, Ana!'
Meu código:
    def saudar(nome):
        return "Olá, nome!"
O que já tentei: reli o enunciado e testei no REPL.
Ambiente: Windows 11, Python 3.14, VS Code.
```

Cole o erro **como texto**, não como foto da tela. E mostre o **menor** pedaço de código
que reproduz o problema. Muitas vezes, ao montar a pergunta, você mesmo acha a resposta.

Onde perguntar: veja as comunidades em `carreira/recursos.md`.

---

## Lendo mensagens de erro deste módulo

### Como ler um traceback

Quando um programa quebra, o Python mostra um **traceback**: o rastro do que estava
acontecendo. **Leia de baixo para cima.**

```text
Traceback (most recent call last):
  File "C:\Users\carlos\projetos\rascunho\nome.py", line 2, in <module>   ← ONDE: arquivo e linha
    pritn("Olá, mundo!")                                                  ← a linha culpada
    ^^^^^                                                                 ← o pedaço exato
NameError: name 'pritn' is not defined. Did you mean: 'print'?            ← O QUÊ: tipo e motivo
```

1. **Última linha:** o tipo do erro (`NameError`) e o motivo.
2. **Acima dela:** o arquivo, o número da linha e o trecho de código.
3. Corrija, salve, rode de novo.

As mensagens abaixo são reais (Python 3.13). Em outras versões os detalhes mudam um pouco,
mas a estrutura é a mesma.

### Erros de Python

**`SyntaxError`: o Python nem conseguiu ler o código.** Ele aponta onde se perdeu:

```text
    print("Olá, mundo!)
          ^
SyntaxError: unterminated string literal (detected at line 1)
```

Faltou fechar as aspas.

Outras mensagens de `SyntaxError` que você vai ver:

| Mensagem | Causa provável |
|---|---|
| `'(' was never closed` | faltou fechar um parêntese |
| `expected ':'` | faltaram os dois-pontos no fim da linha do `def` (ou `if`, `for`...) |
| `invalid syntax` | algo fora do lugar; olhe a linha apontada **e a de cima** |

**`IndentationError`: recuo errado.**

```text
    return "Olá, mundo!"
    ^^^^^^
IndentationError: expected an indented block after function definition on line 1
```

O `return` precisava de 4 espaços de recuo para ficar "dentro" da função.

**`NameError`: nome que o Python não conhece.** Erro de digitação ou variável que não
existe:

```text
    print(peso_total)
          ^^^^^^^^^^
NameError: name 'peso_total' is not defined
```

**`NotImplementedError: Implemente esta função`**: você rodou o teste de um exercício que
ainda está com a linha `raise NotImplementedError(...)`. Apague-a e escreva o código.

**`AssertionError` no teste**: seu código rodou, mas o resultado está diferente do
esperado. Leia as linhas `-` (esperado) e `+` (seu resultado), como na seção 11.3.

**`ModuleNotFoundError: No module named 'pytest'`** (ou `pandas` etc.): a biblioteca não
está instalada **neste** Python. Quase sempre é o `.venv` desativado. Ative e, se precisar,
rode `python -m pip install -r requirements.txt`. (O `curso.py` mostra uma mensagem
amigável quando falta o pytest.)

### Erros do terminal

| Mensagem (resumida) | Causa | Solução |
|---|---|---|
| `O termo 'python' não é reconhecido...` | Python não instalado ou fora do PATH | Seção 2.3 |
| A Microsoft Store abre | Aliases de execução do Windows | Seção 2.3 |
| `...a execução de scripts foi desabilitada neste sistema` | Política do PowerShell | Seção 9.4 |
| `can't open file '...\curso.py': [Errno 2]` | Pasta errada | `cd` para `curso-python` |
| `fatal: not a git repository` | Fora da pasta do repositório | `cd` para dentro de `estudos` |
| `Author identity unknown` | Git sem nome/e-mail | Seção 4.2 |
| `! [rejected] main -> main (fetch first)` | O GitHub tem commits que você não tem | `git pull`, depois `git push` |

O `push` recusado é comum quando você estuda em dois computadores. A mensagem completa
termina com uma dica do próprio Git: `use 'git pull' before pushing again`.

---

## Boas práticas

- **Um ambiente virtual por projeto**, criado dentro da pasta do projeto, com o nome
  `.venv`.
- **Nunca coloque o `.venv` no Git.** Ele é recriado com `requirements.txt`.
- **`python -m pip`** em vez de só `pip`.
- **Projetos fora do OneDrive** e em pastas sem espaço nem acento.
- **Abra a pasta do projeto no VS Code**, não arquivos soltos.
- **Salve antes de testar** (ou ligue o salvamento automático).
- **Commits pequenos e frequentes**, com mensagens que completam "Este commit...".
- **`git pull` no começo, `git push` no fim** de cada sessão.
- **Leia a mensagem de erro inteira** antes de pesquisar ou perguntar.
- **Nada de dados reais da empresa** em repositórios ou ferramentas de IA.

---

## No mundo real

**A planilha que só funcionava no computador do estagiário.**

Uma cena comum na indústria: alguém escreve um script em Python que lê a planilha de
resultados do laboratório e gera um resumo para a reunião. Funciona bem por meses. Aí a
pessoa sai da empresa, ou a TI troca o computador, ou alguém atualiza o pandas "para ver
se melhora". O script para de funcionar e ninguém sabe por quê, nem qual versão de cada
biblioteca ele usava.

Como um profissional evita isso: o script mora num repositório Git, com um
`requirements.txt` listando as bibliotecas. Qualquer colega reproduz o ambiente com
cinco comandos, os mesmos que você usou neste módulo:

```text
git clone https://github.com/<empresa>/resumo-laboratorio.git
cd resumo-laboratorio
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

E se alguém mudar o código e quebrar algo, o histórico do Git mostra **o quê** mudou,
**quando** e **quem** mudou, e permite voltar atrás. Os testes automáticos (como os do
curso) avisam do problema antes de o resumo errado chegar na reunião.

Em entrevista de emprego, contar que você organiza seus scripts assim (repositório,
ambiente virtual, requirements, testes) já te coloca à frente de muita gente que só
"sabe Python".

---

## Resumo

| Tarefa | Comando (Windows / PowerShell) |
|---|---|
| Versão do Python | `python --version` |
| Abrir o REPL / sair | `python` / `exit()` |
| Rodar um script | `python arquivo.py` |
| Pasta atual / listar / entrar / voltar | `pwd` / `ls` / `cd pasta` / `cd ..` |
| Abrir a pasta no VS Code | `code .` |
| Clonar o repositório | `git clone https://github.com/carlos-real/estudos.git` |
| Criar o ambiente virtual | `python -m venv .venv` |
| Ativar o ambiente virtual | `.venv\Scripts\Activate.ps1` |
| Liberar scripts no PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Instalar as bibliotecas | `python -m pip install -r requirements.txt` |
| Conferir o ambiente | `python 00-preparacao/exemplos/04_verificar_ambiente.py` |
| Testar um exercício | `python curso.py testar 00 ex01` |
| Ver o progresso | `python curso.py progresso -d` |
| Ver o que mudou | `git status` |
| Registrar e enviar | `git add ...` → `git commit -m "..."` → `git push` |
| Trazer novidades | `git pull` |

Linux/macOS: `python3`, `source .venv/bin/activate`, caminhos com `/`.

O molde de todo exercício:

```python
def nome_da_funcao(parametro: tipo) -> tipo_do_resultado:
    """O que a função faz."""
    return resultado  # return DEVOLVE; print só mostra
```

---

## Você domina este módulo se...

- [ ] Consigo abrir o PowerShell, ir até `curso-python` com `cd` e explicar a diferença
      entre caminho absoluto e relativo.
- [ ] Sei explicar o que é o PATH e o que fazer quando aparece "o termo 'python' não é
      reconhecido".
- [ ] Consigo criar e ativar o `.venv` sozinho, e sei por que cada projeto deve ter o seu.
- [ ] Sei resolver o erro "a execução de scripts foi desabilitada" e explicar o que o
      `RemoteSigned` permite.
- [ ] Consigo explicar, sem consultar, a diferença entre `print` e `return`.
- [ ] Leio um traceback de baixo para cima e acho a linha e o tipo do erro.
- [ ] Faço o ciclo completo: testar → corrigir → passar → `git add` → `git commit` →
      `git push`.
- [ ] Sei pedir uma **dica** à IA sem pedir a resposta.

---

## Exercícios

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_ola_mundo.py` — Olá, mundo! | ★☆☆ | O ciclo testar → editar → passar; `return` de um texto |
| 02 | `ex02_saudacao.py` — Saudação personalizada | ★☆☆ | Usar um parâmetro; juntar textos com `+` |
| 03 | `ex03_peso_total.py` — Peso total da carga | ★☆☆ | Dois parâmetros; conta com `*`; testes com `approx` |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar de
`raise NotImplementedError`, salve e rode na pasta `curso-python`:

```text
python curso.py testar 00 ex01
python curso.py testar 00 ex02
python curso.py testar 00 ex03
python curso.py testar 00          # os três de uma vez
```

São só três, e fáceis de propósito: aqui o objetivo é validar o ambiente e fixar o ciclo.
A partir do módulo 01 vêm de 10 a 14 exercícios por módulo.

## Desafio do módulo

**Ambiente pronto e primeiro push.** Você vai conferir o ambiente com o verificador,
escrever um pequeno script de apresentação (`meu_cartao.py`) usando o molde `def` +
`return`, e enviar tudo para o GitHub com um commit bem feito.

Enunciado completo, critérios de aceite e dicas: [desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou, **sem consultar**: [quiz.md](quiz.md).

## Para ir além

- Documentação oficial, em português:
  - [Utilizando o interpretador Python](https://docs.python.org/pt-br/3/tutorial/interpreter.html)
  - [Ambientes virtuais e pacotes](https://docs.python.org/pt-br/3/tutorial/venv.html)
  - [Utilizando Python no Windows](https://docs.python.org/pt-br/3/using/windows.html)
- [Configurar o ambiente de desenvolvimento Python no Windows](https://learn.microsoft.com/pt-br/windows/dev-environment/python)
  (Microsoft Learn)
- [about_Execution_Policies](https://learn.microsoft.com/pt-br/powershell/module/microsoft.powershell.core/about/about_execution_policies)
  (o porquê do erro da seção 9.4, na documentação da Microsoft)
- [Pro Git, capítulos 1 e 2](https://git-scm.com/book/pt-br/v2) (livro oficial do Git,
  gratuito e em português)
- [Python no VS Code](https://code.visualstudio.com/docs/python/python-tutorial)
  (tutorial oficial, em inglês)
- [Python Tutor](https://pythontutor.com/): cole um código curto e veja, passo a passo,
  o que o Python faz em cada linha.
