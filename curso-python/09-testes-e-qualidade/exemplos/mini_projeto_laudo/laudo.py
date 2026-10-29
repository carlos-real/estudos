"""Conferência de medições de bobinas contra a tolerância da especificação.

Mini projeto do módulo 09: o código fica aqui e os testes ficam em tests/.
"""

from pathlib import Path


def calcular_limites(nominal: float, tolerancia_pct: float) -> tuple[float, float]:
    """Devolve (mínimo, máximo) para um valor nominal ± tolerância em %."""
    if nominal <= 0:
        raise ValueError(f"nominal deve ser positivo, recebi {nominal}")
    if tolerancia_pct < 0:
        raise ValueError(f"tolerância não pode ser negativa, recebi {tolerancia_pct}")
    margem = nominal * tolerancia_pct / 100
    return nominal - margem, nominal + margem


def avaliar(valor: float, minimo: float, maximo: float) -> str:
    """'APROVADO' se o valor está entre os limites (inclusive), senão 'REPROVADO'."""
    return "APROVADO" if minimo <= valor <= maximo else "REPROVADO"


def media(valores: list[float]) -> float:
    """Média aritmética. Lista vazia é erro: não existe média de nada."""
    if not valores:
        raise ValueError("lista de valores vazia")
    return sum(valores) / len(valores)


def ler_medicoes(caminho: Path) -> list[float]:
    """Lê um arquivo com um valor por linha. Aceita vírgula decimal e ignora linhas vazias."""
    valores = []
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha:
            valores.append(float(linha.replace(",", ".")))
    return valores


def buscar_nominal_no_erp(op: str) -> float:
    """Consulta o valor nominal da OP no ERP.

    No mundo real isso abriria uma conexão com o TOTVS. Aqui só simulamos que o
    computador não tem acesso: os testes substituem esta função com monkeypatch.
    """
    raise ConnectionError(f"sem acesso ao ERP para consultar a OP {op}")


def conferir_op(op: str, valores: list[float], tolerancia_pct: float) -> str:
    """Busca o nominal da OP, calcula os limites, avalia a média e imprime o resumo."""
    nominal = buscar_nominal_no_erp(op)
    minimo, maximo = calcular_limites(nominal, tolerancia_pct)
    valor_medio = media(valores)
    resultado = avaliar(valor_medio, minimo, maximo)
    print(f"OP {op}: média {valor_medio:.2f} em [{minimo:.2f}, {maximo:.2f}] -> {resultado}")
    return resultado
