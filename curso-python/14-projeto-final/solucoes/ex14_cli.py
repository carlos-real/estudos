"""
Exercício 14.14 — A linha de comando (argparse) que junta tudo
Nível: ★★☆

Contexto: Na expedição de sexta-feira ninguém quer abrir o VS Code. O sistema roda
com um comando:
    validador --planilha valores.xlsx --regras regras.db --emails pasta_emails
A CLI é fina: lê argumentos, confere se os arquivos existem, chama quem faz o
trabalho e mostra o resumo. Quem faz o trabalho chega pelo parâmetro `executar`
(injeção de dependência): nos testes, um dublê; no projeto completo, a série real.

Tarefa: implemente duas funções.
1. `criar_parser()` devolve um argparse.ArgumentParser com prog="validador" e:
   --planilha, --regras e --emails: obrigatórios, type=Path;
   --saida: type=Path, padrão Path("saida");
   --emitir: flag (store_true), padrão False;
   -v/--verbose: flag (store_true), padrão False.
2. `main(argv=None, executar=executar_demo)` devolve o código de saída (int):
   a) args = criar_parser().parse_args(argv);
   b) confira, nesta ordem: planilha é arquivo, regras é arquivo, emails é pasta.
      No primeiro que falhar, imprima em sys.stderr
      "Erro: planilha não encontrada: <caminho>" (ou "banco de regras não
      encontrado: ..." ou "pasta de e-mails não encontrada: ...") e devolva 1,
      sem chamar executar;
   c) resumo = executar(planilha=..., regras=..., emails=..., saida=...,
      ensaio=not args.emitir)   (tudo por nome);
   d) imprima "Modo: ENSAIO" (ou "Modo: REAL" com --emitir) e depois uma linha
      "<situacao>: <quantidade>" para cada item do resumo, em ordem alfabética;
   e) devolva 1 se o resumo tiver "falha" maior que zero; senão, 0.

Exemplos:
    >>> main(["--planilha", "valores.xlsx", "--regras", "regras.db",
    ...       "--emails", "emails"], executar=lambda **kw: {"ensaio": 2, "bloqueado": 4})
    Modo: ENSAIO
    bloqueado: 4
    ensaio: 2
    0

Dica: Path.is_file() e Path.is_dir() já dizem se existe E se é do tipo certo.
print(..., file=sys.stderr) escreve na saída de erro. Rode
"python exercicios/ex14_cli.py --help" para ver sua CLI.

Teste com:  python curso.py testar 14 ex14
"""

import argparse
import sys
from collections.abc import Callable
from pathlib import Path

# ============================================================================
# PEÇA PRONTA — um dublê de "executar" para você rodar a CLI sem o resto
# ============================================================================


def executar_demo(
    planilha: Path, regras: Path, emails: Path, saida: Path, ensaio: bool
) -> dict[str, int]:
    """Dublê: no projeto completo, aqui entra a série real (serie.executar_serie)."""
    print(f"[demo] processaria {planilha.name}, {regras.name} e {emails}/ -> {saida}/")
    return {"ensaio": 0, "bloqueado": 0}


# ============================================================================
# SUA PARTE
# ============================================================================


def criar_parser() -> argparse.ArgumentParser:
    """Monta o parser de argumentos da CLI."""
    parser = argparse.ArgumentParser(
        prog="validador",
        description="Confere as OPs da planilha e prepara os certificados.",
    )
    # type=Path: o argparse já entrega Path, não str. required=True: sem ele, o
    # argparse imprime o uso e sai com código 2 (SystemExit) sozinho.
    parser.add_argument("--planilha", type=Path, required=True, help="planilha de valores")
    parser.add_argument("--regras", type=Path, required=True, help="banco de regras (.db)")
    parser.add_argument("--emails", type=Path, required=True, help="pasta dos e-mails")
    parser.add_argument("--saida", type=Path, default=Path("saida"), help="pasta de saída")
    # O padrão SEGURO é o ensaio: emitir de verdade exige pedir explicitamente.
    parser.add_argument("--emitir", action="store_true", help="emite de verdade no TOTVS")
    parser.add_argument("-v", "--verbose", action="store_true", help="log detalhado")
    return parser


def main(
    argv: list[str] | None = None,
    executar: Callable[..., dict[str, int]] = executar_demo,
) -> int:
    """Roda a CLI e devolve o código de saída (0 = ok, 1 = erro ou falha)."""
    # argv=None faz o argparse ler sys.argv; nos testes passamos uma lista.
    args = criar_parser().parse_args(argv)

    # Uma tabela de checagens evita três "if" quase iguais.
    checagens = [
        (args.planilha.is_file(), f"planilha não encontrada: {args.planilha}"),
        (args.regras.is_file(), f"banco de regras não encontrado: {args.regras}"),
        (args.emails.is_dir(), f"pasta de e-mails não encontrada: {args.emails}"),
    ]
    for ok, mensagem in checagens:
        if not ok:
            # Erro vai para stderr: quem redireciona a saída (> resumo.txt) ainda
            # vê o erro na tela, e o Agendador de Tarefas registra separado.
            print(f"Erro: {mensagem}", file=sys.stderr)
            return 1

    resumo = executar(
        planilha=args.planilha,
        regras=args.regras,
        emails=args.emails,
        saida=args.saida,
        ensaio=not args.emitir,
    )
    print("Modo: REAL" if args.emitir else "Modo: ENSAIO")
    for situacao, quantidade in sorted(resumo.items()):
        print(f"{situacao}: {quantidade}")
    # Código de saída diferente de zero avisa o agendador que algo precisa de gente.
    return 1 if resumo.get("falha", 0) > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
