"""
Exercício 07.10 — Argumentos de linha de comando com argparse
Nível: ★★☆

Contexto: O Validador de Certificados vai rodar no terminal (e depois no Agendador de
Tarefas do Windows), assim:
    python validador.py valores.xlsx --linha B --tolerancia 7.5 --desde 01/10/2026 -v
Antes de validar qualquer coisa, o programa precisa entender esses argumentos.

Tarefa:
1. `data_br(texto)` converte "dd/mm/aaaa" em date. Se o texto for inválido, levante
   argparse.ArgumentTypeError com uma mensagem que contenha "dd/mm/aaaa".
   (O argparse transforma esse erro numa mensagem amigável e encerra com código 2.)
2. `criar_parser()` devolve um argparse.ArgumentParser com prog="validador" e:
   - `planilha`: argumento posicional obrigatório (texto);
   - `--linha`: uma de A, B, C, D; aceite minúscula (type=str.upper); padrão None;
   - `--tolerancia`: float, padrão 5.0;
   - `--desde`: data no formato brasileiro (type=data_br), padrão None;
   - `-v` / `--verbose`: liga/desliga (action="store_true").

Exemplos:
    >>> args = criar_parser().parse_args(["valores.xlsx", "--linha", "b"])
    >>> args.planilha, args.linha, args.tolerancia, args.desde, args.verbose
    ('valores.xlsx', 'B', 5.0, None, False)

Dica: nos testes, parse_args recebe uma LISTA de textos, como se fosse o terminal.
Argumento inválido faz o argparse chamar sys.exit(2): isso é um SystemExit.

Teste com:  python curso.py testar 07 ex10
"""

import argparse
from datetime import date


def data_br(texto: str) -> date:
    """Converte 'dd/mm/aaaa' em date (para usar como type= no argparse)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def criar_parser() -> argparse.ArgumentParser:
    """Parser de argumentos do validador."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
