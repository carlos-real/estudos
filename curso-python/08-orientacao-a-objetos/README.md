# Módulo 08 — Orientação a objetos

> **Tempo estimado:** 10 a 14 horas · **Pré-requisitos:** módulos 00 a 07 · **Nível:** intermediário

## O que você vai aprender

- Criar uma classe com `__init__`, atributos e métodos, e explicar o que é `self`.
- Diferenciar atributo de instância de atributo de classe (e evitar a armadilha da
  lista compartilhada).
- Escrever `__str__` e `__repr__` para objetos legíveis no `print` e no REPL.
- Proteger dados com a convenção `_` e com `@property` que valida.
- Criar construtores alternativos com `@classmethod` e utilitários com `@staticmethod`.
- Reaproveitar código com herança e `super()`, e tratar objetos diferentes do mesmo
  jeito (polimorfismo).
- Escolher entre herança ("é um") e composição ("tem um").
- Escrever classes de dados com `@dataclass` (`field`, `frozen`, `order`,
  `__post_init__`).
- Definir igualdade (`__eq__` e `__hash__`) e conjuntos fechados de valores com `Enum`.
- Reconhecer quando uma função ou um dicionário resolvem melhor que uma classe.

## Por que isso importa

O seu sistema fala de **amostras, tolerâncias, especificações, linhas de produção,
pedidos e certificados**. Até aqui, cada uma dessas coisas era um dicionário solto e
um punhado de funções espalhadas. Funciona até o dia em que alguém escreve
`amostra["valro"]`, ou passa a tolerância da linha B para a OP da linha C.

Orientação a objetos é um jeito de organizar o código **em torno das coisas do
problema**: cada coisa vira um tipo (uma classe) que guarda os seus dados e sabe fazer
o que lhe cabe. Uma `Tolerancia` sabe dizer se aprova um valor; uma `LinhaDeProducao`
sabe qual especificação vale para cada OP; um `Certificado` sabe se pode ser emitido.

No mercado, OO está em toda parte: o `DataFrame` do pandas, o `Path` do `pathlib`, as
respostas do `requests` e os modelos do FastAPI (módulo 13) são objetos. Entender
classes é entender as bibliotecas que você usa. E saber **quando não usar** classe é o
que separa quem aprendeu OO de quem decorou OO.

## 1. O problema: dados soltos

Lembra do aviso sobre dicionários? Rode `python exemplos/01_dict_vs_classe.py`:

```python
amostra = {"codigo": "AM-001", "ensaio": "espessura", "valor": 25.3}
amostra["valro"] = 25.1  # erro de digitação: cria uma chave NOVA, em silêncio
print("Valor usado no laudo:", amostra["valor"])
```

Saída:

```text
Valor usado no laudo: 25.3
```

A correção se perdeu e ninguém foi avisado. Com dicionários, nada garante que toda
amostra tem as mesmas chaves, nada impede valor negativo, e as funções que trabalham
com amostras ficam espalhadas pelo código.

Uma **classe** resolve as três coisas: define quais dados uma amostra tem, pode validar
esses dados e junta as funções que operam sobre eles (os **métodos**). Pense na ficha
de amostra do laboratório: a **ficha em branco** (com os campos impressos) é a classe;
cada **ficha preenchida** é um objeto.

## 2. Classes e objetos

```python
class Amostra:
    def __init__(self, codigo, ensaio, valor):
        self.codigo = codigo
        self.ensaio = ensaio
        self.valor = valor

    def esta_entre(self, minimo, maximo):
        return minimo <= self.valor <= maximo


a = Amostra("AM-001", "espessura", 25.3)
b = Amostra("AM-002", "espessura", 28.1)
print(a.codigo, a.valor, a.esta_entre(22.5, 27.5))
print(b.codigo, b.valor, b.esta_entre(22.5, 27.5))
print(type(a).__name__, isinstance(a, Amostra))
try:
    print(a.valro)
except AttributeError as erro:
    print("Erro:", erro)
```

Saída:

```text
AM-001 25.3 True
AM-002 28.1 False
Amostra True
Erro: 'Amostra' object has no attribute 'valro'
```

O erro de digitação agora **aparece na hora** (sem o `try`, o traceback ainda sugere
`Did you mean: 'valor'?`).

Vocabulário (vale para qualquer linguagem):

| Termo | O que é | No exemplo |
|---|---|---|
| **classe** | o molde, o tipo | `Amostra` |
| **objeto** ou **instância** | uma coisa criada a partir do molde | `a`, `b` |
| **atributo** | um dado guardado no objeto | `a.codigo`, `a.valor` |
| **método** | uma função que pertence à classe | `a.esta_entre(...)` |
| **instanciar** | criar um objeto chamando a classe | `Amostra("AM-001", ...)` |

Por convenção, nomes de classe usam **PascalCase** (`LinhaDeProducao`), e o resto
continua em `snake_case`. Você já usa objetos desde o módulo 01: `"texto".upper()` é o
método `upper` de um objeto do tipo `str`; `Path("dados").exists()`, idem.

> 💡 **Dica:** você já escreveu uma classe no módulo 06: `class ErroDeQualidade(Exception):`.
> Aquilo era uma classe que **herda** de `Exception`. A seção 9 explica o que isso quer
> dizer.

## 3. `__init__` e `self`

`__init__` é o método que o Python chama **logo depois de criar** o objeto, para
prepará-lo. É ali que você guarda os dados iniciais. Os dois sublinhados de cada lado
indicam um **método especial** ("dunder", de *double underscore*): você não o chama
diretamente; o Python chama na hora certa.

E o `self`? É o **próprio objeto** sobre o qual o método está trabalhando. Quando você
escreve `a.esta_entre(22.5, 27.5)`, o Python faz, por trás:

```python
Amostra.esta_entre(a, 22.5, 27.5)
```

Ou seja: `self` recebe `a`. Por isso todo método começa com `self`, e é por `self` que
o método enxerga os atributos (`self.valor`). O nome `self` é convenção, não palavra
reservada, mas **sempre** use `self`.

> 🔮 **Preveja antes de rodar:** o que acontece?
>
> ```python
> class Bobina:
>     def __init__(self, lote, peso_kg):
>         self.lote = lote
>         self.peso_kg = peso_kg
>
>     def resumo():
>         return f"{self.lote}: {self.peso_kg} kg"
>
>
> print(Bobina("L01", 150.0).resumo())
> ```

<details><summary>Resposta</summary>

