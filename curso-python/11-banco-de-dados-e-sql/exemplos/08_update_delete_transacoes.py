"""Exemplo 08 — UPDATE, DELETE e transações (commit, rollback, with).

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/08_update_delete_transacoes.py
"""

import sqlite3

from utilitarios import abrir_banco_exemplo

banco = abrir_banco_exemplo()

# 1) Antes de alterar, SELECT com o MESMO WHERE para ver o que vai mudar
alvo = "WHERE status = 'ABERTA' AND numero IN (SELECT op FROM ensaio)"
print(banco.execute(f"SELECT numero FROM op {alvo}").fetchall())

cursor = banco.execute(f"UPDATE op SET status = 'LIBERADA' {alvo}")
print("UPDATE alterou", cursor.rowcount, "linha(s)")
banco.rollback()  # desistimos: tudo volta como estava antes do último commit
print(banco.execute("SELECT status FROM op WHERE numero = 24534").fetchone())

# 2) DELETE: sem WHERE apagaria a tabela inteira!
cursor = banco.execute("DELETE FROM ensaio WHERE valor IS NULL")
print("DELETE apagou", cursor.rowcount, "linha(s)")
banco.commit()

# 3) Transação com "with": commit se tudo der certo, rollback se der erro.
#    Exemplo: certificar a OP 24541 = gravar a expedição E mudar o status, juntos.
try:
    with banco:
        banco.execute(
            "INSERT INTO expedicao (op, nf, peso_kg, data) VALUES (?, ?, ?, ?)",
            (24541, "123480", 250.0, "2026-10-30"),
        )
        banco.execute("UPDATE op SET status = 'CERTIFICADA' WHERE numero = ?", (24541,))
        banco.execute(
            "INSERT INTO expedicao (op, nf, peso_kg, data) VALUES (?, ?, ?, ?)",
            (24541, "123481", -1, "2026-10-30"),  # peso inválido: CHECK falha
        )
except sqlite3.IntegrityError as erro:
    print("Erro, nada foi gravado:", erro)

print(banco.execute("SELECT status FROM op WHERE numero = 24541").fetchone())
print(banco.execute("SELECT COUNT(*) FROM expedicao WHERE nf = '123480'").fetchone())

# 4) "with banco" NÃO fecha a conexão. Feche você (ou use contextlib.closing).
banco.close()
