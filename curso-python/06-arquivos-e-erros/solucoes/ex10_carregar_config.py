"""
Exercício 06.10 — Configuração em JSON
Nível: ★★☆

Contexto: As configurações do robô (pasta dos laudos, casas decimais, texto de
liberação) ficam num arquivo JSON que o próprio usuário edita no Bloco de
Notas. Às vezes o arquivo nem existe; às vezes alguém esquece uma vírgula.

A exceção `ArquivoInvalido` já está criada no arquivo.

Tarefa 1: implemente `carregar_config(caminho, padrao)`:
- se o arquivo não existir, devolva uma CÓPIA de `padrao`;
- se existir, leia o JSON (UTF-8);
- JSON com erro de sintaxe: levante
  ArquivoInvalido(f"{caminho.name}: JSON inválido (linha {erro.lineno})"),
  encadeado com `from erro` (o json.JSONDecodeError original);
- JSON que não é um objeto (por exemplo, uma lista): levante
  ArquivoInvalido(f"{caminho.name}: esperado um objeto JSON");
- devolva um dicionário NOVO com as chaves de `padrao` atualizadas pelas do
  arquivo (o arquivo vence);
- nunca altere o dicionário `padrao` recebido.

Tarefa 2: implemente `salvar_config(caminho, config)`: grave o dicionário em
JSON, UTF-8, com indent=2 e ensure_ascii=False (acentos legíveis), criando as
pastas que faltarem.

Exemplos:
    >>> padrao = {"casas": 2, "liberacao": "COF: liberado"}
    >>> carregar_config(Path("nao_existe.json"), padrao)
    {'casas': 2, 'liberacao': 'COF: liberado'}
    >>> salvar_config(Path("config.json"), {"casas": 3})
    >>> carregar_config(Path("config.json"), padrao)
    {'casas': 3, 'liberacao': 'COF: liberado'}

Dica: `json.JSONDecodeError` tem o atributo `lineno`. Para juntar dois
dicionários num novo: `{**padrao, **dados}` ou `dict(padrao)` + `update`.

Teste com:  python curso.py testar 06 ex10
"""

import json
from pathlib import Path


class ArquivoInvalido(Exception):
    """O arquivo existe, mas não está no formato esperado."""


def carregar_config(caminho: Path, padrao: dict) -> dict:
    """Lê a configuração do JSON, completando com os valores padrão."""
    if not caminho.exists():
        return dict(padrao)  # cópia: quem receber pode alterar sem medo
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except json.JSONDecodeError as erro:
        # "from erro" guarda o erro original em __cause__: o traceback mostra
        # as duas coisas (o que o usuário fez e onde exatamente).
        raise ArquivoInvalido(f"{caminho.name}: JSON inválido (linha {erro.lineno})") from erro
    if not isinstance(dados, dict):
        raise ArquivoInvalido(f"{caminho.name}: esperado um objeto JSON")
    # Desempacotamento de dicionários: as chaves de "dados" sobrescrevem as de
    # "padrao" e o resultado é um dicionário NOVO.
    return {**padrao, **dados}


def salvar_config(caminho: Path, config: dict) -> None:
    """Grava a configuração em JSON legível (indentado e com acentos)."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(config, arquivo, indent=2, ensure_ascii=False)
