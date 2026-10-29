"""
Exercício 14.12 — Emissor do TOTVS em modo ensaio (e a emissão da fila)
Nível: ★★★

Contexto: O robô do TOTVS ainda não existe (vai ser Playwright no Edge). Mas o resto
do sistema já pode ser construído contra uma INTERFACE: a classe Emissor (pronta
abaixo), com `ensaio` e `emitir(item) -> comprovante`. Hoje o EmissorTotvs só tem o
modo ensaio: registra o que faria. Quando o robô ficar pronto, nada fora dele muda.

Tarefa: implemente três coisas.
1. EmissorTotvs.__init__(ensaio=True): se ensaio for False, levante
   EmissaoIndisponivel (o modo real ainda não existe). Senão, guarde
   self.ensaio = True e self.registro = [] (lista vazia).
2. EmissorTotvs.emitir(item): acrescente ao registro o texto
   "emitiria certificado: OP <op> | NF <nf> | <peso com 2 casas> kg | <especificacao>"
   e devolva o comprovante "ENSAIO-<op>-<nf>".
3. emitir_fila(fila, emissor, ja_emitidas=None) devolve uma lista NOVA de ItemFila,
   um para cada item da fila, na mesma ordem:
   - item com situacao diferente de "emitir": volta como está;
   - (op, nf) em ja_emitidas, ou já emitido antes NESTA mesma fila: situacao
     "ignorado" e motivo "certificado já emitido para esta OP/NF" acrescentado
     (o emissor NÃO é chamado);
   - emissor.emitir(item) deu certo: situacao "ensaio" se emissor.ensaio, senão
     "emitido"; comprovante = o que emitir devolveu;
   - emissor.emitir levantou ErroEmissao: situacao "falha" e motivo
     "falha na emissão: <mensagem do erro>" acrescentado; a série CONTINUA;
   - qualquer outra exceção é bug: deixe subir.
   Não altere os itens recebidos nem o conjunto ja_emitidas (trabalhe com cópias).

Exemplos:
    >>> emissor = EmissorTotvs()
    >>> resultado = emitir_fila([item_24518], emissor)
    >>> resultado[0].situacao, resultado[0].comprovante
    ('ensaio', 'ENSAIO-24518-123456')
    >>> emissor.registro
    ['emitiria certificado: OP 24518 | NF 123456 | 1250.50 kg | PADRAO-A']

Dica: dataclasses.replace(item, situacao="falha", motivos=novos) cria uma CÓPIA do
item com esses campos trocados. set(ja_emitidas or ()) cria um conjunto novo (vazio
quando ja_emitidas for None).

Teste com:  python curso.py testar 14 ex12
"""

import logging
from dataclasses import (
    dataclass,
    field,
    replace,  # noqa: F401 (você vai usar)
)

logger = logging.getLogger(__name__)

# ============================================================================
# PEÇAS PRONTAS (etapas anteriores) — não precisa mexer
# ============================================================================


@dataclass
class ItemFila:
    op: str
    nf: str
    peso_kg: float
    situacao: str  # "emitir", "bloqueado", "ensaio", "emitido", "falha", "ignorado"
    especificacao: str = ""
    motivos: list[str] = field(default_factory=list)
    comprovante: str = ""


class ErroEmissao(Exception):
    """Falha esperada ao emitir UM certificado (tela não abriu, campo recusou...)."""


class EmissaoIndisponivel(Exception):
    """O modo real de emissão ainda não está disponível."""


class Emissor:
    """Interface: todo emissor tem `ensaio` e `emitir(item) -> comprovante`."""

    ensaio: bool = False

    def emitir(self, item: ItemFila) -> str:
        raise NotImplementedError


# ============================================================================
# SUA PARTE
# ============================================================================


class EmissorTotvs(Emissor):
    """Emissor do TOTVS. Por enquanto só o modo ensaio: registra o que faria."""

    def __init__(self, ensaio: bool = True) -> None:
        """Só aceita ensaio=True por enquanto."""
        # Escreva seu código aqui
        raise NotImplementedError("Implemente esta função")

    def emitir(self, item: ItemFila) -> str:
        """Registra o que faria e devolve um comprovante de ensaio."""
        # Escreva seu código aqui
        raise NotImplementedError("Implemente esta função")


def emitir_fila(
    fila: list[ItemFila],
    emissor: Emissor,
    ja_emitidas: set[tuple[str, str]] | None = None,
) -> list[ItemFila]:
    """Emite cada item e devolve novos itens com a situação final."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
