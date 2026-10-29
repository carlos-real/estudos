"""Importa o módulo conversoes_br.py que está na mesma pasta.

Rode com:  python exemplos/02_usando_conversoes.py
Repare: o bloco `if __name__ == "__main__":` de conversoes_br NÃO roda aqui.
"""

import conversoes_br
from conversoes_br import formatar_br

peso_total = conversoes_br.numero_br("1.250,5") + conversoes_br.numero_br("980,25")
print("Peso total da NF:", formatar_br(peso_total), "kg")
print("__name__ deste arquivo:", __name__)
print("__name__ do módulo importado:", conversoes_br.__name__)
