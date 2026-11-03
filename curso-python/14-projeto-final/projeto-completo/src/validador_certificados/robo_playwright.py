"""ESQUELETO do robô do TOTVS com Playwright (Edge). NÃO é testado automaticamente.

Este arquivo mostra ONDE cada coisa vai entrar quando você tiver acesso à tela do
TOTVS. Os seletores abaixo são exemplos: a tela real é que manda.

Roteiro para implementar:
 1. Instale:  python -m pip install playwright   (o Edge já vem no Windows)
 2. Grave seus cliques uma vez, para descobrir os seletores:
        playwright codegen --channel msedge https://endereco-do-totvs
 3. Troque os seletores marcados com "AJUSTE" pelos que o codegen mostrou.
    Prefira get_by_role / get_by_label / get_by_text a seletores CSS frágeis.
    Se a tela estiver dentro de um iframe, use pagina.frame_locator(...).
 4. Rode em homologação (base de teste), NUNCA primeiro em produção.
 5. Guarde usuário e senha em variáveis de ambiente (TOTVS_USUARIO, TOTVS_SENHA)
    ou num arquivo .env que NÃO vai para o Git. Nunca no código.
 6. Só então troque o EmissorTotvs pelo EmissorTotvsPlaywright na cli.py.

Boas práticas que já estão no esqueleto: esperas explícitas (sem time.sleep), print
de tela em cada emissão e em cada falha, erro de UMA OP vira ErroEmissao (a série
continua), e o import do Playwright fica dentro do método (quem não usa o robô não
precisa instalar nada).
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path

from .emissao import Emissor, ErroEmissao
from .modelos import ItemFila

logger = logging.getLogger(__name__)

TEMPO_MAXIMO_MS = 30_000  # espera máxima por elemento (30 s)


class EmissorTotvsPlaywright(Emissor):
    """Emissor real. Use como gerenciador de contexto:

    with EmissorTotvsPlaywright(url, pasta_prints) as emissor:
        resultados = emitir_fila(fila, emissor, ja_emitidas)
    """

    ensaio = False

    def __init__(self, url: str, pasta_prints: Path, visivel: bool = True) -> None:
        self.url = url
        self.pasta_prints = Path(pasta_prints)
        self.visivel = visivel  # visível no começo: você acompanha o que o robô faz
        self._playwright = None
        self._navegador = None
        self._pagina = None

    # ------------------------------------------------------------------ ciclo de vida
    def __enter__(self) -> EmissorTotvsPlaywright:
        from playwright.sync_api import sync_playwright  # import tardio (dependência opcional)

        self.pasta_prints.mkdir(parents=True, exist_ok=True)
        self._playwright = sync_playwright().start()
        self._navegador = self._playwright.chromium.launch(
            channel="msedge", headless=not self.visivel
        )
        self._pagina = self._navegador.new_page()
        self._pagina.set_default_timeout(TEMPO_MAXIMO_MS)
        self._entrar()
        return self

    def __exit__(self, *_excecao) -> None:
        if self._navegador is not None:
            self._navegador.close()
        if self._playwright is not None:
            self._playwright.stop()

    # ------------------------------------------------------------------ passos
    def _entrar(self) -> None:
        pagina = self._pagina
        pagina.goto(self.url)
        # AJUSTE: rótulos/botões reais da tela de login
        pagina.get_by_label("Usuário").fill(os.environ["TOTVS_USUARIO"])
        pagina.get_by_label("Senha").fill(os.environ["TOTVS_SENHA"])
        pagina.get_by_role("button", name="Entrar").click()
        # AJUSTE: algo que só aparece depois do login (menu, nome do usuário...)
        pagina.get_by_text("Menu").wait_for()
        logger.info("login no TOTVS feito")

    def emitir(self, item: ItemFila) -> str:
        from playwright.sync_api import TimeoutError as TempoEsgotado

        pagina = self._pagina
        try:
            # AJUSTE: caminho até a rotina de certificado de qualidade
            pagina.get_by_role("menuitem", name="Certificado de Qualidade").click()
            pagina.get_by_label("Ordem de Produção").fill(item.op)
            pagina.get_by_label("Nota Fiscal").fill(item.nf)
            pagina.get_by_label("Peso").fill(f"{item.peso_kg:.2f}".replace(".", ","))
            pagina.get_by_role("button", name="Confirmar").click()
            # AJUSTE: onde a tela mostra o número do certificado gerado
            comprovante = pagina.get_by_test_id("numero-certificado").inner_text()
        except TempoEsgotado as erro:
            self._print_de_tela(f"falha_{item.op}_{item.nf}")
            raise ErroEmissao(f"tela não respondeu: {erro}") from erro
        self._print_de_tela(f"ok_{item.op}_{item.nf}")
        logger.info("certificado %s emitido para OP %s", comprovante, item.op)
        return comprovante

    def _print_de_tela(self, nome: str) -> None:
        carimbo = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._pagina.screenshot(path=self.pasta_prints / f"{carimbo}_{nome}.png")
