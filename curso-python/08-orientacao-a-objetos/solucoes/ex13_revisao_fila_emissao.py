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

import re
from collections.abc import Iterator
from dataclasses import dataclass

PADRAO_ITEM = re.compile(
    r"OP\s*(\d+)\s*-\s*NF\s*(\d+)\s*-\s*Peso\s*:?\s*([\d.,]+)\s*kg", re.IGNORECASE
)


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
        self._pedidos: list[PedidoExpedicao] = []

    def adicionar(self, pedido: PedidoExpedicao) -> None:
        # Pedido é dataclass: "in" usa o __eq__ gerado (mesma op, nf e peso).
        # Aqui a regra é só OP + NF, então comparamos esses dois campos.
        if any(p.op == pedido.op and p.nf == pedido.nf for p in self._pedidos):
            raise ValueError(f"Pedido repetido: {pedido.op} / NF {pedido.nf}")
        self._pedidos.append(pedido)

    def adicionar_do_email(self, texto: str) -> int:
        adicionados = 0
        for op, nf, peso in PADRAO_ITEM.findall(texto):
            pedido = PedidoExpedicao(
                f"OP{op}", nf, float(peso.replace(".", "").replace(",", "."))
            )
            try:
                self.adicionar(pedido)  # reaproveita a regra de repetição
            except ValueError:
                continue  # repetido: ignora em silêncio, como pede o enunciado
            adicionados += 1
        return adicionados

    def proximo(self) -> PedidoExpedicao:
        if not self._pedidos:
            raise FilaVaziaError("Não há pedidos na fila")
        return self._pedidos.pop(0)  # pop(0) tira o primeiro (FIFO)

    def __len__(self) -> int:
        return len(self._pedidos)

    def __iter__(self) -> Iterator[PedidoExpedicao]:
        # Um iterador sobre uma CÓPIA: quem percorre não altera a fila.
        return iter(list(self._pedidos))

    def __contains__(self, nf: object) -> bool:
        return any(p.nf == nf for p in self._pedidos)

    @property
    def peso_total(self) -> float:
        return round(sum(p.peso_kg for p in self._pedidos), 2)

    def __repr__(self) -> str:
        return f"FilaDeEmissao({len(self)} pedidos, {self.peso_total:.2f} kg)"
