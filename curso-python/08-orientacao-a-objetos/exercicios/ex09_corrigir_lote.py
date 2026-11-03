"""
Exercício 08.09 — Leitura de código: o lote que pesava demais
Nível: ★★☆

Contexto: Um colega modelou os lotes de bobinas. O relatório mostrou o lote L02
com o peso de TODOS os lotes, o lote de exportação quebrou com AttributeError e
o programa travou ao colocar lotes num conjunto (set). Leia o código, preveja e
corrija.

Código do colega (com 3 defeitos):

    class Lote:
        bobinas = []

        def __init__(self, codigo):
            self.codigo = codigo

        def adicionar(self, peso_kg):
            self.bobinas.append(peso_kg)

        @property
        def peso_total(self):
            return sum(self.bobinas)

        def __eq__(self, outro):
            return self.codigo == outro.codigo


    class LoteExportacao(Lote):
        def __init__(self, codigo, pais):
            self.pais = pais

Comportamento CORRETO esperado:
- cada lote tem a SUA lista de bobinas (atributo de instância criado no __init__);
- `peso_total` soma só as bobinas daquele lote;
- `LoteExportacao` tem `codigo`, `pais` e a própria lista de bobinas (chame a mãe);
- dois lotes são iguais quando têm o mesmo código; comparar com algo que não é
  Lote (ex.: um texto) devolve False sem quebrar (retorne NotImplemented no __eq__);
- lotes podem ir para um set e ser chave de dicionário: defina __hash__ com base
  no código (quem define __eq__ perde o __hash__ padrão).

Tarefa:
1. ANTES de corrigir, preveja: na versão do colega, depois de
       a = Lote("L01"); b = Lote("L02")
       a.adicionar(100.0); b.adicionar(50.0)
   quanto vale len(b.bobinas)? Devolva sua previsão em
   `previsao_bobinas_do_lote_b()`. Depois rode o código do colega para conferir.
2. Corrija as duas classes abaixo, mantendo nomes e assinaturas.

Exemplos (versão corrigida):
    >>> a = Lote("L01")
    >>> a.adicionar(100.0)
    >>> Lote("L02").peso_total
    0
    >>> Lote("L01") == Lote("L01"), Lote("L01") == "L01"
    (True, False)
    >>> len({Lote("L01"), Lote("L01"), Lote("L02")})
    2

Teste com:  python curso.py testar 08 ex09
"""


def previsao_bobinas_do_lote_b() -> int:
    """Sua previsão para len(b.bobinas) na versão com defeito."""
    # Escreva seu código aqui (devolva o número que você prevê)
    raise NotImplementedError("Implemente esta função")


class Lote:
    """Lote de bobinas."""

    def __init__(self, codigo: str) -> None:
        # Escreva seu código aqui (corrija o código do colega)
        raise NotImplementedError("Implemente este método")

    def adicionar(self, peso_kg: float) -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    @property
    def peso_total(self) -> float:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def __eq__(self, outro: object) -> bool:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def __hash__(self) -> int:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")


class LoteExportacao(Lote):
    """Lote destinado a exportação."""

    def __init__(self, codigo: str, pais: str) -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")
