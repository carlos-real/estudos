"""
Exercício 14.11 — Montar a fila de emissão (a triagem)
Nível: ★★★

Contexto: Chegou a hora de juntar as peças. Para cada pedido da expedição, o sistema
decide: vai para a fila de emissão (OP liberada e aprovada) ou fica bloqueado, com o
motivo. Esta é a camada de serviço: não lê arquivo nenhum, só usa as peças prontas
das etapas anteriores (já estão no arquivo, antes da sua parte).

Tarefa: implemente `montar_fila(pedidos, medicoes, especificacoes)` e devolva a tupla
(fila, bloqueados): duas listas de ItemFila, cada uma na ordem dos pedidos. Para cada
pedido, nesta ordem (as 3 primeiras checagens PARAM no primeiro problema):
  1. Procure a OP do pedido nas medições (medicao.op == pedido.op).
     Nenhuma -> bloqueado ["OP não encontrada na planilha"].
     Mais de uma -> bloqueado ["OP aparece <n> vezes na planilha"].
  2. conferir_linha(medicao.aba, medicao.linha): se devolver texto -> bloqueado [texto].
  3. escolher_especificacao(medicao.especificacao, normalizar_linha(medicao.aba),
     especificacoes): se levantar EspecificacaoDesconhecida -> bloqueado [str(erro)].
  4. validar_medicao(medicao, especificacao): os motivos entram na lista.
  5. Se NÃO esta_liberado(medicao.observacao): acrescente SEM_LIBERACAO.
  Se a lista de motivos dos passos 4-5 estiver vazia -> ItemFila com situacao
  "emitir"; senão, situacao "bloqueado" com os motivos.
Todo ItemFila leva op, nf e peso_kg do pedido. O campo especificacao recebe o título
da especificação escolhida (fica "" quando o bloqueio acontece antes do passo 3).

Exemplos:
    >>> fila, bloqueados = montar_fila(pedidos, medicoes, especificacoes)
    >>> [(i.op, i.situacao) for i in fila]
    [('24518', 'emitir')]
    >>> bloqueados[0].motivos
    ['espessura 44.8 fora de 40 ± 10% (36 a 44)']

Dica: monte antes um índice {op: [medições]} com dict.setdefault(op, []).append(m):
cada pedido acha suas medições direto, sem varrer a lista inteira. A função
auxiliar triar(pedido, encontradas, especificacoes) já está declarada: decidir UM
pedido nela, com retornos antecipados, deixa montar_fila bem curta. (Opcional: se
preferir fazer tudo em montar_fila, pode apagar triar.)

Teste com:  python curso.py testar 14 ex11
"""

import re
import unicodedata
from dataclasses import dataclass, field

# ============================================================================
# PEÇAS PRONTAS (etapas 1 a 10) — não precisa mexer
# ============================================================================

SEM_LIBERACAO = "COF sem liberação na observação"


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


@dataclass(frozen=True)
class Pedido:
    op: str
    nf: str
    peso_kg: float
    origem: str = ""


@dataclass
class ResultadoValidacao:
    op: str
    especificacao: str
    motivos: list[str] = field(default_factory=list)


@dataclass
class ItemFila:
    op: str
    nf: str
    peso_kg: float
    situacao: str  # "emitir" ou "bloqueado"
    especificacao: str = ""
    motivos: list[str] = field(default_factory=list)
    comprovante: str = ""


class EspecificacaoDesconhecida(Exception):
    pass


def validar_medicao(medicao, especificacao):  # etapas 3, 4 e 5
    motivos = []
    for tol in especificacao.tolerancias.values():
        nome, valor = tol.caracteristica, medicao.valores.get(tol.caracteristica)
        if valor is None:
            motivos.append(f"{nome} sem valor medido")
        elif tol.tipo == "fixa":
            if tol.minimo is not None and valor < tol.minimo:
                motivos.append(f"{nome} {valor:g} abaixo do mínimo {tol.minimo:g}")
            elif tol.maximo is not None and valor > tol.maximo:
                motivos.append(f"{nome} {valor:g} acima do máximo {tol.maximo:g}")
        elif medicao.nominais.get(nome) is None:
            motivos.append(f"{nome} sem valor nominal")
        else:
            nominal, pct = medicao.nominais[nome], tol.percentual
            minimo = round(nominal - nominal * pct / 100, 4)
            maximo = round(nominal + nominal * pct / 100, 4)
            if not minimo <= valor <= maximo:
                motivos.append(
                    f"{nome} {valor:g} fora de {nominal:g} ± {pct:g}% "
                    f"({minimo:g} a {maximo:g})"
                )
    return ResultadoValidacao(medicao.op, especificacao.titulo, motivos)


def esta_liberado(observacao):  # etapa 6
    decomposto = unicodedata.normalize("NFKD", observacao or "")
    texto = " ".join(
        "".join(c for c in decomposto if not unicodedata.combining(c)).lower().split()
    )
    return re.search(r"\bcof\s*[:-]?\s*liberad[oa]\b", texto) is not None


def normalizar_linha(texto):  # etapa 8
    achado = re.fullmatch(r"(?:LINHA\s*)?([A-D])", str(texto or "").strip().upper())
    return achado.group(1) if achado else None


def conferir_linha(nome_aba, linha_informada):  # etapa 8
    da_aba = normalizar_linha(nome_aba)
    if da_aba is None:
        return f"aba {nome_aba!r} não corresponde a uma linha de produção"
    informada = normalizar_linha(linha_informada)
    if informada is None:
        texto = "" if linha_informada is None else str(linha_informada)
        return f"linha não informada ou inválida: {texto!r}"
    if informada != da_aba:
        return f"linha informada {informada} diferente da aba {nome_aba}"
    return None


def escolher_especificacao(titulo, linha, especificacoes):  # etapa 9
    padrao = next((e for e in especificacoes.values() if e.linha == linha), None)
    if padrao is None:
        raise EspecificacaoDesconhecida(f"linha {linha} sem especificação padrão cadastrada")
    if titulo is None or not titulo.strip():
        return padrao
    por_chave = {" ".join(t.split()).upper(): e for t, e in especificacoes.items()}
    cliente = por_chave.get(" ".join(titulo.split()).upper())
    if cliente is None:
        raise EspecificacaoDesconhecida(f"especificação {titulo.strip()!r} não cadastrada")
    tolerancias = {**padrao.tolerancias, **cliente.tolerancias}
    return Especificacao(cliente.titulo, cliente.texto, cliente.linha, tolerancias)


# ============================================================================
# SUA PARTE
# ============================================================================


def triar(
    pedido: Pedido, encontradas: list[Medicao], especificacoes: dict[str, Especificacao]
) -> ItemFila:
    """Decide o destino de UM pedido (auxiliar de montar_fila)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def montar_fila(
    pedidos: list[Pedido],
    medicoes: list[Medicao],
    especificacoes: dict[str, Especificacao],
) -> tuple[list[ItemFila], list[ItemFila]]:
    """Devolve (fila_para_emitir, bloqueados), cada uma na ordem dos pedidos."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
