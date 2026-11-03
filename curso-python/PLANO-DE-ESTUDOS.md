# Plano de estudos: a trilha semana a semana

Este é o caminho completo, na ordem certa, com o que fazer em cada semana. Ele foi
montado para **1 hora por dia, 5 dias por semana**. Com mais tempo, avance mais rápido,
mas não pule as revisões.

Duração total: **cerca de 31 semanas (7 meses)**. No fim você terá 4 projetos de
portfólio e o núcleo de um sistema real do seu trabalho.

## Como o curso ensina (e por que funciona)

O curso usa métodos que a pesquisa em ensino de programação mostra que funcionam melhor
do que só assistir ou só ler:

| Método | Como aparece no curso | Por que funciona |
|---|---|---|
| **PRIMM** (Preveja, Rode, Investigue, Modifique, Crie) | Blocos "🔮 Preveja antes de rodar" e "🔧 Modifique" nas aulas | Prever obriga você a pensar como o computador; errar a previsão mostra exatamente o que você ainda não entendeu |
| **Exemplos resolvidos** | Antes de cada assunto novo, um problema resolvido passo a passo | Iniciante aprende mais vendo o raciocínio completo antes de tentar sozinho |
| **Prática com correção imediata** | Testes automáticos em todo exercício | Você descobre o erro na hora, não dias depois |
| **Revisão espaçada e intercalada** | Exercícios `_revisao_` e as sextas-feiras de revisão | Revisar com intervalos e misturando assuntos fixa o conteúdo na memória de longo prazo |
| **Recuperação ativa** | Quiz sem consultar e o "resumo de memória" diário | Lembrar sem olhar fortalece a memória mais do que reler |
| **Projeto contínuo e real** | O Validador de Certificados cresce ao longo do curso | Aprender com um problema que importa para você mantém a motivação |

Para saber mais: Sentance, Waite e Kallia, "Teaching computer programming with PRIMM"
(2019); Sweller, sobre exemplos resolvidos e carga cognitiva; Dunlosky e colegas,
"Improving Students' Learning With Effective Learning Techniques" (2013), sobre prática
espaçada e recuperação ativa.

## A rotina de cada dia (60 minutos)

| Tempo | O que fazer |
|---|---|
| 5 min | **Resumo de memória:** sem olhar nada, escreva no seu diário 3 coisas que lembra da última aula |
| 20 min | **Aula:** leia a próxima seção, digite os exemplos, faça os "Preveja antes de rodar" |
| 30 min | **Exercícios:** um ou dois, rodando `python curso.py testar NN exMM` |
| 5 min | **Diário de bordo:** o que aprendeu, onde travou, e o commit do dia |

Sexta-feira é dia de **revisão** (veja abaixo). Se travar mais de 30 minutos num
exercício, siga o roteiro da seção "Quando travar".

## A rotina da semana

- **Segunda a quinta:** aula e exercícios do módulo atual.
- **Sexta (revisão espaçada):**
  1. Refaça o quiz do módulo **anterior** sem consultar.
  2. Escolha 1 exercício de **2 a 3 módulos atrás**, apague sua solução e refaça do zero.
  3. Rode `python curso.py progresso` e faça o commit da semana no GitHub.

## A trilha

### Fase 1 — A base da linguagem (semanas 1 a 9)

| Semana | Módulo | Meta da semana |
|---|---|---|
| 1 | 00 Preparação | Ambiente pronto, primeiro teste passando, primeiro commit no GitHub |
| 2 | 01 Fundamentos | Aula até formatação de números; metade dos exercícios |
| 3 | 01 Fundamentos | Exercícios restantes, quiz e desafio |
| 4 | 02 Decisões e repetições | Aula e exercícios de if e for |
| 5 | 02 Decisões e repetições | while, exercícios de revisão, quiz e desafio |
| 6 | 03 Coleções | Listas, tuplas e dicionários |
| 7 | 03 Coleções | Conjuntos, compreensões, "tabela" de dicionários, desafio |
| 8 | 04 Funções | Aula completa e exercícios |
| 9 | 04 Funções | Exercícios de revisão e **Marco 1** |

> 🏁 **Marco 1 — Seu primeiro programa útil.** O desafio do módulo 04 vira o primeiro
> projeto do portfólio. Critério: roda no terminal, tem README explicando o que faz e
> está no GitHub.

### Fase 2 — Programas de verdade (semanas 10 a 17)

