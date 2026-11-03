# Módulo 09 — Testes e qualidade de código

> **Tempo estimado:** 12 a 16 horas · **Pré-requisitos:** módulos 00 a 08 · **Nível:** intermediário

## O que você vai aprender

- Escrever testes com `pytest` no padrão AAA (preparar, agir, conferir) e **ler uma falha**
  sem se assustar.
- Usar `pytest.approx` para floats, `pytest.raises` para erros esperados e
  `@pytest.mark.parametrize` para testar vários casos com uma função só.
- Criar fixtures (inclusive em `conftest.py`) e usar as prontas: `tmp_path`, `capsys`,
  `caplog` e `monkeypatch`.
- Desenvolver uma função com **TDD**, no ciclo vermelho → verde → refatorar.
- Escrever testes para um código que você não escreveu, escolhendo casos que pegam bugs.
- Medir a cobertura dos testes e entender o que ela **não** garante.
- Usar o `ruff` para achar problemas (lint) e padronizar o código (format).
- Ler type hints e entender o que o `mypy` confere.
- Trocar `print` por `logging`, com níveis, formato e arquivo de log.
- Depurar com `breakpoint()` (pdb) e com o debugger do VS Code.
- Trabalhar com Git como num time: branch, commits pequenos, pull request e revisão.
- Refatorar com segurança: melhorar nomes e funções sem mudar o comportamento.

## Por que isso importa

Até aqui você escreveu código que funciona. Agora vai aprender a **provar** que funciona,
hoje e daqui a seis meses, depois de dez mudanças. É isso que separa um script de um
sistema.

No laboratório você já pensa assim: ninguém libera um laudo sem conferir o instrumento
com um padrão de referência. Um teste automatizado é o padrão de referência do código.

Vagas de dados, automação e backend pedem `pytest`, Git, pull request e "código limpo";
um repositório com testes e bons commits vale mais que um certificado. E no projeto
final, um erro numa regra de tolerância libera bobina reprovada: os testes são a sua
rede de segurança.

## 1. Por que testar

Você já testa o seu código: roda o script e confere a saída "de olho". Isso é um **teste
manual**. Funciona uma vez. O problema é a segunda, a terceira, a vigésima vez.

Um teste automatizado é uma função que chama o seu código com uma entrada conhecida e
**confere** se a saída é a esperada. Ele **pega regressões** (você corrige um bug, quebra
outra coisa, e o teste antigo avisa), **documenta** (`test_bordas_estao_dentro` explica a
regra), **dá coragem para mudar** e **melhora o design**: código difícil de testar
costuma ser código mal dividido.

```text
          /\        ponta a ponta: o sistema inteiro (robô no TOTVS)
         /  \       poucos, lentos, frágeis
        /----\
       /      \     integração: partes juntas (código + banco SQLite)
      /--------\
     /          \   unidade: uma função isolada (calcular_limites)
    /------------\  muitos, rápidos, baratos
```

Neste módulo o foco é a base da pirâmide: **testes de unidade**.

## 2. `assert`: a peça mais simples

`assert` confere uma condição. Se for verdadeira, nada acontece. Se for falsa, o Python
levanta `AssertionError`. Depois da vírgula vem uma mensagem opcional.

```python
def calcular_limites(nominal, tolerancia_pct):
    margem = nominal * tolerancia_pct / 100
    return nominal - margem, nominal + margem


assert calcular_limites(20.0, 5.0) == (19.0, 21.0)   # silêncio = passou
minimo, maximo = calcular_limites(20.0, 5.0)
assert minimo == 18.0, f"mínimo errado: esperava 18.0, veio {minimo}"
```

```text
AssertionError: mínimo errado: esperava 18.0, veio 19.0
```

Mais casos em `exemplos/01_assert_basico.py` (rode na pasta do módulo).

> ⚠️ **Erro comum:** usar `assert` para validar dados no programa de produção. O Python
> pode rodar com `python -O`, que **desliga todos os asserts**. Para validar entrada, use
> `if` + `raise ValueError(...)` (módulo 06). `assert` é para testes.

> 🔮 **Preveja antes de rodar:** o que acontece com esta linha no REPL?
>
> ```python
> assert 0.1 + 0.2 == 0.3, "a soma não fechou"
> ```

<details><summary>Resposta</summary>

Levanta `AssertionError: a soma não fechou`. Em float, `0.1 + 0.2` vale
`0.30000000000000004` (módulo 01), então a comparação exata é falsa. Na seção 6 você vê
o jeito certo de comparar floats em testes: `pytest.approx`.

</details>

## 3. pytest: primeiros passos

Dá para testar só com `assert`, mas o **pytest** acrescenta o que falta: encontra os
testes sozinho, roda todos e explica **por que** cada falha aconteceu. Ele já está no
`requirements.txt` do curso (`python -m pip install pytest`, se precisar).

**Regras de descoberta.** O pytest procura **arquivos** `test_*.py` (ou `*_test.py`) e,
dentro deles, **funções** cujo nome começa com `test` (e classes que começam com `Test`).
Seguiu o padrão de nome, virou teste. Não existe registro nem "main".

### O mini projeto do módulo

Em `exemplos/mini_projeto_laudo/` há um projeto pequeno, organizado como um real:

```text
mini_projeto_laudo/
  pyproject.toml      configuração do pytest e do ruff
  conftest.py         fixtures compartilhadas (seção 8)
  laudo.py            o código: limites, avaliação, média, leitura de arquivo
  observacao.py       leitura de "COF: liberado" (nasceu com TDD, seção 13)
  tests/
    test_laudo.py
    test_observacao.py
```

Um trecho de `laudo.py`:

```python
def calcular_limites(nominal: float, tolerancia_pct: float) -> tuple[float, float]:
    """Devolve (mínimo, máximo) para um valor nominal ± tolerância em %."""
    if nominal <= 0:
        raise ValueError(f"nominal deve ser positivo, recebi {nominal}")
    if tolerancia_pct < 0:
        raise ValueError(f"tolerância não pode ser negativa, recebi {tolerancia_pct}")
    margem = nominal * tolerancia_pct / 100
    return nominal - margem, nominal + margem


def avaliar(valor: float, minimo: float, maximo: float) -> str:
    """'APROVADO' se o valor está entre os limites (inclusive), senão 'REPROVADO'."""
    return "APROVADO" if minimo <= valor <= maximo else "REPROVADO"
```

E o primeiro teste, em `tests/test_laudo.py`:

```python
import pytest

from laudo import calcular_limites


def test_limites_com_tolerancia_de_5_porcento():
    # Arrange (preparar): os dados de entrada
    nominal, tolerancia = 20.0, 5.0
    # Act (agir): chama UMA vez o que está sendo testado
    minimo, maximo = calcular_limites(nominal, tolerancia)
    # Assert (conferir): o resultado é o esperado?
    assert minimo == pytest.approx(19.0)
    assert maximo == pytest.approx(21.0)
```

### Rodando

Entre na pasta do mini projeto e chame o pytest pelo Python do ambiente virtual
(`python -m pytest` garante que é o pytest do seu `.venv`):

```text
> cd 09-testes-e-qualidade\exemplos\mini_projeto_laudo
> python -m pytest -v
============================= test session starts ==============================
platform linux -- Python 3.13.16, pytest-9.2.0, pluggy-1.7.0 -- /usr/bin/python
rootdir: /home/user/estudos/curso-python/09-testes-e-qualidade/exemplos/mini_projeto_laudo
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.15.1
collecting ... collected 16 items

tests/test_laudo.py::test_limites_com_tolerancia_de_5_porcento PASSED    [  6%]
tests/test_laudo.py::test_limites_com_tolerancia_negativa_levanta_erro PASSED [ 12%]
tests/test_laudo.py::test_avaliar_respeita_as_bordas[19.0-APROVADO] PASSED [ 18%]
tests/test_laudo.py::test_avaliar_respeita_as_bordas[20.0-APROVADO] PASSED [ 25%]
tests/test_laudo.py::test_avaliar_respeita_as_bordas[21.0-APROVADO] PASSED [ 31%]
tests/test_laudo.py::test_avaliar_respeita_as_bordas[18.99-REPROVADO] PASSED [ 37%]
tests/test_laudo.py::test_avaliar_respeita_as_bordas[21.01-REPROVADO] PASSED [ 43%]
tests/test_laudo.py::test_media_de_tres_medicoes PASSED                  [ 50%]
tests/test_laudo.py::test_media_de_lista_vazia_levanta_erro PASSED       [ 56%]
tests/test_laudo.py::test_ler_medicoes_aceita_virgula_decimal PASSED     [ 62%]
tests/test_laudo.py::test_ler_medicoes_ignora_linhas_vazias PASSED       [ 68%]
tests/test_laudo.py::test_conferir_op_sem_acessar_o_erp PASSED           [ 75%]
tests/test_observacao.py::test_ler_liberacoes[um-liberado] PASSED        [ 81%]
tests/test_observacao.py::test_ler_liberacoes[um-reprovado] PASSED       [ 87%]
tests/test_observacao.py::test_ler_liberacoes[dois-ensaios] PASSED       [ 93%]
tests/test_observacao.py::test_status_desconhecido_levanta_erro PASSED   [100%]

============================== 16 passed in 0.04s ==============================
```

