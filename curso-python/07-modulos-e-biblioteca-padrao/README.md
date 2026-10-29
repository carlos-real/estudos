# Módulo 07 — Módulos, pacotes e biblioteca padrão

> **Tempo estimado:** 10 a 14 horas · **Pré-requisitos:** módulos 00 a 06 · **Nível:** iniciante avançando para intermediário

## O que você vai aprender

- Importar módulos das quatro formas (`import x`, `import x as y`, `from x import a`,
  `from x import a as b`) e escolher a certa para cada caso.
- Criar o seu próprio módulo e o seu próprio pacote (pasta com `__init__.py`) e
  importá-los de outro arquivo.
- Usar `if __name__ == "__main__":` para um arquivo funcionar como script **e** como
  módulo.
- Explicar onde o Python procura módulos (`sys.path`) e resolver `ModuleNotFoundError`.
- Organizar um projeto profissional no **src layout**, com `pyproject.toml`.
- Criar ambiente virtual, instalar com `pip`, gerar `requirements.txt` e usar o
  **Poetry** que já está no seu repositório.
- Calcular prazos e validades com `datetime` e `timedelta` e converter datas no
  formato brasileiro.
- Contar, agrupar e nomear dados com `Counter`, `defaultdict` e `namedtuple`.
- Juntar e agrupar sequências com `itertools.chain` e `itertools.groupby`.
- Calcular média, mediana, desvio padrão e CV% com `statistics`, do jeito que o
  laboratório usa.
- Usar `math`, `random` (com semente), `os`, `sys` e `time` no dia a dia.
- Escrever um programa de linha de comando com `argparse`, com opções, validação e
  código de saída.

## Por que isso importa

Até aqui todo o seu código cabia num arquivo. Programa de verdade não cabe. O
Validador de Certificados vai ter leitura de planilha, regras de tolerância, leitura
de e-mail, relatório e robô. Cada parte num arquivo, e os arquivos conversando entre
si por `import`. Saber organizar isso é o que separa "script que funciona no meu
computador" de "sistema que outra pessoa consegue manter".

A outra metade do módulo é a **biblioteca padrão**: tudo o que já vem com o Python,
sem instalar nada. Datas, estatística, contagens, sorteios, linha de comando. Muita
gente reinventa essas coisas (com bugs). Quem conhece a biblioteca padrão escreve
menos código e erra menos. Em entrevista de emprego, `Counter`, `defaultdict` e
`datetime` aparecem o tempo todo.

E tem o lado prático do mercado: `venv`, `pip`, `requirements.txt`, `pyproject.toml`
e Poetry estão em todo projeto Python profissional. Você vai sair deste módulo
entendendo o `pyproject.toml` que já existe no seu repositório.

## 1. Módulo: um arquivo `.py` que outro arquivo usa

Todo arquivo `.py` é um **módulo**. O nome do módulo é o nome do arquivo sem o
`.py`. Se você tem `conversoes_br.py`, outro arquivo na mesma pasta pode escrever
`import conversoes_br` e usar as funções de lá.

Pense na bancada do laboratório: o paquímetro fica numa gaveta, os padrões de
calibração em outra, as planilhas numa pasta. Você não espalha tudo na mesa. Módulos
são as gavetas do seu código.

Veja os dois arquivos da pasta `exemplos/`. Primeiro, o módulo com as funções:

```python
# exemplos/conversoes_br.py
def numero_br(texto: str) -> float:
    """Converte '1.250,5' em 1250.5."""
    return float(texto.strip().replace(".", "").replace(",", "."))


def formatar_br(valor: float, casas: int = 2) -> str:
    """Converte 1250.5 em '1.250,50'."""
    texto = f"{valor:,.{casas}f}"  # '1,250.50' (padrão americano)
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")
```

Depois, o script que usa o módulo:

```python
# exemplos/02_usando_conversoes.py
import conversoes_br
from conversoes_br import formatar_br

peso_total = conversoes_br.numero_br("1.250,5") + conversoes_br.numero_br("980,25")
print("Peso total da NF:", formatar_br(peso_total), "kg")
```

Rodando `python exemplos/02_usando_conversoes.py` (na pasta `curso-python`), a
saída é:

```text
[conversoes_br] carregado; __name__ = 'conversoes_br'
Peso total da NF: 2.230,75 kg
__name__ deste arquivo: __main__
__name__ do módulo importado: conversoes_br
```

A primeira linha vem de um `print` solto dentro de `conversoes_br.py`. Ela mostra
uma coisa importante: **importar um módulo executa o arquivo inteiro**, de cima para
baixo. As funções são criadas e qualquer código solto roda. Guarde isso, vamos usar
já já.

Por que separar em módulos?

- **Reaproveitar**: `numero_br` serve para a planilha, para o e-mail e para o
  relatório. Escreve uma vez, importa em três lugares.
- **Encontrar**: bug na conversão de número? Está em `conversoes_br.py`.
- **Testar**: os testes importam o módulo e conferem cada função isolada (é o que o
  `curso.py` faz com seus exercícios).

## 2. As formas de importar

São quatro formas. Todas funcionam; a escolha é sobre clareza.

```python
>>> import math
>>> math.sqrt(2)
1.4142135623730951
>>> import statistics as st
>>> st.mean([25.1, 24.9, 25.3])
25.1
>>> from datetime import date, timedelta
>>> date(2026, 10, 29) + timedelta(days=30)
datetime.date(2026, 11, 28)
>>> from random import Random as GeradorAleatorio
>>> GeradorAleatorio(42).randint(1, 6)
6
```

| Forma | Como usa depois | Quando usar |
|---|---|---|
| `import math` | `math.sqrt(2)` | Padrão. O prefixo diz de onde veio. |
| `import statistics as st` | `st.mean(...)` | Nome longo com apelido **consagrado** (`pandas as pd`). |
| `from datetime import date` | `date(...)` | Poucos nomes, usados muitas vezes. |
| `from x import a as b` | `b(...)` | Evitar conflito de nomes. |

Existe uma quinta forma, `from modulo import *`, que traz **tudo** de uma vez.
Evite. Você perde a noção de onde cada nome veio e pode sobrescrever nomes sem
perceber:

```python
>>> from os import *
>>> open("ensaios.csv")
Traceback (most recent call last):
  ...
TypeError: open() missing required argument 'flags' (pos 2)
```

O `os` tem uma função chamada `open`, diferente do `open` de sempre. O `import *`
trocou uma pela outra em silêncio.

### Ordem dos imports

Todo projeto profissional organiza os imports no topo do arquivo, em três blocos
separados por uma linha em branco:

```python
import csv  # 1) biblioteca padrão
from datetime import date

import openpyxl  # 2) bibliotecas instaladas (terceiros)

from validador.regras import aprovar  # 3) os seus módulos
```

Você não precisa decorar: o `ruff check --fix` (ou o `isort`, que está no seu
`pyproject.toml`) ordena sozinho.

### Importar executa uma vez só

> 🔮 **Preveja antes de rodar:** existe um arquivo `avisos.py` com estas linhas:
>
> ```python
> print("carregando avisos...")
> LIMITE_CV = 5.0
> ```
>
> E outro arquivo, na mesma pasta, faz:
>
> ```python
> import avisos
> import avisos
> print(avisos.LIMITE_CV)
> ```
>
> Quantas vezes aparece "carregando avisos..."?

<details><summary>Resposta</summary>

Uma vez só. A saída é:

```text
carregando avisos...
5.0
```

Na primeira vez, o Python executa o arquivo e guarda o módulo pronto num "cache"
chamado `sys.modules`. Nos imports seguintes, ele só devolve o que já está lá. Por
isso importar o mesmo módulo em dez arquivos não custa dez vezes.

</details>

> ⚠️ **Erro comum:** mudar o módulo com o REPL aberto e estranhar que nada mudou. O
> módulo já está no cache. Feche e abra o REPL de novo (ou rode o script de novo).

## 3. `if __name__ == "__main__":` — script e módulo ao mesmo tempo

Todo módulo tem uma variável automática chamada `__name__`:

- quando o arquivo é **rodado diretamente** (`python arquivo.py`), `__name__` vale
  `"__main__"`;
- quando o arquivo é **importado**, `__name__` vale o nome do módulo
  (`"conversoes_br"`).

Isso permite ter um trecho que só roda quando o arquivo é executado direto. O final
de `exemplos/conversoes_br.py` é assim:

```python
print(f"[conversoes_br] carregado; __name__ = {__name__!r}")

if __name__ == "__main__":
    # Só roda quando o arquivo é executado diretamente
    print(numero_br("1.250,5"))
    print(formatar_br(1250.5))
```

> 🔮 **Preveja antes de rodar:** o que aparece com
> `python exemplos/conversoes_br.py`? E o bloco do `if` roda quando o
> `02_usando_conversoes.py` importa esse módulo?

<details><summary>Resposta</summary>

Rodando direto:

```text
[conversoes_br] carregado; __name__ = '__main__'
1250.5
1.250,50
```

Importado pelo `02_usando_conversoes.py`, o `print` solto roda (com
`__name__ = 'conversoes_br'`), mas o bloco do `if` **não** roda, porque `__name__`
não é `"__main__"`. Foi o que vimos na seção 1.

</details>

Para que serve na prática:

- **Autoteste rápido**: um exemplo de uso no fim do módulo, sem atrapalhar quem
  importa.
- **Programas de linha de comando**: a função `main()` fica no módulo (e pode ser
  testada), e o `if` chama `main()` só quando você roda pelo terminal. Veremos na
  seção 15.

> 💡 **Dica:** regra de bolso para todo script: funções no corpo do arquivo, e
> **nenhum código solto** fora delas, exceto constantes e o bloco
> `if __name__ == "__main__":`. Assim, importar o arquivo nunca dispara efeitos
> inesperados (como apagar arquivos ou mandar e-mail).

