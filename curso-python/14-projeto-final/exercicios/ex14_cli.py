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
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def main(
    argv: list[str] | None = None,
    executar: Callable[..., dict[str, int]] = executar_demo,
) -> int:
    """Roda a CLI e devolve o código de saída (0 = ok, 1 = erro ou falha)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


if __name__ == "__main__":
    sys.exit(main())
