"""Um programa de linha de comando (CLI) pequeno com argparse.

Calcula a faixa nominal ± % e confere valores.

Rode com:
    python exemplos/11_cli_argparse.py 25 --percentual 10 --valores 24.1 26 27.9
    python exemplos/11_cli_argparse.py --help
Sem argumentos, ele roda uma demonstração (para você ver funcionando).
"""

import argparse
import sys


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="faixa",
        description="Calcula a faixa nominal ± percentual e confere valores.",
        epilog="Exemplo: faixa 25 -p 10 --valores 24.1 26 27.9",
    )
    parser.add_argument("nominal", type=float, help="valor nominal (ex.: 25 para 25 µm)")
    parser.add_argument(
        "-p", "--percentual", type=float, default=10.0, help="tolerância em %% (padrão: 10)"
    )
    parser.add_argument("--unidade", default="µm", help="unidade exibida (padrão: µm)")
    parser.add_argument("--valores", type=float, nargs="+", default=[], help="valores medidos")
    parser.add_argument("-v", "--verbose", action="store_true", help="mostra mais detalhes")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = criar_parser().parse_args(argv)  # argv=None -> usa sys.argv[1:]
    margem = args.nominal * args.percentual / 100
    minimo, maximo = args.nominal - margem, args.nominal + margem
    print(f"Faixa: {minimo:.2f} a {maximo:.2f} {args.unidade}")
    if args.verbose:
        print(f"(nominal {args.nominal} ± {args.percentual}%)")
    fora = 0
    for valor in args.valores:
        ok = minimo <= valor <= maximo
        if not ok:
            fora += 1
        print(f"  {valor:.2f} {args.unidade}: {'ok' if ok else 'FORA'}")
    return 1 if fora else 0  # código de saída: 0 = tudo certo


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("(sem argumentos: rodando uma demonstração)")
        demo = ["25", "-p", "10", "--valores", "24.1", "26", "27.9", "-v"]
        print("faixa", " ".join(demo))
        codigo = main(demo)
        print("Código de saída:", codigo)
        sys.exit(0)
    sys.exit(main())
