# Estudos de Python

[![Curso de Python](https://github.com/carlos-real/estudos/actions/workflows/curso-python.yml/badge.svg)](https://github.com/carlos-real/estudos/actions/workflows/curso-python.yml)

Meu repositório de estudos de programação. O centro dele é um **curso completo de
Python**, do zero ao primeiro sistema profissional, pensado para quem trabalha na
indústria e quer migrar para dados, automação ou desenvolvimento.

## Comece por aqui

| O quê | Onde |
|---|---|
| Visão geral do curso | [`curso-python/README.md`](curso-python/README.md) |
| Trilha semana a semana e método de estudo | [`curso-python/PLANO-DE-ESTUDOS.md`](curso-python/PLANO-DE-ESTUDOS.md) |
| Preparar o computador (primeira aula) | [`curso-python/00-preparacao/`](curso-python/00-preparacao/README.md) |
| Apostila para ler no celular (PDF) | [`apostila-curso-python-celular.pdf`](curso-python/apostila/apostila-curso-python-celular.pdf) |
| Apostila para imprimir (PDF, A4) | [`apostila-curso-python.pdf`](curso-python/apostila/apostila-curso-python.pdf) |
| Guia de carreira | [`curso-python/carreira/`](curso-python/carreira/README.md) |

## O curso em números

| | |
|---|---|
| Módulos | 15 (do 00 ao 14) |
| Exercícios | 191, do ★☆☆ ao ★★★ |
| Testes automáticos | 1.868 |
| Duração sugerida | 31 semanas, com 1 hora por dia |
| Projeto final | Validador de Certificados (laboratório de qualidade) |

Os módulos vão de variáveis e laços até pandas, SQL, automação com robôs, APIs com
FastAPI e um sistema completo com testes. Cada módulo tem aula, exemplos, exercícios com
correção automática, soluções comentadas, desafio e quiz.

## Como usar (Windows)

```powershell
git clone https://github.com/carlos-real/estudos.git
cd estudos\curso-python
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt

python curso.py modulos          # lista os módulos
python curso.py testar 00        # testa os exercícios do módulo 00
python curso.py progresso        # mostra quanto você já avançou
```

No Linux ou macOS, use `python3` e ative o ambiente com `source .venv/bin/activate`.
O passo a passo completo, com os erros mais comuns, está no módulo 00.

## Estrutura do repositório

```text
estudos/
├── curso-python/            o curso
│   ├── 00-preparacao/ … 14-projeto-final/
│   ├── apostila/            PDFs com todas as aulas
│   ├── carreira/            guia de carreira e recursos
│   ├── curso.py             testa exercícios e mostra o progresso
│   └── PLANO-DE-ESTUDOS.md  a trilha semana a semana
├── src/main.py              meu primeiro script de análise de dados (pandas)
├── arquivos/salaries.csv    dados de salários usados no script e no módulo 10
├── pyproject.toml           configuração do Poetry (o módulo 07 explica e arruma)
└── .github/workflows/       verificação automática do curso a cada envio
```

## Primeiros estudos

O `src/main.py` foi meu primeiro script: ele conta os cargos no `arquivos/salaries.csv`
(cerca de 133 mil salários de profissões de dados). Ele fica aqui como registro do ponto
de partida. O módulo 10 do curso usa o mesmo arquivo num laboratório guiado sobre
carreira, e o módulo 07 mostra como organizar o `pyproject.toml` da raiz.

```powershell
python src/main.py
```

## Verificação automática

A cada envio para o GitHub, o [GitHub Actions](.github/workflows/curso-python.yml)
confere que:

- as soluções oficiais passam em todos os testes;
- o código segue o padrão de estilo (ruff);
- o projeto final roda de ponta a ponta com os dados de exemplo.

## Licença

[MIT](LICENSE).
