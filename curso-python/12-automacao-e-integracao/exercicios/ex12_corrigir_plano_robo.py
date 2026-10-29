"""
Exercício 12.12 — Leitura de código: conserte o plano do robô
Nível: ★★☆

Contexto: um colega separou o robô em duas partes: uma função que PLANEJA as
ações (lista de tuplas, sem navegador) e outra que as EXECUTA com o Playwright.
Ótima ideia: o plano pode ser testado sem abrir o Edge. O problema é que o
plano dele tem defeitos, e um deles é grave: CONFIRMA a emissão no modo ensaio.

O código do colega (NÃO copie sem ler; ele tem pelo menos 5 defeitos):

    def planejar_certificado(pedido, ensaio=True, acoes=[]):
        if len(pedido["op"]) != 6:
            raise ValueError("OP inválida")
        acoes.append(("preencher", "OP", pedido["op"]))
        acoes.append(("preencher", "NF", pedido["nf"]))
        acoes.append(("preencher", "Peso (kg)", f"{pedido['peso_kg']:,.2f}"))
        acoes.append(("selecionar", "Linha", pedido["linha"]))
        if pedido["observacao"]:
            acoes.append(("preencher", "Observação", pedido["observacao"]))
        acoes.append(("print", f"antes_de_confirmar_{pedido['op']}", ""))
        if ensaio:
            acoes.append(("clicar", "Confirmar", ""))
        else:
            acoes.append(("clicar", "Cancelar", ""))
        return acoes

Passo 1 (leitura): ANTES de rodar qualquer coisa, leia o código e anote no
papel o que ele devolve para o pedido do exemplo abaixo, chamado DUAS vezes
seguidas. Depois confira copiando o código num arquivo de rascunho.

Passo 2 (conserto): escreva abaixo a versão correta, que segue estas regras:
- A OP deve ter exatamente 6 caracteres e todos dígitos; senão, ValueError.
- peso_kg deve ser maior que zero; senão, ValueError.
- As ações, nesta ordem:
    ("preencher", "OP", op)
    ("preencher", "NF", nf)
    ("preencher", "Peso (kg)", <peso no formato brasileiro, 2 casas: "1.250,50">)
    ("selecionar", "Linha", linha)
    ("preencher", "Observação", obs)   <- só se o pedido TIVER a chave
                                          "observacao" com texto não vazio
    ("print", f"antes_de_confirmar_{op}", "")
    e por último ("clicar", "Cancelar", "") quando ensaio=True,
    ou ("clicar", "Confirmar", "") quando ensaio=False.
- Cada chamada devolve uma lista NOVA (chamadas não podem se misturar).

Exemplos:
    >>> pedido = {"op": "123456", "nf": "98765", "peso_kg": 1250.5, "linha": "B"}
    >>> planejar_certificado(pedido)
    [('preencher', 'OP', '123456'), ('preencher', 'NF', '98765'),
     ('preencher', 'Peso (kg)', '1.250,50'), ('selecionar', 'Linha', 'B'),
     ('print', 'antes_de_confirmar_123456', ''), ('clicar', 'Cancelar', '')]

Dica: módulo 04 (a armadilha do valor padrão mutável) e módulo 05 (números no
formato brasileiro). dict.get() devolve None quando a chave não existe.

Teste com:  python curso.py testar 12 ex12
"""


def planejar_certificado(pedido: dict, ensaio: bool = True) -> list[tuple[str, str, str]]:
    """Devolve a lista de ações do robô para emitir (ou ensaiar) um certificado."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