O cabeçalho (`platform`, `rootdir`, `plugins`) muda de computador para computador: no
Windows aparece `win32` e um caminho `C:\...`. Com `-q` em vez de `-v`, a saída é um
caractere por teste: `.` passou, `F` falhou (um `assert` deu falso), `E` erro (exceção
inesperada fora do `assert`).

| Comando | Para quê |
|---|---|
| `python -m pytest -v` | um teste por linha, com o nome |
| `python -m pytest -x` | para na **primeira** falha (ótimo no TDD) |
| `python -m pytest -k bordas` | só testes cujo nome contém "bordas" |
| `python -m pytest --lf` | só os que falharam na última rodada (*last failed*) |
| `python -m pytest -s` | mostra os `print` (normalmente o pytest os esconde) |

> 💡 **Dica:** o `python curso.py testar 09 ex01` que você usa desde o módulo 00 é um
> atalho: por baixo, ele chama `python -m pytest -v --tb=short` no arquivo de teste do
> exercício. Agora você sabe rodar o pytest direto, com qualquer opção.

## 4. Lendo uma falha do pytest

Uma falha não é uma bronca: é um relatório. Para ver um, coloquei um bug de propósito
numa cópia do mini projeto, trocando `<=` por `<` em `avaliar`:

```text
> python -m pytest -q --tb=short
..F.F...........                                                         [100%]
=================================== FAILURES ===================================
________________ test_avaliar_respeita_as_bordas[19.0-APROVADO] ________________
tests/test_laudo.py:35: in test_avaliar_respeita_as_bordas
    assert avaliar(valor, 19.0, 21.0) == esperado
E   AssertionError: assert 'REPROVADO' == 'APROVADO'
E     
E     - APROVADO
E     ? ^
E     + REPROVADO
E     ? ^^
________________ test_avaliar_respeita_as_bordas[21.0-APROVADO] ________________
tests/test_laudo.py:35: in test_avaliar_respeita_as_bordas
    assert avaliar(valor, 19.0, 21.0) == esperado
E   AssertionError: assert 'REPROVADO' == 'APROVADO'
E     
E     - APROVADO
E     ? ^
E     + REPROVADO
E     ? ^^
=========================== short test summary info ============================
FAILED tests/test_laudo.py::test_avaliar_respeita_as_bordas[19.0-APROVADO] - ...
FAILED tests/test_laudo.py::test_avaliar_respeita_as_bordas[21.0-APROVADO] - ...
2 failed, 14 passed in 0.34s
```

Leia sempre nesta ordem:

1. **Qual teste?** A faixa `____ test_avaliar_respeita_as_bordas[19.0-APROVADO] ____`
   traz o nome e o caso.
2. **Onde?** `tests/test_laudo.py:35`, na linha do `assert`.
3. **Obtido x esperado.** `assert 'REPROVADO' == 'APROVADO'`: à esquerda o que o código
   devolveu, à direita o que o teste esperava.
4. **Padrão.** No resumo, só as bordas (19.0 e 21.0) falharam. Isso já aponta o bug: a
   comparação nas bordas.

Sem o `--tb=short`, o pytest mostra também o código do teste inteiro e os valores dos
parâmetros (`valor = 19.0, esperado = 'APROVADO'`). Com `approx`, mostra a tolerância:
um bug que divide a média por `len(valores) - 1` aparece como
`assert 30.15 == 20.1 ± 2.0e-05`. O número obtido é uma pista: "que conta dá 30.15?"
(`60.3 / 2`, em vez de `60.3 / 3`).

## 5. Anatomia de um bom teste

**O padrão AAA.** Todo teste tem três partes: **Arrange** (preparar os dados), **Act**
(chamar o código, de preferência uma vez) e **Assert** (conferir). Separe-as com linha em
branco ou comentário, como no teste da seção 3.

**Nomes que contam a história.** O nome aparece no relatório de falha: em vez de
`test_1` ou `test_erro`, use `test_media_de_lista_vazia_levanta_erro`.

**Regras de ouro.** Um comportamento por teste (se o nome precisa de "e", talvez sejam
dois). Testes independentes: a ordem não pode importar. Rápidos: sem internet, sem banco
real, sem `sleep`. Determinísticos: o mesmo código dá sempre o mesmo resultado.

### Como escolher os casos (o pensamento por trás)

Não dá para testar todos os números do mundo. Agrupe as entradas em "famílias" que devem
se comportar igual e teste **um representante de cada**, mais as **bordas** entre elas.
Para `avaliar(valor, 19.0, 21.0)`:

```text
   REPROVADO      |        APROVADO         |     REPROVADO
------------------+-------------------------+------------------
      18.99     19.0         20.0         21.0    21.01
  (logo abaixo) (borda)    (meio)       (borda) (logo acima)
```

Cinco casos cobrem a regra inteira. Bugs adoram as bordas (`<` no lugar de `<=`). Para
listas, lembre também: vazia, um elemento, muitos. Para números: zero, negativo, decimal.
Para texto: vazio, espaços, acentos.

## 6. Floats e erros: `pytest.approx` e `pytest.raises`

**approx.** Nunca compare floats com `==` exato. `pytest.approx` aceita uma pequena
diferença (por padrão, um milionésimo do valor). Funciona com listas, tuplas e
dicionários, e você escolhe a tolerância com `abs=` (absoluta) ou `rel=` (relativa).
Rode `exemplos/02_approx_e_raises.py`: `20.1 == pytest.approx(20.0)` dá `False`, mas
`20.1 == pytest.approx(20.0, abs=0.2)` dá `True`.

**raises.** Quando o comportamento correto é **levantar um erro**, use `pytest.raises`
como bloco `with`. O teste passa se o erro acontecer, e falha se não acontecer.

```python
def test_media_de_lista_vazia_levanta_erro():
    with pytest.raises(ValueError, match="vazia"):
        media([])
```

- `match=` confere a mensagem com uma expressão regular (`re.search`, módulo 05). Se a
  mensagem tiver parênteses ou pontos, use `match=re.escape("valor (kg) inválido")`.
- `with pytest.raises(ValueError) as excinfo:` guarda o erro; depois do bloco,
  `str(excinfo.value)` é a mensagem.

> ⚠️ **Erro comum:** `pytest.raises(Exception)`. Ele aceita **qualquer** erro, até um
> `NameError` causado por um bug, e o teste passa por acaso. Sempre use o tipo exato.

> ⚠️ **Erro comum:** colocar várias linhas dentro do `with pytest.raises`. A linha que
> levanta o erro deve ser a última do bloco; o que vem depois dela nunca roda.

## 7. Vários casos: `@pytest.mark.parametrize`

Testar cinco valores copiando o teste cinco vezes é repetição. O `parametrize` roda a
mesma função para cada linha de uma tabela:

```python
@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (19.0, "APROVADO"),  # na borda inferior
        (20.0, "APROVADO"),
        (21.0, "APROVADO"),  # na borda superior
        (18.99, "REPROVADO"),
        (21.01, "REPROVADO"),
    ],
)
def test_avaliar_respeita_as_bordas(valor, esperado):
    assert avaliar(valor, 19.0, 21.0) == esperado
```