> 🔧 **Modifique:** apague o `print` solto de `conversoes_br.py` e rode de novo o
> `02_usando_conversoes.py`. Agora o import fica silencioso, que é o comportamento
> esperado de um módulo bem-educado.

## 4. Onde o Python procura módulos

Quando você escreve `import conversoes_br`, o Python procura um arquivo
`conversoes_br.py` (ou uma pasta `conversoes_br/`) numa lista de pastas, **em ordem**.
Essa lista é o `sys.path`. Rode `python exemplos/03_onde_python_procura.py` para ver
a sua. No meu computador (Linux) saiu algo assim:

```text
Python em uso: /usr/bin/python3
Versão: 3.13.16

Pastas onde o import procura, em ordem:
  0: /home/user/estudos/curso-python/07-modulos-e-biblioteca-padrao/exemplos
  1: /usr/lib/python313.zip
  2: /usr/lib/python3.13
  3: /usr/lib/python3.13/lib-dynload
  4: /usr/local/lib/python3.13/dist-packages
```

No Windows, com o ambiente virtual ativado, você verá caminhos como
`C:\Users\voce\curso-python\.venv\Lib\site-packages`. Três coisas para entender:

1. **A posição 0 é a pasta do script que você rodou.** Por isso
   `02_usando_conversoes.py` acha `conversoes_br.py`: estão na mesma pasta.
2. Depois vêm as pastas da **biblioteca padrão** (`math`, `datetime`...).
3. Por último, a pasta **`site-packages`**: é onde o `pip install` coloca o que você
   instala (pandas, openpyxl...). Cada ambiente virtual tem a sua.

Daí saem os dois problemas mais comuns deste módulo.

**Problema 1: `ModuleNotFoundError`.** O Python percorreu a lista toda e não achou.
Causas típicas: o pacote não foi instalado **neste** Python (venv desativado!), o
nome está errado, ou você rodou o script de outra pasta e o módulo não está na pasta
do script.

**Problema 2: seu arquivo "esconde" um módulo da biblioteca.** Como a pasta do script
vem primeiro, um arquivo seu chamado `random.py`, `statistics.py`, `csv.py` ou
`email.py` é encontrado **antes** do módulo verdadeiro:

```text
Traceback (most recent call last):
  File "C:\Users\voce\testes\random.py", line 1, in <module>
    import random
  File "C:\Users\voce\testes\random.py", line 3, in <module>
    print(random.randint(1, 6))
          ^^^^^^^^^^^^^^
AttributeError: module 'random' has no attribute 'randint' (consider renaming
'C:\Users\voce\testes\random.py' since it has the same name as the standard library
module named 'random' and prevents importing that standard library module)
```

O Python 3.13 até sugere renomear. No 3.12 a mensagem é mais enigmática:
`partially initialized module 'random' has no attribute 'randint' (most likely due to a
circular import)`. Mesma causa: seu arquivo se chama `random.py`. Renomeie para
`sorteio_bobinas.py` e apague a pasta `__pycache__` ao lado, se existir.

> ⚠️ **Erro comum:** dar ao seu arquivo o nome do assunto que você está estudando.
> `statistics.py`, `datetime.py`, `pandas.py` e `openpyxl.py` são os campeões.

### Rodar como módulo: `python -m`

Você já usou `python -m pip` e `python -m pytest`. O `-m` quer dizer "procure este
**módulo** no `sys.path` e rode-o como programa". Diferença prática: com `-m`, a
posição 0 do `sys.path` passa a ser a **pasta atual** do terminal, não a pasta do
arquivo. Isso vai importar para pacotes (próxima seção).

> 💡 **Dica:** `python -m pip install ...` garante que o `pip` usado é o do mesmo
> Python que vai rodar o seu código. Com `pip install ...` puro, no Windows, às vezes
> o `pip` é de outra instalação. Prefira sempre `python -m pip`.

## 5. Pacotes: pastas com `__init__.py`

Quando os módulos crescem, você os agrupa numa **pasta**. Uma pasta de módulos com um
arquivo `__init__.py` é um **pacote**. A pasta `exemplos/labqualidade/` é um pacote
pequeno, feito para você abrir e ler:

```text
exemplos/
├── 04_usando_pacote.py
└── labqualidade/
    ├── __init__.py       # transforma a pasta em pacote; define a "vitrine"
    ├── __main__.py       # roda com: python -m labqualidade
    ├── conversoes.py     # numero_br, data_br
    ├── estatistica.py    # cv_percentual, resumo
    └── tolerancias.py    # faixa_nominal, dentro_da_faixa
```

Com o pacote, os imports ganham um ponto: `pacote.modulo`.

```python
import labqualidade.tolerancias
from labqualidade.tolerancias import dentro_da_faixa
from labqualidade import faixa_nominal  # direto do pacote: veja o __init__.py
```

### O `__init__.py`

Ele roda uma vez, no primeiro `import labqualidade`. Pode ficar vazio (só para
marcar a pasta como pacote), mas costuma servir de **vitrine**: ele traz para o
nível do pacote as funções que quem usa precisa conhecer.

```python
# exemplos/labqualidade/__init__.py
from .conversoes import data_br, numero_br
from .estatistica import cv_percentual, resumo
from .tolerancias import dentro_da_faixa, faixa_nominal

__version__ = "0.1.0"

__all__ = [
    "cv_percentual",
    "data_br",
    "dentro_da_faixa",
    "faixa_nominal",
    "numero_br",
    "resumo",
]
```

- O **ponto** em `from .conversoes import ...` é um **import relativo**: "o módulo
  `conversoes` que está neste mesmo pacote". Dois pontos (`..`) sobem um nível.
- `__all__` lista o que é público. Ele define o que sai num `from labqualidade import *`
  e documenta a vitrine para quem lê.
- `__version__` é uma convenção para a versão do pacote.

Rodando `python exemplos/04_usando_pacote.py`:

```text
labqualidade versão 0.1.0
Faixa: 22.5 a 27.5 µm
   25.1 µm -> ok
   24.8 µm -> ok
   27.9 µm -> FORA
   25.3 µm -> ok
Resumo: {'n': 4, 'media': 25.775, 'desvio': 1.431, 'cv': 5.55}
Na vitrine (__all__): ['cv_percentual', 'data_br', 'dentro_da_faixa', 'faixa_nominal', 'numero_br', 'resumo']
```

E o `__main__.py` permite rodar o pacote inteiro como programa. Entre na pasta
`exemplos` e rode `python -m labqualidade`:

```text
labqualidade 0.1.0
Faixa de 25 µm ± 10%: (22.5, 27.5)
Resumo: {'n': 4, 'media': 25.025, 'desvio': 0.222, 'cv': 0.89}
```

> ⚠️ **Erro comum:** rodar um arquivo de dentro do pacote diretamente, como
> `python exemplos/labqualidade/estatistica.py`, quando ele usa import relativo. O
> Python não sabe que o arquivo pertence a um pacote e reclama:
> `ImportError: attempted relative import with no known parent package`. Rode pelo
> pacote (`python -m labqualidade`, de dentro de `exemplos`) ou por um script de fora.

> 💡 **Dica:** uma pasta **sem** `__init__.py` às vezes também importa (é um
> "namespace package", recurso avançado). Não conte com isso: pacote seu sempre leva
> `__init__.py`, nem que seja vazio.

> 🔧 **Modifique:** crie `exemplos/labqualidade/datas.py` com uma função
> `dias_entre(inicio, fim)` que devolve `(fim - inicio).days`. Exporte-a no
> `__init__.py` e use-a no `04_usando_pacote.py`. Se der `ImportError`, leia a
> mensagem: ela diz exatamente qual nome não foi encontrado em qual módulo.

## 6. Estrutura de projeto profissional: o src layout

O projeto final vai virar um repositório no seu GitHub. A estrutura que o mercado
usa (e que o Poetry cria por padrão) é o **src layout**:

```text
validador-certificados/
├── pyproject.toml            # nome, versão, dependências, configurações
├── poetry.lock               # versões exatas instaladas (gerado pelo Poetry)
├── README.md                 # o que é, como instalar, como usar
├── .gitignore                # .venv/, __pycache__/, saida/ ...
├── src/
│   └── validador/            # o PACOTE (o código de verdade)
│       ├── __init__.py
│       ├── __main__.py       # python -m validador
│       ├── cli.py            # argparse e main()
│       ├── planilha.py       # leitura das 4 abas
│       ├── regras.py         # tolerâncias
│       └── expedicao.py      # leitura dos e-mails
└── tests/
    ├── test_regras.py
    └── test_expedicao.py
```

Por que o pacote fica dentro de `src/` e não na raiz?

- **Obriga a instalar o pacote** antes de usar (`poetry install` ou
  `pip install -e .`). Assim os testes rodam contra o pacote **instalado**, do jeito
  que o usuário vai receber. Se faltar um arquivo na instalação, o teste pega.
- **Evita importar sem querer** a pasta errada só porque o terminal estava nela.
- **Separa** código do produto de testes, documentação e scripts soltos.

O `pip install -e .` (o "e" é de *editable*) instala o pacote apontando para a sua
pasta: você edita o código e a mudança vale na hora, sem reinstalar. O Poetry faz o
mesmo no `poetry install`.

Um `pyproject.toml` mínimo para esse projeto, no formato do Poetry 2:

