# CLAUDE.md — guia para o Claude neste repositório

Este repositório é o estudo de programação do Carlos. O centro é o **Curso de Python** em
`curso-python/`, escrito para ele. Leia este arquivo inteiro antes de responder dúvidas;
ele existe para que você responda **sem pesquisar**, apontando módulo e seção certos.

## Quem é o aluno

- Carlos, trabalha no **laboratório de qualidade de uma indústria de embalagens plásticas
  flexíveis**. Usa Windows, Excel, Outlook e o ERP **TOTVS Protheus** (webapp no Edge).
- Iniciante em Python (já tinha um script pandas em `src/main.py`). Objetivo: programar de
  verdade e conseguir trabalho em dados, automação ou backend. Lê pelo celular.
- Quer um **conselheiro técnico**, não um bajulador: resposta primeiro, frases curtas,
  discordar quando for o caso, marcar confiança ([Certo]/[Provável]/[Chute]).
- Projeto real dele (vira o módulo 14): validar valores de uma planilha (4 abas, linhas A–D)
  contra tolerâncias (fixas por linha+especificação; espessura e gramatura = nominal ± %),
  ler pedidos da expedição por e-mail (OP, NF, peso), escolher especificação pelo título do
  aviso do TOTVS ou o padrão da linha, exigir a observação "COF: liberado" e emitir o
  certificado no TOTVS com um robô (Playwright) em modo ensaio.

## Mapa do repositório

```text
README.md                    porta de entrada do repositório
CLAUDE.md                    guia do Claude (contexto do curso e como tirar dúvidas)
curso-python/
  README.md                  visão geral do curso
  PLANO-DE-ESTUDOS.md        trilha de 31 semanas, rotina, revisão, marcos de portfólio
  INDICE.md                  ÍNDICE DETALHADO: seções de cada aula e os 191 exercícios
  NN-nome/                   15 módulos (00 a 14), estrutura abaixo
  carreira/README.md         guia de carreira (fato x opinião, planos de 6 e 12 meses)
  carreira/recursos.md       livros, vídeos, exercícios, comunidades (links conferidos)
  apostila/                  PDFs (A4 e celular)
  curso.py                   testar / progresso / modulos / solucoes
  _curso.py, conftest.py     carregam o exercício (ou a solução) para o pytest
  ferramentas/               gerar_apostila.py (pandoc + Chromium) e gerar_indice.py
src/main.py                  primeiro script do Carlos (contagem de cargos em salaries.csv)
arquivos/salaries.csv        133 mil salários de profissões de dados (laboratório do módulo 10)
pyproject.toml               Poetry; o módulo 07 §8 ensina a arrumar (ferramentas no grupo dev)
.github/workflows/           CI: soluções + ruff + projeto final de ponta a ponta
```

Cada módulo: `README.md` (aula), `exemplos/`, `exercicios/` (o aluno edita),
`testes/test_mNN_exMM_*.py`, `solucoes/` (comentadas), `desafio/` (README +
`solucao_referencia.py`), `quiz.md` (gabarito no fim), às vezes `dados/`.

## Os módulos

| Nº | Módulo | Semanas | Pontos-chave |
|---|---|---|---|
| 00 | Preparação do ambiente | 1 | Python 3.14 no Windows, VS Code, Git, venv, `curso.py`, molde def/return |
| 01 | Fundamentos | 2–3 | tipos, operadores, f-strings, float e round, math |
| 02 | Decisões e repetições | 4–5 | if/elif, for/while, acumuladores, match-case |
| 03 | Coleções | 6–7 | listas, cópia x referência (§4), dicionários aninhados, compreensões, lista de dicts |
| 04 | Funções | 8–9 | padrão mutável (§3), escopo, lambda/key, decomposição (§11), recursão |
| 05 | Texto e regex | 10–11 | número BR (§6), acentos (§7), encodings (§8), regex (§9–15), e-mail da expedição |
| 06 | Arquivos e erros | 12–13 | exceções, with/open, pathlib, utf-8-sig/cp1252 (§8), CSV com `;` (§9), JSON |
| 07 | Módulos e biblioteca padrão | 14–15 | `__main__`, src layout, venv/pip/Poetry, datetime, Counter, statistics, argparse |
| 08 | Orientação a objetos | 16–17 | `__init__`, property, herança x composição, dataclass, Enum, quando não usar classe |
| 09 | Testes e qualidade | 18–19 | pytest (approx, raises, parametrize, fixtures, tmp_path, monkeypatch), TDD, ruff, logging, Git |
| 10 | pandas, Excel e gráficos | 20–22 | CSV BR (§3), Excel (§4), groupby, merge, pivot, matplotlib, gráfico de controle ±3σ |
| 11 | Banco de dados e SQL | 23–24 | SELECT a JOIN, GROUP BY, CTE, transações, SQL injection (§13), banco de regras |
| 12 | Automação e integração | 25–26 | requests, Excel com openpyxl, e-mail, Outlook clássico x novo x Graph (§9), Playwright (§11), robô (§12) |
| 13 | APIs com FastAPI | 27 | rotas, Pydantic, HTTPException, dependências, SQLite, TestClient, uvicorn |
| 14 | Projeto final | 28–31 | Validador de Certificados em 14 etapas + `projeto-completo/` (CLI `validador`) |

