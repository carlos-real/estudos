"""
Exercício 08.07 — Tolerância com construtores alternativos
Nível: ★★☆

Contexto: As tolerâncias chegam de jeitos diferentes: faixa fixa da linha
("0,10 a 0,30"), nominal ± percentual da especificação ("25 ± 10%") ou números
soltos do banco de regras. Em vez de um __init__ cheio de "se", usamos
@classmethod para criar a mesma Tolerancia a partir de cada formato.

Tarefa: complete a classe `Tolerancia`.
1. `__init__(self, minimo, maximo)`: guarda os dois limites (float). minimo > maximo
   -> ValueError.
2. `por_nominal(cls, nominal, percentual)` (classmethod): faixa nominal ± percentual%.
   Percentual negativo -> ValueError. Ex.: (25, 10) -> mínimo 22.5, máximo 27.5.
3. `converter_numero(texto)` (staticmethod): número no formato brasileiro -> float.
   "1.250,5" -> 1250.5; "0,10" -> 0.1; " 25 " -> 25.0.
4. `de_texto(cls, texto)` (classmethod): aceita (com espaços variados)
   - "0,10 a 0,30"           -> faixa
   - "25 ± 10%" ou "25 +- 10%" -> nominal ± percentual
   Qualquer outro formato -> ValueError. Use converter_numero e por_nominal.
5. `aprova(valor)`: True se minimo <= valor <= maximo.
6. `__repr__`: "Tolerancia(minimo=22.5, maximo=27.5)".
Os classmethods devem criar o objeto com `cls(...)`, para funcionar também em
subclasses.

Exemplos:
    >>> Tolerancia.por_nominal(25, 10)
    Tolerancia(minimo=22.5, maximo=27.5)
    >>> Tolerancia.de_texto("0,10 a 0,30").aprova(0.31)
    False
    >>> Tolerancia.converter_numero("1.250,5")
    1250.5

Dica: re.fullmatch (módulo 05) com grupos resolve o de_texto.

Teste com:  python curso.py testar 08 ex07
"""

import re

PADRAO_FAIXA = re.compile(r"\s*([\d.,]+)\s*a\s*([\d.,]+)\s*")
PADRAO_NOMINAL = re.compile(r"\s*([\d.,]+)\s*(?:±|\+-)\s*([\d.,]+)\s*%\s*")


class Tolerancia:
    """Faixa de aceitação [minimo, maximo]."""

    def __init__(self, minimo: float, maximo: float) -> None:
        if minimo > maximo:
            raise ValueError(f"Mínimo ({minimo}) maior que máximo ({maximo})")
        self.minimo = float(minimo)
        self.maximo = float(maximo)

    @classmethod
    def por_nominal(cls, nominal: float, percentual: float) -> "Tolerancia":
        """Faixa nominal ± percentual%."""
        if percentual < 0:
            raise ValueError("O percentual não pode ser negativo")
        margem = nominal * percentual / 100
        # cls, e não Tolerancia: numa subclasse, cls é a subclasse.
        return cls(nominal - margem, nominal + margem)

    @staticmethod
    def converter_numero(texto: str) -> float:
        """'1.250,5' -> 1250.5 (não usa nada do objeto nem da classe)."""
        return float(texto.strip().replace(".", "").replace(",", "."))

    @classmethod
    def de_texto(cls, texto: str) -> "Tolerancia":
        """Cria a tolerância a partir de '0,10 a 0,30' ou '25 ± 10%'."""
        achado = PADRAO_FAIXA.fullmatch(texto)
        if achado:
            minimo, maximo = (cls.converter_numero(g) for g in achado.groups())
            return cls(minimo, maximo)
        achado = PADRAO_NOMINAL.fullmatch(texto)
        if achado:
            nominal, percentual = (cls.converter_numero(g) for g in achado.groups())
            return cls.por_nominal(nominal, percentual)  # reaproveita o outro construtor
        raise ValueError(f"Formato de tolerância não reconhecido: {texto!r}")

    def aprova(self, valor: float) -> bool:
        """True se o valor está na faixa (limites inclusos)."""
        return self.minimo <= valor <= self.maximo

    def __repr__(self) -> str:
        return f"Tolerancia(minimo={self.minimo!r}, maximo={self.maximo!r})"
