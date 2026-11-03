# Quiz do Módulo 08 — Orientação a objetos

Responda antes de olhar o gabarito. Nas perguntas "o que imprime", preveja primeiro e
só depois rode para conferir.

## Perguntas

**1.** Em `amostra.esta_entre(22.5, 27.5)`, o que o parâmetro `self` de `esta_entre`
recebe?

a) A classe `Amostra`.
b) O objeto `amostra`.
c) O número `22.5`.
d) Nada: `self` é só um enfeite.

**2.** O que imprime?

```python
class Bobina:
    def __init__(self, lote):
        self.lote = lote

    def __repr__(self):
        return f"Bobina({self.lote!r})"


b = Bobina("L01")
print(b)
print([b])
```

**3.** Onde está o erro? Depois de rodar, o lote L02 aparece com o peso do L01.

```python
class Lote:
    bobinas = []

    def __init__(self, codigo):
        self.codigo = codigo

    def adicionar(self, peso_kg):
        self.bobinas.append(peso_kg)
```

**4.** O que imprime?

```python
class Amostra:
    def __init__(self, valor):
        self.valor = valor

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, novo):
        self._valor = max(novo, 0)


print(Amostra(-5).valor)
```

**5.** Qual decorador cria um método que recebe a **classe** como primeiro argumento
(em geral chamado `cls`) e é muito usado para construtores alternativos, como
`Tolerancia.por_nominal(25, 10)`?

a) `@staticmethod`
b) `@property`
c) `@classmethod`
d) `@dataclass`

**6.** Onde está o erro? `EnsaioMinimo("tração", 18, 20).laudo()` dá
`AttributeError: 'EnsaioMinimo' object has no attribute 'nome'`.

```python
class Ensaio:
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor

    def laudo(self):
        return f"{self.nome}: {self.valor}"


class EnsaioMinimo(Ensaio):
    def __init__(self, nome, valor, minimo):
        self.minimo = minimo
```

**7.** Uma linha de produção usa uma especificação padrão e pode ter especificações
próprias por OP. Qual modelagem é a mais adequada?

a) `class LinhaDeProducao(Especificacao)` (herança)
b) `class Especificacao(LinhaDeProducao)` (herança)
c) `LinhaDeProducao` guarda objetos `Especificacao` em atributos (composição)
d) Uma única classe gigante com todos os campos das duas

**8.** O que imprime?

```python
from dataclasses import dataclass


@dataclass
class Pedido:
    op: str
    nf: str


p1 = Pedido("OP1", "100")
p2 = Pedido("OP1", "100")
print(p1 == p2, p1 is p2)
```

**9.** Onde está o erro? O programa quebra antes de criar qualquer lote.

```python
from dataclasses import dataclass


@dataclass
class Lote:
    codigo: str
    bobinas: list = []
```

**10.** O que imprime?

```python
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Medicao:
    linha: str
    valor: float


print(sorted([Medicao("B", 1.0), Medicao("A", 9.0), Medicao("A", 2.0)])[0])
```

**11.** O que imprime?

```python
from enum import Enum


class Situacao(Enum):
    LIBERADO = "liberado"
    REPROVADO = "reprovado"


print(Situacao("reprovado").name, Situacao.LIBERADO.value)
```

**12.** O que acontece na última linha?

```python
class OrdemProducao:
    def __init__(self, numero):
        self.numero = numero

    def __eq__(self, outro):
        return isinstance(outro, OrdemProducao) and self.numero == outro.numero


ops = {OrdemProducao("245101")}
```

**13.** Em qual destes casos uma **função** resolve melhor que uma classe?

a) Pedidos da expedição (OP, NF, peso, cliente) que passam por várias etapas do sistema.
b) Calcular o CV% de uma lista de valores.
c) Uma fila de emissão que guarda pedidos e muda ao longo do dia.
d) Vários tipos de ensaio com regras de aprovação diferentes.

---

## Gabarito

**1. b.** O Python transforma `amostra.esta_entre(22.5, 27.5)` em
`Amostra.esta_entre(amostra, 22.5, 27.5)`: `self` é o próprio objeto.

**2.**

```text
Bobina('L01')
[Bobina('L01')]
```

Sem `__str__`, o `print` usa o `__repr__`; e dentro de listas o Python sempre usa o
`__repr__` de cada item.

**3.** `bobinas = []` no corpo da classe é um atributo **de classe**: uma lista só,
compartilhada por todos os lotes. Crie a lista no `__init__`: `self.bobinas = []`.

**4.** `0`. O `self.valor = valor` do `__init__` passa pelo setter, que troca valores
negativos por 0. É por isso que vale atribuir pela property (e não por `self._valor`)
dentro do `__init__`: a regra vale desde o nascimento do objeto.

**5. c.** `@classmethod` recebe a classe (`cls`) e costuma devolver `cls(...)`.
`@staticmethod` não recebe nem objeto nem classe. `@property` transforma método em
"atributo". `@dataclass` decora a classe inteira.

**6.** O `__init__` da filha substitui o da mãe e não chama `super().__init__(nome,
valor)`. Então `self.nome` e `self.valor` nunca são criados. Correção: primeira linha
do `__init__` da filha: `super().__init__(nome, valor)`.

**7. c.** A linha **tem** especificações; ela não **é** uma especificação. Relação
"tem um" pede composição. Herança (a e b) inverteria o sentido do modelo e não permite
várias especificações por linha.

**8.** `True False`. A dataclass gera um `__eq__` que compara os campos: os pedidos são
**iguais**. Mas são dois objetos diferentes na memória, então `is` dá `False`.

**9.** Padrão mutável num campo de dataclass: `ValueError: mutable default <class 'list'>
for field bobinas is not allowed: use default_factory`. Correção:
`bobinas: list = field(default_factory=list)` (importando `field` de `dataclasses`).

**10.** `Medicao(linha='A', valor=2.0)`. Com `order=True`, a comparação segue a ordem
dos campos: primeiro `linha` ("A" antes de "B"), e no empate, `valor` (2.0 antes de 9.0).

**11.** `REPROVADO liberado`. `Situacao("reprovado")` procura pelo valor e devolve o
membro `REPROVADO`; `.name` é o nome do membro e `.value` é o valor.

**12.** `TypeError: unhashable type: 'OrdemProducao'`. Ao definir `__eq__`, a classe
perde o `__hash__` padrão e não pode mais ir para um `set` nem virar chave de `dict`.
Defina `def __hash__(self): return hash(self.numero)`.

**13. b.** Calcular o CV não guarda estado nem tem variações: é uma função com
parâmetros. Os pedidos (a) viajam juntos pelo sistema (dataclass), a fila (c) tem
estado que muda, e os tipos de ensaio (d) são variações de um mesmo conceito.
