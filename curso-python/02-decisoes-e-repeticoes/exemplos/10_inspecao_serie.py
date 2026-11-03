"""Exemplo 10 — No mundo real: inspeção de uma série de espessura.

Rode com:  python exemplos/10_inspecao_serie.py

O programa recebe a linha, o nominal e as leituras do micrômetro (0 ou negativo =
falha de leitura), classifica cada leitura, aplica a regra "3 seguidas fora = pare a
linha" e emite o veredito.
"""


def acao_do_operador(situacao: str) -> str:
    """O que o operador da extrusora deve fazer para cada situação."""
    match situacao:
        case "ABAIXO":
            return "abrir a matriz"
        case "ACIMA":
            return "fechar a matriz"
        case _:
            return ""


linha = "C"
nominal = 25.0
tolerancia = 8.0  # especificação da OP (ou o padrão da linha)
leituras = [24.9, 25.3, 0.0, 26.1, -1.0, 27.4, 25.0, 22.8, 22.5, 22.9, 25.1]

if tolerancia <= 0:
    print("Tolerância inválida na especificação. Nada a fazer.")
else:
    minimo = nominal - nominal * tolerancia / 100
    maximo = nominal + nominal * tolerancia / 100
    print(f"Linha {linha} | {nominal} µm ± {tolerancia:.0f}% -> {minimo:.2f} a {maximo:.2f}")

    posicao = 0
    validas = 0
    soma = 0.0
    fora = 0
    seguidas = 0
    parar_linha = False
    for valor in leituras:
        posicao += 1
        if valor <= 0:
            print(f"  #{posicao:<2} falha de leitura, ignorada")
            continue
        validas += 1
        soma += valor
        if valor < minimo:
            situacao = "ABAIXO"
        elif valor > maximo:
            situacao = "ACIMA"
        else:
            situacao = "ok"
        if situacao == "ok":
            seguidas = 0
        else:
            fora += 1
            seguidas += 1
        print(f"  #{posicao:<2} {valor:>6.2f} µm  {situacao:<7}{acao_do_operador(situacao)}")
        if seguidas == 3:
            parar_linha = True
            print("  >>> 3 leituras seguidas fora: PARE A LINHA e chame o líder.")
            break

    print("-" * 50)
    if validas == 0:
        print("Nenhuma leitura válida.")
    else:
        media = soma / validas
        if parar_linha:
            veredito = "REPROVADO (processo fora de controle)"
        elif fora > 0:
            veredito = "CONDICIONAL (pontos isolados fora)"
        else:
            veredito = "APROVADO"
        print(f"Válidas: {validas} | média {media:.2f} µm | fora: {fora}")
        print(f"Veredito: {veredito}")
