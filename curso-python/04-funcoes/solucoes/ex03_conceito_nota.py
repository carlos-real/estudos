"""
Solução — Exercício 04.03 — Conceito e situação do aluno

Ideia central: retorno antecipado. Cada if que dá return "encerra o assunto";
por isso não precisamos de elif nem de else, e a leitura é de cima para baixo.
"""


def conceito(nota: float) -> str:
    """Converte a nota (0 a 10) em A, B, C, D ou "inválida"."""
    # Primeiro o caso inválido (guard clause). Daqui para baixo, a nota é válida.
    if nota < 0 or nota > 10:
        return "inválida"
    if nota >= 9:
        return "A"
    if nota >= 7:  # só chega aqui se nota < 9
        return "B"
    if nota >= 5:
        return "C"
    return "D"


def situacao(nota: float, frequencia_pct: float) -> str:
    """Decide a situação final do aluno a partir da nota e da frequência."""
    # A ordem dos ifs É a regra: falta vence tudo, inclusive nota inválida.
    if frequencia_pct < 75:
        return "reprovado por falta"

    letra = conceito(nota)  # reaproveita a outra função em vez de repetir a lógica
    if letra == "inválida":
        return "nota inválida"
    if letra in ("A", "B", "C"):
        return "aprovado"
    return "reprovado por nota"