Dá erro: `TypeError: Bobina.resumo() takes 0 positional arguments but 1 was given`.
O Python passou o objeto como primeiro argumento (o `self`), mas o método não tinha
nenhum parâmetro para recebê-lo. É o erro mais comum de quem está começando com
classes. Correção: `def resumo(self):`.

</details>

Um `__init__` bem escrito **normaliza e valida** os dados na entrada. Assim, todo
objeto que existe já está correto:

```python
class Amostra:
    def __init__(self, codigo: str, ensaio: str, valor: float, unidade: str = "") -> None:
        self.codigo = codigo.strip().upper()
        self.ensaio = ensaio.strip().lower()
        self.valor = float(valor)
        self.unidade = unidade


a = Amostra(" am-001 ", "Espessura", 25, "µm")
print(a.codigo, a.ensaio, a.valor, a.unidade)
```

Saída:

```text
AM-001 espessura 25.0 µm
```

Os parâmetros com padrão (`unidade=""`), as anotações de tipo e as docstrings
funcionam exatamente como nas funções do módulo 04. O `__init__` devolve sempre `None`
(por isso o `-> None`): quem "devolve" o objeto é a chamada `Amostra(...)`.

## 4. Métodos e atributos de classe

Métodos podem chamar outros métodos do mesmo objeto, sempre pelo `self`:

```python
class Amostra:
    def __init__(self, codigo, valor, unidade=""):
        self.codigo = codigo
        self.valor = valor
        self.unidade = unidade

    def esta_entre(self, minimo, maximo):
        return minimo <= self.valor <= maximo

    def situacao(self, minimo, maximo):
        return "aprovada" if self.esta_entre(minimo, maximo) else "reprovada"


print(Amostra("AM-001", 25.3).situacao(22.5, 27.5))
```

Saída:

```text
aprovada
```

Até aqui, todo atributo foi criado com `self.algo = ...` dentro de um método: é um
**atributo de instância**, um por objeto. Um nome criado **no corpo da classe**, fora
dos métodos, é um **atributo de classe**: existe **um só**, compartilhado por todos os
objetos. Serve para constantes do tipo:

```python
>>> class Amostra:
...     laboratorio = "CQ Embalagens"
...     def __init__(self, codigo):
...         self.codigo = codigo
...
>>> a, b = Amostra("AM-001"), Amostra("AM-002")
>>> a.laboratorio, b.laboratorio, Amostra.laboratorio
('CQ Embalagens', 'CQ Embalagens', 'CQ Embalagens')
```

> 🔮 **Preveja antes de rodar:** quanto vale cada contador?
>
> ```python
> class Laudo:
>     emitidos = 0
>
>     def __init__(self):
>         self.emitidos += 1
>
>
> a = Laudo()
> b = Laudo()
> print(a.emitidos, b.emitidos, Laudo.emitidos)
> ```

<details><summary>Resposta</summary>

`1 1 0`. O `self.emitidos += 1` é `self.emitidos = self.emitidos + 1`: a **leitura**
encontra o atributo da classe (0), mas a **atribuição** cria um atributo **novo** no
objeto. Cada laudo ganhou o seu `emitidos = 1`, e o da classe continuou 0. Para
contar na classe, escreva `Laudo.emitidos += 1`.

</details>

> ⚠️ **Erro comum:** colocar uma lista no corpo da classe (`bobinas = []`) achando que
> cada objeto terá a sua. Ela é **uma só**: `self.bobinas.append(...)` não atribui, só
> altera a lista compartilhada, e todos os objetos enxergam a mudança. Lista, dicionário
> e conjunto de cada objeto nascem **no `__init__`**: `self.bobinas = []`. O exercício
> 09 é exatamente esse bug.

## 5. `__str__` e `__repr__`

Imprima um objeto sem esses métodos e você verá algo como
`<__main__.Amostra object at 0x7f3a2c1b9e50>`: o tipo e o endereço na memória. Inútil.
Dois métodos especiais resolvem:

- `__str__`: texto **para pessoas**. Usado por `print()`, `str()` e f-strings.
- `__repr__`: texto **para programadores**. Usado no REPL, dentro de listas, no
  `!r` das f-strings e em logs. Regra de ouro: parecer o código que recria o objeto.

```python
class Bobina:
    def __init__(self, lote, numero, peso_kg):
        self.lote = lote
        self.numero = numero
        self.peso_kg = peso_kg

    def __str__(self):
        return f"Bobina {self.lote}-{self.numero:03d} ({self.peso_kg:.1f} kg)"

    def __repr__(self):
        return f"Bobina(lote={self.lote!r}, numero={self.numero!r}, peso_kg={self.peso_kg!r})"


b = Bobina("L2610", 7, 152.4)
print(b)
print(f"Separada: {b}")
print([b])
print(repr(b))
```

Saída:

```text
Bobina L2610-007 (152.4 kg)
Separada: Bobina L2610-007 (152.4 kg)
[Bobina(lote='L2610', numero=7, peso_kg=152.4)]
Bobina(lote='L2610', numero=7, peso_kg=152.4)
```

Repare no `[b]`: dentro de uma lista o Python usa o `__repr__` de cada item. Se você
só puder escrever um dos dois, escreva o `__repr__`: sem `__str__`, o `print` usa o
`__repr__`.

> 🔧 **Modifique:** apague o `__str__` da `Bobina` e rode de novo. O `print(b)` passa a
> mostrar o texto do `__repr__`. Depois apague também o `__repr__` e veja o
> `<__main__.Bobina object at 0x...>` voltar.

## 6. Encapsulamento: o que é de dentro e o que é de fora

Encapsular é esconder os detalhes internos e oferecer um jeito seguro de usar o objeto.
O Python não tem "privado" de verdade; ele usa **convenções**:

| Nome | Significa | Exemplo |
|---|---|---|
| `valor` | público: use à vontade | `amostra.valor` |
| `_valor` | interno: "não mexa de fora, pode mudar sem aviso" | `amostra._historico` |
| `__valor` | interno com nome embaralhado (*name mangling*) | raro; evite |

Com `__valor`, o Python renomeia o atributo para `_Amostra__valor`, para evitar
conflito em heranças. Não é segurança, e quase nunca é necessário: no dia a dia, um
sublinhado basta. O lema da comunidade é "somos todos adultos": o `_` avisa, e quem
mexe assume o risco.

## 7. `@property`: atributo com validação

