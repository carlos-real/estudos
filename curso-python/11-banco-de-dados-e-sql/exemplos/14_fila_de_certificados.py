"""Exemplo 14 — No mundo real: a fila de emissão de certificados, em SQL.

Para cada carga da expedição: pode emitir o certificado? Se não, por quê?

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/14_fila_de_certificados.py
"""

from utilitarios import abrir_banco_exemplo, mostrar

FILA = """
WITH situacao_op AS (                       -- passo 1: um resumo por OP
    SELECT op,
           COUNT(*)                 AS ensaios,
           SUM(resultado = 'FORA')  AS fora,
           SUM(valor IS NULL)       AS pendentes
    FROM ensaio
    GROUP BY op
)
SELECT x.op, x.nf, x.peso_kg, c.nome AS cliente,     -- passo 2: cada carga
       CASE
           WHEN o.status = 'CERTIFICADA'      THEN 'já certificada'
           WHEN s.ensaios IS NULL             THEN 'sem ensaios'
           WHEN s.fora > 0                    THEN 'ensaio fora'
           WHEN s.pendentes > 0               THEN 'ensaio pendente'
           WHEN o.status <> 'LIBERADA'        THEN 'OP ' || LOWER(o.status)
           ELSE 'EMITIR'
       END AS situacao
FROM expedicao AS x
JOIN op AS o ON o.numero = x.op
JOIN cliente AS c ON c.id = o.cliente_id
LEFT JOIN situacao_op AS s ON s.op = x.op
WHERE x.data BETWEEN :inicio AND :fim
ORDER BY situacao = 'EMITIR' DESC, x.op, x.nf
"""

banco = abrir_banco_exemplo()
# A expedição pediu certificado para mais duas cargas (como nos e-mails do módulo 05):
banco.executemany(
    "INSERT INTO expedicao (op, nf, peso_kg, data) VALUES (?, ?, ?, ?)",
    [(24533, "123490", 1500.0, "2026-10-29"), (24534, "123491", 800.0, "2026-10-29")],
)
mostrar(banco, FILA, {"inicio": "2026-10-25", "fim": "2026-10-31"})

resumo = """
SELECT COUNT(*) AS cargas, ROUND(SUM(x.peso_kg), 1) AS peso_kg
FROM expedicao AS x JOIN op AS o ON o.numero = x.op
WHERE o.status = 'LIBERADA' AND x.data BETWEEN :inicio AND :fim
"""
mostrar(banco, resumo, {"inicio": "2026-10-25", "fim": "2026-10-31"})
banco.close()