| Semana | Módulo | Meta da semana |
|---|---|---|
| 10 | 05 Texto e regex | Strings a fundo, números no formato brasileiro, acentos |
| 11 | 05 Texto e regex | Expressões regulares e leitura dos e-mails da expedição |
| 12 | 06 Arquivos e erros | Exceções, with/open, pathlib |
| 13 | 06 Arquivos e erros | CSV padrão Excel, JSON, desafio |
| 14 | 07 Módulos e biblioteca padrão | Módulos, pacotes, datas, estatística |
| 15 | 07 Módulos e biblioteca padrão | argparse (programas de terminal), desafio |
| 16 | 08 Orientação a objetos | Classes, property, herança e composição |
| 17 | 08 Orientação a objetos | dataclasses, Enum e **Marco 2** |

> 🏁 **Marco 2 — Ferramenta de laboratório.** O desafio do módulo 08 vira o segundo
> projeto do portfólio.
>
> 💼 **No trabalho:** a partir da semana 13 você já consegue automatizar uma tarefa
> pequena e real (ex.: juntar CSVs do laboratório num só). Faça isso. É a primeira prova
> concreta do seu valor com programação.

### Fase 3 — Nível profissional (semanas 18 a 24)

| Semana | Módulo | Meta da semana |
|---|---|---|
| 18 | 09 Testes e qualidade | pytest a fundo e TDD |
| 19 | 09 Testes e qualidade | ruff, logging, depuração, Git com branches |
| 20 | 10 Dados com pandas | DataFrame, leitura de CSV e Excel, filtros |
| 21 | 10 Dados com pandas | groupby, merge, pivot, limpeza de dados |
| 22 | 10 Dados com pandas | Gráficos com matplotlib e laboratório de salários |
| 23 | 11 Banco de dados e SQL | SQL do SELECT ao JOIN |
| 24 | 11 Banco de dados e SQL | sqlite3 no Python, banco de regras e **Marco 3** |

> 🏁 **Marco 3 — Análise de dados com SQL e pandas.** O desafio do módulo 11 vira o
> terceiro projeto do portfólio. Junto com o laboratório de salários do módulo 10, é o
> que um recrutador de vaga de dados quer ver.

### Fase 4 — Mundo real (semanas 25 a 31)

| Semana | Módulo | Meta da semana |
|---|---|---|
| 25 | 12 Automação e integração | APIs com requests, arquivos em lote, Excel |
| 26 | 12 Automação e integração | E-mail, agendamento e robô no navegador |
| 27 | 13 APIs com FastAPI | Criar e testar sua própria API |
| 28 | 14 Projeto final | Etapas 1 a 4: modelos, regras e tolerâncias |
| 29 | 14 Projeto final | Etapas 5 a 8: planilha, especificações e e-mails |
| 30 | 14 Projeto final | Etapas finais: fila, relatório e programa de terminal |
| 31 | 14 Projeto final | Montagem do projeto completo e **Marco 4** |

> 🏁 **Marco 4 — Validador de Certificados.** Seu projeto principal: repositório próprio,
> README com prints, testes rodando no GitHub Actions. É o projeto que você apresenta na
> sua empresa e em entrevistas.

## Quando travar

1. Leia a mensagem de erro de baixo para cima: a última linha diz o tipo do erro, as
   linhas acima dizem onde.
2. Releia a seção da aula sobre o assunto do exercício.
3. Teste pedaços do seu código no terminal do Python (`python` e depois os comandos).
4. Coloque `print()` nos pontos onde você não sabe o que está acontecendo.
5. Explique o problema em voz alta, linha por linha (funciona de verdade).
6. Pergunte a uma IA pedindo **uma dica**, não a resposta. Exemplo: "Não me dê o código.
   Meu teste falha com esta mensagem: ... O que devo investigar?"
7. Só então abra a solução. Depois, feche, espere um dia e refaça sem olhar.

## Diário de bordo

Crie um arquivo `DIARIO.md` na raiz do seu repositório e escreva todo dia, em 3 linhas:

```text
2026-11-03 — Módulo 02, ex05
Aprendi: break sai do laço mais próximo, não de todos.
Travei em: contador fora do laço zerava a cada volta. Resolvido movendo a linha.
```

Em poucas semanas esse diário mostra o quanto você evoluiu, e vira material para contar
sua história em entrevistas.

## Depois das 31 semanas

O curso te deixa no nível de júnior em Python. Para a primeira vaga, siga o plano de 6 e
12 meses do `carreira/README.md`. Em resumo:

- **Vaga de dados:** SQL todos os dias (exercícios online), Power BI e estatística básica.
- **Vaga de automação ou backend:** Docker, publicar uma API na nuvem e mais projetos.
- **Em qualquer caminho:** coloque o Validador em uso real na sua empresa. Um sistema
  funcionando em produção vale mais que qualquer certificado de curso.
