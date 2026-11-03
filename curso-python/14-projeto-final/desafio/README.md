# Desafio do módulo 14 — A API do Validador (extensão FastAPI)

## Contexto

O Validador já roda pela linha de comando. Agora o PCP quer consultar, por um
sistema deles, se uma OP pode ter certificado. E a supervisão quer ver as tolerâncias
de uma especificação sem abrir o banco. A resposta profissional é uma **API**: outra
porta de entrada para o **mesmo núcleo**.

A regra de ouro do desafio: a API **não reescreve regra nenhuma**. Ela importa o
pacote `validador_certificados` (do `projeto-completo/`) e só traduz HTTP para
objetos do domínio e de volta. Se você se pegar copiando a regra de tolerância para
dentro da API, pare: algo está errado na arquitetura.

## Requisitos obrigatórios

1. Uma função `criar_app(caminho_regras)` que carrega as especificações do banco
   **uma vez** e devolve o `FastAPI`.
2. `GET /saude` → `{"status": "ok", "especificacoes": <quantidade>}`.
3. `GET /especificacoes` → lista com título, texto, linha e tolerâncias de cada
   especificação. Aceita `?linha=A` para filtrar.
4. `GET /especificacoes/{titulo}` → uma especificação (sem diferenciar maiúsculas).
   Título inexistente → **404** com a mensagem no `detail`.
5. `POST /validar` com um corpo Pydantic: `op` (só dígitos, 4 a 6), `linha` (`A` a
   `D`), `especificacao` (opcional), `valores`, `nominais` e `observacao`. Responde
   `op`, `especificacao` usada, `aprovado`, `liberado`, `pode_emitir` e `motivos`.
   - Especificação desconhecida → **422** com a mensagem do núcleo.
   - Corpo inválido (linha "E", OP com letra) → **422** automático do Pydantic.
6. Testes com `TestClient` cobrindo cada rota e cada código de status.
7. A documentação automática em `/docs` mostra exemplos de corpo (`examples=`).

## Extras opcionais

- `POST /serie`: recebe a planilha (upload `.xlsx`) e uma lista de pedidos em JSON e
  devolve a triagem completa (fila + bloqueados). Dica: `UploadFile` e um arquivo
  temporário.
- Autenticação simples por token no cabeçalho (`X-Token`) com uma dependência.
- Guardar cada validação numa tabela `consulta` (histórico de quem perguntou o quê).
- Rodar a API como serviço no servidor da fábrica (ver "Para ir além" do módulo 13).

## Exemplo de execução

A solução de referência faz uma demonstração com o `TestClient` (sem abrir
servidor):

```text
python 14-projeto-final/desafio/solucao_referencia.py
GET  /saude                       -> 200 {'status': 'ok', 'especificacoes': 7}
GET  /especificacoes/esp-0412     -> 200 {'titulo': 'ESP-0412', 'tolerancias': 2}
GET  /especificacoes/ESP-9999     -> 404 {'detail': "especificação 'ESP-9999' não cadastrada"}
POST /validar                     -> 200 {'op': '24518', 'especificacao': 'PADRAO-A', 'aprovado': True, 'liberado': True, 'pode_emitir': True, 'motivos': []}
POST /validar                     -> 200 {'op': '24519', 'especificacao': 'PADRAO-A', 'aprovado': False, 'liberado': True, 'pode_emitir': False, 'motivos': ['espessura 44.8 fora de 40 ± 10% (36 a 44)']}
POST /validar                     -> 422 {'detail': "especificação 'ESP-9999' não cadastrada"}
POST /validar                     -> 422 {'erro_de_validacao_no_campo': 'linha'}
```

Para subir o servidor de verdade e testar no navegador:

```text
python 14-projeto-final/desafio/solucao_referencia.py --servir
```

Abra `http://127.0.0.1:8000/docs`, clique em `POST /validar`, "Try it out", e mande o
exemplo que já aparece preenchido.

## Critérios de aceite

- [ ] Nenhuma regra de negócio dentro da API: tudo vem de `validador_certificados`.
- [ ] O banco é aberto só para leitura e carregado uma vez, na criação do app.
- [ ] `GET /especificacoes/esp-0412` funciona (maiúsculas não importam).
- [ ] Título inexistente → 404; especificação desconhecida no `/validar` → 422.
- [ ] Corpo inválido → 422 sem você escrever um `if` sequer (Pydantic faz).
- [ ] `pode_emitir` só é `true` quando aprovado **e** liberado.
- [ ] Pelo menos 8 testes com `TestClient`, todos passando, sem servidor no ar.
- [ ] `ruff check` e `ruff format --check` limpos.
- [ ] `/docs` mostra exemplos de corpo prontos para testar.

## Dicas de como começar

1. Comece pelo `/saude` e por um teste dele. Só depois avance.
2. Crie os modelos Pydantic olhando para os dataclasses: `ToleranciaSaida` tem os
   mesmos campos de `Tolerancia`. `ToleranciaSaida(**vars(tolerancia))` converte.
3. No `/validar`, monte uma `Medicao` com `aba=f"Linha {linha}"` e reaproveite
   `escolher_especificacao`, `validar_medicao` e `esta_liberado`. São 15 linhas.
4. Transforme `EspecificacaoDesconhecida` em `HTTPException(422, detail=str(erro))`.
   É a camada de entrada traduzindo um erro do domínio para a língua do HTTP.
5. Para importar o pacote sem instalar, veja como a solução de referência mexe no
   `sys.path`. No seu repositório próprio, prefira `pip install -e .` e coloque a API
   em `src/validador_certificados/api.py`.
