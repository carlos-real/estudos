# Quiz — Módulo 14: Projeto final

Responda sem rodar. Depois confira no gabarito, no fim da página.

**1.** Em qual camada fica a função que decide se a espessura 44,8 µm está dentro de
40 ± 10%?

- a) Na CLI, porque é ela que recebe os argumentos.
- b) Na leitura da planilha, porque é de lá que o valor vem.
- c) No núcleo de regras, que não lê nem escreve arquivo nenhum.
- d) No emissor, porque é ele que decide se emite.

**2.** O que este código imprime?

```python
print(37 * (1 - 10 / 100), round(37 * (1 - 10 / 100), 4))
```

**3.** O que este código imprime?

```python
padrao = {"cof": 0.35, "selagem": 8}
cliente = {"cof": 0.25}
print({**padrao, **cliente})
print({**cliente, **padrao})
```

**4.** Qual das observações abaixo é considerada liberada pelo padrão
`r"\bcof\s*[:-]?\s*liberad[oa]\b"` (aplicado ao texto já normalizado)?

- a) `cof: nao liberado`
- b) `liberado para corte; cof pendente`
- c) `cof - liberada`
- d) nenhuma das três

**5.** Por que a especificação de título desconhecido (`ESP-9999`) vira pendência em
vez de usar o padrão da linha?

- a) Porque o padrão da linha é mais rígido e reprovaria a OP.
- b) Porque usar uma regra "parecida" pode emitir um certificado com tolerâncias
  erradas; o sistema não chuta.
- c) Porque o SQLite não aceita títulos desconhecidos.
- d) Porque a especificação do cliente sempre tem todas as características.

**6.** Onde está o erro? O programa abaixo deveria listar as especificações, mas dá
`sqlite3.OperationalError: no such table: especificacao`, e um arquivo novo aparece
na pasta.

```python
import sqlite3

conexao = sqlite3.connect("regras_errado.db")  # o nome certo é regras.db
for linha in conexao.execute("SELECT titulo FROM especificacao"):
    print(linha)
```

**7.** O que este código imprime?

```python
from dataclasses import dataclass, field, replace


@dataclass
class ItemFila:
    op: str
    situacao: str
    motivos: list[str] = field(default_factory=list)


a = ItemFila("24518", "emitir")
b = replace(a, situacao="ensaio")
b.motivos.append("x")
print(a.situacao, b.situacao, a.motivos)
```

**8.** A chave de idempotência da emissão é `(OP, NF)`, e não só a OP. Por quê?

- a) Porque a NF é mais curta.
- b) Porque a mesma OP pode sair em duas notas (entregas parciais), e cada nota
  precisa do seu certificado.
- c) Porque o TOTVS exige a NF em maiúsculas.
- d) Tanto faz: OP sozinha daria o mesmo resultado.

**9.** Em `emitir_fila`, por que capturar só `ErroEmissao` e não `except Exception`?

- a) `except Exception` não funciona dentro de laço.
- b) Para que um bug (ex.: `AttributeError` num seletor) apareça e pare a série, em vez
  de virar silenciosamente "falha de tela" em todas as OPs.
- c) Porque `ErroEmissao` é mais rápido.
- d) Porque o Playwright só levanta `ErroEmissao`.

**10.** O que este código imprime?

```python
from dataclasses import dataclass, field


@dataclass
class ResultadoValidacao:
    motivos: list[str] = field(default_factory=list)

    @property
    def aprovado(self) -> bool:
        return not self.motivos


r = ResultadoValidacao()
print(r.aprovado)
r.motivos.append("cof 0.38 acima do máximo 0.35")
print(r.aprovado)
```

**11.** A CLI devolve código de saída `1` quando houve falha de emissão. Para que isso
serve?

- a) Para o Python liberar memória.
- b) Para o Agendador de Tarefas (ou o GitHub Actions) saber que a execução precisa
  de atenção humana, sem ninguém ler o texto da tela.
