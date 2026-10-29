"""
Exercício 12.12 — Leitura de código: conserte o plano do robô (SOLUÇÃO)

Os defeitos do código do colega, do mais grave ao mais sutil:

1. `if ensaio:` clica em CONFIRMAR. Está invertido! No ensaio o robô emitiria
   certificados de verdade. É o tipo de erro que um teste pega em 1 segundo.
2. `acoes=[]` como valor padrão: a lista é criada UMA vez, quando o `def` roda,
   e é reaproveitada em toda chamada. Na segunda chamada, o plano vem com as
   ações da primeira mais as da segunda (12 ações em vez de 6).
3. f"{peso:,.2f}" dá "1,250.50" (formato americano). A tela espera "1.250,50".
4. `pedido["observacao"]` levanta KeyError quando o pedido não tem a chave.
5. `len(op) != 6` aceita "12a456". A regra pede 6 DÍGITOS.
6. Não há validação de peso: 0 ou negativo passariam direto para a tela.

Resposta do Passo 1 (pedido do exemplo, sem a chave "observacao"): as DUAS
chamadas quebram com KeyError: 'observacao'. Pior: como as 4 primeiras ações
são anexadas ANTES do erro, a lista padrão já acumula 8 ações "fantasmas", que
vão aparecer no próximo plano que der certo.
"""


def formatar_peso_br(peso: float) -> str:
    """1250.5 -> '1.250,50'. Troca em 3 passos usando um marcador temporário."""
    americano = f"{peso:,.2f}"  # '1,250.50'
    return americano.replace(",", "#").replace(".", ",").replace("#", ".")


def planejar_certificado(pedido: dict, ensaio: bool = True) -> list[tuple[str, str, str]]:
    """Devolve a lista de ações do robô para emitir (ou ensaiar) um certificado."""
    op = pedido["op"]
    # isdigit() garante que só há dígitos; len garante a quantidade.
    if len(op) != 6 or not op.isdigit():
        raise ValueError(f"OP inválida: {op!r}")
    if pedido["peso_kg"] <= 0:
        raise ValueError(f"Peso inválido: {pedido['peso_kg']}")

    # Lista criada DENTRO da função: nova a cada chamada (defeito 2 resolvido).
    acoes = [
        ("preencher", "OP", op),
        ("preencher", "NF", pedido["nf"]),
        ("preencher", "Peso (kg)", formatar_peso_br(pedido["peso_kg"])),
        ("selecionar", "Linha", pedido["linha"]),
    ]

    # .get() devolve None se a chave não existir; None e "" são falsy.
    observacao = pedido.get("observacao")
    if observacao:
        acoes.append(("preencher", "Observação", observacao))

    acoes.append(("print", f"antes_de_confirmar_{op}", ""))

    # A regra de ouro do robô: em ensaio, NUNCA confirmar.
    botao = "Cancelar" if ensaio else "Confirmar"
    acoes.append(("clicar", botao, ""))
    return acoes
