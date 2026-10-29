# Desafio do módulo 05 — Leitor de e-mails da expedição

## Contexto

Toda carga que sai da fábrica gera um e-mail da expedição para o laboratório, com as
OPs, as NFs e os pesos. Hoje alguém lê cada e-mail, copia os números para uma planilha e
confere tudo à mão. Erros de digitação passam, pedidos repetidos passam, e "1.250" kg
às vezes vira "1,25".

Os e-mails foram salvos como `.txt` na pasta `dados/emails/` deste módulo. E, como na
vida real, cada um foi salvo de um jeito:

```text
dados/emails/
  2025-10-28_carga_embalagens_do_sul.txt         UTF-8, formato padrão
  2025-10-29_carga_flexpack.txt                  cp1252 (Bloco de Notas antigo), digitação variada
  2025-10-30_complemento_embalagens_do_sul.txt   UTF-8 com BOM, quebras de linha do Windows
```

Sua missão: escrever `leitor_emails.py`, um programa que lê todos esses arquivos e
imprime um resumo confiável.

## Requisitos obrigatórios

1. Ler **todos** os arquivos `.txt` da pasta `dados/emails/`, em ordem alfabética.
2. Decodificar cada arquivo corretamente, seja UTF-8, UTF-8 com BOM ou cp1252, e mostrar
   qual encoding foi usado. Nenhum `Ã§` e nenhum `�` na saída.
3. Extrair do cabeçalho o remetente (`De:`), o assunto (`Assunto:`) e o cliente
   (`Cliente:`), com o nome do cliente padronizado (como no ex01).
4. Extrair os pedidos aceitando as mesmas variações do ex12 (rótulos em maiúsculas ou
   minúsculas, `|` ou `;`, NF com pontos, `kg` opcional).
5. Para cada e-mail, imprimir os pedidos ordenados por OP no formato do ex14 (NF com 9
   dígitos e pontos, peso brasileiro alinhado) e a linha de total.
6. Apontar as **linhas para conferir**: linhas que falam de OP e também de NF ou peso,
   mas que não estão no formato de pedido (OP com 5 dígitos, peso "a confirmar"...).
7. No fim, um **resumo geral**: quantidade de e-mails, clientes (sem repetir, mesmo que
   escritos de jeitos diferentes), total de pedidos, peso total no formato brasileiro,
   lista das linhas para conferir e as **OPs repetidas** em mais de um e-mail.

## Extras opcionais

- Aceitar o caminho da pasta como argumento na linha de comando (`sys.argv`, uma prévia
  do módulo 07).
- Gerar o texto pronto de resposta à expedição: "Recebemos N pedidos (X kg). As linhas
  abaixo precisam de correção: ...".
- Avisar quando o mesmo pedido (OP e NF iguais) aparece duas vezes **no mesmo** e-mail.
- Destacar pesos muito acima da média (por exemplo, mais que o dobro), que podem ser
  erro de digitação.
- Salvar o resumo num arquivo `.txt` em UTF-8 (prévia do módulo 06).

## Exemplo de execução

Na pasta `curso-python`:

```text
python 05-texto-e-regex/desafio/leitor_emails.py
```

Saída esperada (a da solução de referência):

