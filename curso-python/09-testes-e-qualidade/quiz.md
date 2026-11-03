# Quiz — Módulo 09: Testes e qualidade de código

Responda no papel (ou num arquivo) antes de olhar o gabarito no final.

---

**1.** Você roda só `python -m pytest`, sem indicar arquivo. Com as regras padrão de
descoberta, qual destas funções **não** é executada?

a) `test_media` no arquivo `test_calculos.py`
b) `testar_media` no arquivo `test_calculos.py`
c) `test_media` no arquivo `calculos.py`
d) `test_limites` no arquivo `tests/test_tolerancia.py`

---

**2.** O que este código imprime?

```python
import pytest

print(0.1 + 0.2 == 0.3, 0.1 + 0.2 == pytest.approx(0.3))
```

a) `True True`  b) `False False`  c) `False True`  d) `True False`

---

**3.** Onde está o problema deste teste?

```python
def test_media_de_lista_vazia():
    with pytest.raises(Exception):
        media([])
```

---

**4.** Qual é a ordem correta do ciclo do TDD?

a) Escrever o código, escrever o teste, refatorar.
b) Escrever um teste que falha, escrever o código mínimo para ele passar, refatorar.
c) Refatorar, escrever o teste, escrever o código.
d) Escrever todos os testes do sistema, depois todo o código.

---

**5.** Rodando `python -m pytest -s` (o `-s` mostra os prints), em que ordem aparecem as
palavras "criando", "testando" e "limpando"?

```python
import pytest


@pytest.fixture
def bobina():
    print("criando")
    yield {"peso": 250.0}
    print("limpando")


def test_peso(bobina):
    print("testando")
    assert bobina["peso"] == 250.0
```

---

**6.** Para que serve a fixture `monkeypatch`?

a) Para corrigir bugs automaticamente.
b) Para trocar temporariamente uma função, atributo ou variável de ambiente durante um
   teste, desfazendo a troca no final.
c) Para medir a cobertura dos testes.
d) Para rodar os testes em paralelo.

---

**7.** Depois de executar `print("OK")` e `print("FORA")` dentro de um teste, o que
`capsys.readouterr().out` devolve?

---

**8.** O que este programa mostra no terminal?

```python
import logging

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logging.debug("a")
logging.info("b")
logging.warning("c")
logging.error("d")
```

---

**9.** O `ruff check` avisou `F401 'os' imported but unused`. O que isso significa e
qual é a diferença entre `ruff check` e `ruff format`?

---

**10.** Qual é a melhor mensagem de commit?

a) `ajustes`
b) `Corrige borda mínima na classificação de tolerância`
c) `commit final agora vai`
d) `mudei umas coisas no arquivo de tolerância e também no relatório e no log`

---

**11.** Seu projeto tem 100% de cobertura de testes. Isso garante que não há bugs?

---

**12.** Uma função tem a anotação `def somar(a: int, b: int) -> int`. O que acontece ao
rodar `somar("10", "20")` com `python`?

a) `TypeError` antes de executar.
b) Devolve `30`.
c) Devolve `"1020"`: o Python não confere as anotações ao rodar.
d) O programa não abre.

---

**13.** Este código passa ou levanta erro? O que ele imprime?

```python
import pytest

with pytest.raises(ValueError, match="linha 1") as excinfo:
    raise ValueError("linha 13: valor inválido")
print("passou:", excinfo.value)
```

---

**14.** Você está no depurador (pdb), parado dentro de um laço. Qual comando mostra o
valor da variável `total`, e qual a diferença entre `n` e `s`?

---

## Gabarito

1. **c.** O pytest só abre arquivos `test_*.py` ou `*_test.py`; `calculos.py` nem é
   lido. Pegadinha da (b): para **funções**, a regra é o prefixo `test`, sem exigir o
   sublinhado, então `testar_media` **é** executada. Por isso, nos exercícios "escreva os
   testes", a função `testar_...` fica num arquivo `exNN_...py`, que o pytest não coleta.
2. **c.** `0.1 + 0.2` vale `0.30000000000000004`, então `==` dá `False`. O
   `pytest.approx` compara com uma tolerância relativa (1 milionésimo), então dá `True`.
3. `Exception` é genérico demais: o teste passa com **qualquer** erro, até com um
   `TypeError` ou `NameError` causado por um bug. Use o tipo exato: `pytest.raises(ValueError)`
   (e, se quiser, `match=` para conferir a mensagem).
4. **b.** Vermelho (teste falhando), verde (código mínimo), refatorar (melhorar com os
   testes passando). Um teste por vez.
5. criando, testando, limpando. O código antes do `yield` roda antes do teste; o que
   está depois do `yield` roda no final, mesmo que o teste falhe.
6. **b.** Tudo o que o `monkeypatch` troca é desfeito sozinho no fim do teste, então um
   teste não "suja" o outro.
7. `"OK\nFORA\n"`: tudo o que foi impresso, com as quebras de linha que o `print`
   acrescenta.
8. Só `WARNING: c` e `ERROR: d`. Com `level=logging.WARNING`, as mensagens DEBUG e INFO
   ficam de fora (os níveis, do menor para o maior: DEBUG, INFO, WARNING, ERROR,
   CRITICAL).
9. F401 é "import não usado": o módulo `os` foi importado e ninguém usa. `ruff check`
   procura **problemas** (erros prováveis, más práticas, imports não usados);
   `ruff format` mexe só na **aparência** (espaços, quebras de linha, aspas), sem mudar
   o comportamento.
10. **b.** Verbo no imperativo, curta, diz o quê e onde. (a) e (c) não dizem nada; (d)
    mistura vários assuntos, o que indica que deveriam ser commits separados.
11. Não. Cobertura diz quais linhas **rodaram** durante os testes, não se os asserts
    conferem as coisas certas. Um teste sem assert cobre linhas e não testa nada.
    Cobertura baixa mostra o que falta testar; cobertura alta não prova ausência de bugs.
12. **c.** Type hints são documentação para pessoas e ferramentas (como o mypy). O
    Python as ignora ao executar: `"10" + "20"` concatena textos.
13. Passa e imprime `passou: linha 13: valor inválido`. O `match` usa `re.search`,
    que procura o padrão em **qualquer parte** da mensagem, e "linha 1" está dentro de
    "linha 13". Para exigir mais precisão, use algo como `match=r"^linha 1:"`.
14. `p total` mostra o valor. `n` (next) executa a linha atual inteira e para na
    próxima; `s` (step) **entra** na função chamada na linha atual.