- c) Para o Excel abrir o relatório automaticamente.
- d) Não serve para nada; é só costume.

**12.** Você clonou o projeto, rodou `python -m pytest` e recebeu
`ModuleNotFoundError: No module named 'validador_certificados'`. Qual é a correção
mais profissional?

- a) Copiar todos os arquivos de `src/validador_certificados` para a pasta `tests`.
- b) Ativar o ambiente virtual e rodar `python -m pip install -e ".[dev]"`.
- c) Renomear `src` para `validador_certificados`.
- d) Apagar o `pyproject.toml`.

**13.** Qual destes arquivos **não** deve ir para o repositório público do portfólio?

- a) `tests/test_regras.py`
- b) `dados/planilha_valores.xlsx` com dados fictícios
- c) a planilha real do laboratório com OPs e clientes da empresa
- d) `.github/workflows/testes.yml`

**14.** O modo ensaio é o padrão da CLI e emitir de verdade exige `--emitir`. Qual é a
razão principal?

- a) Ensaio é mais rápido.
- b) O erro mais caro é emitir certificado errado; o padrão seguro protege contra o
  esquecimento de quem roda.
- c) O argparse não aceita flags com valor padrão `True`.
- d) O TOTVS bloqueia robôs que rodam sem flag.

---

## Gabarito

1. **c.** Regra de negócio fica no núcleo puro: recebe números, devolve resultado. Assim
   se testa sem planilha e serve igual para a CLI, para a API e para o robô.
2. **`33.300000000000004 33.3`.** O float não representa 0,9 exatamente. Por isso os
   limites são arredondados com `round(..., 4)`: sem isso, 33,3 seria reprovado.
3. **`{'cof': 0.25, 'selagem': 8}`** e depois **`{'cof': 0.35, 'selagem': 8}`**. No
   `{**a, **b}`, quem vem depois vence. A ordem `{**padrao, **cliente}` é a que faz o
   cliente sobrescrever o padrão.
4. **c.** Em (a), depois de `cof:` vem `nao`, e o padrão exige `liberad` logo depois dos
   separadores. Em (b), `liberado` aparece antes de `cof`, e o padrão exige `cof`
   primeiro.
5. **b.** "Nunca chutar": uma pendência custa um minuto do técnico; um certificado
   errado custa uma reclamação de cliente.
6. **`sqlite3.connect` cria o arquivo se ele não existe.** O banco novo está vazio, por
   isso "no such table". Abra só para leitura (`?mode=ro` com `uri=True`) ou confira
   `Path(...).is_file()` antes: o erro passa a dizer o que realmente aconteceu.
7. **`emitir ensaio ['x']`.** `replace` faz cópia **rasa**: o novo objeto aponta para a
   MESMA lista `motivos`. É por isso que `emitir_fila` cria uma lista nova
   (`item.motivos + [...]`) em vez de dar `append`.
8. **b.** Entregas parciais existem. Com a OP sozinha, a segunda nota ficaria sem
   certificado.
9. **b.** Erro esperado (uma tela que não respondeu) é tratado e a série continua.
   Erro inesperado é bug: esconder um bug só adia e espalha o problema.
10. **`True`** e depois **`False`**. A propriedade é calculada na hora a partir dos
    motivos: não existe um `aprovado` guardado que possa ficar desatualizado.
11. **b.** Código de saída é a forma padrão de um programa dizer "deu certo" (0) ou
    "precisa de alguém" (diferente de 0) para outro programa.
12. **b.** Com o src layout, o pacote precisa ser instalado. O `-e` (editável) faz o
    Python enxergar o código da pasta `src` sem copiar nada.
13. **c.** Dado real de cliente e de produção é da empresa. No portfólio, só dados
    fictícios, gerados por script.
14. **b.** Um padrão seguro protege contra o esquecimento. Para fazer a ação perigosa,
    é preciso pedir explicitamente.
