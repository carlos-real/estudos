# Desafio do Módulo 08 — O Validador de Certificados orientado a objetos

## Contexto

Chegou a hora de modelar o coração do seu projeto com classes. Todo dia o
laboratório tem:

- **regras** por linha de produção: tolerâncias fixas (COF, tração) e uma
  especificação padrão (espessura e gramatura com nominal ± %), além de
  especificações **próprias** de algumas OPs (título + texto + tolerâncias);
- **pedidos** da expedição: OP, NF, cliente, peso e linha;
- **medições** da planilha, às vezes com uma observação de liberação, como
  `COF: liberado` ou `COF: pendente`.

O programa decide, para cada pedido, se o certificado **pode ser emitido** ou está
**bloqueado**, e por quê. Os arquivos estão em `../dados/`:

```text
regras.json     linhas A-D (fixas + padrao) e especificacoes_op
pedidos.csv     op;nf;cliente;peso_kg;linha            (UTF-8, ";", vírgula decimal)
medicoes.csv    op;ensaio;valor;unidade;observacao
```

## Requisitos obrigatórios

1. **Enums** para a linha de produção (A–D) e para a situação de cada ensaio
   (aprovado, liberado pela qualidade, pendente, reprovado, informativo).
2. **`Tolerancia`** como dataclass imutável, com mínimo e/ou máximo, um
   `@classmethod` para nominal ± % e outro para criar a partir do dicionário do JSON.
3. **`Especificacao`** (título, texto, tolerâncias) e **`LinhaDeProducao`** por
   **composição**: a linha tem tolerâncias fixas, uma especificação padrão e as
   especificações próprias das OPs. As tolerâncias de uma OP = fixas + as da
   especificação (a da especificação vence se o ensaio se repetir).
4. **Regra da observação**: um ensaio fora da tolerância vira "liberado pela
   qualidade" se a observação da medição disser `<ensaio>: liberado`, e "pendente" se
   disser `<ensaio>: pendente`. Ensaio medido sem tolerância é "informativo" e não
   bloqueia.
5. **`Certificado`** com `numero` (`CQ-AAAAMMDD-OP`), `pode_emitir` (property: há
   ensaio avaliado e nenhum reprovado ou pendente), a lista de pendências e o texto do
   certificado com números no formato brasileiro.
6. Linha de comando: `--data dd/mm/aaaa` (padrão: hoje), `--op OPxxxxx` (só uma OP) e
   `--saida pasta` (grava um `.txt` por certificado emitível). Arquivo inexistente:
   mensagem no `stderr` e código 2.
7. Nenhuma regra de negócio solta no `main()`: ele só lê argumentos, chama os objetos e
   imprime.

## Extras opcionais

- `__str__` e `__repr__` úteis em todas as classes.
- Um `Validador` que recebe as linhas e as medições e tem um método
  `certificar(pedido, emissao)`.
- Exportar um resumo em JSON (OP, situação, pendências).
- Escrever testes pytest para `Tolerancia`, `LinhaDeProducao.tolerancias_para` e a
  regra da observação (o módulo 09 aprofunda).

## Exemplo de execução

```text
> python 08-orientacao-a-objetos/desafio/solucao_referencia.py --op OP245118 --data 29/10/2026
CERTIFICADO DE QUALIDADE Nº CQ-20261029-OP245118
Cliente: Pet Nutri
OP: OP245118 | NF: 123460 | Linha: B | Peso: 1.105,00 kg
Especificação: Filme PE 25 µm
  Padrão da linha B
Emissão: 29/10/2026
- espessura: 25,60 µm [tol.: 22,5 a 27,5] -> aprovado
- gramatura: 23,60 g/m² [tol.: 20,7 a 25,3] -> aprovado
- cof: 0,33 [tol.: 0,1 a 0,3] -> liberado pela qualidade
- tração: 26,50 MPa [tol.: mín. 20] -> aprovado
=> PODE EMITIR

Resumo: 1 para emitir, 0 bloqueado(s).
```

Sem `--op`, os seis pedidos são avaliados e o resumo é
`3 para emitir, 3 bloqueado(s)`: OP245103 (espessura reprovada), OP245106 (espessura
fora da especificação **própria** da OP, embora dentro da padrão da linha) e
OP245109 (COF pendente de decisão).

## Critérios de aceite

- [ ] Com `--data 29/10/2026`, OP245101, OP245104 e OP245118 podem ser emitidas;
      OP245103, OP245106 e OP245109 ficam bloqueadas, com o motivo.
- [ ] OP245106 usa a especificação "Café Montanha - embalagem a vácuo"; OP245118 usa
      a padrão da linha B.
- [ ] O COF 0,33 da OP245118 aparece como "liberado pela qualidade".
- [ ] `--saida` grava `CQ-20261029-OP245118.txt` (e os demais emitíveis) em UTF-8.
- [ ] Pasta de dados inexistente: mensagem clara e código de saída 2, sem traceback.
- [ ] As regras estão nas classes (dá para testar `Tolerancia` e `LinhaDeProducao`
      sem ler arquivo nenhum).
- [ ] `ruff check` e `ruff format --check` passam.

## Dicas para começar

1. **Comece pelo modelo, não pelos arquivos.** Escreva `Tolerancia`, `Especificacao`
   e `LinhaDeProducao` e teste no REPL com valores digitados à mão.
2. Depois escreva as funções que leem os arquivos e **devolvem objetos**. O resto do
   programa não deve saber que existe CSV ou JSON.
3. Para a regra da observação, reaproveite o exercício 08.05 (`interpretar_observacao`).
4. Desenhe antes, no papel, quem "tem" quem (composição) e quem "é" quem (herança).
   Aqui quase tudo é "tem".
5. Compare com a `solucao_referencia.py` só depois de tentar.