```toml
[project]
name = "validador-certificados"
version = "0.1.0"
description = "Confere ensaios com as tolerâncias e prepara certificados de qualidade"
authors = [{ name = "Carlos Eduardo" }]
readme = "README.md"
requires-python = ">=3.12"
dependencies = ["openpyxl (>=3.1,<4)"]

[project.scripts]
validador = "validador.cli:main"   # cria o comando "validador" no terminal

[tool.poetry]
packages = [{ include = "validador", from = "src" }]

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

A seção `[project.scripts]` é um bônus: depois do `poetry install`, o comando
`validador` passa a existir no ambiente e chama a função `main()` de
`src/validador/cli.py`. Eu conferi esse fluxo com o Poetry 2.4.

> 💡 **Dica:** compare com o seu repositório `estudos`: lá o código está em `src/main.py`
> (um script, não um pacote) e o `pyproject.toml` tem `package-mode = false`. Isso
> diz ao Poetry: "só gerencie as dependências, não há pacote para instalar". Para
> estudos está ótimo. Para o projeto final, você vai querer o pacote.

## 7. Ambiente virtual e pip a fundo

Você viu o básico no módulo 00. Agora com calma, porque é aqui que mora metade dos
"no meu computador funciona".

### O problema

Seu computador tem **um** Python instalado e vários projetos. O projeto A precisa de
`pandas 2.2`; o projeto B, de `pandas 3.0`. Se tudo for instalado no mesmo lugar, um
quebra o outro. O **ambiente virtual** (venv) é uma pasta com uma cópia leve do
Python e um `site-packages` **só daquele projeto**.

### Criar, ativar, desativar (Windows, PowerShell)

```powershell
cd C:\Users\voce\curso-python
python -m venv .venv                 # cria a pasta .venv
.venv\Scripts\activate               # ativa (o prompt ganha "(.venv)")
python -m pip install -r requirements.txt
deactivate                           # desativa
```

- Se o PowerShell disser que a execução de scripts está desabilitada, rode uma vez:
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.
- No `cmd` antigo: `.venv\Scripts\activate.bat`.
- No Linux/macOS: `python3 -m venv .venv` e `source .venv/bin/activate`.
- Tem mais de uma versão de Python no Windows? `py -3.12 -m venv .venv` escolhe a versão.

### Qual Python está rodando?

A pergunta que resolve 80% dos problemas de instalação:

```powershell
python -c "import sys; print(sys.executable)"
```

Com o venv ativado, a resposta tem que ser algo como
`C:\Users\voce\curso-python\.venv\Scripts\python.exe`. Se aparecer outro caminho,
você está instalando num Python e rodando em outro. No VS Code, escolha o mesmo
interpretador em "Python: Select Interpreter" (`Ctrl+Shift+P`).

### pip: os comandos que você vai usar

```powershell
python -m pip install openpyxl               # instala a versão mais nova
python -m pip install "pandas>=2.2,<4"       # com restrição de versão (aspas!)
python -m pip install -U openpyxl            # atualiza
python -m pip uninstall openpyxl             # remove
python -m pip list                           # o que está instalado
python -m pip list --outdated                # o que tem versão nova
python -m pip show openpyxl                  # detalhes: versão, dependências, local
python -m pip freeze > requirements.txt      # "foto" exata do ambiente
python -m pip install -r requirements.txt    # recria o ambiente a partir da foto
```

> ⚠️ **Erro comum:** no PowerShell, `pip install pandas>=2.2` sem aspas cria um
> arquivo chamado `=2.2`! O `>` é redirecionamento no terminal. Use aspas sempre que
> houver `<` ou `>`.

### Restrições de versão

| Escrita | Significa |
|---|---|
| `openpyxl==3.1.5` | exatamente essa versão |
| `openpyxl>=3.1` | 3.1 ou mais nova |
| `openpyxl>=3.1,<4` | da 3.1 até antes da 4 (o mais comum em bibliotecas) |
| `openpyxl~=3.1.2` | "compatível": `>=3.1.2` e `<3.2` |

### `requirements.txt`: duas filosofias

- **Escrito à mão**, com faixas (`pandas>=2.2`): é o que o curso usa. Diz o que o
  projeto **precisa**.
- **Gerado com `pip freeze`**, com versões exatas (`pandas==2.2.3`), incluindo as
  dependências das dependências: é uma **foto** para reproduzir o ambiente igualzinho
  (bom para colocar um robô em produção).

Um padrão comum é separar o que vai para produção do que é só de desenvolvimento:

```text
# requirements-dev.txt
-r requirements.txt     # inclui o outro arquivo
pytest>=8.0
ruff>=0.6
```

> 💡 **Dica:** a pasta `.venv` **nunca** vai para o Git (ela tem centenas de MB e é
> específica do seu computador). O `.gitignore` do curso já a ignora. O que vai para o
> Git é a receita: `requirements.txt` ou `pyproject.toml` + `poetry.lock`.

## 8. Poetry: o gerenciador que já está no seu repositório

O pip instala pacotes. O **Poetry** gerencia o projeto inteiro: cria o venv,
instala, registra no `pyproject.toml` o que você adicionou, trava as versões exatas
no `poetry.lock` e roda comandos dentro do ambiente.

### Lendo o `pyproject.toml` que você já tem

Este é o arquivo da raiz do seu repositório `estudos`:

```toml
[tool.poetry]
name = "estudos"
version = "1.0.0"
description = "Apenas arquivo de estudos"
authors = ["Carlos Eduardo"]
license = "MIT"
readme = "README.md"
package-mode = false

[tool.poetry.dependencies]
python = ">=3.10"
black = ">=25.1.0,<26.0.0"
isort = ">=6.0.1,<7.0.0"
pylint = ">=3.3.7,<4.0.0"
flake8 = ">=7.3.0,<8.0.0"
pytest = ">=8.4.1,<9.0.0"
python-dotenv = ">=1.1.1,<2.0.0"

[tool.poetry.group.dev.dependencies]