Cada linha vira um teste separado, com o caso entre colchetes:
`test_avaliar_respeita_as_bordas[19.0-APROVADO]`. Se um caso falha, os outros continuam.
Quando os valores são longos ou têm acentos, o nome gerado fica feio
(`Tra\xe7\xe3o: reprovado-esperado1`). Dê nomes aos casos com
`ids=["um-liberado", "um-reprovado", "dois-ensaios"]` como último argumento do
`parametrize` (veja `tests/test_observacao.py` no mini projeto).

> 🔮 **Preveja antes de rodar:** quantos testes o pytest conta neste arquivo?
>
> ```python
> @pytest.mark.parametrize("linha", ["A", "B", "C", "D"])
> @pytest.mark.parametrize("ensaio", ["espessura", "cof"])
> def test_combinacoes(linha, ensaio):
>     assert linha in "ABCD"
> ```

<details><summary>Resposta</summary>

**8.** Dois `parametrize` empilhados geram todas as combinações: 4 linhas × 2 ensaios.
Saída real: `8 passed in 0.01s`.

</details>

> 🔧 **Modifique:** no mini projeto, acrescente ao `test_avaliar_respeita_as_bordas` o caso
> `(0.0, "REPROVADO")` e rode `python -m pytest -k bordas -v`. Depois mude o esperado de
> propósito para `"APROVADO"` e leia a falha.

## 8. Fixtures: preparando o terreno

Vários testes precisam dos mesmos dados: uma lista de medições, um arquivo, uma conexão.
Uma **fixture** é uma função que prepara esse terreno. O teste a pede pelo **nome do
parâmetro** e o pytest entrega o valor pronto. Pense na bancada que o técnico arruma antes
de cada ensaio: a fixture arruma a bancada, o teste faz o ensaio.

```python
@pytest.fixture
def medicoes_espessura() -> list[float]:
    """Três medições de espessura (µm) de uma bobina com nominal de 20 µm."""
    return [20.1, 19.8, 20.4]


def test_media_de_tres_medicoes(medicoes_espessura):
    assert media(medicoes_espessura) == pytest.approx(20.1)
```

- **Uma fixture nova para cada teste** (por padrão). Se um teste altera a lista, o
  próximo recebe outra, intacta.
- **Fixture pode usar fixture.** No mini projeto, `arquivo_medicoes` pede `tmp_path` e
  `medicoes_espessura`.
- **`conftest.py`** guarda as fixtures compartilhadas. O pytest carrega esse arquivo
  sozinho, e as fixtures dele ficam disponíveis para os testes da pasta, sem `import`.
- **Limpeza com `yield`.** O que vem antes do `yield` prepara; o que vem depois roda no
  fim do teste, mesmo que ele falhe:

```python
@pytest.fixture
def conexao():
    con = sqlite3.connect(":memory:")   # prepara (módulo 11)
    yield con                           # entrega para o teste
    con.close()                         # limpa no final
```

> 🔮 **Preveja antes de rodar:** com `python -m pytest -s`, quantas vezes aparece
> "criando bobina"? O segundo teste passa?
>
> ```python
> @pytest.fixture
> def bobina():
>     print("criando bobina")
>     return {"op": "12345", "peso": 250.0}
>
>
> def test_peso(bobina):
>     bobina["peso"] = 0.0
>     assert bobina["peso"] == 0.0
>
>
> def test_peso_continua_original(bobina):
>     assert bobina["peso"] == 250.0
> ```

<details><summary>Resposta</summary>

Aparece **duas vezes**, e os dois testes passam (`2 passed`). A fixture roda de novo para
cada teste, então o segundo recebe um dicionário novo, com o peso original. É isso que
deixa os testes independentes.

</details>

## 9. Arquivos de verdade em pasta temporária: `tmp_path`

Para testar código que lê ou grava arquivos sem sujar seu computador, a fixture pronta
`tmp_path` entrega um `Path` (módulo 06) para uma **pasta temporária nova, só deste
teste**. O padrão é: criar o arquivo do caso, chamar a função, conferir.

```python
def test_ler_medicoes_ignora_linhas_vazias(tmp_path):
    arquivo = tmp_path / "com_buracos.txt"
    arquivo.write_text("20,1\n\n   \n19,8\n", encoding="utf-8")
    assert ler_medicoes(arquivo) == [20.1, 19.8]
```

Quando vários testes criam arquivos, uma *fixture fábrica* evita repetição: em vez de um
valor, ela devolve uma **função** que cria arquivos. Veja a fixture `criar_arquivo` no
teste do exercício 08 (`testes/test_m09_ex08_ler_medicoes.py`).

## 10. O que foi impresso e o que foi registrado: `capsys` e `caplog`

**capsys.** Funções que imprimem também se testam. `capsys.readouterr()` devolve o que
saiu no terminal até aquele momento, em `.out` (saída normal) e `.err` (saída de erro).

```python
def test_conferir_op_sem_acessar_o_erp(monkeypatch, capsys, medicoes_espessura):
    monkeypatch.setattr(laudo, "buscar_nominal_no_erp", lambda op: 20.0)

    resultado = conferir_op("12345", medicoes_espessura, 5.0)

    assert resultado == "APROVADO"
    saida = capsys.readouterr().out
    assert saida == "OP 12345: média 20.10 em [19.00, 21.00] -> APROVADO\n"
```

Repare no `\n` no fim: o `print` acrescenta a quebra de linha (o `monkeypatch` da
primeira linha fica para a seção 11).

> 🔮 **Preveja antes de rodar:** este teste passa ou falha?
>
> ```python
> def test_capsys_duas_vezes(capsys):
>     print("primeira")
>     a = capsys.readouterr().out
>     print("segunda")
>     b = capsys.readouterr().out
>     assert (a, b) == ("primeira\n", "segunda\n")
> ```

<details><summary>Resposta</summary>

**Passa.** Cada `readouterr()` devolve o que foi impresso **desde a leitura anterior** e
"esvazia" o capturado. Por isso `b` tem só a segunda linha.

</details>

**caplog.** Para código que usa `logging` (seção 17), a fixture `caplog` captura os
registros. Cada registro tem nível (`levelname`), nome do logger (`name`) e mensagem
(`getMessage()`); `caplog.text` junta tudo num texto só.

```python
def test_aviso_vai_para_o_log(caplog):
    logger = logging.getLogger("inspecao")
    logger.warning("OP %s FORA", "12346")
    assert caplog.records[0].levelname == "WARNING"
    assert "12346 FORA" in caplog.text
```

Por padrão o logging só deixa passar WARNING para cima. Para capturar INFO, chame
`caplog.set_level(logging.INFO)` no começo do teste.

## 11. Trocando peças: `monkeypatch`

O `conferir_op` do mini projeto consulta o ERP. Nos testes, não dá para depender do
TOTVS: é lento, precisa de rede e senha, e os dados mudam. A fixture `monkeypatch`
**troca uma peça durante o teste** e desfaz a troca sozinha no final:

```python
monkeypatch.setattr(laudo, "buscar_nominal_no_erp", lambda op: 20.0)
```

Lê-se: "no módulo `laudo`, durante este teste, `buscar_nominal_no_erp` passa a ser uma
função que sempre devolve 20.0".

| Chamada | Efeito durante o teste |
|---|---|
| `monkeypatch.setattr(modulo, "nome", novo)` | troca uma função ou atributo |
| `monkeypatch.setenv("LAB_OPERADOR", "Maria")` | cria ou altera variável de ambiente |
| `monkeypatch.delenv("LAB_OPERADOR", raising=False)` | apaga a variável (se existir) |
| `monkeypatch.chdir(tmp_path)` | muda a pasta atual |

> ⚠️ **Erro comum:** trocar a peça no lugar errado. `conferir_op` procura o nome
> `buscar_nominal_no_erp` **dentro do módulo `laudo`** na hora em que roda, por isso
> trocamos `laudo.buscar_nominal_no_erp`. Regra: troque onde a função é **usada**.

**A alternativa elegante: injeção de dependência.** Quando é você quem escreve o código,
receba a dependência como parâmetro, com o valor real como padrão (funções são valores,
módulo 04). O teste passa a função falsa direto, sem `monkeypatch`:

