"""
Exercício 08.13 — Revisão: a fila de emissão de certificados
Nível: ★★★

Revisão de: módulo 05 (regex e número brasileiro), módulo 06 (exceção
personalizada) e módulo 03 (listas e conjuntos), junto com os métodos especiais
__len__, __iter__ e __contains__ deste módulo.

Contexto: Os e-mails da expedição viram pedidos (OP, NF, peso). Eles entram numa
FILA: o robô emite um certificado por vez, na ordem de chegada. A mesma linha de
e-mail às vezes chega duas vezes (alguém respondeu "para todos"), e o pedido
repetido não pode entrar de novo.

Já estão prontos: `PedidoExpedicao` (dataclass imutável) e `FilaVaziaError`.
Tarefa: complete a classe `FilaDeEmissao`.
1. `__init__()`: fila vazia.
2. `adicionar(pedido)`: põe no fim. Pedido repetido (mesma OP e mesma NF) ->
   ValueError.
3. `adicionar_do_email(texto)`: lê as linhas no formato
   "OP 245101 - NF 123456 - Peso: 1.250,5 kg" (sem diferenciar maiúsculas,
   espaços variados; OP vira "OP245101"; peso em formato brasileiro), adiciona os
   pedidos que ainda não estão na fila (ignora os repetidos, sem erro) e devolve
   QUANTOS entraram.
4. `proximo()`: tira e devolve o PRIMEIRO pedido (quem chegou antes sai antes).
   Fila vazia -> FilaVaziaError.
5. `len(fila)` (__len__): quantos pedidos esperam.
6. `for pedido in fila` (__iter__): percorre na ordem, SEM tirar da fila.
7. `"123456" in fila` (__contains__): True se algum pedido tem essa NF.
8. `peso_total` (property): soma dos pesos, round(..., 2).
9. `__repr__`: "FilaDeEmissao(2 pedidos, 2230.50 kg)".

Exemplo:
    >>> fila = FilaDeEmissao()
    >>> fila.adicionar_do_email("OP 245101 - NF 123456 - Peso: 1.250,5 kg")
    1
    >>> len(fila), "123456" in fila
    (1, True)
    >>> fila.proximo()
    PedidoExpedicao(op='OP245101', nf='123456', peso_kg=1250.5)

Dica: __iter__ pode simplesmente devolver iter(uma_lista). O padrão do item é o
mesmo do exercício 07.12.

Teste com:  python curso.py testar 08 ex13
"""

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class PedidoExpedicao:
    """Um item do e-mail da expedição (pronto)."""

    op: str
    nf: str
    peso_kg: float


class FilaVaziaError(Exception):
    """Pediram o próximo pedido de uma fila vazia (pronta)."""


class FilaDeEmissao:
    """Fila (primeiro a entrar, primeiro a sair) de pedidos para certificar."""

    def __init__(self) -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def adicionar(self, pedido: PedidoExpedicao) -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def adicionar_do_email(self, texto: str) -> int:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def proximo(self) -> PedidoExpedicao:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def __len__(self) -> int:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def __iter__(self) -> Iterator[PedidoExpedicao]:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def __contains__(self, nf: object) -> bool:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    @property
    def peso_total(self) -> float:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def __repr__(self) -> str:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")
