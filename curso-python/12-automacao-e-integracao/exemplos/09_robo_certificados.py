"""Exemplo 09 — Robô de emissão de certificados com Playwright (modo ensaio).

O robô treina no SIMULADOR local (dados/simulador_certificados.html), uma página
que imita a tela de um ERP. Quando estiver seguro aqui, você adapta os seletores
para a tela real do Protheus (veja a aula, seção 11).

Instalação (uma vez, com o ambiente virtual ativado):
    pip install playwright
Não é preciso baixar navegador: usamos o Microsoft Edge que já vem no Windows
(channel="msedge"). Sem Edge (Linux/macOS), rode uma vez
    python -m playwright install chromium
e use a opção --navegador chromium.

Uso:
    python exemplos/09_robo_certificados.py               # ENSAIO: preenche e cancela
    python exemplos/09_robo_certificados.py --confirmar   # emite de verdade (no simulador)
    python exemplos/09_robo_certificados.py --headless    # sem abrir a janela
    python exemplos/09_robo_certificados.py --trace       # grava trace.zip para depurar
"""

from __future__ import annotations

import argparse
import csv
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import Page, expect, sync_playwright
except ImportError:  # Playwright não instalado: main() explica o que fazer
    sync_playwright = None

PASTA = Path(__file__).resolve().parent
SIMULADOR = PASTA.parent / "dados" / "simulador_certificados.html"
SAIDA = PASTA / "saida" / "robo"
REGISTRO = SAIDA / "emitidos.csv"

# Na vida real estes pedidos vêm dos e-mails da expedição (exemplo 07).
PEDIDOS = [
    {"op": "123456", "nf": "98765", "peso_kg": 1250.5, "linha": "B", "obs": "COF: liberado"},
    {"op": "123789", "nf": "98766", "peso_kg": 980.25, "linha": "A", "obs": ""},
    {"op": "12400", "nf": "98770", "peso_kg": 2310.0, "linha": "C", "obs": ""},  # OP errada
    {"op": "124050", "nf": "98771", "peso_kg": 640.0, "linha": "D", "obs": "Selagem: ok"},
]

log = logging.getLogger("robo")


# ----------------------------------------------------------------------------
# Peças pequenas e testáveis (não dependem do navegador)
# ----------------------------------------------------------------------------
def configurar_log(pasta: Path) -> Path:
    """Log no terminal E num arquivo por dia (o arquivo é o que você lê depois)."""
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = pasta / f"robo_{datetime.now():%Y-%m-%d}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(), logging.FileHandler(arquivo, encoding="utf-8")],
    )
    return arquivo


def formatar_peso(peso: float) -> str:
    """1250.5 -> '1.250,50' (o formato que a tela espera)."""
    return f"{peso:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def problemas_do_pedido(pedido: dict) -> list[str]:
    """Valida ANTES de abrir a tela. Lista vazia = pedido bom."""
    problemas = []
    if not re.fullmatch(r"\d{6}", pedido["op"]):
        problemas.append(f"OP inválida: {pedido['op']!r}")
    if pedido["peso_kg"] <= 0:
        problemas.append("peso deve ser positivo")
    if pedido["linha"] not in "ABCD":
        problemas.append(f"linha inválida: {pedido['linha']!r}")
    return problemas


def ler_registro(caminho: Path) -> set[tuple[str, str]]:
    """Pares (OP, NF) já emitidos. É isto que deixa o robô idempotente."""
    if not caminho.exists():
        return set()
    with caminho.open(encoding="utf-8", newline="") as f:
        return {(linha["op"], linha["nf"]) for linha in csv.DictReader(f, delimiter=";")}


def registrar(caminho: Path, pedido: dict, certificado: str) -> None:
    novo = not caminho.exists()
    with caminho.open("a", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f, delimiter=";")
        if novo:
            escritor.writerow(["op", "nf", "certificado", "data_hora"])
        escritor.writerow([pedido["op"], pedido["nf"], certificado, f"{datetime.now():%Y-%m-%d %H:%M:%S}"])


# ----------------------------------------------------------------------------
# Peças que conversam com o navegador
# ----------------------------------------------------------------------------
def preencher(page: Page, pedido: dict) -> None:
    # get_by_label acha o campo pelo texto do rótulo, como uma pessoa faria.
    # exact=True evita que "OP" case com outro rótulo que contenha "op".
    page.get_by_label("OP", exact=True).fill(pedido["op"])
    page.get_by_label("NF", exact=True).fill(pedido["nf"])
    page.get_by_label("Peso (kg)").fill(formatar_peso(pedido["peso_kg"]))
    page.get_by_label("Linha").select_option(pedido["linha"])
    page.get_by_label("Observação").fill(pedido["obs"])