[tool.black]
line-length = 95
...
```

Linha a linha:

- `[tool.poetry]`: dados do projeto. `package-mode = false` = só dependências, sem
  pacote (seção 6).
- `[tool.poetry.dependencies]`: o que o projeto precisa, com faixas de versão.
  `python = ">=3.10"` diz quais versões do Python servem.
- `[tool.poetry.group.dev.dependencies]`: o grupo de **desenvolvimento** (testes,
  formatadores). Está vazio, e as ferramentas `black`, `isort`, `pylint`, `flake8` e
  `pytest` estão nas dependências principais. Funciona, mas o certo é elas ficarem no
  grupo `dev`: quem só usa o programa não precisa delas.
- `[tool.black]` e `[tool.isort]`: configuração das ferramentas. O `pyproject.toml`
  virou o lugar padrão para isso.
- `[build-system]`: como construir o pacote (o `poetry-core`).

> 💡 **Dica:** projetos novos do Poetry 2 usam a seção padrão `[project]` (como no
> exemplo da seção 6), que outras ferramentas também entendem. O formato antigo, só com
> `[tool.poetry]`, continua funcionando.

### Os comandos do dia a dia

```powershell
poetry install                      # cria o venv e instala tudo do poetry.lock
poetry add openpyxl                 # adiciona dependência (e atualiza o lock)
poetry add --group dev pytest ruff  # adiciona no grupo de desenvolvimento
poetry remove flake8                # remove
poetry show --tree                  # dependências e de quem cada uma depende
poetry run python src/main.py       # roda DENTRO do venv do projeto
poetry run pytest                   # idem para os testes
poetry lock                         # recalcula o poetry.lock
poetry env info --path              # onde está o venv
poetry check                        # confere se o pyproject.toml está válido
```

Para **ativar** o venv do Poetry no terminal, o Poetry 2 trocou o antigo
`poetry shell` por `poetry env activate`, que **mostra** o comando de ativação. No
PowerShell, rode: `Invoke-Expression (poetry env activate)`.

> 💡 **Dica:** `poetry config virtualenvs.in-project true` faz o Poetry criar o venv
> numa pasta `.venv` dentro do projeto. O VS Code acha sozinho e você sabe sempre onde
> ele está.

Para arrumar o seu `pyproject.toml`, movendo as ferramentas para o grupo de
desenvolvimento:

```powershell
poetry remove black isort pylint flake8 pytest
poetry add --group dev black isort pylint flake8 pytest
```

No seu arquivo, o Poetry grava a seção `[tool.poetry.group.dev.dependencies]`
(conferi com uma cópia do seu projeto). Em projetos criados no formato novo, versões
recentes do Poetry gravam numa seção `[dependency-groups]`. O efeito é o mesmo.

### `poetry.lock`: por que ele existe

O `pyproject.toml` diz "openpyxl entre 3.1 e 4". O `poetry.lock` diz "openpyxl
**3.1.5**, et-xmlfile **2.0.0**", com tudo resolvido. Quem clonar o projeto e rodar
`poetry install` recebe exatamente as mesmas versões. **Faça commit do
`poetry.lock`** (você já fez: ele está no repositório).

### pip, Poetry ou uv?

| Ferramenta | O que faz | Quando |
|---|---|---|
| `venv` + `pip` + `requirements.txt` | o básico, vem com o Python | scripts, cursos, robôs simples |
| Poetry | projeto completo: dependências, lock, grupos, build | projetos e portfólio |
| uv | o mesmo que o Poetry, muito mais rápido | cada vez mais comum no mercado |

Saber `venv` + `pip` é obrigatório. Poetry (ou uv) é o próximo passo, e os conceitos
são os mesmos: ambiente isolado, lista de dependências, lock.

## 9. Datas e prazos com `datetime`

O módulo `datetime` tem três tipos que você vai usar sempre:

- `date`: uma data (dia, mês, ano). Ex.: data de emissão do laudo.
- `datetime`: data **e** hora. Ex.: início do ensaio de tração.
- `timedelta`: uma **duração** (dias, horas, minutos). Ex.: validade de 180 dias.

```python
>>> from datetime import date, datetime, timedelta
>>> emissao = date(2026, 10, 29)
>>> emissao.year, emissao.month, emissao.day
(2026, 10, 29)
>>> emissao.weekday()
3
>>> emissao + timedelta(days=180)
datetime.date(2027, 4, 27)
>>> date(2027, 4, 27) - emissao
datetime.timedelta(days=180)
>>> (date(2027, 4, 27) - emissao).days
180
>>> date(2026, 11, 2) > emissao
True
```

- `weekday()` devolve 0 para segunda e 6 para domingo. A quinta-feira é 3.
- **data + timedelta = data**; **data − data = timedelta**; datas se comparam com
  `<`, `>`, `==`.
- `date.today()` devolve a data de hoje e `datetime.now()` o instante atual. Eles
  mudam a cada execução, por isso os exercícios recebem `hoje` como parâmetro.

### Texto ↔ data no formato brasileiro

A planilha e o e-mail trazem texto. Para fazer contas, converta com `strptime`
("string **p**arse time"); para mostrar, volte com `strftime` ("string **f**ormat
time"):

```python
>>> from datetime import date, datetime
>>> datetime.strptime("29/10/2026", "%d/%m/%Y")
datetime.datetime(2026, 10, 29, 0, 0)
>>> datetime.strptime("29/10/2026", "%d/%m/%Y").date()
datetime.date(2026, 10, 29)
>>> datetime.strptime("28/10/2026 14:30", "%d/%m/%Y %H:%M")
datetime.datetime(2026, 10, 28, 14, 30)
>>> date(2026, 3, 5).strftime("%d/%m/%Y")
'05/03/2026'
>>> f"{date(2026, 3, 5):%d/%m/%Y}"
'05/03/2026'
>>> date.fromisoformat("2026-10-29")
datetime.date(2026, 10, 29)
```

| Código | Significa | Exemplo |
|---|---|---|
| `%d` | dia com 2 dígitos | `05` |
| `%m` | mês com 2 dígitos | `03` |
| `%Y` | ano com 4 dígitos | `2026` |
| `%H:%M` | hora e minuto (24 h) | `14:30` |
| `%A` | nome do dia **no idioma do sistema** | `Thursday` (cuidado!) |

O formato `"2026-10-29"` é o **ISO 8601**: o padrão internacional (e o que bancos de
dados usam). O `fromisoformat` lê esse formato direto.

> ⚠️ **Erro comum:** confiar no `%A` para o nome do dia. No seu Windows em português
> pode sair "quinta-feira"; no servidor da empresa, "Thursday". Use uma lista:
> `["segunda", "terça", ...][data.weekday()]`.

> ⚠️ **Erro comum:** `from datetime import datetime` e depois `datetime.date(2026, 1, 1)`.
> Aqui `datetime` é a **classe**, não o módulo, e `datetime.date` é um método dela. O
> erro é confuso: `TypeError: descriptor 'date' for 'datetime.datetime' objects doesn't
> apply to a 'int' object`. Importe os dois tipos: `from datetime import date, datetime`.

### Não existe "somar um mês"

`timedelta` aceita `days`, `weeks`, `hours`, `minutes`, `seconds`, mas **não** meses
nem anos, porque meses têm tamanhos diferentes. Por isso validades e prazos costumam
ser definidos em dias.

> 🔮 **Preveja antes de rodar:** qual data sai?
>
> ```python
> from datetime import date, timedelta
> print(date(2026, 1, 31) + timedelta(days=30))
> ```

<details><summary>Resposta</summary>

`2026-03-02`. Janeiro tem 31 dias e fevereiro de 2026 tem 28: 30 dias depois de
31/01 caem em 02/03, e não "no fim de fevereiro". Quem pensa "um mês depois" erra o
prazo. Se a regra do cliente for "mesmo dia do mês seguinte", você precisa de uma
função própria (ou da biblioteca `python-dateutil`).

</details>

### Exemplo resolvido: validade do laudo

**Problema:** o laudo vale 180 dias a partir da emissão. Dada a emissão e a data de
hoje, quero saber se ainda vale e quantos dias faltam.

**Como eu pensei:**

1. "Vale até quando?" é uma conta: emissão + 180 dias. Isso é `timedelta`.
2. "Ainda vale?" é uma comparação: hoje <= vencimento. No dia do vencimento ainda vale
   (confirme essa regra com a qualidade; regra de negócio não se adivinha).
3. "Quantos dias faltam?" é uma subtração de datas, que dá um `timedelta`; o número
   está em `.days`.
4. Não vou usar `date.today()` dentro da função: recebo `hoje` como parâmetro. Assim
   consigo testar com qualquer data.

```python
>>> from datetime import date, timedelta
>>> def situacao_laudo(emissao, hoje, validade_dias=180):
...     vencimento = emissao + timedelta(days=validade_dias)
...     faltam = (vencimento - hoje).days
...     if faltam < 0:
...         return f"VENCIDO há {-faltam} dias (venceu em {vencimento:%d/%m/%Y})"
...     return f"válido por mais {faltam} dias (até {vencimento:%d/%m/%Y})"
...
>>> situacao_laudo(date(2026, 10, 29), date(2027, 4, 20))
'válido por mais 7 dias (até 27/04/2027)'
>>> situacao_laudo(date(2026, 10, 29), date(2027, 5, 1))
'VENCIDO há 4 dias (venceu em 27/04/2027)'
```

> 🔧 **Modifique:** acrescente o caso "vence hoje" (quando `faltam == 0`) com uma
> mensagem própria. Teste com `date(2027, 4, 27)`.

### Exemplo resolvido: prazo em dias úteis

**Problema:** o certificado deve sair em até 5 dias úteis depois da NF. Dias úteis =
segunda a sexta, menos feriados.

**Como eu pensei:** não existe "somar dias úteis" pronto. Mas eu sei andar um dia
(`+ timedelta(days=1)`) e sei perguntar se um dia é útil (`weekday() < 5` e não está
na lista de feriados). Então: ando um dia de cada vez e só conto os úteis, até chegar
a 5. Primeiro avanço, depois testo: o dia da NF não conta.

```python
>>> from datetime import date, timedelta
>>> def somar_dias_uteis(inicio, dias, feriados=None):
...     feriados = feriados or set()
...     atual = inicio
...     contados = 0
...     while contados < dias:
...         atual += timedelta(days=1)
...         if atual.weekday() < 5 and atual not in feriados:
...             contados += 1
...     return atual
...
>>> nf = date(2026, 10, 29)
>>> somar_dias_uteis(nf, 5)
datetime.date(2026, 11, 5)
>>> somar_dias_uteis(nf, 5, {date(2026, 11, 2)})
datetime.date(2026, 11, 6)
```

Repare em `feriados=None` e `feriados = feriados or set()`: é o jeito seguro de ter um
padrão "vazio" sem cair na armadilha do default mutável (módulo 04). O exercício 09
mostra o que acontece quando a ordem "avança, depois testa" é invertida.

O script `exemplos/05_datas_e_prazos.py` junta tudo isso; rode e leia.

## 10. `collections`: Counter, defaultdict e namedtuple

O módulo `collections` tem versões "turbinadas" de dicionário e tupla para tarefas
muito comuns.

### `Counter`: contar sem `if`

Você já contou coisas com dicionário e `if chave in contagem` (módulo 03). O
`Counter` faz isso numa linha:

```python
>>> from collections import Counter
>>> reprovacoes = Counter(["C", "B", "C", "A", "C", "B"])
>>> reprovacoes
Counter({'C': 3, 'B': 2, 'A': 1})
>>> reprovacoes["C"]
3
>>> reprovacoes["D"]
0
>>> reprovacoes.most_common(2)
[('C', 3), ('B', 2)]
>>> reprovacoes.update(["D", "C"])
>>> reprovacoes
Counter({'C': 4, 'B': 2, 'A': 1, 'D': 1})
>>> reprovacoes.total()
8
```

- Chave ausente vale **0** (não dá `KeyError`).
- `most_common(n)` devolve os `n` mais frequentes, do maior para o menor; empates
  ficam na ordem em que apareceram.
- `update` soma novas contagens; `total()` (Python 3.10+) soma tudo.

Com uma expressão geradora (a compreensão sem colchetes, módulo 03), você conta direto
de uma lista de dicionários:

```python
>>> from collections import Counter
>>> ensaios = [
...     {"linha": "A", "resultado": "aprovado"},
...     {"linha": "C", "resultado": "reprovado"},
...     {"linha": "C", "resultado": "reprovado"},
...     {"linha": "B", "resultado": "reprovado"},
... ]
>>> Counter(e["linha"] for e in ensaios if e["resultado"] == "reprovado")
Counter({'C': 2, 'B': 1})
```

### `defaultdict`: agrupar sem testar a chave

Agrupar OPs por linha com `dict` comum exige o teste "a chave já existe?". O
`defaultdict` cria o valor inicial sozinho, chamando a função que você passou:

```python
>>> from collections import defaultdict
>>> ops_por_linha = defaultdict(list)
>>> for op, linha in [("OP1", "A"), ("OP2", "C"), ("OP3", "A")]:
...     ops_por_linha[linha].append(op)
...
>>> dict(ops_por_linha)
{'A': ['OP1', 'OP3'], 'C': ['OP2']}
>>> peso_por_nf = defaultdict(float)
>>> for nf, peso in [("123456", 1250.5), ("123457", 980.0), ("123456", 310.25)]:
...     peso_por_nf[nf] += peso
...
>>> dict(peso_por_nf)
{'123456': 1560.75, '123457': 980.0}
```

Passe o **nome** do tipo, sem parênteses: `defaultdict(list)` (lista vazia),
`defaultdict(int)` (zero), `defaultdict(float)` (0.0), `defaultdict(set)`.

> 🔮 **Preveja antes de rodar:**
>
> ```python
> from collections import defaultdict
> grupos = defaultdict(list)
> print("Z" in grupos)
> if grupos["Z"]:
>     print("tem coisa no Z")
> print("Z" in grupos)
> print(dict(grupos))
> ```

<details><summary>Resposta</summary>

```text
False
True
{'Z': []}
```

Só **ler** `grupos["Z"]` já cria a chave com uma lista vazia. Por isso: para
consultar, use `in` ou `.get()`; e devolva `dict(grupos)` para quem usa a sua função
não levar esse susto.

</details>

### `namedtuple`: tupla com nome nos campos

`m[2]` não diz nada. `m.valor` diz tudo. A `namedtuple` cria um "tipo de tupla" com
campos nomeados:

```python
>>> from collections import namedtuple
>>> Medicao = namedtuple("Medicao", ["op", "ensaio", "valor"])
>>> m = Medicao("OP245101", "espessura", 25.3)
>>> m
Medicao(op='OP245101', ensaio='espessura', valor=25.3)
>>> m.valor, m[2]
(25.3, 25.3)
>>> op, ensaio, valor = m
>>> m._replace(valor=25.1)
Medicao(op='OP245101', ensaio='espessura', valor=25.1)
>>> m._asdict()
{'op': 'OP245101', 'ensaio': 'espessura', 'valor': 25.3}
```

Continua sendo tupla: imutável, desempacota, cabe em `set` e serve de chave de
dicionário. Para mudar um valor, `_replace` cria **outra** tupla. Quando você
precisar de validação e métodos, a ferramenta é a `dataclass`, do módulo 08.

> 💡 **Dica:** o acesso com ponto (`m.valor`) é o mesmo jeito de pegar atributos de
> qualquer **objeto**. Você vai ver isso de novo no `argparse` (`args.linha`) e vai
> entender a fundo no módulo 08.

## 11. `itertools`: chain e groupby

`itertools` tem ferramentas para percorrer sequências. Elas devolvem **iteradores**:
objetos que entregam os itens um de cada vez, sob demanda, sem montar a lista toda
na memória. Para ver o conteúdo, passe por `list()` ou percorra com `for`.

### `chain`: emendar sequências

```python
>>> from itertools import chain
>>> email_1 = [("OP1", "123456", 1250.5)]
>>> email_2 = [("OP2", "123457", 980.0), ("OP3", "123457", 410.0)]
>>> list(chain(email_1, email_2))
[('OP1', '123456', 1250.5), ('OP2', '123457', 980.0), ('OP3', '123457', 410.0)]
>>> abas = {"A": [20.1, 19.8], "B": [25.2], "C": [40.3, 39.9]}
>>> list(chain.from_iterable(abas.values()))
[20.1, 19.8, 25.2, 40.3, 39.9]
```

`chain(a, b, c)` emenda as sequências que você passa; `chain.from_iterable(x)` emenda
as sequências **de dentro** de `x` (uma lista de listas, os valores de um dicionário).

### `groupby`: agrupar vizinhos

`groupby` percorre a sequência e junta os itens **vizinhos** que têm a mesma chave.
Para cada grupo, ele entrega a chave e um iterador com os itens:

```python
>>> from itertools import groupby
>>> resultados = ["A", "A", "R", "R", "R", "A"]
>>> [(chave, len(list(grupo))) for chave, grupo in groupby(resultados)]
[('A', 2), ('R', 3), ('A', 1)]
```

> 🔮 **Preveja antes de rodar:** quantos grupos saem?
>
> ```python
> from itertools import groupby
> lotes = ["L02", "L01", "L02"]
> print([(lote, len(list(g))) for lote, g in groupby(lotes)])
> ```

<details><summary>Resposta</summary>

Três grupos: `[('L02', 1), ('L01', 1), ('L02', 1)]`. O `groupby` **não** procura
iguais na lista inteira; ele só junta vizinhos. Para agrupar por lote, **ordene pela
mesma chave antes**: `groupby(sorted(lotes))` dá `[('L01', 1), ('L02', 2)]`.

</details>

Com `key=`, você escolhe por qual informação agrupar (a mesma ideia do `key=` do
`sorted`, módulo 04):

```python
>>> from itertools import groupby
>>> bobinas = [("L02", 150.0), ("L01", 120.5), ("L02", 149.5), ("L01", 121.0)]
>>> def lote(bobina):
...     return bobina[0]
...
>>> for nome, grupo in groupby(sorted(bobinas, key=lote), key=lote):
...     pesos = [peso for _, peso in grupo]
...     print(nome, len(pesos), sum(pesos))
...
L01 2 241.5
L02 2 299.5
```

> ⚠️ **Erro comum:** ler o `grupo` duas vezes. Ele é um iterador: depois de
> percorrido, fica vazio. Se precisar usar mais de uma vez, guarde numa lista:
> `itens = list(grupo)`.

> 💡 **Dica:** quando quiser agrupar a lista **inteira** (e não só vizinhos), o
> `defaultdict(list)` costuma ser mais simples. O `groupby` brilha em sequências que
> já vêm em ordem: produção ao longo do turno, registros por data, resultados
> seguidos.

Outras ferramentas de `itertools` que valem conhecer pelo nome: `islice` (fatiar um
iterador), `pairwise` (pares vizinhos: bom para "variação entre medições
seguidas"), `product` e `combinations` (combinações para planejar ensaios).

### Exemplo resolvido: a maior sequência de reprovações

**Problema:** a máquina da linha C reprovou várias bobinas seguidas? Qual foi a maior
sequência de "R"?

**Como eu pensei:** "sequência seguida" = "vizinhos iguais" = `groupby`. Para cada
grupo, guardo o tamanho só se a chave for "R". No fim, pego o maior. E se não houver
nenhum "R"? `max` de lista vazia dá erro, então uso `max(..., default=0)`.

```python
>>> from itertools import groupby
>>> def maior_sequencia(resultados, alvo="R"):
...     tamanhos = [len(list(g)) for valor, g in groupby(resultados) if valor == alvo]
...     return max(tamanhos, default=0)
...
>>> maior_sequencia(["A", "R", "R", "A", "R", "R", "R", "A"])
3
>>> maior_sequencia(["A", "A"])
0
```

## 12. `statistics`: a estatística do laboratório

O módulo `statistics` tem as contas que o laboratório faz todo dia, sem instalar
nada:

```python
>>> import statistics
>>> espessuras = [25.1, 24.8, 25.3, 24.9, 25.4, 25.0]
>>> round(statistics.mean(espessuras), 3)
25.083
>>> statistics.median(espessuras)
25.05
>>> round(statistics.stdev(espessuras), 3)
0.232
>>> round(statistics.pstdev(espessuras), 3)
0.211
>>> statistics.mode(["A", "C", "A", "B"])
'A'
>>> [round(q, 3) for q in statistics.quantiles(espessuras, n=4)]
[24.875, 25.05, 25.325]
```

| Python | Excel (português) | O que é |
|---|---|---|
| `statistics.mean` | `MÉDIA` | média aritmética |
| `statistics.median` | `MED` | valor do meio (com dados em ordem) |
| `statistics.stdev` | `DESVPAD.A` (ou `DESVPAD`) | desvio padrão **amostral** (divide por n − 1) |
| `statistics.pstdev` | `DESVPAD.P` | desvio padrão **populacional** (divide por n) |
| `statistics.mode` | `MODO` | valor mais frequente |
| `statistics.quantiles(x, n=4)` | `QUARTIL` | quartis (o método padrão é parecido com `QUARTIL.EXC`) |

**Qual desvio usar?** No laboratório você mede uma **amostra** (6 pontos da bobina,
não a bobina inteira). Então o certo, em geral, é o **amostral**: `stdev`, o mesmo
`DESVPAD` padrão do Excel. Se o seu laudo antigo usava `DESVPAD.P`, os números vão
diferir um pouco; isso não é erro do Python, é a fórmula.

**Coeficiente de variação (CV%)**: o desvio em relação à média.
`CV% = desvio / média × 100`. Ele permite comparar a uniformidade de coisas com
tamanhos diferentes: um desvio de 0,5 µm é muito para um filme de 12 µm e pouco para
um de 100 µm.

```python
>>> import statistics
>>> espessuras = [25.1, 24.8, 25.3, 24.9, 25.4, 25.0]
>>> round(statistics.stdev(espessuras) / statistics.mean(espessuras) * 100, 2)
0.92
```

> 🔮 **Preveja antes de rodar:** alguém digitou 52 em vez de 25,2. O que muda mais, a
> média ou a mediana?
>
> ```python
> import statistics
> com_erro = [25.1, 24.8, 25.3, 24.9, 25.4, 25.0, 52.0]
> print(round(statistics.mean(com_erro), 2), statistics.median(com_erro))
> ```

<details><summary>Resposta</summary>

`28.93 25.1`. A média pulou de 25,08 para 28,93; a mediana quase não mexeu (de 25,05
para 25,1). A mediana é **robusta** a valores estranhos. Quando a média e a mediana
estão muito diferentes, desconfie de erro de digitação ou de medição.

</details>

> ⚠️ **Erro comum:** chamar `stdev` com um valor só. Não existe variação com um
> ponto: `statistics.StatisticsError: stdev requires at least two data points` (no
> Python 3.10 a mensagem fala em `variance`). O `StatisticsError` é um tipo de
> `ValueError`, então `except ValueError` também o captura.

### Exemplo resolvido: CV% por linha de produção

**Problema:** a partir do arquivo `dados/ensaios_linhas.csv`, quero o CV% da
espessura de cada linha, para ver qual está instável.

**Como eu pensei:** decompus em etapas que eu já sei fazer:

1. Ler o CSV com `;` (módulo 06) e converter o valor "20,4" em número (módulo 05).
2. Ficar só com a espessura.
3. Agrupar os valores por linha: `defaultdict(list)`.
4. Para cada linha, em ordem: média, desvio, CV.

```python
import csv
import statistics
from collections import defaultdict