Problema real: alguém digitou `-25` na espessura. Você quer que **toda** atribuição a
`amostra.valor` seja validada, sem obrigar quem usa a trocar `a.valor = 30` por
`a.definir_valor(30)`. A `@property` faz um método se parecer com um atributo:

```python
class Amostra:
    def __init__(self, codigo, valor):
        self._codigo = codigo.upper()
        self.valor = valor  # já passa pelo setter: validação desde o início

    @property
    def codigo(self):  # só getter: atributo somente leitura
        return self._codigo

    @property
    def valor(self):  # getter: roda em "a.valor"
        return self._valor

    @valor.setter
    def valor(self, novo):  # setter: roda em "a.valor = ..."
        if novo < 0:
            raise ValueError(f"Valor não pode ser negativo: {novo}")
        self._valor = float(novo)


a = Amostra("am-001", 25.4)
a.valor = 30
print(a.codigo, a.valor)
try:
    a.valor = -5
except ValueError as erro:
    print("ValueError:", erro)
try:
    a.codigo = "X"
except AttributeError as erro:
    print("AttributeError:", erro)
```

Saída:

```text
AM-001 30.0
ValueError: Valor não pode ser negativo: -5
AttributeError: property 'codigo' of 'Amostra' object has no setter
```

Os pontos-chave:

- O dado de verdade mora em `self._valor` (com `_`); a property `valor` é a porta de
  entrada. Se a property e o atributo tivessem o mesmo nome, o setter chamaria a si
  mesmo para sempre (`RecursionError`).
- No `__init__`, `self.valor = valor` (sem `_`) passa pelo setter: nenhum objeto nasce
  inválido.
- Property **sem setter** é somente leitura. (No Python 3.10, a mensagem é só
  `can't set attribute`.)
- Property também serve para valores **calculados**, sem guardar nada:
  `@property def em_mils(self): return self._valor / 25.4`.

### Exemplo resolvido: peso líquido da bobina

**Problema:** a balança pesa a bobina **com** o tubete. O certificado precisa do peso
líquido. O peso bruto não pode ser menor que o tubete, e ninguém deve conseguir
"setar" o líquido na mão.

**Como eu pensei:** o bruto é um dado que pode ser corrigido (precisa de setter com
validação). O tubete é fixo por bobina. O líquido **não é um dado**: é uma conta sobre
os outros dois, então é uma property só com getter. Assim ele nunca fica
desatualizado.

```python
class Bobina:
    def __init__(self, lote, peso_bruto_kg, tubete_kg=2.5):
        self.lote = lote
        self.tubete_kg = tubete_kg
        self.peso_bruto_kg = peso_bruto_kg

    @property
    def peso_bruto_kg(self):
        return self._peso_bruto_kg

    @peso_bruto_kg.setter
    def peso_bruto_kg(self, novo):
        if novo <= self.tubete_kg:
            raise ValueError(f"Peso bruto {novo} kg não passa do tubete ({self.tubete_kg} kg)")
        self._peso_bruto_kg = float(novo)

    @property
    def peso_liquido_kg(self):
        return round(self._peso_bruto_kg - self.tubete_kg, 2)


b = Bobina("L2610", 154.9)
print(b.peso_liquido_kg)
b.peso_bruto_kg = 160.0
print(b.peso_liquido_kg)
```

Saída:

```text
152.4
157.5
```

Repare na ordem do `__init__`: `tubete_kg` é guardado **antes** do peso bruto, porque o
setter do bruto usa o tubete.

> 🔧 **Modifique:** tente `b.peso_liquido_kg = 100`. Leia o erro: ele diz que a
> property não tem setter. É exatamente o que queríamos.

## 8. `@classmethod` e `@staticmethod`

Tolerâncias chegam de jeitos diferentes: "0,10 a 0,30", "25 ± 10%", números do banco.
Um `__init__` cheio de "se o formato for X" fica confuso. A saída são **construtores
alternativos**, com `@classmethod`:

- um método comum recebe o **objeto** (`self`);
- um `@classmethod` recebe a **classe** (`cls`) e costuma devolver um objeto novo;
- um `@staticmethod` não recebe nem um nem outro: é uma função comum que mora dentro da
  classe porque tem a ver com ela.

```python
class Tolerancia:
    def __init__(self, minimo, maximo):
        self.minimo = minimo
        self.maximo = maximo

    @classmethod
    def por_nominal(cls, nominal, percentual):
        margem = nominal * percentual / 100
        return cls(nominal - margem, nominal + margem)

    @classmethod
    def de_texto(cls, texto):  # "0,10 a 0,30"
        minimo, maximo = texto.split(" a ")
        return cls(cls.numero_br(minimo), cls.numero_br(maximo))

    @staticmethod
    def numero_br(texto):
        return float(texto.strip().replace(".", "").replace(",", "."))

    def __repr__(self):
        return f"Tolerancia({self.minimo!r}, {self.maximo!r})"


print(Tolerancia(0.10, 0.30))
print(Tolerancia.por_nominal(25, 10))
print(Tolerancia.de_texto("0,10 a 0,30"))
print(Tolerancia.numero_br("1.250,5"))
```

Saída:

```text
Tolerancia(0.1, 0.3)
Tolerancia(22.5, 27.5)
Tolerancia(0.1, 0.3)
1250.5
```

Por que `cls(...)` e não `Tolerancia(...)`? Porque, se alguém criar
`class ToleranciaEspessura(Tolerancia)`, o `ToleranciaEspessura.por_nominal(...)`
devolve um objeto da **subclasse**. Você já usou classmethods sem saber:
`date.today()`, `datetime.strptime(...)` e `dict.fromkeys(...)` são construtores
alternativos.

> 💡 **Dica:** está em dúvida se um método deve ser `@staticmethod`? Se ele não usa
> `self` nem `cls`, provavelmente sim. Se ele também não tem nada a ver com a classe,
> provavelmente deveria ser uma função comum, fora dela.

## 9. Herança e `super()`

Espessura, tração e COF são todos **ensaios**: têm nome, valor e unidade e geram uma
linha de laudo. Só a regra de aprovação muda. **Herança** permite escrever o que é
comum uma vez (na classe-mãe) e só a diferença nas classes-filhas:

```python
class Ensaio:
    def __init__(self, nome, valor, unidade=""):
        self.nome = nome
        self.valor = valor
        self.unidade = unidade

    def aprovado(self):
        raise NotImplementedError("Cada tipo de ensaio define a sua regra")

    def laudo(self):
        situacao = "APROVADO" if self.aprovado() else "REPROVADO"
        return f"{self.nome}: {self.valor} {self.unidade} -> {situacao}"


class EnsaioMinimo(Ensaio):  # "EnsaioMinimo É UM Ensaio"
    def __init__(self, nome, valor, minimo, unidade=""):
        super().__init__(nome, valor, unidade)  # a mãe cuida do que é comum
        self.minimo = minimo  # a filha guarda só o que é dela

    def aprovado(self):  # sobrescreve (override) o método da mãe
        return self.valor >= self.minimo


tracao = EnsaioMinimo("tração", 18.0, 20.0, "MPa")
print(tracao.laudo())
print(isinstance(tracao, EnsaioMinimo), isinstance(tracao, Ensaio))
print([classe.__name__ for classe in EnsaioMinimo.__mro__])
```

Saída:

```text
tração: 18.0 MPa -> REPROVADO
True True
['EnsaioMinimo', 'Ensaio', 'object']
```

- `class EnsaioMinimo(Ensaio)`: a filha **herda** todos os métodos da mãe (`laudo`
  veio de graça).
- `super().__init__(...)` chama o `__init__` da mãe. Sem ele, `self.nome` nunca seria
  criado: a filha que define `__init__` **substitui** o da mãe.
- **Sobrescrever** (*override*): a filha define um método com o mesmo nome; o dela vale.
- O `__mro__` (*method resolution order*) é a ordem em que o Python procura um método:
  primeiro na filha, depois na mãe, por fim em `object`, a mãe de todas as classes.

> ⚠️ **Erro comum:** esquecer o `super().__init__(...)` na filha. Nada reclama na
> criação; o erro aparece depois, longe dali: `AttributeError: 'EnsaioMinimo' object
> has no attribute 'nome'`.

**Classe abstrata.** Faz sentido criar um `Ensaio("x", 1)` genérico? Não. O módulo
`abc` deixa isso explícito:

```python
from abc import ABC, abstractmethod

class Ensaio(ABC):
    @abstractmethod
    def aprovado(self) -> bool:
        """Toda filha é obrigada a implementar."""
```

Tentar criar um `Ensaio` dá `TypeError: Can't instantiate abstract class Ensaio
without an implementation for abstract method 'aprovado'` (a frase muda um pouco entre
versões). Veja `exemplos/05_heranca_polimorfismo.py`.

## 10. Polimorfismo e "duck typing"

Polimorfismo ("muitas formas") é tratar objetos de tipos diferentes **pela mesma
interface**. O método `laudo()` da mãe chama `self.aprovado()`, e cada objeto responde
com a sua própria regra. Quem usa não precisa de `if tipo == ...`:

```python
class EnsaioFaixa:
    def __init__(self, nome, valor, minimo, maximo):
        self.nome, self.valor, self.minimo, self.maximo = nome, valor, minimo, maximo

    def aprovado(self):
        return self.minimo <= self.valor <= self.maximo


class EnsaioMaximo:
    def __init__(self, nome, valor, maximo):
        self.nome, self.valor, self.maximo = nome, valor, maximo

    def aprovado(self):
        return self.valor <= self.maximo


ensaios = [EnsaioFaixa("espessura", 28.0, 22.5, 27.5), EnsaioMaximo("cof", 0.22, 0.30)]
print([e.nome for e in ensaios if not e.aprovado()])
```

Saída:

```text
['espessura']
```

Repare: essas duas classes **nem herdam** de uma mãe comum, e funciona. O Python não
pergunta o tipo; ele só chama `.aprovado()`. É o **duck typing**: "se anda como pato e
grasna como pato, é pato". Você já viu isso: `len()` funciona com lista, texto e
dicionário, e `for` funciona com qualquer coisa que se deixe percorrer. A herança
ajuda a **garantir** a interface (com `ABC`) e a **reaproveitar** código; o
polimorfismo em si vem do duck typing.

> 🔧 **Modifique:** crie `class EnsaioMinimo` com `aprovado()` próprio (valor >=
> mínimo) e acrescente um objeto dela na lista `ensaios`. A última linha não muda nada
> e continua funcionando.

## 11. Composição: "tem um" em vez de "é um"

Herança é para "**é um**": um `EnsaioMinimo` **é um** `Ensaio`. Muita coisa do mundo
real é "**tem um**": uma linha de produção **tem** uma especificação padrão; um
certificado **tem** resultados de ensaio. Isso é **composição**: um objeto guarda
outros objetos como atributos e **delega** o trabalho a eles.

```text
LinhaDeProducao "B"
├── fixas: {"cof": Tolerancia(0.10, 0.30)}              (tem tolerâncias fixas)
├── padrao: Especificacao "Filme PE 25 µm"              (tem uma especificação padrão)
│           └── tolerancias: {"espessura": Tolerancia(22.5, 27.5)}
└── por OP: {"OP245110": Especificacao "Café Montanha"} (tem especificações próprias)
```

### Exemplo resolvido: a regra da especificação por OP

**Problema:** cada linha tem tolerâncias fixas e uma especificação padrão. Se a OP tem
especificação própria, ela vale no lugar da padrão. Preciso saber, para uma OP,
quais tolerâncias aplicar.

**Como eu pensei:**

1. Primeira tentação: `class LinhaDeProducao(Especificacao)`. Mas a frase "uma linha
   **é uma** especificação" é falsa, e uma linha precisa de **várias** especificações
   (a padrão e as das OPs). Herança não serve.
2. Então a linha **guarda** uma especificação padrão e um dicionário `{op: Especificacao}`.
3. "Qual especificação vale para a OP?" é um `.get(op, padrao)`.
4. "Quais tolerâncias aplicar?" são as fixas mais as da especificação, e a da
   especificação vence: `{**fixas, **especificacao.tolerancias}`.

```python
class Especificacao:
    def __init__(self, titulo, tolerancias):
        self.titulo = titulo
        self.tolerancias = dict(tolerancias)  # cópia: protege de mudanças de fora


class LinhaDeProducao:
    def __init__(self, nome, fixas, padrao):
        self.nome = nome
        self.fixas = dict(fixas)
        self.padrao = padrao  # composição: a linha TEM uma especificação
        self._por_op = {}

    def cadastrar(self, op, especificacao):
        self._por_op[op] = especificacao

    def especificacao_para(self, op):
        return self._por_op.get(op, self.padrao)

    def tolerancias_para(self, op):
        return {**self.fixas, **self.especificacao_para(op).tolerancias}


padrao = Especificacao("Filme PE 25 µm", {"espessura": (22.5, 27.5)})
linha_b = LinhaDeProducao("B", {"cof": (0.10, 0.30)}, padrao)
linha_b.cadastrar("OP245110", Especificacao("Café Montanha", {"espessura": (24.0, 26.0)}))
print(linha_b.especificacao_para("OP245102").titulo, linha_b.tolerancias_para("OP245102"))
print(linha_b.especificacao_para("OP245110").titulo, linha_b.tolerancias_para("OP245110"))
```

