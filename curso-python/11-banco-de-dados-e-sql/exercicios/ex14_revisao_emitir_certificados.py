"""
Exercício 11.14 — Revisão: emitir certificados numa transação
Nível: ★★★

Revisão intercalada: dataclass (módulo 08), datas (módulo 07), coleções e
funções (módulos 03 e 04) e transações com sqlite3 (este módulo).

Contexto: cada carga da expedição precisa de um certificado de qualidade. O
banco do laboratório ganhou uma tabela nova:
    CREATE TABLE certificado (
        id           INTEGER PRIMARY KEY,
        numero       TEXT NOT NULL UNIQUE,                -- 'CQ-2026-0001'
        expedicao_id INTEGER NOT NULL UNIQUE REFERENCES expedicao (id),
        emitido_em   TEXT NOT NULL                        -- 'AAAA-MM-DD'
    )

Tarefa: implemente emitir_certificados(conexao, data), que emite os
certificados pendentes e devolve a lista de Certificado (dataclass abaixo, já
pronta). Uma carga (linha de expedicao) recebe certificado quando:
  - ainda não tem certificado;
  - a OP dela está com status 'LIBERADA';
  - a OP tem pelo menos um ensaio e NENHUM ensaio com resultado 'FORA' ou
    com valor NULL.
Regras:
  - cargas processadas em ordem de expedicao.id;
  - número "CQ-AAAA-NNNN", com AAAA = ano de `data` e NNNN = sequência de 4
    dígitos que CONTINUA a partir do maior número já existente daquele ano
    (sem nenhum no ano, começa em 0001);
  - emitido_em = data no formato 'AAAA-MM-DD';
  - tudo numa transação: se qualquer INSERT falhar, nenhum certificado fica
    gravado e o erro sobe (sqlite3.IntegrityError, por exemplo).
Rodar de novo logo depois não emite nada (devolve lista vazia).

Exemplo (banco do laboratório):
    >>> emitidos = emitir_certificados(conexao, date(2026, 10, 30))
    >>> len(emitidos), emitidos[0]
    (6, Certificado(numero='CQ-2026-0001', op=24518, nf='123456', peso_kg=1250.5,
                    emitido_em='2026-10-30'))

Dica: um SELECT com JOIN e NOT EXISTS acha as cargas; para a sequência,
SELECT MAX(numero) ... WHERE numero LIKE 'CQ-2026-%' e int(numero[-4:]);
f"{n:04d}" escreve 7 como "0007".

Teste com:  python curso.py testar 11 ex14
"""

import sqlite3
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Certificado:
    """Certificado emitido (já pronto, não precisa mexer)."""

    numero: str
    op: int
    nf: str
    peso_kg: float
    emitido_em: str


def emitir_certificados(conexao: sqlite3.Connection, data: date) -> list[Certificado]:
    """Emite os certificados pendentes e devolve a lista, em ordem de carga."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
