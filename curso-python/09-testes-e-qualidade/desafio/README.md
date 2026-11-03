# Desafio do módulo 09 — Do script legado ao código profissional

## Contexto

Todo laboratório tem aquele script que "funciona, mas ninguém mexe". O nosso é o
`legado_conferencia.py`: ele lê a planilha de medições (`dados/medicoes_exemplo.csv`),
confere cada valor com os limites da linha de produção e imprime um relatório.

Funciona. Mas tem nomes de uma letra, índices mágicos (`x[3]`), uma função gigante,
avisos com `print` e nenhum teste. Agora o laboratório pediu uma regra nova:

> Uma medição FORA da tolerância que tenha, na coluna `observacao`, a liberação técnica
> do mesmo ensaio (por exemplo, `COF: liberado`) deve aparecer como **LIBERADO**, e o
> resumo deve contar as liberadas.

Mexer nesse script sem testes é pedir para quebrar o que funciona. Sua missão é fazer
o que um profissional faria: proteger, refatorar, melhorar e só então acrescentar a
regra nova.

## Requisitos obrigatórios

1. **Testes de caracterização primeiro.** Antes de mudar qualquer linha, escreva testes
   que congelam o comportamento atual (rode o legado, guarde a saída e compare).
2. **Refatoração em funções pequenas**, com nomes claros e type hints: ler o CSV,
   converter número brasileiro, classificar uma medição, resumir por linha, montar o
   relatório. Regras (limites) separadas da lógica.
3. **logging no lugar dos avisos com print.** Linha inválida vira `WARNING` no log. Com
   a opção `--log arquivo.log`, o log também vai para um arquivo.
4. **Regra nova com TDD:** a liberação pela observação. Escreva o teste, veja falhar,
   implemente, refatore. Cuidado: a liberação de **outro** ensaio não vale (uma
   observação `Selagem: liberado` não libera o COF).
5. **Pelo menos 12 testes**, usando no total: `parametrize`, uma fixture sua,
   `tmp_path`, `capsys` ou `caplog`, `pytest.raises` e `pytest.approx`.
6. **`ruff check` e `ruff format --check` sem problemas.**
7. **Git de verdade:** crie um repositório seu (ou uma pasta no seu repositório de
   estudos), trabalhe numa branch `refatora-conferencia`, faça **pelo menos 4 commits
   pequenos** com boas mensagens e abra um **pull request** no GitHub com descrição
   (o que mudou, por quê, como testar).

## Extras (opcionais)