```text
==============================================================
E-mail : 2025-10-28_carga_embalagens_do_sul.txt  (UTF-8)
De     : expedicao@plastifort.com.br
Assunto: Certificados - carga de 28/10
Cliente: Embalagens do Sul Ltda
--------------------------------------------------------------
OP 123456 | NF 000.098.765 |   1.250,50 kg
OP 123457 | NF 000.098.766 |     980,00 kg
OP 123458 | NF 000.098.767 |   2.040,75 kg
Total: 3 pedidos           |   4.271,25 kg
==============================================================
E-mail : 2025-10-29_carga_flexpack.txt  (cp1252)
De     : Márcia (Expedição) <expedicao@plastifort.com.br>
Assunto: Liberação urgente - caminhão às 14h
Cliente: Flexpack Indústria e Comércio de Embalagens
--------------------------------------------------------------
OP 223344 | NF 000.012.345 |   2.000,00 kg
OP 223345 | NF 000.012.346 |     750,25 kg
Total: 2 pedidos           |   2.750,25 kg
  ! conferir: OP: 22335 | NF: 12347 | Peso: 500 kg
==============================================================
E-mail : 2025-10-30_complemento_embalagens_do_sul.txt  (UTF-8 com BOM)
De     : expedicao@plastifort.com.br
Assunto: Complemento da carga de 28/10
Cliente: Embalagens do Sul Ltda
--------------------------------------------------------------
OP 123457 | NF 000.098.766 |     980,00 kg
OP 334455 | NF 000.099.001 |   1.100,00 kg
Total: 2 pedidos           |   2.080,00 kg
  ! conferir: OP 334456 | NF 99002 | Peso: a confirmar
==============================================================
RESUMO GERAL
E-mails lidos  : 3
Clientes       : Embalagens do Sul Ltda, Flexpack Indústria e Comércio de Embalagens
Pedidos        : 7
Peso total     : 9.101,50 kg
Para conferir  : 2 linha(s)
  - 2025-10-29_carga_flexpack.txt: OP: 22335 | NF: 12347 | Peso: 500 kg
  - 2025-10-30_complemento_embalagens_do_sul.txt: OP 334456 | NF 99002 | Peso: a confirmar
OPs repetidas  :
  - OP 123457 em: 2025-10-28_carga_embalagens_do_sul.txt, 2025-10-30_complemento_embalagens_do_sul.txt
```

O seu layout pode ser diferente. O que importa são os números e os avisos.

## Critérios de aceite

- [ ] Roda sem erro com `python 05-texto-e-regex/desafio/leitor_emails.py`, sem pedir
      nada ao usuário.
- [ ] Os três e-mails aparecem com acentos corretos ("Márcia", "Expedição").
- [ ] São encontrados exatamente 7 pedidos, somando 9.101,50 kg.
- [ ] As 2 linhas com problema aparecem para conferência, e a frase "A OP 123459 vai na
      próxima carga." **não** aparece (ela não é um pedido).
- [ ] A OP 123457 é apontada como repetida.
- [ ] "Embalagens do Sul Ltda" aparece uma vez só na lista de clientes.
- [ ] Nenhuma conta é feita com texto: os pesos viram `float` na leitura e voltam a ser
      texto brasileiro só na impressão.
- [ ] Cada tarefa está numa função pequena com nome claro (decodificar, ler cabeçalho,
      ler pedidos, montar resumo...).
- [ ] Todas as regex usam `r"..."`, e as grandes estão compiladas em constantes.

## Dicas de como começar

1. **Comece pelos bytes.** Para chegar na pasta dos e-mails a partir do seu script, use
   `Path(__file__).resolve().parent.parent / "dados" / "emails"`: `Path(__file__)` é o
   caminho do próprio script, `.parent` sobe uma pasta (detalhes no módulo 06). Depois,
   `sorted(pasta.glob("*.txt"))` lista os arquivos e `arquivo.read_bytes()` lê os bytes.
2. **Decodifique antes de tudo.** Reaproveite a função `decodificar` da seção 8 da aula.
   Imprima as primeiras linhas de cada e-mail e confira os acentos antes de seguir.
3. **Reaproveite seus exercícios.** `limpar_nome` (ex01), `formatar_nf` (ex02),
   `float_para_br` (ex06), `ler_email_expedicao` (ex12) e `montar_resumo` (ex14) já
   fazem metade do trabalho. Copie-os para o seu arquivo.
4. **Um e-mail de cada vez.** Faça funcionar para o primeiro arquivo, depois rode nos
   três. O segundo e o terceiro existem justamente para quebrar o que funcionou no
   primeiro.
5. **Linhas para conferir.** Percorra as linhas: se casou com o padrão do pedido, é
   pedido; se não casou, mas tem "OP" e também "NF" ou "Peso", é suspeita.
6. **OPs repetidas.** Monte um dicionário `{op: [arquivos onde apareceu]}` e mostre só
   as OPs com mais de um arquivo.

A solução de referência está em `solucao_referencia.py`. Abra só depois de tentar.
