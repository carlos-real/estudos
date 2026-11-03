"""Exemplo 03 — raise, raise ... from e exceções personalizadas (seções 4 e 5).

Rode na pasta curso-python:
    python 06-arquivos-e-erros/exemplos/03_excecoes_personalizadas.py
"""


class ErroDeQualidade(Exception):
    """Base de todos os erros do sistema de qualidade."""


class ValorForaDaTolerancia(ErroDeQualidade):
    """Uma medição saiu da faixa permitida."""


class ArquivoInvalido(ErroDeQualidade):
    """O arquivo existe, mas não está no formato esperado."""


def emitir_certificado(lote, espessura, minimo, maximo):
    if not minimo <= espessura <= maximo:
        raise ValorForaDaTolerancia(
            f"lote {lote}: espessura {espessura} fora de [{minimo}, {maximo}]"
        )
    return f"Certificado do lote {lote}: espessura {espessura} µm (OK)"


def ler_peso(texto):
    try:
        return float(texto.replace(".", "").replace(",", "."))
    except ValueError as erro:
        raise ValueError(f"peso inválido no e-mail da expedição: {texto!r}") from erro


for lote, espessura in [("L001", 25.1), ("L002", 28.3), ("L003", 24.0)]:
    try:
        print(emitir_certificado(lote, espessura, 22.5, 27.5))
    except ErroDeQualidade as erro:  # a "mãe" captura as filhas
        print(f"NÃO EMITIDO ({type(erro).__name__}): {erro}")

print()
try:
    ler_peso("1.250,5 kg")
except ValueError as erro:
    print("Erro novo   :", erro)
    print("Erro original:", erro.__cause__)  # guardado pelo "from erro"