valores = defaultdict(list)
with open("dados/ensaios_linhas.csv", encoding="utf-8", newline="") as arquivo:
    for registro in csv.DictReader(arquivo, delimiter=";"):
        if registro["ensaio"] == "espessura":
            valores[registro["linha"]].append(float(registro["valor"].replace(",", ".")))

for linha in sorted(valores):
    media = statistics.mean(valores[linha])
    cv = statistics.stdev(valores[linha]) / media * 100
    print(f"Linha {linha}: média {media:.2f} µm, CV {cv:.2f}%")
```

Saída:

```text
Linha A: média 19.60 µm, CV 1.99%
Linha B: média 25.38 µm, CV 3.08%
Linha C: média 41.68 µm, CV 6.44%
Linha D: média 59.48 µm, CV 1.64%
```

A linha C se destaca. Esse é o coração do exemplo "No mundo real" deste módulo.

> 🔧 **Modifique:** troque `"espessura"` por `"cof"`. Os CVs ficam bem maiores. Isso
> quer dizer que o COF está ruim? Não necessariamente: cada ensaio tem a sua
> variabilidade natural, e o limite de CV deve ser definido **por ensaio**.

## 13. `math` e `random`

### `math`: as contas que faltam nos operadores

```python
>>> import math
>>> math.pi
3.141592653589793
>>> math.sqrt(16)
4.0
>>> math.ceil(4.2), math.floor(4.8)
(5, 4)
>>> math.isclose(0.1 + 0.2, 0.3)
True
>>> 0.1 + 0.2 == 0.3
False
>>> math.prod([2, 3, 4])
24
```

- `ceil` arredonda **para cima**; `floor`, **para baixo**. Para "quantas bobinas
  preciso?" é sempre `ceil`: 4,2 bobinas viram 5.
- `isclose` compara floats com tolerância (lembra do `0.1 + 0.2` do módulo 01?). É o
  mesmo princípio do `pytest.approx` dos testes.

**Exemplo do dia a dia:** quantos metros de filme tem uma bobina? A bobina é um anel
de filme em volta do tubete. Área do anel ÷ espessura = comprimento:
`L = π × (D² − d²) / (4 × e)`, com tudo em metros.

```python
>>> import math
>>> externo, tubete, espessura = 0.600, 0.152, 25e-6
>>> comprimento = math.pi * (externo**2 - tubete**2) / (4 * espessura)
>>> round(comprimento)
10584
>>> math.ceil(50_000 / comprimento)
5
```

(`25e-6` é notação científica: 25 × 10⁻⁶ m = 25 µm. O `_` em `50_000` só separa os
milhares para facilitar a leitura.)

### `random`: sorteios reproduzíveis

```python
>>> import random
>>> gerador = random.Random(7)
>>> gerador.sample(["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08"], 3)
['B06', 'B02', 'B04']
>>> gerador.randint(1, 6)
6
>>> gerador.choice("ABCD")
'A'
```

| Função | Faz |
|---|---|
| `random()` | float entre 0 e 1 |
| `uniform(a, b)` | float entre a e b |
| `randint(a, b)` | inteiro entre a e b, **incluindo os dois** |
| `choice(seq)` | um item |
| `choices(seq, k=n)` | n itens **com** reposição (pode repetir) |
| `sample(seq, n)` | n itens **sem** reposição |
| `shuffle(lista)` | embaralha a própria lista |

**Semente (seed):** o "aleatório" do computador é uma conta. Com a mesma semente, a
sequência de sorteios é sempre a mesma. Isso é ótimo para testes e para auditoria
("este foi o sorteio, pode repetir para conferir"). Prefira criar um gerador próprio
com `random.Random(semente)` em vez de `random.seed(semente)`, que mexe no gerador
global de todo o programa.

> 🔮 **Preveja antes de rodar:**
>
> ```python
> import random
> amostras = ["AM1", "AM2", "AM3"]
> embaralhadas = random.shuffle(amostras)
> print(embaralhadas)
> ```

<details><summary>Resposta</summary>

`None`. O `shuffle` embaralha a **própria** lista e não devolve nada (como o
`list.sort()` do módulo 03). Quem queria uma lista nova tem de copiar e depois
embaralhar a cópia: `copia = list(amostras)` e `random.shuffle(copia)`.

</details>

> ⚠️ **Erro comum:** usar `random` para senha ou token. Ele é previsível de propósito.
> Para segurança, use o módulo `secrets` (`secrets.token_hex(16)`).

## 14. `os`, `sys` e `time`

Três módulos para conversar com o sistema operacional e com o próprio Python.

### `os`: ambiente e sistema de arquivos

```python
import os

