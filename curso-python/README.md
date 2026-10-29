# Curso de Python: do zero ao primeiro sistema profissional

Um curso completo, prático e em português para aprender a programar de verdade com
Python, pensado para quem trabalha na indústria e quer migrar para dados, automação ou
desenvolvimento.

Você não vai só assistir: vai **escrever código todos os dias**. Cada exercício tem
testes automáticos que dizem na hora se o seu código está certo. No fim, você terá
construído o núcleo de um sistema real (o Validador de Certificados) e terá um portfólio
para mostrar.

## O que tem aqui

- **15 módulos** com aula completa, exemplos executáveis, exercícios corrigidos
  automaticamente, desafio e quiz.
- **Soluções oficiais comentadas** para cada exercício (abra só depois de tentar).
- **Projeto final** baseado num problema real de laboratório de qualidade.
- **Guia de carreira**: qual trilha seguir, o que estudar além do curso e como conseguir
  a primeira oportunidade.
- **Apostila em PDF** (versão A4 e versão para celular) com todas as aulas, enunciados,
  desafios e quizzes, na pasta `apostila/`.
- **Ferramenta `curso.py`** que testa seus exercícios e mostra seu progresso.

## Mapa do curso

| Módulo | Assunto | O que você passa a conseguir fazer |
|---|---|---|
| 00 | Preparação do ambiente | Instalar Python, VS Code e Git, e rodar o primeiro teste |
| 01 | Fundamentos | Variáveis, tipos, contas e textos formatados |
| 02 | Decisões e repetições | Programas que decidem e repetem: if, for, while |
| 03 | Coleções | Guardar e organizar dados: listas, dicionários, conjuntos |
| 04 | Funções | Quebrar problemas grandes em peças pequenas e reutilizáveis |
| 05 | Texto e expressões regulares | Ler e-mails, limpar textos, converter números brasileiros |
| 06 | Arquivos e erros | Ler e gravar CSV e JSON, tratar erros sem o programa quebrar |
| 07 | Módulos e biblioteca padrão | Organizar projetos, datas, estatística, programas de terminal |
| 08 | Orientação a objetos | Modelar o mundo real com classes e dataclasses |
| 09 | Testes e qualidade | Escrever testes, usar Git, depurar e manter código limpo |
| 10 | Dados com pandas | Analisar planilhas e CSV, fazer gráficos, gerar relatórios Excel |
| 11 | Banco de dados e SQL | Criar e consultar bancos de dados com SQL |
| 12 | Automação e integração | APIs, e-mail, Excel, pastas e robôs no navegador |
| 13 | APIs com FastAPI | Criar sua própria API web, com testes |
| 14 | Projeto final | Construir o Validador de Certificados de ponta a ponta |

Os módulos 01 a 09 são a base de qualquer carreira com Python. Do 10 em diante você entra
nas ferramentas que o mercado pede para dados e automação.

## Como começar

1. Leia `PLANO-DE-ESTUDOS.md` (10 minutos): ele mostra o caminho e a rotina.
1. Abra `00-preparacao/README.md` e siga o passo a passo para preparar o computador.
1. Na pasta `curso-python`, com o ambiente virtual ativado, rode:

   ```text
   python curso.py modulos
   python curso.py testar 00
   ```

1. Faça um módulo de cada vez, na ordem.

## Como cada módulo funciona

```text
NN-nome-do-modulo/
  README.md      a aula: leia com calma e digite os exemplos
  exemplos/      os códigos da aula, prontos para rodar
  exercicios/    ONDE VOCÊ TRABALHA: complete as funções
  testes/        os testes que corrigem seus exercícios (não precisa mexer)
  solucoes/      as soluções oficiais comentadas (abra só depois de tentar)
  desafio/       um mini projeto para juntar tudo
  quiz.md        perguntas de revisão com gabarito
```

O ciclo de cada exercício:

1. Abra `exercicios/exNN_....py` e leia o enunciado no topo do arquivo.
2. Apague a linha `raise NotImplementedError(...)` e escreva o seu código.
3. Rode `python curso.py testar NN exMM`.
4. Se falhar, leia a mensagem: ela mostra o que era esperado e o que seu código devolveu.
5. Passou? Compare com `solucoes/` para aprender outra forma de pensar.

Para ver o quanto você já avançou:

```text
python curso.py progresso
python curso.py progresso --detalhes
```

## Ritmo sugerido

Com **1 hora por dia, 5 dias por semana**, o curso leva cerca de **31 semanas (7
meses)**. Com 2 horas por dia, cerca de 4 meses. Mais importante que a velocidade é a
constância: programar um pouco todo dia ensina mais do que uma maratona por semana.

| Fase | Módulos | Semanas (1h/dia) | Marco de portfólio |
|---|---|---|---|
| Base da linguagem | 00 a 04 | 1 a 9 | Primeiro programa útil |
| Programas de verdade | 05 a 08 | 10 a 17 | Ferramenta de laboratório |
| Profissional | 09 a 11 | 18 a 24 | Análise de dados com SQL e pandas |
| Mundo real | 12 a 14 | 25 a 31 | Validador de Certificados |

O passo a passo de cada semana, a rotina diária e o método de estudo estão em
**`PLANO-DE-ESTUDOS.md`**. Leia antes de começar.

## Regras do jogo

- **Digite, não copie.** A memória dos dedos é parte do aprendizado.
- **Tente de verdade antes de abrir a solução.** Travou por mais de 30 minutos? Releia a
  aula, teste pedaços no terminal do Python e só então olhe a solução.
- **Erro é informação.** Toda mensagem de erro diz o que aconteceu e em qual linha.
- **Use IA como professor, não como cola.** Peça explicações e dicas, não a resposta
  pronta.
- **Faça commit do seu progresso** no GitHub. Ele vira o seu portfólio.

## Depois do curso

Leia `carreira/README.md` para escolher a trilha (dados, automação ou backend) e montar o
plano dos próximos meses, e `carreira/recursos.md` para livros, vídeos e comunidades.

## Para quem mantém o curso

```text
python curso.py solucoes             # todas as soluções oficiais passam nos testes
ruff check . && ruff format --check .
python ferramentas/gerar_apostila.py # gera os PDFs (precisa de pandoc e Chrome/Edge)
```