```python
def conferir_op(op, valores, tolerancia_pct, buscar_nominal=buscar_nominal_no_erp):
    nominal = buscar_nominal(op)
    ...


def test_conferir_op_com_erp_falso():
    resultado = conferir_op("12345", [20.1, 19.8, 20.4], 5.0, buscar_nominal=lambda op: 20.0)
    assert resultado == "APROVADO"
```

> 💡 **Dica:** prefira injeção de dependência no código novo; use `monkeypatch` para código
> que você não pode mudar e para variáveis de ambiente. Os dois voltam nos módulos 12 e 13
> (APIs e robôs testados sem internet).

## 12. Exemplo resolvido: testes para uma função que você não escreveu

Três exercícios deste módulo invertem o papel: a função existe e **você escreve os
testes**. O curso confere se eles aprovam a versão certa e reprovam versões com bug. Veja
como eu penso um caso parecido, passo a passo.

**O problema:** testar `contar_fora(valores, minimo, maximo)`, que conta quantos valores
estão fora de `[minimo, maximo]`, com as bordas dentro.

**Passo 1, listar as regras.** Releio a especificação e anoto uma regra por linha:
(a) conta os de fora; (b) bordas estão dentro; (c) lista vazia dá 0.

**Passo 2, um caso por regra.** Para (a), uma lista com valores dentro e fora, e um
resultado que não seja óbvio (2, não 0). Para (b), valores exatamente nas bordas. Para
(c), lista vazia.

**Passo 3, perguntar "que bug este caso pega?".** O das bordas pega quem usou `<=` no
lugar de `<`. Se um caso não pega nenhum bug novo, é repetido.

**Passo 4, escrever, com mensagens úteis:**

```python
def testar_contar_fora(contar_fora):
    # Regra: conta os valores fora de [mínimo, máximo]
    assert contar_fora([20.0, 22.5, 18.0], 19.0, 21.0) == 2
    # Bordas: estão DENTRO
    assert contar_fora([19.0, 21.0], 19.0, 21.0) == 0, "bordas devem estar dentro"
    # Lista vazia: nada fora
    assert contar_fora([], 19.0, 21.0) == 0
```

**Passo 5, provar que os testes funcionam.** Rodo contra uma versão certa e uma com bug
(`valor <= minimo`):

```text
versão correta: aprovada
versão com bug: reprovada (bordas devem estar dentro)
```

Um teste que nunca falha não protege nada. Sempre confira que ele **consegue** falhar.

## 13. TDD passo a passo: vermelho → verde → refatorar

TDD (*Test-Driven Development*) inverte a ordem: o teste vem **antes** do código. O ciclo
tem três passos curtos:

```text
VERMELHO: teste que falha -> VERDE: código mínimo -> REFATORAR: melhora com tudo verde
   ^                                                                    |
   +------------------------ próximo comportamento ---------------------+
```

Você pensa no **uso** antes da implementação, avança em passos pequenos e termina com
testes para tudo. Vamos construir `ler_liberacoes`, que lê a observação de liberação da
planilha do projeto final: `"COF: liberado; Selagem: reprovado"` deve virar
`{"COF": True, "SELAGEM": False}`.

### Ciclo 1: o caso mais simples

**Vermelho.** Em `tests/test_observacao.py`:

```python
from observacao import ler_liberacoes


def test_um_ensaio_liberado():
    assert ler_liberacoes("COF: liberado") == {"COF": True}
```

O arquivo `observacao.py` ainda nem existe. Trecho da saída:

```text
> python -m pytest tests/test_observacao.py -q
...
E   ModuleNotFoundError: No module named 'observacao'
...
1 error in 0.16s
```

Vermelho também conta: o teste pediu algo que não existe.

**Verde.** O código **mínimo** para passar. Mínimo mesmo:

```python
def ler_liberacoes(observacao: str) -> dict[str, bool]:
    return {"COF": True}
```

Resultado: `1 passed`. Parece trapaça, mas prova que o teste está ligado ao código. Quem
vai forçar a lógica de verdade é o próximo teste.

### Ciclo 2: generalizar

**Vermelho.** Um caso que o "código falso" não resolve:

```python
def test_um_ensaio_reprovado():
    assert ler_liberacoes("Tração: reprovado") == {"TRAÇÃO": False}
```

```text
.F                                                                       [100%]
...
>       assert ler_liberacoes("Tração: reprovado") == {"TRAÇÃO": False}
E       AssertionError: assert {'COF': True} == {'TRAÇÃO': False}
```

**Verde.** Agora sim, separar ensaio e status:

```python
def ler_liberacoes(observacao: str) -> dict[str, bool]:
    ensaio, status = observacao.split(":")
    return {ensaio.strip().upper(): status.strip() == "liberado"}
```

Resultado: `2 passed`.

### Ciclo 3: vários ensaios

**Vermelho.**

```python
def test_varios_ensaios_separados_por_ponto_e_virgula():
    resultado = ler_liberacoes("COF: liberado; Selagem: reprovado")
    assert resultado == {"COF": True, "SELAGEM": False}
```

```text
..F                                                                      [100%]
...
>       ensaio, status = observacao.split(":")
        ^^^^^^^^^^^^^^
E       ValueError: too many values to unpack (expected 2)

observacao.py:2: ValueError
```

O erro está no **nosso** código: com dois ensaios, o `split(":")` devolve três pedaços.

**Verde.** Primeiro separar por `;`, depois cada item por `:`. Resultado: `3 passed`.

```python
def ler_liberacoes(observacao: str) -> dict[str, bool]:
    resultado = {}
    for item in observacao.split(";"):
        ensaio, status = item.split(":")
        resultado[ensaio.strip().upper()] = status.strip() == "liberado"
    return resultado
```

### Ciclo 4: status desconhecido é erro

Hoje, `"COF: pendente"` vira `{"COF": False}`, como se fosse reprovado. Perigoso. Regra
nova: status desconhecido levanta `ValueError`.

**Vermelho.**

```python
def test_status_desconhecido_levanta_erro():
    with pytest.raises(ValueError, match="pendente"):
        ler_liberacoes("COF: pendente")
```

```text
...F                                                                     [100%]
...
>       with pytest.raises(ValueError, match="pendente"):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE ValueError
```

**Verde.** Dentro do laço, um `if status == "liberado"` / `elif status == "reprovado"` e,
no `else`, `raise ValueError(f"status desconhecido: {status!r}")`. Resultado: `4 passed`.

### Refatorar

Tudo verde. Agora, **sem mudar o comportamento**, melhoro o código: o `if/elif` vira um
dicionário de status válidos, e a leitura de um item ganha uma função com nome. Os três
primeiros testes, iguais na forma, viram um `parametrize` (o da seção 7).

```python
STATUS_VALIDOS = {"liberado": True, "reprovado": False}


def _ler_item(item: str) -> tuple[str, bool]:
    """Converte 'COF: liberado' em ('COF', True)."""
    ensaio, status = item.split(":")
    status = status.strip()
    if status not in STATUS_VALIDOS:
        raise ValueError(f"status desconhecido: {status!r}")
    return ensaio.strip().upper(), STATUS_VALIDOS[status]


def ler_liberacoes(observacao: str) -> dict[str, bool]:
    """Converte 'COF: liberado; Selagem: reprovado' em {'COF': True, 'SELAGEM': False}."""
    return dict(_ler_item(item) for item in observacao.split(";"))
```

Rodando de novo, os 4 testes continuam passando. Este é o `observacao.py` do mini
projeto. Repare como os testes deram coragem para reescrever a função inteira.

> 🔧 **Modifique:** o técnico às vezes digita `"COF: LIBERADO"`. Faça um ciclo de TDD:
> escreva o teste (vermelho), mude uma linha de `_ler_item` (verde) e rode tudo.

> 💡 **Dica:** no TDD, rode com `-x` para parar na primeira falha e trabalhe **um teste
> por vez**. Nos exercícios, na pasta `curso-python`:
> `python -m pytest 09-testes-e-qualidade/testes/test_m09_ex08_ler_medicoes.py -x`.

## 14. Cobertura de testes (conceito)

**Cobertura** responde: "quais linhas do meu código rodaram durante os testes?". A
ferramenta mais usada é o plugin `pytest-cov` (`python -m pip install pytest-cov`). No
mini projeto:

