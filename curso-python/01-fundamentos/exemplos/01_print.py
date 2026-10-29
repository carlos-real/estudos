"""Exemplo 01 — print: o programa falando com você.

Rode com:  python exemplos/01_print.py
"""

print("Olá, laboratório!")
print("OP", 12345, "liberada")  # vários valores: o print separa com um espaço
print("Espessura:", 25.4, "µm")
print("A", "B", "C", "D", sep=" | ")  # sep troca o separador
print("Medindo...", end=" ")  # end troca o final da linha (o padrão é quebrar a linha)
print("pronto!")
print()  # print vazio = linha em branco
print("Linha 1\nLinha 2")  # \n quebra a linha dentro do texto
print("Amostra\tResultado")  # \t é uma tabulação
print('Ela disse: "COF liberado"')  # aspas duplas dentro de aspas simples