pasta = os.environ.get("LAB_PASTA", r"C:\laboratorio")  # variável de ambiente
print(os.getcwd())                                      # pasta atual do terminal
```

**Variáveis de ambiente** são configurações que ficam fora do código: pasta dos
dados, endereço do servidor, senha do e-mail (senha **nunca** vai no código nem no
Git). Para definir uma no terminal antes de rodar o programa:

```powershell
$env:LAB_PASTA = "C:\laboratorio"          # PowerShell (vale até fechar o terminal)
python exemplos/10_os_sys_time.py
```

No Linux/macOS: `export LAB_PASTA=/home/voce/laboratorio`. O `python-dotenv` que está
no seu `pyproject.toml` lê essas variáveis de um arquivo `.env` (que também fica fora
do Git).

Para arquivos e pastas, o `os` tem funções antigas (`os.listdir`, `os.path.join`),
mas você já aprendeu o jeito moderno: `pathlib` (módulo 06). Use `pathlib`.

**Tornando funções testáveis.** Uma função que lê `os.environ` lá dentro é difícil de
testar. O truque é **receber o ambiente como parâmetro**, com `os.environ` como padrão:

```python
import os
from collections.abc import Mapping


def cv_maximo(ambiente: Mapping[str, str] | None = None) -> float:
    if ambiente is None:
        ambiente = os.environ
    return float(ambiente.get("LAB_CV_MAX", "5.0"))
```

No programa, você chama `cv_maximo()`. No teste, `cv_maximo({"LAB_CV_MAX": "3"})`.
O `Mapping` na anotação quer dizer "qualquer coisa que funcione como dicionário só
para leitura", porque o `os.environ` parece um dicionário, mas não é um `dict`. O
exercício 11 usa exatamente esse padrão.

### `sys`: o próprio Python

```python
import sys

print(sys.version)      # versão do Python
print(sys.executable)   # QUAL Python está rodando (venv!)
print(sys.platform)     # 'win32', 'linux' ou 'darwin' (macOS)
print(sys.argv)         # argumentos da linha de comando
print("deu ruim", file=sys.stderr)   # mensagem de erro no canal de erro
sys.exit(1)             # encerra o programa com código de saída 1
```

- `sys.argv` é a lista do que foi digitado: `python script.py a b` dá
  `['script.py', 'a', 'b']`. Funciona, mas tratar isso na mão é sofrido; a seção 15
  resolve.
- **Código de saída**: todo programa termina com um número. `0` = deu certo; outro =
  algo falhou. O Agendador de Tarefas do Windows mostra esse número em "Resultado da
  Última Execução". No PowerShell, veja com `$LASTEXITCODE`; no Linux, `echo $?`.
- `sys.stderr` é o canal de **erros**. Separar erro (stderr) de resultado (stdout)
  permite, por exemplo, gravar o relatório num arquivo e ainda ver os erros na tela.

### `time`: medir e esperar

```python
import time

inicio = time.perf_counter()
# ... algo demorado ...
print(f"levou {time.perf_counter() - inicio:.3f} s")
time.sleep(2)   # espera 2 segundos (robôs esperando a tela do TOTVS carregar)
```

`perf_counter` é o cronômetro certo para medir duração. Para **datas**, use
`datetime`; `time.time()` existe, mas devolve segundos desde 1970, nada amigável.

O script `exemplos/10_os_sys_time.py` mostra os três juntos. Rode com
`python exemplos/10_os_sys_time.py primeiro segundo` e veja o `sys.argv`.

## 15. `argparse`: programas de linha de comando

O projeto final vai rodar assim:

```powershell
python -m validador valores.xlsx --linha B --tolerancia 7.5 --desde 01/10/2026 -v
```

Tratar isso com `sys.argv` na mão é um pesadelo: ordem dos argumentos, conversão de
tipos, valores padrão, mensagem de ajuda, erro amigável. O `argparse` faz tudo isso.

### O básico em quatro passos

```python
import argparse

parser = argparse.ArgumentParser(prog="faixa", description="Calcula nominal ± %.")  # 1
parser.add_argument("nominal", type=float, help="valor nominal")                   # 2
parser.add_argument("-p", "--percentual", type=float, default=10.0)                 # 2
parser.add_argument("-v", "--verbose", action="store_true")                         # 2
args = parser.parse_args(["25", "-p", "5"])                                         # 3
print(args.nominal, args.percentual, args.verbose)                                  # 4
```

Saída:

```text
25.0 5.0 False
```

1. Cria o parser.
2. Declara cada argumento.
3. Lê os argumentos. **Sem** parâmetro, `parse_args()` lê o `sys.argv` do terminal.
   **Com** uma lista, lê a lista: é assim que se testa.
4. Usa: cada argumento vira um atributo (`args.percentual`). O `args` é um objeto do
   tipo `Namespace` (objetos e atributos: módulo 08).

### Os tipos de argumento

| Declaração | Uso no terminal | Valor em `args` |
|---|---|---|
| `add_argument("planilha")` | `valores.xlsx` (obrigatório, sem `--`) | `'valores.xlsx'` |
| `add_argument("--linha")` | `--linha B` (opcional) | `'B'` ou `None` |
| `add_argument("--tol", type=float, default=5.0)` | `--tol 7.5` | `7.5` ou `5.0` |
| `add_argument("--linha", choices=["A", "B"])` | `--linha E` | erro amigável |
| `add_argument("-v", "--verbose", action="store_true")` | `-v` | `True` ou `False` |
| `add_argument("--valores", type=float, nargs="+")` | `--valores 24.1 26` | `[24.1, 26.0]` |
| `add_argument("--cv-max", type=float)` | `--cv-max 5` | `args.cv_max` (hífen vira `_`) |

O `type` pode ser **qualquer função** que receba texto: `type=float`,
`type=str.upper` (aceita "b" e transforma em "B" antes de conferir o `choices`) ou
uma função sua, como `data_br`, que converte "01/10/2026". Se a sua função levantar
`argparse.ArgumentTypeError`, o argparse mostra a mensagem e encerra com código 2.

### O `--help` de graça

Rode `python exemplos/11_cli_argparse.py --help`:

```text
usage: faixa [-h] [-p PERCENTUAL] [--unidade UNIDADE]
             [--valores VALORES [VALORES ...]] [-v]
             nominal

