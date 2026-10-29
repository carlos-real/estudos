"""labqualidade: funções de apoio para o laboratório de qualidade.

Este arquivo transforma a pasta `labqualidade/` num PACOTE. Ele roda uma vez,
na primeira vez que alguém faz `import labqualidade`.

Aqui escolhemos o que fica na "vitrine" do pacote: quem usa pode escrever
`from labqualidade import faixa_nominal` sem saber em qual arquivo ela mora.
"""

from .conversoes import data_br, numero_br
from .estatistica import cv_percentual, resumo
from .tolerancias import dentro_da_faixa, faixa_nominal

__version__ = "0.1.0"

# __all__ diz o que sai num "from labqualidade import *" (e documenta a vitrine)
__all__ = [
    "cv_percentual",
    "data_br",
    "dentro_da_faixa",
    "faixa_nominal",
    "numero_br",
    "resumo",
]
