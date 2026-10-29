"""Exemplo 10 — Log em arquivo e idempotência: rodar duas vezes não duplica nada.

Processa os e-mails de dados/emails/ e anota o Message-ID de cada um num
arquivo JSON. Na segunda rodada, os e-mails já vistos são pulados.

Rode com:  python exemplos/10_log_e_idempotencia.py
"""

import json
import logging
import tempfile
from email import policy
from email.parser import BytesParser
from pathlib import Path

PASTA_EMAILS = Path(__file__).resolve().parent.parent / "dados" / "emails"

log = logging.getLogger("leitor_de_pedidos")


def carregar_vistos(caminho: Path) -> set[str]:
    if not caminho.exists():
        return set()
    return set(json.loads(caminho.read_text(encoding="utf-8")))


def salvar_vistos(caminho: Path, vistos: set[str]) -> None:
    # Grava num arquivo temporário e troca no fim: se o PC desligar no meio,
    # o arquivo antigo continua inteiro (gravação "atômica").
    temporario = caminho.with_suffix(".tmp")
    temporario.write_text(json.dumps(sorted(vistos), indent=2), encoding="utf-8")
    temporario.replace(caminho)


def processar(pasta: Path, arquivo_vistos: Path) -> int:
    vistos = carregar_vistos(arquivo_vistos)
    novos = 0
    for caminho in sorted(pasta.glob("*.eml")):
        msg = BytesParser(policy=policy.default).parsebytes(caminho.read_bytes())
        identificador = msg["Message-ID"]
        if identificador in vistos:
            log.debug("%s já processado, pulando", caminho.name)
            continue
        log.info("Novo pedido: %s | %s", caminho.name, msg["Subject"])
        vistos.add(identificador)
        salvar_vistos(arquivo_vistos, vistos)  # salva a cada item, não só no fim
        novos += 1
    return novos


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        arquivo_log = Path(tmp) / "leitor.log"
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)-5s %(message)s",
            handlers=[logging.StreamHandler(), logging.FileHandler(arquivo_log, encoding="utf-8")],
        )
        vistos = Path(tmp) / "vistos.json"

        print("--- 1ª rodada ---")
        print("novos:", processar(PASTA_EMAILS, vistos))
        print("--- 2ª rodada (nada mudou na pasta) ---")
        print("novos:", processar(PASTA_EMAILS, vistos))

        linhas = arquivo_log.read_text(encoding="utf-8").splitlines()
        print(f"--- o arquivo de log tem {len(linhas)} linhas; a primeira é: ---")
        print(linhas[0])
        logging.shutdown()  # fecha o arquivo de log antes de apagar a pasta


if __name__ == "__main__":
    main()