- Cobertura acima de 90% com `pytest-cov` (`python -m pip install pytest-cov`).
- `mypy` sem erros no seu código.
- Argumento `--so-fora` que imprime só as medições FORA.
- Um workflow do GitHub Actions que roda `ruff` e `pytest` a cada push (seção "No mundo
  real" da aula).

## Exemplo de execução

Legado (antes), na pasta `09-testes-e-qualidade`:

```text
> python desafio/legado_conferencia.py
AVISO: linha 9 ignorada, valor: abc
CONFERÊNCIA DE MEDIÇÕES
OP 12345 | linha A | espessura | 20,30 | OK
OP 12345 | linha A | gramatura | 18,60 | OK
OP 12345 | linha A | cof | 0,38 | FORA
OP 12346 | linha A | espessura | 21,40 | FORA
OP 12347 | linha B | espessura | 24,80 | OK
OP 12347 | linha B | gramatura | 22,10 | OK
OP 12347 | linha B | cof | 0,22 | OK
OP 12349 | linha C | espessura | 30,20 | OK
OP 12349 | linha C | cof | 0,41 | FORA
OP 12350 | linha D | espessura | 15,00 | OK
OP 12350 | linha D | gramatura | 14,20 | OK
OP 12350 | linha D | tracao | 35,00 | SEM REGRA
RESUMO POR LINHA
A: 4 medições, 2 fora (50,0%)
B: 3 medições, 0 fora (0,0%)
C: 2 medições, 1 fora (50,0%)
D: 2 medições, 0 fora (0,0%)
```

Versão nova (depois). O aviso agora vem do logging (a data e a hora serão outras):

```text
> python desafio/solucao_referencia.py
2026-10-29 09:52:00,648 WARNING conferencia: linha 9 ignorada, valor: abc
CONFERÊNCIA DE MEDIÇÕES
OP 12345 | linha A | espessura | 20,30 | OK
OP 12345 | linha A | gramatura | 18,60 | OK
OP 12345 | linha A | cof | 0,38 | LIBERADO
OP 12346 | linha A | espessura | 21,40 | FORA
OP 12347 | linha B | espessura | 24,80 | OK
OP 12347 | linha B | gramatura | 22,10 | OK
OP 12347 | linha B | cof | 0,22 | OK
OP 12349 | linha C | espessura | 30,20 | OK
OP 12349 | linha C | cof | 0,41 | FORA
OP 12350 | linha D | espessura | 15,00 | OK
OP 12350 | linha D | gramatura | 14,20 | OK
OP 12350 | linha D | tracao | 35,00 | SEM REGRA
RESUMO POR LINHA
A: 4 medições, 1 fora (25,0%), 1 liberada(s)
B: 3 medições, 0 fora (0,0%), 0 liberada(s)
C: 2 medições, 1 fora (50,0%), 0 liberada(s)
D: 2 medições, 0 fora (0,0%), 0 liberada(s)
```

Repare: o COF da OP 12345 virou LIBERADO (a observação diz `COF: liberado`), mas o COF
da OP 12349 continua FORA (a observação libera a selagem, não o COF).

> 💡 **Dica:** quando a regra nova entrar, um dos seus testes de caracterização vai
> falhar (a linha do COF da OP 12345 muda de FORA para LIBERADO). Isso é esperado: o
> requisito mudou. Atualize esse teste **no mesmo commit** da regra nova e explique na
> mensagem do commit.

## Critérios de aceite

- [ ] Existe um teste de caracterização que roda o código antigo e compara a saída.
- [ ] Nenhuma função tem mais de ~20 linhas; nenhum nome de uma letra (fora `i` em laço).
- [ ] Linha com valor inválido gera `WARNING` no log e não derruba o programa.
- [ ] `--log conferencia.log` grava o log num arquivo em UTF-8.
- [ ] Medição FORA com liberação do mesmo ensaio aparece como LIBERADO.
- [ ] Liberação de outro ensaio não libera.
- [ ] O resumo mostra total, fora, percentual e liberadas por linha.
- [ ] `python -m pytest` passa com pelo menos 12 testes.
- [ ] `ruff check .` e `ruff format --check .` sem problemas.
- [ ] Branch, 4+ commits com mensagens no imperativo e pull request aberto.

## Dicas para começar

1. Copie `legado_conferencia.py` e a pasta `dados/` para o seu repositório. Faça o
   primeiro commit **antes** de mudar qualquer coisa: "Adiciona script legado de
   conferência".
2. Teste de caracterização: rode o legado com `subprocess.run([...], capture_output=True,
   text=True)` (ou chame a função `f` e use `capsys`) e compare com a saída que você
   guardou num arquivo `saida_esperada.txt`.
3. Refatore em passos pequenos: extraia UMA função, rode os testes, faça commit. Repita.
4. Faça a função que monta o relatório **devolver texto** em vez de imprimir: fica muito
   mais fácil de testar.
5. Para a regra nova, comece pelo teste mais simples ("COF: liberado" libera o COF).

Uma solução de referência está em `solucao_referencia.py`, com 22 testes em
`test_solucao_referencia.py`. Para rodar os testes (na pasta `curso-python`):

```text
python -m pytest 09-testes-e-qualidade/desafio -v
```

Tente fazer sozinho antes de abrir. Depois compare: não existe uma única resposta certa.