Saída:

```text
Filme PE 25 µm {'cof': (0.1, 0.3), 'espessura': (22.5, 27.5)}
Café Montanha {'cof': (0.1, 0.3), 'espessura': (24.0, 26.0)}
```

(Para o exemplo ficar curto, as tolerâncias aqui são tuplas; no exercício 11 elas são
objetos `Tolerancia`.) Prefira composição na dúvida: ela é mais flexível (dá para
trocar a especificação de uma linha em tempo de execução) e não amarra uma classe à
outra. Use herança quando a relação "é um" for verdadeira **e** a filha puder ser usada
em qualquer lugar onde a mãe é usada.

## 12. `dataclasses`: classes de dados sem repetição

Muitas classes só **guardam dados**: o `__init__` copia parâmetros para atributos, o
`__repr__` lista os campos, o `__eq__` compara campo a campo. A `@dataclass` escreve
tudo isso a partir das anotações de tipo:

```python
>>> from dataclasses import dataclass
>>> @dataclass
... class ResultadoEnsaio:
...     ensaio: str
...     valor: float
...     unidade: str = ""
...     aprovado: bool = True
...     def rotulo(self) -> str:
...         return f"{self.ensaio}: {self.valor} ({'ok' if self.aprovado else 'falhou'})"
...
>>> r = ResultadoEnsaio("cof", 0.32, aprovado=False)
>>> r
ResultadoEnsaio(ensaio='cof', valor=0.32, unidade='', aprovado=False)
>>> r == ResultadoEnsaio("cof", 0.32, "", False)
True
>>> r.rotulo()
'cof: 0.32 (falhou)'
```

As anotações são obrigatórias (é por elas que a dataclass acha os campos) e campos com
valor padrão vêm depois dos sem padrão, como nos parâmetros de função. Métodos comuns
convivem normalmente com os gerados.

### Os recursos que você vai usar

```python
>>> from dataclasses import dataclass, field, replace, asdict
>>> from datetime import date
>>> @dataclass
... class Bobina:
...     lote: str
...     peso_kg: float
...     defeitos: list[str] = field(default_factory=list)
...     def __post_init__(self):
...         if self.peso_kg <= 0:
...             raise ValueError(f"Peso inválido: {self.peso_kg}")
...
>>> b = Bobina("L2610", 152.4)
>>> b.defeitos.append("gel")
>>> Bobina("L2611", 150.0).defeitos
[]
>>> asdict(b)
{'lote': 'L2610', 'peso_kg': 152.4, 'defeitos': ['gel']}
>>> Bobina("L2612", 0)
Traceback (most recent call last):
  ...
ValueError: Peso inválido: 0
>>> @dataclass(frozen=True, order=True)
... class Medicao:
...     data: date
...     linha: str
...     valor: float
...     observacao: str = field(default="", compare=False)
...
>>> m1 = Medicao(date(2026, 10, 2), "A", 20.4)
>>> m2 = Medicao(date(2026, 10, 1), "B", 25.2, "redigitada")
>>> sorted([m1, m2])[0].linha
'B'
>>> m1 == Medicao(date(2026, 10, 2), "A", 20.4, "outra observação")
True
>>> m1.valor = 99
Traceback (most recent call last):
  ...
dataclasses.FrozenInstanceError: cannot assign to field 'valor'
>>> replace(m1, valor=20.1).valor
20.1
>>> len({m1, m1, m2})
2
```

| Recurso | Para quê |
|---|---|
| `field(default_factory=list)` | lista (ou dict) **nova** para cada objeto |
| `__post_init__` | validar ou ajustar logo depois do `__init__` gerado |
| `frozen=True` | imutável (atribuir dá `FrozenInstanceError`) e "hashable": vai para `set` e vira chave de `dict` |
| `order=True` | gera `<`, `>`... comparando os campos **na ordem declarada** |
| `field(compare=False)` | o campo fica fora de `==`, da ordenação e do hash |
| `asdict(obj)` | vira dicionário (bom para JSON) |
| `replace(obj, campo=...)` | cópia com um campo trocado (o jeito de "alterar" um frozen) |

> 🔮 **Preveja antes de rodar:**
>
> ```python
> from dataclasses import dataclass
>
>
> @dataclass
> class Lote:
>     codigo: str
>     bobinas: list = []
> ```

<details><summary>Resposta</summary>

O erro acontece **na definição da classe**, antes de criar qualquer lote:
`ValueError: mutable default <class 'list'> for field bobinas is not allowed: use
default_factory`. A dataclass protege você da armadilha do default mutável (módulo
04 e seção 4). O certo é `bobinas: list = field(default_factory=list)`.

</details>

> 💡 **Dica:** dataclass, `namedtuple` (módulo 07) ou dicionário? Dicionário para dados
> passageiros e formatos variáveis (uma linha de CSV recém-lida). `namedtuple` para
> registros pequenos e imutáveis. Dataclass quando houver validação, métodos, valores
> padrão ou quando o tipo aparecer em vários lugares do sistema.

## 13. Igualdade: `is`, `==`, `__eq__` e `__hash__`

- `a is b`: são o **mesmo objeto** na memória?
- `a == b`: têm o **mesmo valor**? Quem decide é o método `__eq__` da classe.

Sem `__eq__`, uma classe comum usa a identidade: dois objetos com os mesmos dados são
**diferentes**.

> 🔮 **Preveja antes de rodar:**
>
> ```python
> class OrdemProducao:
>     def __init__(self, numero):
>         self.numero = numero
>
>
> a = OrdemProducao("245101")
> b = OrdemProducao("245101")
> print(a == b, a is b, a == a)
> ```

<details><summary>Resposta</summary>

`False False True`. Sem `__eq__`, `==` compara identidade: `a` e `b` são duas fichas
diferentes, ainda que preenchidas igual. (A dataclass gera um `__eq__` que compara os
campos: com `@dataclass`, o primeiro seria `True`.)