```text
> python -m pytest --cov=laudo --cov=observacao --cov-report=term-missing
................                                                         [100%]
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.13.16-final-0 _______________

Name            Stmts   Miss  Cover   Missing
---------------------------------------------
laudo.py           30      2    93%   12, 47
observacao.py       9      0   100%
---------------------------------------------
TOTAL              39      2    95%
16 passed in 0.09s
```

A coluna `Missing` lista as linhas que **nenhum** teste executou:

- Linha 12 de `laudo.py`: o `raise` de "nominal deve ser positivo". Esquecemos de testar
  nominal zero ou negativo. Lacuna real.
- Linha 47: o `raise ConnectionError` do ERP, que trocamos com `monkeypatch` de propósito.
  Lacuna aceitável.

> ⚠️ **Erro comum:** perseguir 100% como meta. Cobertura mostra o que **não** foi testado,
> mas não prova que o resto foi bem testado: um teste sem `assert` "cobre" linhas e não
> confere nada. Use a cobertura como lanterna, não como nota.

> 🔧 **Modifique:** escreva no mini projeto um teste para `calcular_limites(0.0, 5.0)` com
> `pytest.raises(ValueError)` e rode a cobertura de novo. A linha 12 sai do `Missing`.

## 15. ruff: lint e formatação automáticos

Revisar espaço em branco e import esquecido é trabalho de máquina. O **ruff** faz duas
coisas, muito rápido:

- `ruff check` (**lint**) procura problemas: import não usado, variável esquecida,
  armadilhas conhecidas.
- `ruff format` (**formatação**) padroniza espaços, quebras de linha e aspas. Muda a
  aparência, nunca o comportamento. (`black` e `isort`, que você conhece de nome, fazem
  parte do que o ruff faz, num programa só.)

O arquivo `ruff.toml`, na raiz do curso, vale para todos os módulos: linhas de até 95
caracteres, código compatível com Python 3.10+ e estas famílias de regras:

| Código | Família | Exemplo do que pega |
|---|---|---|
| `E`, `W` | estilo (pycodestyle) | dois imports na mesma linha, espaço no fim da linha |
| `F` | erros prováveis (pyflakes) | import não usado, variável nunca usada |
| `I` | ordem dos imports (isort) | imports fora da ordem padrão |
| `B` | armadilhas (bugbear) | lista como valor padrão de parâmetro |
| `UP` | modernização (pyupgrade) | `"%s" % x` no lugar de f-string |

O `exemplos/05_ruff_na_pratica.py` cria um arquivo bagunçado numa pasta temporária e roda
o ruff nele. O arquivo:

```python
import os, sys
import json


def conferir(valores, minimo, maximo, avisos=[]):
    aprovados = []
    total = len(valores)
    for i in range(len(valores)):
        v = valores[i]
        if v >= minimo and v <= maximo:
            aprovados.append(v)
        else:
            avisos.append("fora: %s" % v)
    return len(aprovados) == len(valores)
```

E o que o ruff diz:

```text
> ruff check --output-format concise conferencia.py
conferencia.py:1:1: E401 [*] Multiple imports on one line
conferencia.py:1:1: I001 [*] Import block is un-sorted or un-formatted
conferencia.py:1:8: F401 [*] `os` imported but unused
conferencia.py:1:12: F401 [*] `sys` imported but unused
conferencia.py:2:8: F401 [*] `json` imported but unused
conferencia.py:5:46: B006 Do not use mutable data structures for argument defaults
conferencia.py:7:5: F841 Local variable `total` is assigned to but never used
conferencia.py:13:27: UP031 Use format specifiers instead of percent format
Found 8 errors.
[*] 5 fixable with the `--fix` option (3 hidden fixes can be enabled with the `--unsafe-fixes` option).
```

Cada linha traz `arquivo:linha:coluna: CÓDIGO mensagem`. O `[*]` marca o que o ruff
conserta sozinho com `ruff check --fix`. Os outros três exigem você: apagar `total`,
trocar o `%` por f-string e resolver o `avisos=[]`. (Sem `--output-format concise`, cada
problema vem com o trecho do código e uma sugestão.)

> 🔮 **Preveja antes de rodar:** o B006 não é frescura. Lembra do módulo 04? O que este
> código imprime?
>
> ```python
> def conferir(valor, avisos=[]):
>     if valor > 21.0:
>         avisos.append(f"fora: {valor}")
>     return avisos
>
>
> print(conferir(22.0))
> print(conferir(23.5))
> ```

<details><summary>Resposta</summary>

```text
['fora: 22.0']
['fora: 22.0', 'fora: 23.5']
```

A lista padrão é criada **uma vez**, quando a função é definida, e é reaproveitada em
todas as chamadas: o aviso da primeira OP "vaza" para a segunda. A correção é
`avisos=None` e, dentro, `if avisos is None: avisos = []`. O ruff pegou um bug real.

</details>

No dia a dia: `ruff check .` lista os problemas da pasta, `ruff check --fix .` conserta
os que têm `[*]`, `ruff format --diff .` mostra o que a formatação mudaria, `ruff format .`
formata tudo e `ruff format --check .` só confere (útil no CI).

> 💡 **Dica:** no VS Code, instale a extensão **Ruff** (da Astral), escolha-a como
> formatador padrão de Python e ligue **Format On Save** nas configurações. O código passa
> a ser formatado sempre que você salva.

## 16. Type hints e mypy (conceito)

Você lê type hints desde o módulo 01, nos exercícios: `def media(valores: list[float]) ->
float`. Eles dizem o que a função espera e o que devolve. O ponto que pouca gente sabe:
**o Python não confere os type hints ao rodar.** Em `exemplos/07_type_hints.py`, a função
`juntar(a: int, b: int) -> int` recebe `"10"` e `"20"` e devolve `"1020"`, sem reclamar. Quem confere os tipos
é uma ferramenta separada, o **mypy**, que lê o código **sem executá-lo**. Num arquivo
`pesos.py`, com três problemas que só apareceriam rodando o programa num caso específico:

```python
def somar_pesos(pesos: list[float]) -> float:
    return sum(pesos)


def peso_medio(pesos: list[float]) -> float:
    if not pesos:
        return None
    return somar_pesos(pesos) / len(pesos)


total = somar_pesos(["250,5", "120,0"])
print(total.upper())
```

```text
> python -m pip install mypy
> mypy pesos.py
pesos.py:7: error: Incompatible return value type (got "None", expected "float")  [return-value]
pesos.py:11: error: List item 0 has incompatible type "str"; expected "float"  [list-item]
pesos.py:11: error: List item 1 has incompatible type "str"; expected "float"  [list-item]
pesos.py:12: error: "float" has no attribute "upper"  [attr-defined]
Found 4 errors in 1 file (checked 1 source file)
```

A linha 7 é a mais interessante: a anotação promete `float`, mas a função pode devolver
`None`. Se for de propósito, a anotação certa é `-> float | None`, e o mypy passa a
obrigar quem chama a tratar o `None`.

Nos exercícios "escreva os testes" aparece `Callable[[list[float]], float]` (de
`collections.abc`): "uma função que recebe lista de floats e devolve float". A sua função
de teste recebe **outra função** como parâmetro.

> 💡 **Dica:** type hints são **graduais**: comece pelas funções públicas. O VS Code
> (Pylance) já usa as anotações para autocompletar e sublinhar erros enquanto você digita.

## 17. logging: os prints dos profissionais

O robô do projeto final vai rodar sozinho, de madrugada. Ninguém vai ver o terminal. Se
algo der errado, você precisa de um **registro** do que aconteceu, com data, hora e
gravidade. É para isso que existe o módulo `logging`.

| Nível | Quando usar | Exemplo |
|---|---|---|
| `DEBUG` | detalhes para quem está depurando | "lendo linha 37 da aba A" |
| `INFO` | o normal, marcos do processo | "OP 12345 conferida" |
| `WARNING` | algo estranho, mas o programa segue | "OP 12346 fora da tolerância" |
| `ERROR` | uma operação falhou | "não consegui ler o valor da OP 12347" |
| `CRITICAL` | o programa não consegue continuar | "planilha de regras não encontrada" |

O padrão de uso tem três partes: (1) em cada módulo, um logger com nome,
`logger = logging.getLogger(__name__)`; (2) **uma vez**, no início do programa, a
configuração com `logging.basicConfig(...)`; (3) no código, `logger.info(...)`,
`logger.warning(...)` etc. Trecho de `exemplos/03_logging_inspecao.py`:

```python
logging.basicConfig(
    level=logging.INFO,  # DEBUG fica de fora; INFO e acima aparecem
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    handlers=[
        logging.StreamHandler(),  # terminal
        logging.FileHandler(ARQUIVO_LOG, mode="w", encoding="utf-8"),  # arquivo
    ],
)
```

```text
> python exemplos/03_logging_inspecao.py
29/10/2026 02:43:42 INFO     inspecao: Início da conferência
29/10/2026 02:43:42 INFO     inspecao: OP 12345: 20.10 dentro de [19.00, 21.00]
29/10/2026 02:43:42 WARNING  inspecao: OP 12346: 22.40 FORA de [19.00, 21.00]
29/10/2026 02:43:42 ERROR    inspecao: OP 12347: valor ilegível na planilha
Traceback (most recent call last):
  File ".../exemplos/03_logging_inspecao.py", line 47, in main
    conferir("12347", float("vinte"), 19.0, 21.0)
                      ~~~~~^^^^^^^^^
ValueError: could not convert string to float: 'vinte'
29/10/2026 02:43:42 INFO     inspecao: Fim da conferência

Log gravado em: inspecao.log
```

A data e a hora serão as do seu computador (encurtei o caminho do arquivo). O mesmo
conteúdo foi gravado em `exemplos/saida/inspecao.log`, em UTF-8. Repare:

- `logger.exception(...)`, dentro de um `except`, registra no nível ERROR **com o
  traceback completo**. É o que você vai querer ler no dia seguinte.
- O `logger.debug(...)` do exemplo não apareceu, porque o nível mínimo é INFO. Para
  investigar um problema, mude para `level=logging.DEBUG` sem tocar no resto do código.
- O exemplo usa o estilo tradicional, `logger.info("OP %s: %.2f", op, valor)`, em que o
  texto só é montado se a mensagem for aparecer. f-string também funciona.

> ⚠️ **Erro comum:** chamar `basicConfig` dentro de funções ou em vários módulos. Só a
> primeira chamada vale; as outras são ignoradas em silêncio. Configure uma vez, no `main`.

## 18. Depuração: `breakpoint()` e o debugger do VS Code

