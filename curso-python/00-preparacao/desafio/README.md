# Desafio 00 — Ambiente pronto e primeiro push

## Contexto

Na indústria, um script só tem valor se outra pessoa (ou você, em outro computador)
consegue rodar de novo. Neste desafio você prova que o seu ambiente está completo, escreve
um pequeno programa no molde do curso e publica tudo no GitHub, do jeito que um
profissional faz.

É também o primeiro commit do seu portfólio.

## Requisitos obrigatórios

1. **Ambiente completo.** Python 3.12+, VS Code com a extensão Python, Git configurado
   com seu nome e e-mail, repositório `estudos` clonado, `.venv` criado em `curso-python`
   e bibliotecas instaladas com `python -m pip install -r requirements.txt`.
2. **Verificador sem ✘.** Na pasta `curso-python`, com o `.venv` ativo:
   `python 00-preparacao/exemplos/04_verificar_ambiente.py` mostra todas as linhas com ✔
   (um ⚠ na versão do Python é aceitável se você estiver na 3.10 ou 3.11).
3. **Exercícios do módulo resolvidos.** `python curso.py testar 00` termina com
   `19 passed` e a mensagem `✔ Tudo certo!`.
4. **Seu cartão de apresentação.** Crie o arquivo `00-preparacao/desafio/meu_cartao.py`
   que, ao rodar, mostra pelo menos:
   - seu nome;
   - sua função atual;
   - o seu objetivo com o curso;
   - a versão do Python em uso.
5. **Pelo menos uma função no molde `def` + `return`** dentro do `meu_cartao.py`, usada
   para montar alguma linha do cartão (ex.: `montar_linha(rotulo, valor)`).
6. **Commit e push.** Os exercícios resolvidos e o `meu_cartao.py` estão no GitHub, num
   ou mais commits com mensagens claras (nada de "teste" ou "ajustes").

## Extras (opcionais)

- Mostrar no cartão se o ambiente virtual está ativo (veja a dica 4).
- Ligar o salvamento automático do VS Code e instalar a extensão **Ruff** (você vai usá-la
  no módulo 09).
- Criar o arquivo `DIARIO.md` na raiz do repositório (veja o `PLANO-DE-ESTUDOS.md`) com a
  primeira entrada do seu diário de bordo.
- Rodar o mesmo repositório em um segundo computador (clone, `.venv`, `pip install`) e
  conferir que tudo funciona igual.

## Exemplo de execução

```text
python 00-preparacao/desafio/meu_cartao.py
```

```text
--------------------------------------------------
CARTÃO DE APRESENTAÇÃO
--------------------------------------------------
Nome: Carlos Eduardo
Função atual: Laboratório de Qualidade (embalagens plásticas flexíveis)
Objetivo: Trabalhar com dados e automação usando Python
Python: 3.14.0
Ambiente virtual ativo: sim
--------------------------------------------------
```

O seu não precisa ficar igual: o formato é livre. A versão do Python será a sua.

## Critérios de aceite

- [ ] O verificador de ambiente mostra todas as linhas com ✔.
- [ ] `python curso.py testar 00` passa nos 19 testes.
- [ ] `python curso.py progresso` mostra `00 Preparacao ... 3/3`.
- [ ] `python 00-preparacao/desafio/meu_cartao.py` roda sem erro e mostra as 4
      informações pedidas.
- [ ] O `meu_cartao.py` tem pelo menos uma função com `return` que é chamada no script.
- [ ] `git status` mostra "nothing to commit, working tree clean" (tudo commitado).
- [ ] No site `https://github.com/carlos-real/estudos` aparecem o `meu_cartao.py` e os
      exercícios resolvidos.
- [ ] Nenhum dado real da empresa foi para o GitHub.

## Dicas de como começar

1. **Faça na ordem dos requisitos.** Não adianta escrever o cartão se o `.venv` não
   ativa. Siga as seções 2 a 9 da aula e rode o verificador.
2. **Comece pelo mínimo que roda.** Crie o `meu_cartao.py` com um único
   `print("Nome: Carlos Eduardo")`, rode, e só depois vá acrescentando linhas.
3. **A versão do Python** se pega assim (copie estas duas linhas; `import` é assunto do
   módulo 07):

   ```python
   import platform

   print("Python: " + platform.python_version())
   ```

4. **Ambiente virtual ativo?** O verificador usa a comparação
   `sys.prefix != sys.base_prefix` (precisa de `import sys`). Se quiser mostrar isso no
   cartão, `print(sys.prefix != sys.base_prefix)` mostra `True` ou `False`.
5. **Commit em partes.** Um commit para os exercícios ("Resolve exercícios do módulo
   00") e outro para o cartão ("Adiciona cartão de apresentação do desafio 00") deixa o
   histórico mais fácil de ler.
6. **Antes do `git add .`, rode `git status`** e confira se não está indo nada que não
   devia.

Só depois de terminar, compare com `solucao_referencia.py`. Ela mostra uma forma de
organizar o cartão em funções pequenas.
