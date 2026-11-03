"""
Exercício 09.11 — Revisão: resumo por linha de produção (conserte os bugs)
Nível: ★★★

Solução comentada. Veja o enunciado completo em exercicios/ex11_revisao_resumo_por_linha.py.
"""


def resumir_por_linha(
    registros: list[str], tolerancias: dict[str, tuple[float, float]]
) -> dict[str, dict]:
    """Resumo por linha: total de medições, quantas fora e o percentual fora."""
    resumo: dict[str, dict] = {}
    for registro in registros:
        # A leitura do registro já estava certa (módulo 05): separa, normaliza
        # a linha e converte a vírgula decimal.
        linha, texto_valor = registro.split(";")
        linha = linha.strip().upper()
        valor = float(texto_valor.strip().replace(",", "."))

        # BUG 4: tolerancias[linha] levantava KeyError para linha desconhecida.
        # A regra pede ValueError com mensagem clara. Conferir com "in" antes
        # é mais legível do que capturar o KeyError.
        if linha not in tolerancias:
            raise ValueError(f"linha {linha} sem tolerância cadastrada")
        minimo, maximo = tolerancias[linha]

        # BUG 2: "valor <= minimo" jogava a borda inferior para FORA. As bordas
        # estão DENTRO, então FORA é estritamente menor ou estritamente maior.
        fora = valor < minimo or valor > maximo

        # BUG 1: o original fazia resumo[linha] = {"total": 1, ...} a cada
        # registro, apagando a contagem anterior. Crie o "contador" só na
        # primeira vez que a linha aparece e depois some.
        if linha not in resumo:
            resumo[linha] = {"total": 0, "fora": 0}
        resumo[linha]["total"] += 1
        resumo[linha]["fora"] += int(fora)  # True vira 1, False vira 0

    for dados in resumo.values():
        # BUG 3: "//" é divisão inteira: 1 // 3 dá 0, e o percentual sumia.
        # A divisão comum "/" dá 0.333..., que vira 33.3 depois do round.
        dados["percentual_fora"] = round(dados["fora"] / dados["total"] * 100, 1)
    return resumo


# Por que os 4 bugs não apareceram de uma vez? Com o BUG 1, todo total era 1,
# o que mascarava o BUG 3 (1 // 1 * 100 = 100, que até parece certo). Bugs se
# escondem atrás de outros bugs: por isso corrija um de cada vez e rode tudo.
