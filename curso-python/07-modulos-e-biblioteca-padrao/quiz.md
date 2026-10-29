# Quiz do Módulo 07 — Módulos, pacotes e biblioteca padrão

Responda no papel (ou num arquivo) antes de olhar o gabarito. Nas perguntas "o que
imprime", tente prever e só depois rode no REPL para conferir.

## Perguntas

**1.** Na pasta do seu script existe um arquivo chamado `statistics.py`, feito por
você para testar umas contas. Outro script, na mesma pasta, faz
`import statistics` e chama `statistics.mean([1, 2, 3])`. O que acontece?

a) Funciona normalmente: o Python sempre prefere a biblioteca padrão.
b) O Python importa o **seu** `statistics.py`, e o `mean` provavelmente não existe nele.
c) O Python junta os dois arquivos num só.
d) Dá `ModuleNotFoundError`.

**2.** O que aparece ao rodar `python main.py`?

```python
# util.py
print("util:", __name__)
```

```python
# main.py
import util

print("main:", __name__)
```

**3.** Para que serve o arquivo `__init__.py` dentro de uma pasta?

a) É obrigatório em toda pasta do computador que tenha arquivos `.py`.
b) Marca a pasta como pacote e roda no primeiro import dele; pode servir de "vitrine".
c) Guarda as senhas do projeto.
d) Substitui o `requirements.txt`.

**4.** O que imprime?

```python
from datetime import date, timedelta
print(date(2026, 2, 27) + timedelta(days=2))
```

**5.** O que imprime?

```python
from datetime import date
print((date(2026, 12, 25) - date(2026, 10, 29)).days)
```

**6.** Onde está o erro? A célula da planilha tem o texto `"2026-10-29"`.

```python
from datetime import datetime
emissao = datetime.strptime("2026-10-29", "%d/%m/%Y").date()
```

**7.** O que imprime?

```python
from collections import Counter
print(Counter("abracadabra").most_common(2))
```

**8.** O que imprime?

```python
from itertools import groupby
print([(k, len(list(g))) for k, g in groupby([1, 1, 2, 1])])
```

**9.** O que imprime?

```python
from collections import defaultdict
contagem = defaultdict(int)
contagem["x"] += 1
contagem["y"]
print(len(contagem))
```

**10.** No laboratório você mede 6 pontos de uma bobina e quer o mesmo desvio padrão
que o `DESVPAD.A` do Excel. Qual função usa?

a) `statistics.pstdev`
b) `statistics.stdev`
c) `statistics.variance`
d) `statistics.median`

**11.** Onde está o erro?

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cv-max", type=float, default=5.0)
args = parser.parse_args([])
print(args.cv-max)
```

**12.** No PowerShell, com o venv ativado, você digita
`pip install pandas>=2.2` (sem aspas). O que acontece?

a) Instala o pandas 2.2 ou mais novo.
b) Dá erro de sintaxe no pip.
c) O `>` vira redirecionamento: o pip instala `pandas` e a saída vai para um arquivo
   chamado `=2.2`.
d) Instala a versão 2.2 exata.

**13.** O que imprime?

```python
import random
print(random.Random(5).randint(1, 100) == random.Random(5).randint(1, 100))
```

---

## Gabarito

**1. b.** A pasta do script vem **primeiro** no `sys.path`, então o seu
`statistics.py` "esconde" o módulo da biblioteca. O resultado é um `AttributeError`
(no Python 3.13 a mensagem até sugere renomear o arquivo). Nunca dê a um arquivo seu o
nome de um módulo existente.

**2.**

```text
util: util
main: __main__
```

O import executa o `util.py` inteiro, e lá `__name__` vale o nome do módulo. O arquivo
rodado diretamente (`main.py`) tem `__name__ == "__main__"`.

**3. b.** O `__init__.py` transforma a pasta em pacote e roda uma vez, no primeiro
import. Pode ficar vazio ou trazer para o nível do pacote as funções públicas
(`from .tolerancias import faixa_nominal`).

**4.** `2026-03-01`. Fevereiro de 2026 tem 28 dias: 27/02 + 1 = 28/02; + 2 = 01/03. O
`timedelta` sabe o tamanho de cada mês, você não precisa saber.

**5.** `57`. São 2 dias até o fim de outubro, 30 de novembro e 25 de dezembro.
Subtrair datas dá um `timedelta`; `.days` é o número de dias.

**6.** O formato não combina com o texto: o dado está em ISO (`ano-mês-dia`) e o
formato pede `dia/mês/ano`. Dá `ValueError: time data '2026-10-29' does not match format
'%d/%m/%Y'`. Use `"%Y-%m-%d"` ou, mais simples, `date.fromisoformat("2026-10-29")`.

**7.** `[('a', 5), ('b', 2)]`. O "a" aparece 5 vezes. "b" e "r" empatam com 2; no
empate, o `most_common` mantém a ordem em que apareceram, e o "b" veio antes.

**8.** `[(1, 2), (2, 1), (1, 1)]`. O `groupby` junta só **vizinhos** iguais. O último
`1` forma um grupo novo. Para agrupar todos os `1`, ordene antes.

**9.** `2`. A linha `contagem["y"]`, mesmo só lendo, cria a chave `"y"` com valor `0`.
Para consultar sem criar, use `"y" in contagem` ou `contagem.get("y")`.

**10. b.** `stdev` é o desvio **amostral** (divide por n − 1), igual ao `DESVPAD.A`
(e ao `DESVPAD` padrão). `pstdev` é o populacional (`DESVPAD.P`). `variance` é o
desvio ao quadrado.

**11.** O Python lê `args.cv-max` como `args.cv` **menos** `max`. Como não existe
`args.cv`, dá `AttributeError: 'Namespace' object has no attribute 'cv'`. O argparse
troca o hífen por sublinhado no nome do atributo: use `args.cv_max`.

**12. c.** No terminal, `>` é redirecionamento de saída. O pip recebe só `pandas` e o
texto que ele imprimiria vai para um arquivo `=2.2`. Escreva
`python -m pip install "pandas>=2.2"`, com aspas.

**13.** `True`. Dois geradores com a **mesma semente** produzem a mesma sequência. É
isso que torna um sorteio reproduzível (e testável).
