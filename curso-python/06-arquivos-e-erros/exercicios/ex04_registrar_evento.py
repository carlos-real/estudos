"""
Exercício 06.04 — Escrever um registro (log)
Nível: ★☆☆

Contexto: O robô dos certificados precisa deixar um rastro do que fez: um
arquivo de texto com uma linha por evento. Se o robô parar no meio, o registro
mostra até onde ele chegou.

Tarefa: implemente `registrar_evento(caminho, momento, mensagem)`:
- acrescente ao FIM do arquivo a linha f"{momento} | {mensagem}", seguida de
  uma quebra de linha;
- se o arquivo não existir, ele deve ser criado; se as pastas do caminho não
  existirem, crie-as também;
- nunca apague o que já estava no arquivo;
- use UTF-8.
A função não devolve nada.

Exemplos:
    >>> log = Path("logs") / "robo.log"
    >>> registrar_evento(log, "2025-10-28 08:00", "Início")
    >>> registrar_evento(log, "2025-10-28 08:01", "Certificado da OP 123456 emitido")
    >>> print(log.read_text(encoding="utf-8"), end="")
    2025-10-28 08:00 | Início
    2025-10-28 08:01 | Certificado da OP 123456 emitido

Dica: modo "a" (append). Para as pastas: `caminho.parent.mkdir(...)` com os
argumentos que evitam erro quando a pasta já existe.

Teste com:  python curso.py testar 06 ex04
"""

from pathlib import Path


def registrar_evento(caminho: Path, momento: str, mensagem: str) -> None:
    """Acrescenta "momento | mensagem" numa nova linha no fim do arquivo."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