def emitir(page: Page, pedido: dict, confirmar: bool, pasta_prints: Path) -> str | None:
    """Preenche a tela. Em ensaio, cancela; senão confirma e devolve o nº do certificado."""
    op = page.get_by_label("OP", exact=True)
    expect(op).to_be_empty()  # a tela está pronta para um pedido novo?

    preencher(page, pedido)
    page.screenshot(path=pasta_prints / f"{pedido['op']}_1_preenchido.png")

    mensagem = page.get_by_role("status")
    if not confirmar:
        page.get_by_role("button", name="Cancelar").click()
        expect(mensagem).to_have_text("Operação cancelada")
        return None

    page.get_by_role("button", name="Confirmar").click()
    # Espera o SISTEMA responder: sucesso ou erro. Nada de time.sleep()!
    expect(mensagem).to_have_text(re.compile(r"Certificado \d+ gerado|Erro"), timeout=15_000)
    texto = mensagem.inner_text()
    page.screenshot(path=pasta_prints / f"{pedido['op']}_2_resultado.png")
    if texto.startswith("Erro"):
        raise RuntimeError(f"a tela recusou o pedido: {texto}")
    return re.search(r"Certificado (\d+)", texto).group(1)


def rodar(page: Page, confirmar: bool, pasta_prints: Path) -> dict[str, int]:
    contagem = {"emitidos": 0, "ensaiados": 0, "pulados": 0, "falhas": 0}
    ja_emitidos = ler_registro(REGISTRO)
    for pedido in PEDIDOS:
        chave = (pedido["op"], pedido["nf"])
        if chave in ja_emitidos:
            log.info("OP %s / NF %s já emitida antes: pulando", *chave)
            contagem["pulados"] += 1
            continue
        problemas = problemas_do_pedido(pedido)
        if problemas:
            log.error("OP %s com dados inválidos: %s", pedido["op"], "; ".join(problemas))
            contagem["falhas"] += 1
            continue
        try:
            certificado = emitir(page, pedido, confirmar, pasta_prints)
        except (PlaywrightError, RuntimeError):
            log.exception("Falha na OP %s", pedido["op"])  # registra o traceback
            page.screenshot(path=pasta_prints / f"{pedido['op']}_ERRO.png")
            page.get_by_role("button", name="Cancelar").click()  # limpa a tela
            contagem["falhas"] += 1
            continue
        if certificado is None:
            log.info("[ENSAIO] OP %s preenchida e cancelada", pedido["op"])
            contagem["ensaiados"] += 1
        else:
            registrar(REGISTRO, pedido, certificado)
            ja_emitidos.add(chave)
            log.info("OP %s: certificado %s emitido", pedido["op"], certificado)
            contagem["emitidos"] += 1
    return contagem


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Robô de certificados (treino).")
    parser.add_argument("--confirmar", action="store_true", help="emite de verdade")
    parser.add_argument("--headless", action="store_true", help="não abre a janela")
    parser.add_argument("--navegador", choices=["msedge", "chromium"], default="msedge")
    parser.add_argument("--url", default=SIMULADOR.as_uri(), help="endereço da tela")
    parser.add_argument("--trace", action="store_true", help="grava saida/robo/trace.zip")
    args = parser.parse_args(argv)

    if sync_playwright is None:
        print("O Playwright não está instalado neste Python.")
        print("Instale com:  pip install playwright")
        print("No Windows, o robô usa o Edge já instalado (channel='msedge').")
        return 0

    configurar_log(SAIDA)
    pasta_prints = SAIDA / f"prints_{datetime.now():%Y-%m-%d_%H%M%S}"
    pasta_prints.mkdir(parents=True)
    log.info("Início. Modo: %s", "CONFIRMAR" if args.confirmar else "ENSAIO")

    with sync_playwright() as p:
        canal = "msedge" if args.navegador == "msedge" else None
        navegador = p.chromium.launch(
            channel=canal,
            headless=args.headless,
            slow_mo=0 if args.headless else 250,  # deixa você acompanhar com os olhos
        )
        contexto = navegador.new_context(viewport={"width": 1280, "height": 900})
        if args.trace:
            contexto.tracing.start(screenshots=True, snapshots=True)
        page = contexto.new_page()
        page.set_default_timeout(10_000)  # 10 s para cada ação, no máximo
        try:
            page.goto(args.url)
            expect(page.get_by_role("heading", name="Emissão de Certificado")).to_be_visible()
            contagem = rodar(page, args.confirmar, pasta_prints)
        finally:
            if args.trace:
                contexto.tracing.stop(path=SAIDA / "trace.zip")
            contexto.close()
            navegador.close()

    log.info("Fim. %s", contagem)
    return 1 if contagem["falhas"] else 0


if __name__ == "__main__":
    sys.exit(main())
