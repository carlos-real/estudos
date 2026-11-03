# Quiz — Módulo 00: Preparação do ambiente

Responda **sem consultar** a aula nem o computador. Anote suas respostas num papel e só
depois confira o gabarito no final. Errou? Volte à seção indicada no gabarito.

---

**1.** O que o interpretador Python faz com o seu arquivo `.py`?

- a) Transforma o arquivo num `.exe` e apaga o original.
- b) Lê o código e executa as instruções, de cima para baixo.
- c) Corrige automaticamente os erros de digitação.
- d) Envia o código para o GitHub.

**2.** Você instalou o Python, digitou `python --version` e apareceu
`O termo 'python' não é reconhecido como nome de cmdlet...`. Cite as duas causas mais
prováveis.

**3.** Para que serve um ambiente virtual (`.venv`)?

- a) Para o Python rodar mais rápido.
- b) Para cada projeto ter o seu próprio Python e as suas bibliotecas, sem interferir nos
  outros.
- c) Para guardar uma cópia do código na nuvem.
- d) Para esconder o código de outras pessoas.

**4.** Qual comando **ativa** o ambiente virtual no PowerShell?

- a) `python -m venv .venv`
- b) `.venv\Scripts\Activate.ps1`
- c) `pip install venv`
- d) `cd .venv`

**5.** Ao ativar o `.venv`, o PowerShell diz que "a execução de scripts foi desabilitada
neste sistema". Qual comando resolve no seu computador pessoal, sem precisar de
administrador? E o que esse comando passa a permitir?

**6.** Por que o curso recomenda `python -m pip install ...` em vez de só `pip install ...`?

**7.** O que este código imprime?

```python
def dobro(n):
    return n * 2


print(dobro(5))
print(dobro(1.5))
```

**8.** O que este código imprime?

```python
def ola():
    print("Oi")


x = ola()
print(x)
```

**9.** Onde está o erro? Qual mensagem o Python mostra?

```python
def saudar(nome)
    return "Olá, " + nome + "!"
```

**10.** Este código roda sem erro, mas o teste do exercício 00.02 falha. Por quê?

```python
def saudar(nome):
    return "Olá, nome!"


print(saudar("Ana"))
```

**11.** Leia o traceback. Em que linha está o problema, qual o tipo do erro e como
corrigir?

```text
Traceback (most recent call last):
  File "C:\Users\carlos\projetos\rascunho\relatorio.py", line 4, in <module>
    print(peso_totl)
          ^^^^^^^^^
NameError: name 'peso_totl' is not defined. Did you mean: 'peso_total'?
```

**12.** Qual a ordem certa para enviar um exercício resolvido ao GitHub?

- a) `git push` → `git commit` → `git add`
- b) `git add` → `git commit` → `git push`
- c) `git commit` → `git add` → `git push`
- d) `git pull` → `git push` → `git add`

**13.** O `git push` foi recusado com `! [rejected] main -> main (fetch first)`. O que
aconteceu e o que fazer?

**14.** Qual destes é o melhor uso de uma IA enquanto você faz os exercícios?

- a) Colar o enunciado e pedir o código pronto, para ganhar tempo.
- b) Colar a planilha real do laboratório para ela gerar os dados de teste.
- c) Mostrar a mensagem de erro do teste e pedir uma dica, sem a resposta.
- d) Pedir para ela resolver e depois só ler a resposta com atenção.

**15.** Você editou o exercício, rodou `python curso.py testar 00 ex01` e o resultado não
mudou nada, como se você não tivesse mexido. Qual a causa mais comum?

---

## Gabarito

**1. b.** O interpretador (o programa `python`) lê o código-fonte e executa as instruções
na ordem. Ele não corrige nada: quando encontra algo que não entende, para e mostra um
traceback. (Seção 1.)

**2.** (1) O Python não foi instalado, ou (2) foi instalado sem marcar "Add python.exe to
PATH". Uma terceira possibilidade comum: o terminal ficou aberto durante a instalação e
não enxerga o PATH novo. Feche e abra de novo. (Seção 2.3.)

**3. b.** Cada projeto tem as suas bibliotecas, nas versões de que precisa. Atualizar o
pandas de um projeto não quebra outro. Guardar na nuvem é papel do Git/GitHub. (Seção 9.1.)

**4. b.** A alternativa a **cria** o ambiente (uma vez só); a b **ativa** (em todo
terminal novo). Funcionou se aparecer `(.venv)` no começo do prompt. (Seção 9.3.)

**5.** `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. Vale só para o seu usuário.
Passa a permitir scripts criados no seu computador (como o `Activate.ps1`) e continua
exigindo assinatura digital de scripts baixados da internet. Em computador da empresa a
TI pode impor outra política: não tente burlar. (Seção 9.4.)

**6.** Porque `python -m pip` usa o pip **do mesmo Python** que vai rodar o código. Com o
`.venv` ativo, as bibliotecas vão para o `.venv`, e não para outro Python qualquer do
computador. (Seção 9.5.)

**7.**

```text
10
3.0
```

`dobro(1.5)` dá `3.0`, e não `3`: número com ponto decimal continua com ponto decimal
depois da conta. (Seção 10.3.)

**8.**

```text
Oi
None
```

A função **mostra** "Oi" com `print`, mas não tem `return`, então devolve `None`. O `x`
guarda `None`, e o último `print` mostra isso. (Seção 10.3.)

**9.** Faltam os dois-pontos no fim da linha do `def`. O Python mostra
`SyntaxError: expected ':'` apontando o fim da linha 1. (Seção "Lendo mensagens de
erro".)

**10.** Dentro das aspas, `nome` é texto fixo, não o parâmetro. A função devolve sempre
`'Olá, nome!'` (o `print` mostra `Olá, nome!`). O certo é `"Olá, " + nome + "!"`, com
`nome` **fora** das aspas. (Seção 10.5 e exercício 00.02.)

**11.** Linha 4. É um `NameError`: o nome `peso_totl` não existe. É erro de digitação, e
o próprio Python sugere `peso_total`. Corrija para `print(peso_total)`. Leia sempre de
baixo para cima: a última linha diz o quê, as de cima dizem onde. (Seção "Lendo
mensagens de erro".)

**12. b.** `add` coloca na área de preparação, `commit` registra no histórico local,
`push` envia para o GitHub. (Seção 12.)

**13.** O GitHub tem commits que o seu computador ainda não tem (por exemplo, você enviou
algo de outro computador). Rode `git pull` para trazer as novidades e depois `git push`
de novo. (Seção "Lendo mensagens de erro".)

**14. c.** Pedir uma dica a partir da mensagem de erro mantém o raciocínio com você. A
alternativa a e a d entregam a solução (você não aprende a resolver). A b expõe dados da
empresa: nunca cole dados reais em ferramentas de IA. (Seção 13.5.)

**15.** O arquivo não foi salvo. O teste lê o arquivo do disco, não o que está na tela do
VS Code. Use `Ctrl+S` ou ligue o salvamento automático. Outra causa possível: você editou
o arquivo de `solucoes/` em vez do de `exercicios/`. (Seções 3.3 e 11.)