</details>

Para definir a igualdade você mesmo:

```python
>>> class OrdemProducao:
...     def __init__(self, numero):
...         self.numero = "".join(c for c in numero if c.isdigit())
...     def __eq__(self, outro):
...         if not isinstance(outro, OrdemProducao):
...             return NotImplemented
...         return self.numero == outro.numero
...     def __hash__(self):
...         return hash(self.numero)
...
>>> OrdemProducao("OP-245101") == OrdemProducao("op 245101")
True
>>> OrdemProducao("OP-245101") == "245101"
False
>>> len({OrdemProducao("OP-245101"), OrdemProducao("245101"), OrdemProducao("245102")})
2
```

Duas regras que pegam todo mundo:

1. **Outro tipo → `return NotImplemented`** (não `False`, não erro). É o jeito de dizer
   "não sei comparar com isso"; o Python tenta o outro lado e, por fim, responde
   `False`. Sem esse cuidado, `op == "245101"` quebraria com `AttributeError`.
2. **Definiu `__eq__`, defina `__hash__`.** Ao criar `__eq__`, o Python **apaga** o
   `__hash__` herdado, e o objeto deixa de entrar em `set` e de ser chave de `dict`
   (`TypeError: unhashable type`). Objetos iguais precisam ter o mesmo hash: use os
   mesmos campos do `__eq__`. E só faça isso com campos que não mudam depois.

## 14. `Enum`: conjuntos fechados de valores

Linha de produção é A, B, C ou D. Situação é liberado, reprovado ou pendente. Guardar
isso como texto solto convida ao erro (`"Liberado"`, `"liberada"`, `"LIBERADO "`). Uma
`Enum` define o conjunto **fechado** de valores possíveis:

```python
>>> from enum import Enum
>>> class Situacao(Enum):
...     LIBERADO = "liberado"
...     REPROVADO = "reprovado"
...     PENDENTE = "pendente"
...
>>> s = Situacao.LIBERADO
>>> s
<Situacao.LIBERADO: 'liberado'>
>>> s.name, s.value
('LIBERADO', 'liberado')
>>> Situacao("reprovado")
<Situacao.REPROVADO: 'reprovado'>
>>> Situacao["PENDENTE"]
<Situacao.PENDENTE: 'pendente'>
>>> [membro.value for membro in Situacao]
['liberado', 'reprovado', 'pendente']
>>> s is Situacao.LIBERADO
True
>>> Situacao("liberada")
Traceback (most recent call last):
  ...
ValueError: 'liberada' is not a valid Situacao
```

- `Situacao("reprovado")` procura pelo **valor** (bom para ler da planilha);
  `Situacao["PENDENTE"]`, pelo **nome**.
- Membros são únicos: compare com `is`.
- Enum pode ter métodos, `@property` e `@classmethod` como qualquer classe (o
  exercício 05 cria `Situacao.de_texto(...)` e `situacao.pode_emitir`).
- Quando os valores não importam, `from enum import auto` e `LIBERADO = auto()` numera
  sozinho.

> ⚠️ **Erro comum:** imprimir o membro direto num relatório. `print(Situacao.LIBERADO)`
> mostra `Situacao.LIBERADO`. Para o texto, use `.value` (ou `.name`). E cuidado com
> enums que herdam de `str` (`class Situacao(str, Enum)`): no Python 3.10,
> `f"{s}"` mostra `liberado`; do 3.11 em diante, mostra `Situacao.LIBERADO`. Usando
> sempre `.value`, o resultado é o mesmo em qualquer versão.

## 15. Outros métodos especiais

Os "dunders" ligam a sua classe à sintaxe do Python. Os que você já viu e mais alguns:

| Você escreve | O Python chama | Exemplo |
|---|---|---|
| `Classe(...)` | `__init__` | criar a fila |
| `print(obj)`, `f"{obj}"` | `__str__` | texto do certificado |
| REPL, `[obj]`, `f"{obj!r}"` | `__repr__` | depuração |
| `a == b` | `__eq__` | OPs iguais |
| `{obj}`, `dict[obj]` | `__hash__` | OP em conjunto |
| `a < b`, `sorted(...)` | `__lt__` (e companhia) | ordenar medições |
| `len(obj)` | `__len__` | quantos pedidos na fila |
| `for x in obj` | `__iter__` | percorrer a fila |
| `x in obj` | `__contains__` | "essa NF está na fila?" |

```python
class FilaDeEmissao:
    def __init__(self):
        self._pedidos = []

    def adicionar(self, op):
        self._pedidos.append(op)

    def __len__(self):
        return len(self._pedidos)

    def __iter__(self):
        return iter(self._pedidos)  # iter() devolve um iterador da lista

    def __contains__(self, op):
        return op in self._pedidos


fila = FilaDeEmissao()
fila.adicionar("OP245101")
fila.adicionar("OP245118")
print(len(fila), "OP245118" in fila, [op for op in fila])
```

Saída:

```text
2 True ['OP245101', 'OP245118']
```

Com três métodos curtos, a fila se comporta como uma coleção do Python. É o que o
exercício 13 pede.

## 16. Quando NÃO usar classes

Classe é ferramenta, não obrigação. Muito código Python profissional é feito de
**funções e dicionários**, com poucas classes bem escolhidas. Sinais de que a classe
está sobrando:

- **Só tem `__init__` e um método.** Provavelmente é uma função com parâmetros.
- **Não guarda estado** (nenhum `self.algo` é usado). É uma função, ou um módulo de
  funções (módulo 07).
- **Só agrupa constantes.** Um dicionário, um módulo `config.py` ou uma `Enum`.
- **Só guarda dados, sem regra nenhuma.** Dicionário, `namedtuple` ou `@dataclass`.
- **Hierarquia "para o futuro".** `ClasseBaseAbstrataDeEnsaioGenerico` com uma filha só
  é complexidade sem retorno. Herança se cria quando a segunda filha aparecer.

```python
import statistics


class CalculadoraDeCV:  # exagero: sem estado, só embrulha uma conta
    def calcular(self, valores):
        return statistics.stdev(valores) / statistics.mean(valores) * 100


def cv_percentual(valores):  # simples: faz o mesmo, testa igual
    return statistics.stdev(valores) / statistics.mean(valores) * 100


valores = [25.1, 24.8, 25.3, 24.9, 25.4, 25.0]
print(round(CalculadoraDeCV().calcular(valores), 2), round(cv_percentual(valores), 2))
```

