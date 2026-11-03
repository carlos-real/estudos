"""Desafio do módulo 01 — Ficha de medição da bobina (solução de referência).

Rode na pasta curso-python:
    python 01-fundamentos/desafio/solucao_referencia.py

Os dados de entrada estão no topo, como TEXTO, do jeito que chegariam de um
formulário ou planilha. Para a versão interativa (extra), troque cada valor por um
input(), por exemplo:  op_digitada = input("OP: ")
"""

import math

# =============================================================================
# 1. ENTRADA: dados brutos da amostra (do jeito que chegam)
# =============================================================================
op_digitada = "  op-48.213 "
linha_digitada = " c "
cliente_digitado = "  embalagens sul ltda "
medicao_1 = "24,8"
medicao_2 = "25,3"
medicao_3 = "25,1"
medicao_4 = "24,6"
medicao_5 = "25,4"
espessura_nominal_um = 25.0
tolerancia_pct = 8.0
massa_corpo_prova = "0,4710"  # gramas, corpo de prova 10 cm x 10 cm
largura_corpo_prova_cm = 10.0
comprimento_corpo_prova_cm = 10.0
largura_bobina_mm = 640
comprimento_bobina_m = 6000
diametro_tubete_mm = 76
producao_total_m = 45500  # extra: quantas bobinas saem da OP inteira


# =============================================================================
# Funções auxiliares (o molde def + return da seção 14)
# =============================================================================
def texto_para_float(texto: str) -> float:
    """Converte '24,8' (com vírgula e espaços) em 24.8."""
    return float(texto.strip().replace(",", "."))


def formatar_br(valor: float, casas: int) -> str:
    """Formata no padrão brasileiro: 1234.5 com 2 casas vira '1.234,50'."""
    # As chaves dentro do formato deixam o número de casas variável:
    # com casas = 2, o formato vira ",.2f".
    americano = f"{valor:,.{casas}f}"
    return americano.replace(",", "X").replace(".", ",").replace("X", ".")


def linha_da_ficha(rotulo: str, valor: str) -> str:
    """Monta uma linha com o rótulo à esquerda e o valor à direita (44 colunas)."""
    return f"{rotulo:<26}{valor:>18}"


# =============================================================================
# 2. LIMPEZA E CONVERSÃO
# =============================================================================
numero_op = op_digitada.upper().replace("OP", "").replace("-", "").replace(".", "")
op = "OP" + numero_op.strip()
linha = linha_digitada.strip().upper()
cliente = cliente_digitado.strip().upper()

e1 = texto_para_float(medicao_1)
e2 = texto_para_float(medicao_2)
e3 = texto_para_float(medicao_3)
e4 = texto_para_float(medicao_4)
e5 = texto_para_float(medicao_5)
massa_g = texto_para_float(massa_corpo_prova)

# =============================================================================
# 3. CÁLCULOS (todas as casas; arredondamento só na exibição)
# =============================================================================
media_um = (e1 + e2 + e3 + e4 + e5) / 5
minimo_um = espessura_nominal_um - espessura_nominal_um * tolerancia_pct / 100
maximo_um = espessura_nominal_um + espessura_nominal_um * tolerancia_pct / 100
desvio = (media_um - espessura_nominal_um) / espessura_nominal_um  # fração: 0.0024

area_corpo_prova_m2 = (largura_corpo_prova_cm / 100) * (comprimento_corpo_prova_cm / 100)
gramatura = massa_g / area_corpo_prova_m2
peso_kg = gramatura * (largura_bobina_mm / 1000) * comprimento_bobina_m / 1000

comprimento_mm = comprimento_bobina_m * 1000
espessura_mm = media_um / 1000
diametro_mm = math.sqrt(diametro_tubete_mm**2 + 4 * comprimento_mm * espessura_mm / math.pi)

bobinas_completas = producao_total_m // comprimento_bobina_m
sobra_m = producao_total_m % comprimento_bobina_m

# =============================================================================
# 4. SAÍDA: a ficha
# =============================================================================
print("=" * 44)
print(f"{'FICHA DE MEDIÇÃO DA BOBINA':^44}")
print("=" * 44)
print(linha_da_ficha("OP", op))
print(linha_da_ficha("Linha", linha))
print(linha_da_ficha("Cliente", cliente))
print("-" * 44)
medicoes = f"{e1:.1f} | {e2:.1f} | {e3:.1f} | {e4:.1f} | {e5:.1f}".replace(".", ",")
print("Medições (µm):")
print(f"{medicoes:>44}")
print(linha_da_ficha("Espessura média (µm)", formatar_br(media_um, 2)))
print(
    linha_da_ficha(
        "Nominal (µm)", f"{formatar_br(espessura_nominal_um, 1)} ± {tolerancia_pct:.0f}%"
    )
)
print(
    linha_da_ficha(
        "Faixa aceita (µm)", f"{formatar_br(minimo_um, 2)} a {formatar_br(maximo_um, 2)}"
    )
)
print(linha_da_ficha("Desvio do nominal", f"{desvio:+.2%}".replace(".", ",")))
print("-" * 44)
print(linha_da_ficha("Gramatura (g/m²)", formatar_br(gramatura, 1)))
print(linha_da_ficha("Peso estimado (kg)", formatar_br(peso_kg, 2)))
print(linha_da_ficha("Diâmetro estimado (mm)", formatar_br(diametro_mm, 0)))
print(linha_da_ficha("Bobinas na OP", f"{bobinas_completas} + sobra {sobra_m} m"))
print("=" * 44)
print("Veredito automático: fica para o módulo 02 (if/else).")
