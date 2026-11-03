"""
Solução de referência — Desafio 00: meu cartão de apresentação.

Rode na pasta curso-python:
    python 00-preparacao/desafio/solucao_referencia.py

O seu `meu_cartao.py` não precisa ficar igual a este. Ele só precisa cumprir os
requisitos do desafio/README.md.
"""

# `platform` e `sys` são módulos que já vêm com o Python. Você vai estudar `import`
# no módulo 07; por enquanto, basta saber que eles trazem funções prontas.
import platform
import sys

# Dados do cartão. Troque pelos seus.
NOME = "Carlos Eduardo"
FUNCAO_ATUAL = "Laboratório de Qualidade (embalagens plásticas flexíveis)"
OBJETIVO = "Trabalhar com dados e automação usando Python"


def montar_linha(rotulo: str, valor: str) -> str:
    """Devolve uma linha do cartão no formato 'Rótulo: valor'."""
    # O molde do curso: recebe valores, DEVOLVE um texto. Quem chama decide o que
    # fazer com ele (aqui, mostrar com print).
    return rotulo + ": " + valor


def versao_do_python() -> str:
    """Devolve a versão do Python que está rodando este script, ex.: '3.14.0'."""
    return platform.python_version()


def ambiente_virtual_ativo() -> str:
    """Devolve 'sim' se o script está rodando dentro de um ambiente virtual."""
    # Dentro de um venv, sys.prefix aponta para a pasta .venv e fica diferente de
    # sys.base_prefix (o Python "de fábrica"). O `if` é assunto do módulo 02.
    if sys.prefix != sys.base_prefix:
        return "sim"
    return "não (ative com .venv\\Scripts\\Activate.ps1)"


def main() -> None:
    separador = "-" * 50  # o * repete o texto: "-" * 3 vira "---"
    print(separador)
    print("CARTÃO DE APRESENTAÇÃO")
    print(separador)
    print(montar_linha("Nome", NOME))
    print(montar_linha("Função atual", FUNCAO_ATUAL))
    print(montar_linha("Objetivo", OBJETIVO))
    print(montar_linha("Python", versao_do_python()))
    print(montar_linha("Ambiente virtual ativo", ambiente_virtual_ativo()))
    print(separador)


# Este bloco faz o main() rodar quando você executa o arquivo diretamente.
# O módulo 07 explica o `if __name__ == "__main__"` em detalhes.
if __name__ == "__main__":
    main()
