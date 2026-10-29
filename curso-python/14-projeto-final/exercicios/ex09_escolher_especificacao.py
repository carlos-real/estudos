"""
Exercício 14.09 — Escolher a especificação da OP (sem chutar)
Nível: ★★☆

Contexto: Na planilha, a coluna "Especificação" traz o título da especificação do
cliente (ex.: "ESP-0412") ou fica vazia. Vazia = vale o padrão da linha. A
especificação do cliente lista só o que muda: o resto vem do padrão da linha. Título
que não existe no banco é pendência: usar o padrão "porque é parecido" pode liberar
um certificado errado.

Tarefa: implemente duas funções.
1. `chave_titulo(titulo)`: a forma "canônica" do título, para comparar: sem espaços
   nas pontas, espaços repetidos viram um só, tudo em maiúsculas.
2. `escolher_especificacao(titulo, linha, especificacoes)`:
- `especificacoes` é {titulo: Especificacao}. O padrão da linha é a especificação
  cujo campo `linha` é igual a `linha` ("A".."D"). Se a linha não tiver padrão,
  levante EspecificacaoDesconhecida("linha <linha> sem especificação padrão
  cadastrada").
- Título None, vazio ou só espaços: devolva o padrão da linha.
- Título informado: compare as chaves (chave_titulo) do título e dos títulos do
  dicionário (" esp-0412 " encontra "ESP-0412"). Se não existir, levante
  EspecificacaoDesconhecida("especificação '<titulo sem espaços nas pontas>' não
  cadastrada"). NUNCA devolva o padrão nesse caso.
- Título encontrado: devolva uma NOVA Especificacao com titulo, texto e linha da
  especificação encontrada e tolerancias = as do padrão, sobrescritas pelas da
  especificação do cliente. Não altere os objetos originais.

Exemplos:
    >>> chave_titulo("  esp-0412 ")
    'ESP-0412'
    >>> escolher_especificacao("", "A", especificacoes).titulo
    'PADRAO-A'
    >>> esp = escolher_especificacao(" esp-0412 ", "C", especificacoes)
    >>> esp.titulo, esp.tolerancias["cof"].maximo, esp.tolerancias["espessura"].percentual
    ('ESP-0412', 0.25, 8.0)
    >>> escolher_especificacao("ESP-9999", "A", especificacoes)
    Traceback (most recent call last):
    EspecificacaoDesconhecida: especificação 'ESP-9999' não cadastrada

Dica: {**a, **b} cria um dicionário novo com tudo de a e, por cima, tudo de b.
Para achar o padrão: next((e for e in especificacoes.values() if ...), None).

Teste com:  python curso.py testar 14 ex09
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
    linha: str = ""  # preenchida só nos padrões de linha
    tolerancias: dict[str, Tolerancia] = field(default_factory=dict)


class EspecificacaoDesconhecida(Exception):
    """O título informado não existe no banco (ou a linha não tem padrão)."""


# ============================================================================
# SUA PARTE
# ============================================================================


def chave_titulo(titulo: str) -> str:
    """Forma canônica do título: " esp-0412 " -> "ESP-0412"."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def escolher_especificacao(
    titulo: str | None, linha: str, especificacoes: dict[str, Especificacao]
) -> Especificacao:
    """Padrão da linha, especificação do cliente (herdando do padrão) ou erro."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