Calcula a faixa nominal ± percentual e confere valores.

positional arguments:
  nominal               valor nominal (ex.: 25 para 25 µm)

options:
  -h, --help            show this help message and exit
  -p, --percentual PERCENTUAL
                        tolerância em % (padrão: 10)
  --unidade UNIDADE     unidade exibida (padrão: µm)
  --valores VALORES [VALORES ...]
                        valores medidos
  -v, --verbose         mostra mais detalhes

Exemplo: faixa 25 -p 10 --valores 24.1 26 27.9
```

E um argumento errado vira uma mensagem clara, com código de saída 2:

```text
> python exemplos/11_cli_argparse.py abc
usage: faixa [-h] [-p PERCENTUAL] [--unidade UNIDADE]
             [--valores VALORES [VALORES ...]] [-v]
             nominal
faixa: error: argument nominal: invalid float value: 'abc'
```

(As mensagens fixas do argparse saem em inglês, e o desenho do `--help` muda um pouco
entre versões do Python. Os textos de `help=` e `description=` são seus.)

> 💡 **Dica:** dentro do `help=`, o `%` tem significado especial. Para escrever "%"
> literal, use `%%`: `help="tolerância em %%"`.

> 🔮 **Preveja antes de rodar:**
>
> ```python
> import argparse
> parser = argparse.ArgumentParser()
> parser.add_argument("--linha", type=str.upper, choices=["A", "B", "C", "D"])
> parser.add_argument("--cv-max", type=float, default=5)
> args = parser.parse_args(["--linha", "c"])
> print(args.linha, args.cv_max, type(args.cv_max).__name__)
> ```

<details><summary>Resposta</summary>

`C 5 int`. O `type=str.upper` roda **antes** do `choices`, então "c" vira "C" e é
aceito. Já o `default=5` **não** passa pelo `type`: ficou o inteiro `5` que você
escreveu. Para ter float sempre, escreva `default=5.0`.

</details>

### O molde profissional: `main(argv=None)`

```python
import argparse
import sys


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="faixa")
    parser.add_argument("nominal", type=float)
    parser.add_argument("-p", "--percentual", type=float, default=10.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = criar_parser().parse_args(argv)
    margem = args.nominal * args.percentual / 100
    print(f"{args.nominal - margem:.2f} a {args.nominal + margem:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Cada peça tem um motivo:

- `criar_parser()` separado: dá para testar o parser sozinho.
- `main(argv=None)`: no terminal, `argv` é `None` e o argparse lê o `sys.argv`. No
  teste, você chama `main(["25", "-p", "5"])` e confere a saída com `capsys`.
- `return` de um número + `sys.exit(main())`: o código de saída chega ao sistema
  operacional.
- `if __name__ == "__main__":` (seção 3): importar o arquivo no teste **não** dispara
  o programa.

O `curso.py`, que você usa desde o módulo 00, segue esse molde, com um recurso a
mais: **subcomandos** (`testar`, `progresso`, `modulos`), feitos com
`add_subparsers`. Abra e leia: agora você entende cada linha.

### Exemplo resolvido: um CLI do zero

**Problema:** quero `python conferir.py 25 24.1 26 27.9 --percentual 10` mostrando
quais valores estão fora de 25 ± 10%, com código de saída 1 se algum estiver fora.

**Como eu pensei:**

1. **Entradas**: o nominal (obrigatório), os valores (um ou mais), o percentual
   (opcional, padrão 10). Posicionais para o que é sempre preciso; `--` para o que tem
   padrão.
2. **Saída**: uma linha por valor e o código de saída.
3. Escrevo o parser e testo **sem terminal**, passando listas para `parse_args`.
4. Só depois escrevo a regra, reaproveitando a conta de faixa.

```python
>>> import argparse
>>> parser = argparse.ArgumentParser(prog="conferir")
>>> _ = parser.add_argument("nominal", type=float)
>>> _ = parser.add_argument("valores", type=float, nargs="+")
>>> _ = parser.add_argument("-p", "--percentual", type=float, default=10.0)
>>> args = parser.parse_args(["25", "24.1", "26", "27.9"])
>>> args
Namespace(nominal=25.0, valores=[24.1, 26.0, 27.9], percentual=10.0)
>>> margem = args.nominal * args.percentual / 100
>>> fora = [v for v in args.valores if not (args.nominal - margem <= v <= args.nominal + margem)]
>>> fora
[27.9]
>>> codigo_saida = 1 if fora else 0
>>> codigo_saida
1
```

(O `_ =` só esconde o objeto que o `add_argument` devolve, para o REPL não poluir a
tela.) A versão completa, com `main()`, está em `exemplos/11_cli_argparse.py`.

> 🔧 **Modifique:** no `11_cli_argparse.py`, acrescente `--saida` com `choices=["texto",
> "csv"]`. No modo `csv`, imprima `valor;situacao` em cada linha. Rode com `--help` e
> veja a opção nova aparecer sozinha.

## Lendo mensagens de erro deste módulo

**`ModuleNotFoundError: No module named 'openpyxl'`**
O pacote não está instalado **no Python que está rodando**. Ative o venv e rode
`python -m pip install openpyxl`. Confira com
`python -c "import sys; print(sys.executable)"`.

**`ModuleNotFoundError: No module named 'labqualidade'`**
Seu próprio módulo não foi achado. O arquivo está na mesma pasta do script que você
rodou? Lembre: a posição 0 do `sys.path` é a pasta **do script**, não a do terminal.

**`ImportError: cannot import name 'media' from 'statistics'`**
O módulo existe, mas o nome não. Erro de digitação (é `mean`) ou a função está em
outro módulo. Confira com `dir(statistics)` no REPL ou na documentação.

**`AttributeError: module 'random' has no attribute 'randint'`** (com "consider
renaming" ou "partially initialized module")
Seu arquivo tem o nome de um módulo da biblioteca. Renomeie.

**`ImportError: attempted relative import with no known parent package`**
Você rodou diretamente um arquivo que usa `from .algo import ...`. Rode pelo pacote
(`python -m pacote`) ou por um script de fora.

**`ValueError: time data '2026-10-29' does not match format '%d/%m/%Y'`**
O texto não segue o formato. Leia os dois lados: o dado veio em ISO (`ano-mês-dia`) e
o formato pedia `dia/mês/ano`.

**`ValueError: day is out of range for month`**
Data impossível: `date(2026, 2, 30)`. Em dados reais, é sinal de digitação errada na
planilha. Trate com `try/except ValueError` (módulo 06).

**`TypeError: '<' not supported between instances of 'datetime.date' and 'datetime.datetime'`**
Você comparou uma data com uma data e hora. Converta: `momento.date()` pega só a data
de um `datetime`. (No Python 3.12 e anteriores a mensagem é
`can't compare datetime.datetime to datetime.date`.)

**`statistics.StatisticsError: stdev requires at least two data points`**
Desvio padrão com menos de 2 valores. Confira o filtro: talvez a linha pedida não
tenha dados no período.

**`faixa: error: argument --linha: invalid choice: 'E' (choose from 'A', 'B', 'C', 'D')`**
Não é um traceback: é o argparse explicando o que estava errado. O programa terminou
com código 2. Leia a linha `usage:` acima dela para ver o formato esperado.

## Boas práticas

- **Um módulo, um assunto.** `regras.py` tem regras; `planilha.py` lê planilha. Se o
  nome do arquivo precisa de "e" (`planilha_e_email.py`), divida.
- **Imports no topo**, em três blocos (padrão, terceiros, seus), em ordem. Deixe o
  `ruff check --fix` ordenar.
- **Nada de `import *`**, exceto no REPL para brincar.
- **Nunca dê a um arquivo seu o nome de um módulo** da biblioteca ou de um pacote
  instalado.
- **Todo script termina com** `if __name__ == "__main__":`, chamando `main()`.
- **Um venv por projeto**, criado com `python -m venv .venv`, fora do Git.
- **Dependências registradas**: `requirements.txt` ou `pyproject.toml` +
  `poetry.lock`. Se não está registrado, não existe para quem vai rodar depois.
- **Datas como `date`, não como texto.** Converta na entrada (`strptime`) e formate
  só na saída (`strftime`).
- **Funções recebem `hoje`, `ambiente` e `semente` como parâmetros** em vez de
  chamarem `date.today()`, `os.environ` e `random` lá dentro. Fica testável.
- **Mensagens de erro no `stderr` e código de saída significativo** em programas de
  linha de comando.

## No mundo real

O script `exemplos/12_relatorio_linhas.py` é o tipo de ferramenta que você vai rodar
toda semana no laboratório: lê o CSV exportado da planilha de ensaios, filtra por
ensaio, linha e período, calcula média, desvio e CV% por linha e conta as reprovações.
Com `--estrito`, termina com código 1 quando alguma linha passa do CV máximo (assim o
Agendador de Tarefas pode avisar alguém).

Repare como ele usa quase tudo do módulo:

| Parte do script | Ferramenta |
|---|---|
| opções `--ensaio`, `--linha`, `--desde`, `--ate`, `--cv-max`, `--estrito` | `argparse` com `type=`, `choices=` e uma função `data_br` |
| CV máximo padrão vindo do computador | `os.environ.get("LAB_CV_MAX", "5.0")` |
| caminho do CSV relativo ao próprio script | `Path(__file__).resolve().parent.parent / "dados"` |
| datas da planilha | `datetime.strptime(...).date()` e comparações |
| valores agrupados por linha | `defaultdict(list)` |
| reprovações por linha | `Counter` + `most_common()` |
| média, desvio, CV | `statistics` |
| erros e código de saída | `sys.stderr`, `return 2`, `sys.exit(main())` |

Rodando sem opções (na pasta `curso-python`):

```text
> python 07-modulos-e-biblioteca-padrao/exemplos/12_relatorio_linhas.py
Ensaio: espessura | período: 01/10/2026 a 03/11/2026
Linha   n    Média  Desvio    CV%  Situação
A       6    19.60    0.39   1.99  estável
B       6    25.38    0.78   3.08  estável
C       6    41.68    2.68   6.44  ALERTA: CV alto
D       6    59.48    0.97   1.64  estável

Reprovações no período (todos os ensaios):
  Linha C: 4
  Linha B: 2
```

Agora só a gramatura da primeira quinzena:

```text
> python 07-modulos-e-biblioteca-padrao/exemplos/12_relatorio_linhas.py --ensaio gramatura --desde 01/10/2026 --ate 15/10/2026
Ensaio: gramatura | período: 01/10/2026 a 15/10/2026
Linha   n    Média  Desvio    CV%  Situação
A       3    18.13    0.60   3.32  estável
B       3    23.47    0.42   1.77  estável
C       3    35.27    3.69  10.47  ALERTA: CV alto
D       2    54.30    1.13   2.08  estável

Reprovações no período (todos os ensaios):
  Linha C: 3
  Linha B: 1
```

Abra o arquivo e leia de cima para baixo. Ele tem pouco mais de 100 linhas e cada
função faz uma coisa. No projeto final, essas funções vão morar em módulos separados
dentro de `src/validador/`, e o mesmo esqueleto (`criar_parser` + `main`) vira o
comando `validador`.

No mercado, esse padrão de "pequena ferramenta de linha de comando que lê um
arquivo, calcula e devolve um código de saída" está em toda parte: pipelines de dados,
rotinas agendadas, verificações em CI. Saber escrever uma bem feita é habilidade de
entrevista.

## Resumo

| Assunto | Sintaxe essencial |
|---|---|
| Importar | `import math` · `import pandas as pd` · `from datetime import date` |
| Script e módulo | `if __name__ == "__main__":` |
| Onde procura | `sys.path` (pasta do script primeiro, `site-packages` no fim) |
| Pacote | pasta + `__init__.py` · `from .modulo import nome` · `python -m pacote` |
| venv | `python -m venv .venv` · `.venv\Scripts\activate` · `deactivate` |
| pip | `python -m pip install "x>=1,<2"` · `freeze > requirements.txt` · `install -r` |
| Poetry | `poetry install` · `poetry add x` · `poetry add --group dev x` · `poetry run x` |
| Datas | `date(2026, 10, 29)` · `+ timedelta(days=180)` · `(d2 - d1).days` · `weekday()` |
| Texto ↔ data | `datetime.strptime(t, "%d/%m/%Y").date()` · `d.strftime("%d/%m/%Y")` |
| Contar | `Counter(seq)` · `.most_common(n)` · chave ausente vale 0 |
| Agrupar | `defaultdict(list)` · `defaultdict(float)` · devolva `dict(...)` |
| Tupla nomeada | `namedtuple("Medicao", ["op", "valor"])` · `m.valor` · `m._replace(...)` |
| Emendar | `chain(a, b)` · `chain.from_iterable(lista_de_listas)` |
| Agrupar vizinhos | `groupby(sorted(x, key=k), key=k)` |
| Estatística | `mean` · `median` · `stdev` (amostral) · `pstdev` · CV = stdev/mean×100 |
| math | `pi` · `sqrt` · `ceil` · `floor` · `isclose` |
| random | `random.Random(semente)` · `.sample` · `.choice` · `.randint` · `.shuffle` |
| os / sys / time | `os.environ.get` · `sys.argv` · `sys.exit(n)` · `sys.stderr` · `time.perf_counter` |
| argparse | `ArgumentParser` · `add_argument(..., type=, default=, choices=, action="store_true")` · `parse_args(argv)` |

## Você domina este módulo se...

- [ ] Consigo explicar, sem consultar, o que acontece quando o Python executa
      `import conversoes_br`: onde ele procura, o que ele executa e por que o segundo
      import não executa de novo.
- [ ] Sei dizer o valor de `__name__` quando o arquivo é rodado e quando é importado,
      e para que serve o `if __name__ == "__main__":`.
- [ ] Monto um pacote com `__init__.py` que exporta funções de dois módulos e o uso de
      outro script.
- [ ] Crio e ativo um venv no PowerShell, instalo dependências e descubro qual Python
      está rodando.
- [ ] Leio o `pyproject.toml` do meu repositório e explico cada seção, inclusive
      `package-mode = false` e o grupo `dev`.
- [ ] Calculo validade e prazo (inclusive em dias úteis) com `date` e `timedelta`, e
      converto datas brasileiras nos dois sentidos.
- [ ] Escolho entre `Counter`, `defaultdict` e `groupby` para um problema de contar ou
      agrupar, e sei por que o `groupby` precisa de dados ordenados.
- [ ] Escrevo um programa com `argparse` no molde `main(argv=None)` e testo o parser
      passando uma lista.

## Exercícios

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_comprimento_bobina` | ★☆☆ | `math.pi`, `math.ceil`, conversão de unidades, `ValueError` |
| 02 | `ex02_validade_laudo` | ★☆☆ | `date`, `timedelta`, comparar datas, `.days` |
| 03 | `ex03_datas_brasileiras` | ★☆☆ | `strptime`, `strftime`, `weekday()` |
| 04 | `ex04_estatistica_ensaio` | ★☆☆ | `statistics.mean/median/stdev`, CV% |
| 05 | `ex05_contar_reprovacoes` | ★☆☆ | `Counter`, `most_common`, taxa por linha |
| 06 | `ex06_sorteio_amostras` | ★★☆ | `random.Random(semente)`, `sample`, `shuffle` numa cópia |
| 07 | `ex07_agrupar_expedicao` | ★★☆ | `chain.from_iterable`, `defaultdict(list)` e `(float)` |
| 08 | `ex08_sequencias_groupby` | ★★☆ | `groupby`, ordenar antes de agrupar, `max(default=)` |
| 09 | `ex09_corrigir_dias_uteis` | ★★☆ | **leitura de código**: prever e corrigir 3 defeitos em prazos |
| 10 | `ex10_parser_cli` | ★★☆ | `argparse`: posicional, `choices`, `type` próprio, `store_true` |
| 11 | `ex11_cli_relatorio` | ★★★ | programa completo: CSV, `statistics`, `os.environ`, `stderr`, código de saída |
| 12 | `ex12_revisao_expedicao` | ★★★ | **revisão**: regex e número BR (05) + datas e `defaultdict` |
| 13 | `ex13_revisao_relatorio_csv` | ★★★ | **revisão**: CSV, JSON e erros (06) + agrupar e datas |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar
de `raise NotImplementedError` e rode, na pasta `curso-python`:

```powershell
python curso.py testar 07 ex01
```

Para testar o módulo inteiro: `python curso.py testar 07`.

> 💡 **Dica:** neste módulo, **você** escreve os imports. Os arquivos de exercício só
> trazem os imports usados nas anotações de tipo. Se aparecer `NameError: name
> 'statistics' is not defined`, falta o `import statistics` no topo.

## Desafio do módulo

**Agenda de validade de laudos**: um programa de linha de comando que lê
`dados/laudos.csv`, separa os laudos em vencidos, a vencer (numa janela de dias) e em
dia, mostra um resumo por cliente e devolve um código de saída útil para o Agendador
de Tarefas. Junta `datetime`, `Counter`, `argparse`, `os.environ` e `sys`.

Enunciado completo, exemplo de execução e critérios de aceite em
[desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou em [quiz.md](quiz.md): 12 perguntas com gabarito comentado.

## Para ir além

- Tutorial oficial, módulos e pacotes:
  <https://docs.python.org/pt-br/3/tutorial/modules.html>
- Ambientes virtuais e pacotes: <https://docs.python.org/pt-br/3/tutorial/venv.html>
- Tour pela biblioteca padrão (parte 1 e 2):
  <https://docs.python.org/pt-br/3/tutorial/stdlib.html>
- `datetime`: <https://docs.python.org/pt-br/3/library/datetime.html> (a tabela de
  códigos `%d`, `%m`... fica na seção "strftime() and strptime() Format Codes")
- `collections`: <https://docs.python.org/pt-br/3/library/collections.html>
- `itertools`: <https://docs.python.org/pt-br/3/library/itertools.html>
- `statistics`: <https://docs.python.org/pt-br/3/library/statistics.html>
- Tutorial de `argparse`: <https://docs.python.org/pt-br/3/howto/argparse.html>
- Poetry, guia básico: <https://python-poetry.org/docs/basic-usage/>
- Leitura extra: "src layout vs flat layout", no guia oficial de empacotamento
  (<https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/>).
- Leitura extra: Python Module of the Week, um exemplo comentado para cada módulo da
  biblioteca padrão (<https://pymotw.com/3/>).