Saída:

```text
0.92 0.92
```

E sinais de que a classe **vale a pena**: os mesmos dados viajam juntos por várias
funções (OP + NF + peso + cliente); existem regras que precisam valer sempre (peso
positivo, código imutável); várias variações do mesmo conceito (tipos de ensaio); ou
um objeto com estado que muda ao longo do tempo (a fila de emissão). O modelo do
Validador tem tudo isso; o cálculo do CV, não.

> 🔧 **Modifique:** abra `exemplos/09_quando_nao_usar_classe.py` e pense em uma classe
> que você escreveria para o seu trabalho. Ela passa no teste acima? Escreva a versão
> com funções e compare.

## Lendo mensagens de erro deste módulo

**`TypeError: Amostra.esta_entre() takes 2 positional arguments but 3 were given`**
— faltou o `self` na definição do método. O Python sempre passa o objeto como primeiro
argumento.

**`TypeError: Amostra.__init__() missing 1 required positional argument: 'valor'`** —
você criou o objeto sem um argumento obrigatório. Confira a assinatura do `__init__`.

**`AttributeError: 'Amostra' object has no attribute 'valro'. Did you mean: 'valor'?`**
— nome errado (o Python até sugere o certo) ou atributo nunca criado. Se o atributo
"deveria existir", procure um `super().__init__(...)` esquecido ou um
`self.algo = ...` que nunca rodou.

**`AttributeError: property 'codigo' of 'Amostra' object has no setter`** (no 3.10:
`can't set attribute`) — você tentou atribuir a uma property somente leitura. Ou é
de propósito (o dado não deve mudar), ou falta o `@codigo.setter`.

**`RecursionError: maximum recursion depth exceeded`** dentro de uma property — o
setter faz `self.valor = ...` em vez de `self._valor = ...` e chama a si mesmo sem fim.

**`TypeError: unhashable type: 'OrdemProducao'`** — a classe tem `__eq__` mas não tem
`__hash__` (ou é uma dataclass sem `frozen=True`). Defina `__hash__` ou use
`frozen=True`.

**`dataclasses.FrozenInstanceError: cannot assign to field 'valor'`** — a dataclass é
`frozen`. Use `replace(obj, valor=...)` para criar uma cópia alterada.

**`TypeError: non-default argument 'valor' follows default argument`** (no 3.13+:
`... follows default argument 'unidade'`) — na dataclass, um campo sem padrão veio
depois de um com padrão. Reordene os campos.

**`ValueError: 'liberada' is not a valid Situacao`** — o texto não corresponde a
nenhum valor da Enum. Normalize antes (`strip().lower()`) ou trate com
`try/except ValueError`.

**`TypeError: Can't instantiate abstract class Ensaio ...`** — você criou um objeto da
classe abstrata, ou a filha esqueceu de implementar um `@abstractmethod`.

## Boas práticas

- **Nomes**: classes em `PascalCase` e substantivos (`Tolerancia`, `Certificado`);
  métodos em `snake_case` e verbos (`aprova`, `emitir`, `salvar`).
- **Objeto nasce válido**: normalize e valide no `__init__` (ou no `__post_init__`).
- **Coleções de cada objeto nascem no `__init__`** (ou com `default_factory`), nunca no
  corpo da classe.
- **Escreva `__repr__`** em toda classe sua. A depuração agradece.
- **`_` para o que é interno**; `@property` quando precisar validar ou calcular. Não
  crie getters e setters "por via das dúvidas", como em Java: atributo público simples
  está ótimo até precisar de regra.
- **Prefira `@dataclass`** para classes que são basicamente dados; `frozen=True` para
  registros que não devem mudar (medições, resultados).
- **Composição antes de herança.** Herança só para "é um" verdadeiro.
- **Classes pequenas**, cada uma com uma responsabilidade. Se a descrição da classe
  precisa de "e", talvez sejam duas.
- **Não use classe onde uma função resolve** (seção 16).

## No mundo real

O script `exemplos/10_modelo_validador.py` é o esqueleto do Validador de Certificados
em objetos. Ele junta tudo do módulo:

```text
Linha (Enum)            Situacao (Enum: aprovado / liberado / reprovado)
Tolerancia (dataclass frozen, @classmethod por_nominal, aprova)
Especificacao (dataclass: título, tolerâncias, texto)
LinhaDeProducao ──tem──> fixas + Especificacao padrão + especificações por OP
Pedido, Medicao (dataclasses frozen: dados do dia)
Resultado ──tem──> Medicao + Situacao
Certificado ──tem──> Pedido + Especificacao + [Resultado]   (@property aprovado)
avaliar(pedido, linha, medicoes, liberados, emissao) -> Certificado
```

Rodando `python exemplos/10_modelo_validador.py`:

```text
CERTIFICADO OP245101 | NF 123456 | Alimentos Bom Sabor | 1250.5 kg
  Especificação: Filme PE 20 µm  (29/10/2026)
  - espessura: 20.4 µm (aprovado)
  - cof: 0.21 (aprovado)
  - tração: 31 MPa (aprovado)
  => PODE EMITIR

CERTIFICADO OP245106 | NF 123457 | Café Montanha | 980 kg
  Especificação: Café Montanha  (29/10/2026)
  - espessura: 26.3 µm (reprovado)
  - cof: 0.28 (aprovado)
  => BLOQUEADO

CERTIFICADO OP245118 | NF 123460 | Pet Nutri | 2010.75 kg
  Especificação: Filme PE 25 µm  (29/10/2026)
  - espessura: 25.1 µm (aprovado)
  - cof: 0.33 (liberado pela qualidade)
  => PODE EMITIR
```

Repare em duas regras de negócio que ficaram **claras** graças aos objetos:

- A OP245106 seria aprovada pelo padrão da linha B (22,5 a 27,5 µm), mas tem
  especificação própria (24 a 26 µm) e fica bloqueada. A regra mora num lugar só:
  `LinhaDeProducao.especificacao_para`.
- O COF 0,33 da OP245118 está fora, mas a planilha tinha "COF: liberado". Em vez de um
  `True`/`False`, o resultado carrega uma `Situacao` com três valores, e o certificado
  sai com a anotação.

Quando você ligar isso ao SQLite (módulo 11), à planilha (módulo 10) e ao robô (módulo
12), **o modelo não muda**: só muda de onde vêm os dados. É a vantagem de separar as
regras (os objetos) da entrada e da saída. No desafio do módulo, você faz exatamente
isso lendo os dados de arquivos.

