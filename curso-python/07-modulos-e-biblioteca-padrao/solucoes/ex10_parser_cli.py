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
from datetime import date, datetime


def data_br(texto: str) -> date:
    """Converte 'dd/mm/aaaa' em date (para usar como type= no argparse)."""
    try:
        return datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        # ArgumentTypeError é o "idioma" do argparse para "valor inválido".
        # "from None" esconde o erro original do strptime (em inglês) da mensagem.
        raise argparse.ArgumentTypeError(
            f"data inválida: {texto!r} (use dd/mm/aaaa)"
        ) from None


def criar_parser() -> argparse.ArgumentParser:
    """Parser de argumentos do validador."""
    parser = argparse.ArgumentParser(
        prog="validador",
        description="Confere os valores da planilha com as tolerâncias.",
    )
    # Posicional: sem "--" e obrigatório por padrão.
    parser.add_argument("planilha", help="arquivo .xlsx com os valores")
    # type roda ANTES de conferir choices: "b" vira "B" e aí é aceito.
    parser.add_argument("--linha", type=str.upper, choices=["A", "B", "C", "D"])
    parser.add_argument("--tolerancia", type=float, default=5.0, help="tolerância em %%")
    # type pode ser QUALQUER função que receba texto e devolva o valor convertido.
    parser.add_argument("--desde", type=data_br, help="data inicial (dd/mm/aaaa)")
    # store_true: presente -> True; ausente -> False.
    parser.add_argument("-v", "--verbose", action="store_true", help="mostra detalhes")
    return parser
