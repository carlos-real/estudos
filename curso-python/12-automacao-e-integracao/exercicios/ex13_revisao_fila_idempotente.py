"""
Exercício 12.13 — Revisão: fila de emissão idempotente
Nível: ★★★

Revisão de: funções como valores (módulo 04), CSV com ";" e tratamento de
erros (módulo 06), conjuntos e dicionários (módulo 03) + robôs (este módulo).

Contexto: o Agendador roda o robô às 7h e às 13h. Se a fila da manhã ainda
estiver na pasta à tarde, o robô NÃO pode emitir os mesmos certificados de
novo. E se um pedido falhar (a tela travou), os outros precisam continuar.
A solução é um "livro de registro": um CSV com tudo o que já foi emitido.

Tarefa: implemente processar_fila(pedidos, emitir, registro).
- `pedidos`: lista de dicionários com pelo menos "op" e "nf".
- `emitir`: uma FUNÇÃO que recebe um pedido e devolve o número do certificado
  (str), ou levanta uma exceção se algo der errado. Nos testes ela é falsa; no
  programa real, ela chama o robô.
- `registro`: caminho de um CSV com delimitador ";" e cabeçalho
  op;nf;certificado  (encoding utf-8). Se não existir, crie-o com o cabeçalho.
- Para cada pedido, na ordem:
  - se o par (op, nf) já está no registro -> não chame emitir; conte "pulados";
  - senão chame emitir(pedido):
    - deu certo -> acrescente a linha op;nf;certificado no registro NA HORA
      (não só no fim: se o PC desligar, o que já foi feito está anotado) e
      conte "emitidos";
    - levantou qualquer Exception -> conte "falhas", não registre, siga em frente.
- Pedidos repetidos dentro da mesma fila também só são emitidos uma vez.
- Devolva {"emitidos": n, "pulados": n, "falhas": n}.

Exemplos:
    >>> processar_fila(pedidos, emitir, Path("emitidos.csv"))   # 1ª vez
    {'emitidos': 3, 'pulados': 0, 'falhas': 0}
    >>> processar_fila(pedidos, emitir, Path("emitidos.csv"))   # 2ª vez
    {'emitidos': 0, 'pulados': 3, 'falhas': 0}

Dica: leia o registro uma vez para um set de tuplas (op, nf) e vá
acrescentando a esse set. Para gravar uma linha, abra com modo "a" e
newline="" e use csv.writer(arquivo, delimiter=";").

Teste com:  python curso.py testar 12 ex13
"""

from collections.abc import Callable
from pathlib import Path


def processar_fila(
    pedidos: list[dict], emitir: Callable[[dict], str], registro: Path
) -> dict[str, int]:
    """Emite os pedidos ainda não registrados; nunca emite o mesmo par (OP, NF) duas vezes."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