Depurar é investigar, com o método de uma análise de não conformidade: (1)
**reproduza** com um caso pequeno, de preferência um teste que falha; (2) **observe** o
que entra, o que sai e onde muda; (3) **formule uma hipótese** ("o total está sendo
zerado a cada volta"); (4) **teste a hipótese** no REPL ou no depurador; (5) **corrija**
e mantenha o teste, que impede a volta do bug.

`print` ajuda a observar, mas o **depurador** é mais poderoso: ele **pausa** o programa
numa linha e deixa você ver todas as variáveis e avançar uma linha por vez.

### breakpoint() e o pdb

O `exemplos/04_depuracao.py` calcula a média do COF e erra:

```text
> python exemplos/04_depuracao.py
Leituras: ['0,32', '0,35', '0,30']
Média calculada: 0.1000
Média esperada:  0.3233  (0,32 + 0,35 + 0,30) / 3
```

Dentro de `media_cof` há um `breakpoint()`, ativado com `--depurar`. Quando o Python
chega nele, abre o **pdb**, o depurador que vem com o Python. Trecho de uma sessão real
(os comandos digitados vêm depois de `(Pdb)`; encurtei os caminhos):

```text
> python exemplos/04_depuracao.py --depurar
> .../exemplos/04_depuracao.py(26)media_cof()
-> breakpoint()  # o programa para aqui e abre o depurador
(Pdb) n
> .../exemplos/04_depuracao.py(27)media_cof()
-> total = 0.0
...
> .../exemplos/04_depuracao.py(30)media_cof()
-> total = valor  # BUG de propósito: deveria ser total += valor
(Pdb) p valor, total
(0.35, 0.32)
(Pdb) n
> .../exemplos/04_depuracao.py(28)media_cof()
-> for leitura in leituras:
(Pdb) p total
0.35
(Pdb) c
```

Na segunda volta, antes da linha 30, `valor` é 0.35 e `total` é 0.32. Depois dela, o
`total` deveria ser `0.32 + 0.35 = 0.67`, mas virou `0.35`: foi **substituído**, não
somado. Hipótese confirmada: `total = valor` deveria ser
`total += valor`.

| Comando pdb | Faz |
|---|---|
| `n` (next) | executa a linha atual e para na próxima |
| `s` (step) | entra na função chamada na linha atual |
| `c` (continue) | segue até o próximo breakpoint (ou o fim) |
| `p expr` / `pp expr` | mostra o valor de uma expressão (`pp` formata listas e dicionários) |
| `l` (list) / `w` (where) | mostra o código em volta / a pilha de chamadas |
| `q` (quit) | encerra o programa |

> 💡 **Dica:** `python -m pytest --pdb` abre o pdb **no ponto exato da falha** de um teste.
> E a variável de ambiente `PYTHONBREAKPOINT=0` desliga todos os `breakpoint()`. Antes do
> commit, remova os `breakpoint()` esquecidos.

> ⚠️ **Erro comum:** estranhar a linha onde o pdb para. A partir do Python 3.13, ele para
> **na própria linha** do `breakpoint()`; em versões anteriores, na linha seguinte.

### O debugger do VS Code

O VS Code faz o mesmo com cliques:

1. Abra `exemplos/04_depuracao.py`, clique à esquerda do número da linha `total = valor`
   (ou **F9**): aparece a bolinha vermelha do *breakpoint*.
2. **F5** → **Python Debugger: Current File**. O programa para ali. O painel
   **Variables** mostra `leitura`, `valor` e `total`; em **Watch**, acrescente
   expressões como `total + valor`.
3. Avance com **F10** (próxima linha), **F11** (entrar na função), **Shift+F11** (sair
   dela) e **F5** (continuar). Na **Debug Console**, digite qualquer expressão Python.
4. Botão direito na bolinha → **Edit Breakpoint** cria um *breakpoint condicional*
   (`leitura == "0,30"`): só para quando a condição é verdadeira.

Para depurar um **teste**, configure o pytest no VS Code (ícone do frasco, **Testing** →
**Configure Python Tests** → **pytest** → pasta `curso-python`) e use **Debug Test** no
botão direito do teste.

## 19. Git no dia a dia

No módulo 00 você usou Git sozinho, na branch principal. Num time, ninguém mexe direto na
`main`: cada mudança nasce numa **branch**, vira um **pull request** (PR), passa por
**revisão** e só então entra na `main`, que fica sempre funcionando.

Fluxo executado num repositório de exemplo (no seu computador, o Git pode responder em
português):

```text
> git switch -c corrige-borda-tolerancia
Switched to a new branch 'corrige-borda-tolerancia'
```

Você edita o código e roda os testes. Antes do commit, **sempre** confira o que mudou
(`git status` lista os arquivos; `git diff` mostra as linhas):

```text
> git diff
diff --git a/tolerancia.py b/tolerancia.py
index 3524197..d5f5cb5 100644
--- a/tolerancia.py
+++ b/tolerancia.py
@@ -1,2 +1,2 @@
 def avaliar(valor, minimo, maximo):
-    return "APROVADO" if minimo < valor < maximo else "REPROVADO"
+    return "APROVADO" if minimo <= valor <= maximo else "REPROVADO"
```

Linhas com `-` saíram, com `+` entraram. Agora o commit, com título e corpo (cada `-m`
vira um parágrafo):

```text
> git add tolerancia.py
> git commit -m "Corrige bordas na avaliação de tolerância" -m "Valores iguais ao mínimo ou ao máximo estão dentro da especificação. Antes, uma bobina com espessura exatamente no limite era reprovada."
[corrige-borda-tolerancia cf2cfbb] Corrige bordas na avaliação de tolerância
 1 file changed, 1 insertion(+), 1 deletion(-)
```

Por fim, `git push -u origin corrige-borda-tolerancia` manda a branch para o GitHub, que
oferece o botão **Compare & pull request**.

### Commits pequenos, mensagens boas

Um commit é **uma ideia**: "corrige a borda", e não "corrige a borda, muda o relatório e
renomeia três funções". Commits pequenos são fáceis de revisar e de desfazer. Mensagens
como `ajustes` ou `commit final agora vai` não dizem nada; `Troca prints de aviso por
logging` diz. Título no imperativo ("Corrige", "Adiciona", "Remove"), com até uns 50 caracteres e sem
ponto final. Se precisar, deixe uma linha em branco e explique **por que** mudou (o "o
quê" o diff já mostra). `git add -p` mostra cada trecho alterado e pergunta se ele entra
no commit: é o jeito de separar duas ideias misturadas no mesmo arquivo.

### Pull request e revisão de código

A descrição de um PR responde três perguntas:

```text
O que muda
- avaliar() passa a considerar as bordas como dentro da tolerância.

Por que
- Bobinas com espessura exatamente no limite estavam sendo reprovadas (laudo da OP 12345).

Como testar
- python -m pytest -k bordas
```

**Revisão de código** é outra pessoa lendo o seu PR antes do merge: a segunda conferência
do laudo. **Como autor:** PR pequeno, testes passando, ruff limpo, descrição clara;
releia o próprio diff antes de pedir revisão. **Como revisor:** o código faz o que a
descrição diz? Há teste para o caso novo? Os nomes são claros? Comente o código, nunca a
pessoa, e sugira ("que tal extrair isto para uma função?") em vez de ordenar.

> ⚠️ **Erro comum:** fazer commit de senha, token ou planilha com dados de cliente. Uma vez
> no GitHub, considere vazado: o histórico guarda tudo. Use variáveis de ambiente (como no
> exercício 04) e um `.gitignore` para arquivos como `.env` e `saida/`.

## 20. Código limpo e refatoração

Código é lido muito mais vezes do que é escrito, inclusive por você daqui a seis meses.
Regras práticas:

- **Nomes que contam a história:** `margem`, `tolerancia_pct`, `media_cof`. Nada de `x`,
  `d`, `aux2`.
- **Funções pequenas que fazem uma coisa.** Se a descrição tem "e" ("lê o arquivo **e**
  confere **e** imprime"), divida.
- **Sem números mágicos:** `if valor > 0.35` não diz nada; `if valor > COF_MAXIMO` diz.
- **Sem repetição** (a mesma regra em dois lugares vai divergir um dia) e com **retorno
  antecipado** (casos especiais no começo, sem `if` dentro de `if`).
- **Separe cálculo de impressão:** uma função que **devolve** o texto do relatório é fácil
  de testar; uma que só imprime precisa de `capsys`.
- **Comentário explica o porquê**, não o quê: `# a norma conta a borda como aprovada`.

**Refatorar é mudar a estrutura sem mudar o comportamento**, e só se faz com testes
passando antes **e** depois. Diante de código antigo sem testes, o primeiro passo é um
**teste de caracterização**: ele registra o que o código faz **hoje**, certo ou errado.
O `exemplos/06_refatoracao.py` mostra o antes:

```python
def proc(d, t):
    r = []
    for x in d:
        if x[1] == "esp":
            if x[2] >= t["esp"][0] and x[2] <= t["esp"][1]:
                r.append((x[0], "OK"))
            else:
                r.append((x[0], "FORA"))
        elif x[1] == "gram":
            if x[2] >= t["gram"][0] and x[2] <= t["gram"][1]:
                r.append((x[0], "OK"))
            else:
                r.append((x[0], "FORA"))
    return r
```

E o depois, com nomes claros, uma função pequena para a regra que se repetia e type hints
(`Medicao` e `Limites` são apelidos de tipo definidos no arquivo):

```python
def situacao(valor: float, limites: Limites) -> str:
    minimo, maximo = limites
    return "OK" if minimo <= valor <= maximo else "FORA"


def conferir_medicoes(
    medicoes: list[Medicao], tolerancias: dict[str, Limites]
) -> list[tuple[str, str]]:
    return [
        (op, situacao(valor, tolerancias[ensaio]))
        for op, ensaio, valor in medicoes
        if ensaio in tolerancias
    ]
```

```text
> python exemplos/06_refatoracao.py
Antes:  [('101', 'OK'), ('102', 'OK'), ('103', 'FORA'), ('104', 'FORA'), ('105', 'OK')]
Depois: [('101', 'OK'), ('102', 'OK'), ('103', 'FORA'), ('104', 'FORA'), ('105', 'OK')]
Mesmo resultado: refatoração segura.
```

Repare: o código antigo **ignora** ensaios sem tolerância (o COF da OP 106 sumiu do
resultado). Parece um bug, mas a refatoração **manteve** o comportamento. Refatorar e
corrigir são passos separados, em commits separados; misturar os dois é o jeito mais
rápido de não saber o que quebrou.

> 🔧 **Modifique:** em `exemplos/06_refatoracao.py`, troque `<=` por `<` em `situacao` e
> rode. O `assert` de caracterização pega a mudança? Desfaça e acrescente às `MEDICOES` o
> caso `("107", "esp", 19.0)`: a refatoração continua segura?

## Lendo mensagens de erro deste módulo

| Mensagem | O que significa | Como resolver |
|---|---|---|
| `NotImplementedError: Implemente esta função` | o teste chamou o exercício e achou o `raise` | apague a linha e escreva o código |
| `ERROR collecting ... ModuleNotFoundError` | o `import` do arquivo de teste falhou; o teste nem começou | confira nome do arquivo, pasta de onde rodou e se o código existe |
| `fixture 'tmp_pat' not found` | o parâmetro não corresponde a nenhuma fixture | erro de digitação ou fixture num `conftest.py` de outra pasta |
| `Failed: DID NOT RAISE ValueError` | o código terminou sem o erro esperado | falta o `raise`, ou o caso não é inválido como você pensou |
| `Regex pattern did not match.` | o erro certo aconteceu, mas a mensagem não bate com o `match=` | compare `Expected regex` com `Actual message` |
| `assert 30.15 == 20.1 ± 2.0e-05` | comparação com `approx` falhou | descubra que conta produz o valor obtido |
| `Unknown 'parametrise' mark, did you mean 'parametrize'?` | erro de digitação no decorator | é `parametrize`, com z |
| `no tests ran` (código de saída 5) | o pytest não achou testes | prefixos `test_`/`test` nos nomes, ou pasta errada |
| ruff `F401`, `F841` | import ou variável sem uso | apague; `I001` se resolve com `ruff check --fix` |
| mypy `Incompatible return value type` | a função promete um tipo e pode devolver outro | corrija o código ou a anotação (`float \| None`) |

Dica: o `fixture not found` vem seguido da lista de fixtures disponíveis
(`available fixtures: ..., caplog, capsys, ..., tmp_path, ...`). Procure nela o nome certo.

## Boas práticas

- Rode os testes **antes** de começar a mexer (para saber que estava verde) e depois de
  cada mudança pequena.
- Todo bug corrigido ganha um teste que falhava antes da correção. Assim ele não volta.
- Um teste que nunca falhou pode estar testando nada: quebre o código de propósito uma vez
  e veja o vermelho.
- Teste comportamento, não implementação: confira **o que** a função devolve, não
  **como** ela faz. Assim você refatora sem reescrever os testes.
- Nada de internet, banco real, data/hora atual ou aleatoriedade sem controle nos testes
  de unidade: injete a dependência ou use `monkeypatch`.
- `ruff check` e `ruff format` antes de cada commit (melhor ainda: ao salvar no VS Code).
- `logging` para o que o programa faz; `print` só para o resultado que o usuário pediu.
- Uma branch por mudança, commits pequenos, mensagens no imperativo.
- Refatorar e corrigir bug são passos separados.

## No mundo real

**Situação:** o laboratório decidiu que a gramatura da linha B passa a ter tolerância de
nominal ± 4% (nominal 22 g/m²), em vez de mínimo e máximo fixos. Você mantém o validador
de certificados. O caminho, do pedido ao merge:

1. **Branch:** `git switch -c gramatura-linha-b-percentual`.
2. **Teste primeiro (vermelho)**, com os números da norma. 22 ± 4% dá limites 21,12 e
   22,88; as bordas e os vizinhos logo fora são os casos que importam:

   ```python
   @pytest.mark.parametrize(
       ("valor", "esperado"),
       [(21.12, "OK"), (22.88, "OK"), (21.11, "FORA"), (22.89, "FORA")],
       ids=["borda-inferior", "borda-superior", "logo-abaixo", "logo-acima"],
   )
   def test_gramatura_linha_b_usa_nominal_22_mais_ou_menos_4_porcento(valor, esperado):
       regra = buscar_regra("B", "gramatura")
       assert classificar(valor, regra) == esperado
   ```

3. **Código mínimo (verde)** e **refatoração**, com `python -m pytest -x` a cada passo.
4. **Qualidade, commits e PR:** `ruff check .`, `ruff format .`, `python -m pytest -q`;
   commits pequenos ("Adiciona regra de tolerância percentual") e um PR com "o que muda /
   por que / como testar".
5. **Integração contínua (CI):** um robô roda os testes a cada push. No GitHub isso se
   chama **GitHub Actions**, configurado em `.github/workflows/testes.yml`:

   ```yaml
   name: testes
   on: [push, pull_request]
   jobs:
     qualidade:
       runs-on: windows-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: "3.12"
         - run: python -m pip install -r requirements.txt
         - run: ruff check .
         - run: ruff format --check .
         - run: python -m pytest -q
   ```

6. **Revisão:** a colega pergunta "e a linha A, que continua com mínimo e máximo fixos,
   tem teste?". Você acrescenta o teste num commit novo, ela aprova, e o merge acontece.
7. **Uma semana depois**, alguém mexe na leitura da planilha e quebra sem querer o cálculo
   da linha B. O CI fica vermelho no PR dessa pessoa, **antes** de qualquer certificado
   errado sair. É para esse dia que os testes existem.

## Resumo

| Preciso... | Uso |
|---|---|
| conferir um resultado | `assert obtido == esperado, "mensagem"` |
| comparar floats | `assert valor == pytest.approx(20.1)` |
| conferir que levanta erro | `with pytest.raises(ValueError, match="texto"):` |
| testar vários casos | `@pytest.mark.parametrize(("a", "b"), [(1, 2), ...], ids=[...])` |
| preparar dados reutilizáveis | `@pytest.fixture` (compartilhada em `conftest.py`) |
| limpar depois do teste | `yield` dentro da fixture |
| arquivo temporário | fixture `tmp_path` (um `Path`) |
| capturar `print` / log | `capsys.readouterr().out` / `caplog.records`, `caplog.text` |
| trocar função / variável de ambiente | `monkeypatch.setattr`, `setenv`, `delenv` |
| rodar testes | `python -m pytest` (`-v`, `-q`, `-x`, `-k nome`, `--lf`, `-s`, `--pdb`) |
| cobertura | `python -m pytest --cov=modulo --cov-report=term-missing` |
| lint / formatação | `ruff check --fix .` / `ruff format .` |
| conferir tipos | `mypy arquivo.py` |
| registrar o que acontece | `logger = logging.getLogger(__name__)`; `logger.info(...)` |
| pausar e investigar | `breakpoint()` → `n`, `s`, `p var`, `c`, `q` |
| fluxo Git | `git switch -c nome` → `git diff` → `git add` → `git commit` → `git push` → PR |
| ciclo TDD | vermelho → verde → refatorar, um teste por vez |

## Você domina este módulo se...

- [ ] Escrevo um teste no padrão AAA e explico, sem consultar, cada parte da saída de uma
      falha do pytest.
- [ ] Escolho casos de teste pensando em famílias de entrada e bordas, e sei explicar por
      que `pytest.raises(Exception)` é uma armadilha.
- [ ] Uso `parametrize`, uma fixture minha e as fixtures `tmp_path`, `capsys` e
      `monkeypatch` sem olhar a aula.
- [ ] Desenvolvo uma função pequena em TDD, dizendo em qual passo do ciclo estou.
- [ ] Explico a diferença entre `ruff check` e `ruff format`, e entre o que o Python faz
      com type hints e o que o mypy faz.
- [ ] Troco `print` por `logging` com nível e formato certos, e sei onde chamar
      `basicConfig`.
- [ ] Acho um bug com `breakpoint()` ou com o debugger do VS Code, inspecionando variáveis
      linha a linha.
- [ ] Faço uma mudança numa branch, com commits pequenos e mensagens no imperativo, e
      escrevo a descrição de um pull request.

## Exercícios

Este módulo tem três tipos de exercício:

- **Implementar (TDD):** os testes já existem e são a especificação. Leia, rode, veja
  falhar e faça passar, um por vez.
- **Conserte o bug (leitura de código):** não há `NotImplementedError`; o código já está
  lá, com defeitos. Leia, preveja o que ele faz, rode os testes e corrija.
- **Escreva os testes:** a função a testar chega **como parâmetro** e você escreve os
  asserts. O curso roda os seus testes contra uma versão certa (nada pode falhar) e contra
  versões com bug (cada uma tem de ser reprovada). Veja o exemplo resolvido da seção 12.
  Para usar `pytest.raises`, escreva `import pytest` no topo do arquivo.

| Nº | Exercício | Tipo | Nível | O que pratica |
|---|---|---|---|---|
| 01 | `ex01_limites_tolerancia` | implementar (TDD) | ★☆☆ | ler testes como especificação, `approx`, `raises` |
| 02 | `ex02_conserte_numero_br` | conserte o bug | ★☆☆ | ler código, testar hipótese no REPL |
| 03 | `ex03_testes_media` | escreva os testes | ★☆☆ | escolher casos, `approx`, `raises` |
| 04 | `ex04_operador_do_laudo` | implementar (TDD) | ★☆☆ | variável de ambiente, `monkeypatch` |
| 05 | `ex05_log_de_inspecao` | implementar (TDD) | ★☆☆ | `logging` com níveis, `caplog` |
| 06 | `ex06_conserte_pesos_por_nf` | conserte o bug | ★★☆ | acumulador em dicionário, depuração |
| 07 | `ex07_testes_classificar` | escreva os testes | ★★☆ | bordas, rótulos, casos de erro |
| 08 | `ex08_ler_medicoes` | implementar (TDD) | ★★☆ | `tmp_path`, mensagens de erro úteis |
| 09 | `ex09_relatorio_no_terminal` | implementar (TDD) | ★★☆ | `capsys`, formatação brasileira |
| 10 | `ex10_conserte_codigos_bobinas` | conserte o bug | ★★☆ | off-by-one, validação |
| 11 | `ex11_revisao_resumo_por_linha` | revisão: conserte o bug | ★★★ | 4 bugs; dicionários, texto BR, exceções |
| 12 | `ex12_revisao_testes_lotes` | revisão: escreva os testes | ★★★ | listas, fatiamento, mutabilidade |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar de
`raise NotImplementedError` (ou conserte o código, nos exercícios de bug) e rode, na pasta
`curso-python`:

```text
python curso.py testar 09 ex01
```

## Desafio do módulo

**Do script legado ao código profissional.** Você recebe um script antigo de conferência
de medições (funciona, mas não tem testes e é difícil de ler). A missão: protegê-lo com
testes de caracterização, refatorar em funções pequenas com type hints, trocar `print` por
`logging`, deixar o ruff limpo, acrescentar com TDD a regra de liberação pela observação
(`"COF: liberado"`) e entregar tudo numa branch com pull request.

Enunciado completo: [desafio/README.md](desafio/README.md).

## Quiz

14 perguntas para revisar o módulo: [quiz.md](quiz.md).

## Para ir além

- Documentação do pytest (em inglês, com ótimos exemplos): https://docs.pytest.org/
- `logging`, HOWTO oficial: https://docs.python.org/pt-br/3/howto/logging.html
- `pdb`, o depurador do Python: https://docs.python.org/pt-br/3/library/pdb.html
- `typing`, type hints: https://docs.python.org/pt-br/3/library/typing.html
- Ruff (regras e configuração): https://docs.astral.sh/ruff/
- mypy, primeiros passos: https://mypy.readthedocs.io/en/stable/getting_started.html
- Depuração no VS Code: https://code.visualstudio.com/docs/python/debugging
- Livro gratuito *Pro Git*, em português: https://git-scm.com/book/pt-br/v2
- Leituras extras: Kent Beck, *TDD: Desenvolvimento Guiado por Testes*; Robert C. Martin,
  *Código Limpo* (os capítulos sobre nomes e funções já valem o livro).
