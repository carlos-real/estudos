"""Exemplo 04 — strings básicas.

Rode com:  python exemplos/04_strings.py
"""

cliente = "  Embalagens Sul  "
produto = "filme bopp"

print("Concatenação:", "Linha " + "B")
print("Repetição:", "-" * 20)
print("Tamanho:", len(produto))
print("Maiúsculas:", produto.upper())
print("Minúsculas:", "COF LIBERADO".lower())
print("Sem espaços nas pontas: [" + cliente.strip() + "]")
print("Substituição:", "25,4".replace(",", "."))
print("Contém 'bopp'?", "bopp" in produto)
print("Contém 'BOPP'?", "BOPP" in produto)  # diferencia maiúsculas!

# Encadeando métodos: cada um devolve um texto novo
codigo = " op-12345 ".strip().upper().replace("-", "")
print("Código limpo:", codigo)

# Strings não mudam: o método devolve uma cópia e o original fica igual
nome = "laudo"
nome.upper()
print("Original continua:", nome)
nome = nome.upper()  # para "mudar", guarde o resultado
print("Agora sim:", nome)
