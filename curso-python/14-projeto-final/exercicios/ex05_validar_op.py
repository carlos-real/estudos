"""
Exercício 14.05 — Validar uma OP inteira
Nível: ★★☆

Contexto: Você já tem as regras fixa e nominal (peças prontas abaixo). Agora é
juntar: para cada tolerância da especificação, pegar o valor medido da OP, aplicar a
regra certa e acumular TODOS os motivos de reprovação. Quem corrige a OP quer ver
todos os problemas de uma vez, não um por vez.

Tarefa: implemente `validar_medicao(medicao, especificacao)` e devolva um
ResultadoValidacao(op=medicao.op, especificacao=especificacao.titulo, motivos=[...]).
Para cada Tolerancia em especificacao.tolerancias (na ordem do dicionário):
- valor = medicao.valores.get(caracteristica). Se não houver valor:
  motivo "<caracteristica> sem valor medido" e passe para a próxima.
- tipo "fixa": use verificar_fixa(caracteristica, valor, minimo, maximo).
- tipo "nominal": o nominal vem de medicao.nominais. Se não houver:
  motivo "<caracteristica> sem valor nominal". Se houver: use verificar_nominal.
- Se a regra devolver um texto, ele entra na lista de motivos.
Características medidas que a especificação não exige são ignoradas.

Exemplos:
    >>> resultado = validar_medicao(medicao_24519, padrao_a)
    >>> resultado.motivos
    ['espessura 44.8 fora de 40 ± 10% (36 a 44)']
    >>> resultado.aprovado
    False

Dica: o laço é "for tolerancia in especificacao.tolerancias.values():". Use continue
para pular para a próxima característica depois de anotar um motivo.

Teste com:  python curso.py testar 14 ex05
"""

from dataclasses import dataclass, field

# ============================================================================
# PEÇAS PRONTAS (etapas anteriores) — não precisa mexer
# ============================================================================


@dataclass(frozen=True)
class Tolerancia:
    caracteristica: str
    tipo: str  # "fixa" ou "nominal"
    minimo: float | None = None
    maximo: float | None = None
    percentual: float | None = None


@dataclass
class Especificacao:
    titulo: str
    texto: str = ""
    linha: str = ""
    tolerancias: dict[str, Tolerancia] = field(default_factory=dict)


@dataclass
class Medicao:
    op: str
    aba: str
    linha: str
    valores: dict[str, float] = field(default_factory=dict)
    nominais: dict[str, float] = field(default_factory=dict)
    especificacao: str = ""
    observacao: str = ""
    produto: str = ""
    linha_excel: int = 0


@dataclass
class ResultadoValidacao:
    op: str
    especificacao: str
    motivos: list[str] = field(default_factory=list)

    @property
    def aprovado(self) -> bool:
        return not self.motivos


def verificar_fixa(caracteristica, valor, minimo, maximo):  # etapa 3
    if minimo is not None and valor < minimo:
        return f"{caracteristica} {valor:g} abaixo do mínimo {minimo:g}"
    if maximo is not None and valor > maximo:
        return f"{caracteristica} {valor:g} acima do máximo {maximo:g}"
    return None


def verificar_nominal(caracteristica, valor, nominal, percentual):  # etapa 4
    folga = nominal * percentual / 100
    minimo, maximo = round(nominal - folga, 4), round(nominal + folga, 4)
    if minimo <= valor <= maximo:
        return None
    return (
        f"{caracteristica} {valor:g} fora de {nominal:g} ± {percentual:g}% "
        f"({minimo:g} a {maximo:g})"
    )


# ============================================================================
# SUA PARTE
# ============================================================================


def validar_medicao(medicao: Medicao, especificacao: Especificacao) -> ResultadoValidacao:
    """Confere todas as características exigidas pela especificação."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
