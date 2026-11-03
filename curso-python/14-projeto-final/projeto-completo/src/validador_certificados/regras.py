"""Regras de negócio puras: tolerâncias, validação da OP e escolha da especificação.

Este módulo não faz I/O. Recebe dados, devolve resultados. Por isso é o mais fácil
de testar e o primeiro a ser escrito.

Convenção: cada regra devolve None quando está tudo certo, ou um texto com o motivo
da reprovação. O motivo vai direto para o relatório.
"""

from __future__ import annotations

from .modelos import Especificacao, EspecificacaoDesconhecida, Medicao, ResultadoValidacao


def verificar_fixa(
    caracteristica: str, valor: float, minimo: float | None, maximo: float | None
) -> str | None:
    """Confere limites fixos (inclusivos). None em um dos lados = sem limite."""
    if minimo is not None and valor < minimo:
        return f"{caracteristica} {valor:g} abaixo do mínimo {minimo:g}"
    if maximo is not None and valor > maximo:
        return f"{caracteristica} {valor:g} acima do máximo {maximo:g}"
    return None


def limites_nominal(nominal: float, percentual: float) -> tuple[float, float]:
    """Faixa nominal ± percentual, arredondada em 4 casas (evita 27.599999999999998)."""
    if nominal <= 0 or percentual <= 0:
        raise ValueError("nominal e percentual devem ser maiores que zero")
    folga = nominal * percentual / 100
    return round(nominal - folga, 4), round(nominal + folga, 4)


def verificar_nominal(
    caracteristica: str, valor: float, nominal: float, percentual: float
) -> str | None:
    """Confere valor contra nominal ± percentual (limites inclusivos)."""
    minimo, maximo = limites_nominal(nominal, percentual)
    if minimo <= valor <= maximo:
        return None
    return (
        f"{caracteristica} {valor:g} fora de {nominal:g} ± {percentual:g}% "
        f"({minimo:g} a {maximo:g})"
    )


def validar_medicao(medicao: Medicao, especificacao: Especificacao) -> ResultadoValidacao:
    """Confere todas as características exigidas pela especificação."""
    motivos: list[str] = []
    for tolerancia in especificacao.tolerancias.values():
        nome = tolerancia.caracteristica
        valor = medicao.valores.get(nome)
        if valor is None:
            motivos.append(f"{nome} sem valor medido")
            continue
        if tolerancia.tipo == "fixa":
            motivo = verificar_fixa(nome, valor, tolerancia.minimo, tolerancia.maximo)
        else:
            nominal = medicao.nominais.get(nome)
            if nominal is None:
                motivos.append(f"{nome} sem valor nominal")
                continue
            motivo = verificar_nominal(nome, valor, nominal, tolerancia.percentual)
        if motivo:
            motivos.append(motivo)
    return ResultadoValidacao(
        op=medicao.op, especificacao=especificacao.titulo, motivos=motivos
    )


def _chave_titulo(titulo: str) -> str:
    return " ".join(titulo.split()).upper()


def escolher_especificacao(
    titulo: str | None, linha: str, especificacoes: dict[str, Especificacao]
) -> Especificacao:
    """Escolhe a especificação da OP. Nunca chuta.

    - título vazio -> padrão da linha;
    - título conhecido -> padrão da linha + tolerâncias do título (o título vence);
    - título desconhecido -> EspecificacaoDesconhecida (vira pendência).
    """
    padrao = next((e for e in especificacoes.values() if e.linha == linha), None)
    if padrao is None:
        raise EspecificacaoDesconhecida(f"linha {linha} sem especificação padrão cadastrada")
    if titulo is None or not titulo.strip():
        return padrao
    por_chave = {_chave_titulo(t): e for t, e in especificacoes.items()}
    especifica = por_chave.get(_chave_titulo(titulo))
    if especifica is None:
        raise EspecificacaoDesconhecida(f"especificação {titulo.strip()!r} não cadastrada")
    return Especificacao(
        titulo=especifica.titulo,
        texto=especifica.texto,
        linha=especifica.linha,
        tolerancias={**padrao.tolerancias, **especifica.tolerancias},
    )
