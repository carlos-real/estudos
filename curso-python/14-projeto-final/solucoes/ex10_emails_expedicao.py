"""
Exercício 14.10 — Ler os pedidos da expedição (OP, NF e peso)
Nível: ★★☆

Contexto: A expedição pede certificado por e-mail, cada pessoa de um jeito: "OP:
24518", "OP nº 24541", "NF 123457", "NF-e nº 123.789", "Nota fiscal: 123460",
"Peso: 1.250,5 kg", "Peso líquido: 2.040 kg". Um e-mail = um pedido. Se faltar algo,
ou se houver dois valores diferentes para o mesmo campo (duas OPs, por exemplo), o
e-mail fica "fora do padrão": o sistema não escolhe por você.

Tarefa: implemente três funções.
1. `numero_br(texto)`: "1.250,5" -> 1250.5; "2.040" -> 2040.0; "980,0" -> 980.0.
2. `ler_email(texto, origem="")` devolve Pedido(op, nf, peso_kg, origem). Os padrões
   RE_OP, RE_NF e RE_PESO já estão prontos (vêm do módulo 05). Com eles:
   - NF: tire os pontos ("123.789" -> "123789"), inclusive um ponto final de frase;
   - peso: converta com numero_br;
   - valores repetidos iguais contam uma vez só (a OP costuma estar no assunto E
     no corpo; "1.500 kg" e "1500 kg" são o mesmo peso);
   - junte TODOS os problemas, nesta ordem, e levante PedidoInvalido com eles
     separados por "; ":
       "OP não encontrada" / "mais de uma OP no e-mail (24520, 24521)"
       "NF não encontrada" / "mais de uma NF no e-mail (1, 2)"
       "peso não encontrado" / "mais de um peso no e-mail (1500, 1700)"
       "peso deve ser maior que zero"
     (nas listas, valores em ordem crescente; pesos formatados com :g).
3. `separar_emails(emails)` recebe {nome_do_arquivo: texto} e devolve
   (lista de Pedido com origem=nome, {nome: mensagem do PedidoInvalido}).

Exemplos:
    >>> ler_email("OP: 24518\\nNF: 123456\\nPeso: 1.250,5 kg")
    Pedido(op='24518', nf='123456', peso_kg=1250.5, origem='')
    >>> ler_email("A carga da OP 24555 (1.500 kg) está pronta. A NF sai amanhã.")
    Traceback (most recent call last):
    PedidoInvalido: NF não encontrada; peso não encontrado

Dica: RE_OP.findall(texto) devolve a lista dos grupos ("24518", ...); set() tira
as repetições e sorted() põe em ordem. Teste os padrões no REPL antes de escrever o
resto: é assim que se descobre o que eles devolvem.

Teste com:  python curso.py testar 14 ex10
"""

import re
from dataclasses import dataclass

# ============================================================================
# PEÇAS PRONTAS (etapas anteriores) — não precisa mexer
# ============================================================================


# Padrões do módulo 05. Cada um tem UM grupo: o valor que interessa.
RE_OP = re.compile(r"\bOP\b\s*(?:n[º°o]\.?\s*)?[:#-]?\s*(\d{4,6})\b", re.IGNORECASE)
RE_NF = re.compile(
    r"\b(?:NF-?e?|nota\s+fiscal)\s*(?:n[º°o]\.?\s*)?[:#-]?\s*(\d[\d.]*)", re.IGNORECASE
)
RE_PESO = re.compile(
    r"\bpeso(?:\s+l[ií]quido)?\s*[:=-]?\s*(\d[\d.]*(?:,\d+)?)\s*kg\b", re.IGNORECASE
)


@dataclass(frozen=True)
class Pedido:
    op: str
    nf: str
    peso_kg: float
    origem: str = ""

    def __post_init__(self) -> None:
        if not self.op.strip() or not self.nf.strip():
            raise ValueError("pedido precisa de OP e NF")
        if self.peso_kg <= 0:
            raise ValueError(f"peso deve ser maior que zero (recebido: {self.peso_kg})")


class PedidoInvalido(ValueError):
    """E-mail da expedição fora do padrão."""


# ============================================================================
# SUA PARTE
# ============================================================================


def numero_br(texto: str) -> float:
    """Converte número no formato brasileiro ("1.250,5") para float."""
    # A ordem importa: primeiro some o ponto de milhar, depois a vírgula vira ponto.
    # Ao contrário, "1.250,5" viraria "1.250.5" -> ValueError.
    return float(texto.strip().replace(".", "").replace(",", "."))


def ler_email(texto: str, origem: str = "") -> Pedido:
    """Extrai o Pedido do e-mail ou levanta PedidoInvalido com todos os problemas."""
    # Conjuntos tiram repetições ("OP 24518" no assunto e no corpo = uma OP só).
    ops = sorted(set(RE_OP.findall(texto)))
    # rstrip(".") tira o ponto final da frase ("NF 123456."); replace tira o milhar.
    nfs = sorted({nf.rstrip(".").replace(".", "") for nf in RE_NF.findall(texto)})
    # Pesos comparados como número: "1.500" e "1500" são o MESMO peso.
    pesos = sorted({numero_br(p) for p in RE_PESO.findall(texto)})

    # Uma tabela de (achados, mensagem se faltar, mensagem se sobrar) evita repetir
    # o mesmo if três vezes.
    campos = (
        (ops, "OP não encontrada", "mais de uma OP no e-mail"),
        (nfs, "NF não encontrada", "mais de uma NF no e-mail"),
        ([f"{p:g}" for p in pesos], "peso não encontrado", "mais de um peso no e-mail"),
    )
    problemas = []
    for achados, se_faltar, se_sobrar in campos:
        if not achados:
            problemas.append(se_faltar)
        elif len(achados) > 1:
            problemas.append(f"{se_sobrar} ({', '.join(achados)})")
    if len(pesos) == 1 and pesos[0] <= 0:
        problemas.append("peso deve ser maior que zero")
    if problemas:
        raise PedidoInvalido("; ".join(problemas))
    return Pedido(op=ops[0], nf=nfs[0], peso_kg=pesos[0], origem=origem)


def separar_emails(emails: dict[str, str]) -> tuple[list[Pedido], dict[str, str]]:
    """(pedidos válidos, {arquivo: problema}) na ordem do dicionário recebido."""
    pedidos: list[Pedido] = []
    fora_do_padrao: dict[str, str] = {}
    for nome, texto in emails.items():
        try:
            pedidos.append(ler_email(texto, origem=nome))
        except PedidoInvalido as erro:
            # Capturamos SÓ PedidoInvalido. Qualquer outro erro é bug e deve
            # aparecer, não virar "e-mail fora do padrão".
            fora_do_padrao[nome] = str(erro)
    return pedidos, fora_do_padrao