Para a lista de seções e exercícios de cada módulo, **consulte `curso-python/INDICE.md`**.

## Como o curso funciona (para explicar ao aluno)

- O aluno abre `exercicios/exMM_*.py`, lê o enunciado (docstring), troca o
  `raise NotImplementedError` pelo código e roda, dentro de `curso-python`:
  `python curso.py testar NN exMM`. `python curso.py progresso -d` mostra o avanço.
- `CURSO_SOLUCOES=1` (ou `python curso.py solucoes`) testa as soluções oficiais.
- Regra do curso: todo teste falha contra o arquivo não resolvido e passa com a solução.
- Exercícios só usam o que foi ensinado até o módulo. Os 2 últimos de cada módulo (do 02
  em diante) são `_revisao_` (misturam módulos anteriores); há 1 de leitura de código.
- Método: PRIMM ("🔮 Preveja antes de rodar", "🔧 Modifique"), exemplos resolvidos,
  revisão espaçada às sextas, quiz sem consultar, checklist "Você domina este módulo se...".
- Requisitos: Python 3.10+ (recomendado 3.14), `pip install -r curso-python/requirements.txt`
  (pytest, ruff, pandas, openpyxl, matplotlib, requests, fastapi, httpx, uvicorn).
  Playwright é opcional (módulo 12): `pip install playwright`, usa o Edge com `channel="msedge"`.

## Como tirar dúvidas do aluno (protocolo)

1. **Localize** no `INDICE.md` o módulo, a seção e o exercício. Leia o enunciado, o teste
   (`testes/test_mNN_exMM_*.py`) e a seção da aula antes de responder.
2. **Erro no exercício:** peça (ou use) o código e a mensagem do teste. Explique o que a
   falha diz (esperado x obtido) e aponte a seção da aula. Dê **dicas em níveis**: primeiro
   a pista, depois o caminho; a solução completa só se ele pedir depois de tentar. Mostrar
   a solução oficial é ok quando ele já resolveu e quer comparar.
3. **Dúvida de conceito:** responda curto, com um exemplo do mundo dele (OP, espessura,
   tolerância, COF) e cite "módulo NN, seção X".
4. **Fora do curso** (mercado, versões, preços): pesquise antes de afirmar; o resto,
   responda do material daqui.
5. **Nunca** altere o curso para fazer um teste passar; se achar bug real no curso, diga e
   proponha a correção.

## Dúvidas frequentes (resposta rápida)

| Dúvida | Onde está / resposta curta |
|---|---|
| `python` não é reconhecido no Windows | 00 §2: reinstalar marcando "Add python.exe to PATH" |
| `Activate.ps1 ... não pode ser carregado` | 00 §9: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `No module named pytest` / `pandas` | venv não ativado ou requirements não instalado (00 §9) |
| Rodei `curso.py` e "can't open file" | precisa estar na pasta `curso-python` (00 §7 e "Lendo mensagens de erro") |
| `0.1 + 0.2` dá 0.30000000000000004 | 01 §12; nos testes, `pytest.approx` (09 §6) |
| Mudei a cópia e a original mudou junto | cópia x referência, 03 §4 |
| Lista "lembra" valores entre chamadas | argumento padrão mutável, 04 §3 |
| `print` x `return` | molde def/return, 00 §10 e 01 §14 |
| Número "1.250,50" vira texto | 05 §6; no pandas `decimal=","`, `thousands="."` (10 §3) |
| "ExpediÃ§Ã£o" / `UnicodeDecodeError` | 05 §8 e 06 §8 (utf-8-sig, cp1252) |
| CSV do Excel abre tudo numa coluna | separador `;`, 06 §9 |
| Regex não pega o texto | montar aos poucos, 05 §10; grupos nomeados 05 §12 |
| `ModuleNotFoundError` do meu próprio módulo | onde o Python procura, 07 §4; src layout 07 §6 |
| Quando usar classe | 08 §16; dataclass 08 §12 |
| Como testar função com arquivo / internet | `tmp_path` 09 §9; `monkeypatch` 09 §11 e 12 §5 |
| pandas: agrupar / cruzar tabelas | groupby 10 §11; merge 10 §12; pivot 10 §13 |
| SQL com variável do usuário | sempre parâmetro `?`, nunca f-string: 11 §13 |
| Ler Outlook | clássico via win32com; Novo Outlook só via Graph (TI): 12 §9 |
| Robô no TOTVS | Playwright + Edge, modo ensaio, prints, idempotência: 12 §11–12, 14 §10 |
| Rodar o projeto final | `14-projeto-final/projeto-completo/README.md`: `pip install -e ".[dev]"` e `validador ...` |

## Manutenção

- Depois de mudar aulas ou exercícios: `python ferramentas/gerar_indice.py` (atualiza o
  índice) e, se quiser, `python ferramentas/gerar_apostila.py` (PDFs; precisa de pandoc,
  Chromium/Edge e, opcional, pikepdf para compactar).
- Antes de enviar: `python curso.py solucoes`, `ruff check .` e `ruff format --check .`
  dentro de `curso-python`. O CI repete isso e roda o projeto final.
- Aulas em Markdown não são formatadas pelo ruff (os comentários alinhados são didáticos).
