"""
Exercício 06.12 — Gravação segura de JSON
Nível: ★★★

Contexto: O arquivo regras.json guarda as tolerâncias de todas as linhas. Se o
programa der erro NO MEIO da gravação (ou a energia cair), o arquivo fica pela
metade e o robô do dia seguinte não funciona. A técnica profissional: gravar
num arquivo temporário e só no fim trocar pelo definitivo.

Tarefa: implemente `salvar_json_seguro(caminho, dados)`:
1. gere o JSON com indent=2 e ensure_ascii=False e grave-o, em UTF-8, num
   arquivo temporário na MESMA pasta, com o nome do destino + ".tmp"
   (para "regras.json", o temporário é "regras.json.tmp");
2. só depois que tudo deu certo, troque o temporário pelo destino com
   `temporario.replace(caminho)`;
3. se der erro ao gerar o JSON (por exemplo, TypeError porque `dados` tem um
   set), apague o temporário (se ele existir) e deixe o erro subir. O arquivo
   de destino antigo tem que continuar exatamente como estava.

Exemplos:
    >>> salvar_json_seguro(Path("regras.json"), {"linha": "A", "cof": [0.15, 0.3]})
    >>> salvar_json_seguro(Path("regras.json"), {"linhas": {"A", "B"}})
    Traceback (most recent call last):
      ...
    TypeError: Object of type set is not JSON serializable
    >>> Path("regras.json").read_text(encoding="utf-8")   # continua o antigo
    '{\\n  "linha": "A",\\n  "cof": [\\n    0.15,\\n    0.3\\n  ]\\n}'

Dica: `caminho.with_name(caminho.name + ".tmp")` monta o nome do temporário.
Use try/except com `raise` sozinho para relançar o mesmo erro depois de limpar.

Teste com:  python curso.py testar 06 ex12
"""

# Este exercício usa o módulo json.
# Apague o "# " do começo da linha abaixo para importá-lo:
# import json
from pathlib import Path


def salvar_json_seguro(caminho: Path, dados) -> None:
    """Grava JSON de forma atômica: temporário primeiro, troca no final."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