## Resumo

| Assunto | Sintaxe essencial |
|---|---|
| Classe e objeto | `class Amostra:` · `a = Amostra(...)` · `isinstance(a, Amostra)` |
| Inicializar | `def __init__(self, codigo): self.codigo = codigo` |
| Método | `def aprova(self, valor): ...` · chamada `t.aprova(25.3)` |
| Atributo de classe | no corpo da classe; um só para todos (cuidado com listas!) |
| Texto | `__str__` (pessoas, `print`) · `__repr__` (programadores, REPL, listas) |
| Interno | `self._valor` (convenção) |
| Property | `@property def valor(self)` · `@valor.setter def valor(self, novo)` |
| Construtor alternativo | `@classmethod def por_nominal(cls, ...): return cls(...)` |
| Utilitário | `@staticmethod def numero_br(texto): ...` |
| Herança | `class Filha(Mae):` · `super().__init__(...)` · sobrescrever método |
| Abstrata | `class Ensaio(ABC):` · `@abstractmethod` |
| Composição | `self.padrao = Especificacao(...)` (tem um) |
| Dataclass | `@dataclass` · `field(default_factory=list)` · `__post_init__` |
| Dataclass imutável/ordenável | `@dataclass(frozen=True, order=True)` · `field(compare=False)` · `replace` |
| Igualdade | `__eq__` (outro tipo: `return NotImplemented`) + `__hash__` |
| Enum | `class Situacao(Enum): LIBERADO = "liberado"` · `Situacao("liberado")` · `.value` |
| Coleção própria | `__len__` · `__iter__` (`return iter(lista)`) · `__contains__` |

## Você domina este módulo se...

- [ ] Consigo explicar, sem consultar, o que é `self` e o que o Python faz por trás de
      `a.esta_entre(1, 2)`.
- [ ] Sei por que `bobinas = []` no corpo da classe é um bug e onde a lista deve nascer.
- [ ] Escrevo `__str__` e `__repr__` e sei qual deles aparece no `print`, no REPL e
      dentro de uma lista.
- [ ] Protejo um atributo com `@property` e setter que valida, e faço uma property
      somente leitura.
- [ ] Explico a diferença entre método comum, `@classmethod` e `@staticmethod`, com um
      exemplo de cada no domínio do laboratório.
- [ ] Decido entre herança e composição usando "é um" / "tem um", e lembro do
      `super().__init__`.
- [ ] Escrevo uma dataclass com valor padrão mutável correto, `__post_init__`,
      `frozen` e `order`, e sei o que cada um gera.
- [ ] Reconheço uma classe desnecessária e reescrevo como função.

## Exercícios

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_classe_amostra` | ★☆☆ | `class`, `__init__`, `self`, métodos |
| 02 | `ex02_bobina_str_repr` | ★☆☆ | `__str__` e `__repr__` |
| 03 | `ex03_tolerancia` | ★☆☆ | validação no `__init__`, limites opcionais (`None`) |
| 04 | `ex04_dataclass_resultado` | ★☆☆ | `@dataclass`, campos com padrão, `__repr__`/`__eq__` gerados |
| 05 | `ex05_enum_situacao` | ★☆☆ | `Enum`, `@classmethod` e `@property` numa Enum |
| 06 | `ex06_amostra_property` | ★★☆ | `@property`, setter com validação, somente leitura, histórico |
| 07 | `ex07_tolerancia_construtores` | ★★☆ | `@classmethod` (nominal ± %, texto), `@staticmethod`, `cls(...)` |
| 08 | `ex08_heranca_ensaios` | ★★☆ | herança, `super()`, sobrescrita, polimorfismo |
| 09 | `ex09_corrigir_lote` | ★★☆ | **leitura de código**: prever e corrigir lista compartilhada, `super()` e `__eq__`/`__hash__` |
| 10 | `ex10_dataclass_medicao` | ★★☆ | `frozen`, `order`, `field(compare=False)`, hash e `set` |
| 11 | `ex11_especificacao_linha` | ★★★ | composição: `Especificacao` e `LinhaDeProducao` (regra real do projeto) |
| 12 | `ex12_revisao_certificado` | ★★★ | **revisão**: dataclass + número BR (05) + arquivo e exceção (06) + datas (07) |
| 13 | `ex13_revisao_fila_emissao` | ★★★ | **revisão**: regex (05) + exceção (06) + `__len__`/`__iter__`/`__contains__` |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar
de `raise NotImplementedError` e rode, na pasta `curso-python`:

```powershell
python curso.py testar 08 ex01     # um exercício
python curso.py testar 08          # o módulo inteiro
```

> 💡 **Dica:** nos exercícios 04, 10 e 12 o arquivo traz um `__init__` provisório que
> só levanta erro. Apague-o e transforme a classe numa `@dataclass`, como o enunciado
> pede.

## Desafio do módulo

**O Validador de Certificados orientado a objetos**: leia as regras das linhas
(`regras.json`), os pedidos da expedição e as medições do laboratório, aplique
tolerâncias fixas, especificação padrão ou própria da OP e as observações de liberação
("COF: liberado"), e diga quais certificados podem ser emitidos. Junta Enum,
dataclasses, `@classmethod`, composição e `@property`.

Enunciado completo, exemplo de execução e critérios de aceite em
[desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou em [quiz.md](quiz.md): 13 perguntas com gabarito comentado.

## Para ir além

- Tutorial oficial, classes: <https://docs.python.org/pt-br/3/tutorial/classes.html>
- `dataclasses`: <https://docs.python.org/pt-br/3/library/dataclasses.html>
- `enum` (e o guia "Enum HOWTO"): <https://docs.python.org/pt-br/3/library/enum.html> e
  <https://docs.python.org/pt-br/3/howto/enum.html>
- `abc`, classes abstratas: <https://docs.python.org/pt-br/3/library/abc.html>
- Métodos especiais (a lista completa dos "dunders"):
  <https://docs.python.org/pt-br/3/reference/datamodel.html#special-method-names>
- Leitura extra: Luciano Ramalho, *Python Fluente* (Novatec), capítulos sobre o modelo
  de dados e classes. Escrito por um brasileiro, é a referência para ir fundo.
- Leitura extra: "Stop Writing Classes", palestra de Jack Diederich (PyCon 2012), sobre
  a seção 16: <https://www.youtube.com/watch?v=o9pEzgHorH0>
