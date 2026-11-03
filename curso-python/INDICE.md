# Índice detalhado do curso

Gerado por `ferramentas/gerar_indice.py` a partir das aulas e dos exercícios.
Use para achar em que módulo e seção cada assunto é ensinado.

## Módulo 00 — Preparação do ambiente

Pasta: `00-preparacao/`

**Seções da aula:**

- 1. O que é programar (e o que o Python faz com o seu código)
- 2. Instalando o Python no Windows
- 3. VS Code e a extensão Python
- 4. Git for Windows: instalar e configurar
- 5. O terminal (PowerShell) sem medo
- 6. O REPL: conversando com o Python
- 7. Seu primeiro script
- 8. Baixando o curso: clonar (ou atualizar) o repositório
- 9. Ambiente virtual (venv) e pip
- 10. O molde dos exercícios: `def` e `return`
- 11. Seu primeiro teste: o ciclo do curso
- 12. Git no dia a dia: status, add, commit, push, pull
- 13. Como estudar este curso
- Lendo mensagens de erro deste módulo
- Você domina este módulo se...

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_ola_mundo` | Olá, mundo! | ★☆☆ | implemente `ola_mundo()`, que DEVOLVE (com `return`) exatamente o texto "Olá, mundo!": |
| `ex02_saudacao` | Saudação personalizada | ★☆☆ | implemente `saudar(nome)`, que DEVOLVE o texto "Olá, <nome>!". |
| `ex03_peso_total` | Peso total da carga | ★☆☆ | implemente `peso_total(peso_bobina_kg, quantidade)`, que DEVOLVE o peso total: |

**Desafio:** Desafio 00 — Ambiente pronto e primeiro push

## Módulo 01 — Fundamentos

Pasta: `01-fundamentos/`

**Seções da aula:**

- 1. Dois jeitos de rodar Python: REPL e script
- 2. print: o programa falando com você
- 3. Comentários: notas para humanos
- 4. Variáveis e nomes
- 5. Tipos de dados: int, float, str, bool e None
- 6. Operadores aritméticos e precedência
- 7. Atribuição composta: atualizando valores
- 8. Strings básicas: trabalhando com texto
- 9. Conversões: int(), float() e str()
- 10. input(): perguntando ao usuário
- 11. f-strings e formatação de números
- 12. O problema do float e o round()
- 13. O módulo math
- 14. O molde dos exercícios: def e return
- 15. Pensando como programador
- Lendo mensagens de erro deste módulo

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_apresentacao` | Apresentação | ★☆☆ | implemente `apresentar(nome, idade, cidade)`, que DEVOLVE (com return, sem print) exatamente a frase: |
| `ex02_cabecalho` | Cabeçalho de laudo | ★☆☆ | implemente `imprimir_cabecalho(titulo, largura)`, que IMPRIME (com print) três linhas: |
| `ex03_media_notas` | Média de notas | ★☆☆ | 1. |
| `ex04_celsius_fahrenheit` | Celsius e Fahrenheit | ★☆☆ | 1. |
| `ex05_contem_termo` | Procurar um termo na observação | ★☆☆ | implemente `contem_termo(texto, termo)`, que devolve True se `termo` aparece dentro de `texto` e False caso contrário. |
| `ex06_peso_liquido` | Peso líquido do palete | ★★☆ | implemente `calcular_peso_liquido(peso_bruto_kg, tara_palete_kg, qtd_bobinas, peso_tubete_kg)`, que devolve: |
| `ex07_dividir_conta` | Dividir a conta | ★★☆ | 1. |
| `ex08_normalizar_op` | Normalizar o número da OP | ★★☆ | implemente `normalizar_op(texto)`, que: |
| `ex09_gramatura` | Gramatura e peso da bobina | ★★☆ | 1. |
| `ex10_faixa_tolerancia` | Faixa de tolerância | ★★☆ | 1. |
| `ex11_texto_para_numero` | Texto para número | ★★☆ | 1. |
| `ex12_formatar_reais` | Formatar em reais | ★★★ | implemente `formatar_reais(valor)`, que devolve o valor no formato "R$ 1.234,56": |
| `ex13_diametro_bobina` | Diâmetro da bobina | ★★★ | 1. |
| `ex14_tempo_de_producao` | Tempo de produção | ★★★ | 1. |

**Desafio:** Desafio do módulo 01 — Ficha de medição da bobina

## Módulo 02 — Decisões e repetições

Pasta: `02-decisoes-e-repeticoes/`

**Seções da aula:**

- 1. Comparações: perguntas de sim ou não
- 2. Combinando condições: and, or e not
- 3. if, elif e else: o programa decide
- 4. Expressão condicional: um if numa linha
- 5. Truthy e falsy: o que conta como verdadeiro
- 6. match-case: escolhendo entre vários casos
- 7. while: repetir enquanto for verdade
- 8. for e range: repetir para cada item
- 9. Percorrendo uma lista recebida
- 10. break e continue: controlando o laço por dentro
- 11. Contadores e acumuladores
- 12. Padrões clássicos: buscar, contar, maior e menor
- 13. Laços aninhados
- 14. Validação de dados: não confie na entrada
- 15. Depurando laços: o teste de mesa
- Lendo mensagens de erro deste módulo
- Você domina este módulo se...

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_situacao_aluno` | Situação do aluno | ★☆☆ | implemente `situacao(media)`, que devolve: |
| `ex02_dentro_da_faixa` | Dentro da faixa? | ★☆☆ | 1. |
| `ex03_ano_bissexto` | Ano bissexto | ★☆☆ | 1. |
| `ex04_tolerancia_da_linha` | Tolerância da linha | ★☆☆ | implemente `tolerancia_da_linha(linha)`, que devolve a tolerância (float) da linha informada, ou None se a linha não existir. |
| `ex05_contar_vogais` | Contar vogais | ★☆☆ | implemente `contar_vogais(texto)`, que devolve quantas vogais o texto tem. |
| `ex06_fatorial` | Fatorial e soma acumulada | ★☆☆ | 1. |
| `ex07_classificar_medicao` | Classificar uma medição | ★★☆ | implemente `classificar_medicao(valor, nominal, tolerancia_pct)`, que: |
| `ex08_media_das_medicoes` | Média das medições válidas | ★★☆ | 1. |
| `ex09_amplitude` | Maior, menor e amplitude | ★★☆ | o objetivo é praticar o padrão): |
| `ex10_anos_para_dobrar` | Quanto tempo até a meta? | ★★☆ | 1. |
| `ex11_leitura_de_lacos` | Leitura de código: preveja e conserte | ★★☆ | Programador passa mais tempo LENDO código do que escrevendo. |
| `ex12_sequencia_fora` | Três seguidas fora: pare a linha | ★★★ | implemente `inicio_sequencia_fora(valores, minimo, maximo, tamanho)`, que devolve a POSIÇÃO (contando a partir de 1) da medição que inicia a primeira sequência de `tamanho` medições consecutivas fora da faixa [minimo,... |
| `ex13_revisao_tabela_limites` | Revisão: tabela de limites por linha | ★★★ | implemente `tabela_limites(linhas, nominais)`: |
| `ex14_revisao_resumo_serie` | Revisão: resumo de uma série vinda da planilha | ★★★ | 1. |

**Desafio:** Desafio do módulo 02 — Inspetor de série no terminal

## Módulo 03 — Coleções: listas, tuplas, dicionários e conjuntos

Pasta: `03-colecoes/`

**Seções da aula:**

- 1. Listas: vários valores numa variável só
- 2. Fatiamento: recortando pedaços
- 3. Modificando listas: os métodos
- 4. Mutabilidade: cópia ou referência?
- 5. Tuplas e desempacotamento
- 6. Percorrendo melhor: `enumerate` e `zip`
- 7. Dicionários: buscar pelo nome, não pela posição
- 8. Dicionários aninhados: a tabela de tolerâncias
- 9. Conjuntos: sem repetição, com matemática
- 10. Compreensões: montar coleções numa linha
- 11. Funções embutidas que economizam laços
- 12. Lista de dicionários: sua primeira tabela
- 13. Qual coleção usar?
- Lendo mensagens de erro deste módulo
- Você domina este módulo se...

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_ultimas_medicoes` | Últimas medições | ★☆☆ | implemente `ultimas_medicoes(medicoes, n)`, que devolve uma lista NOVA com as `n` últimas medições, na ordem original. |
| `ex02_resumo_espessura` | Resumo de espessura | ★☆☆ | implemente `resumo_espessura(medicoes)`, que devolve um dicionário com as chaves exatamente nesta forma: |
| `ex03_dentro_da_tolerancia` | Dentro da tolerância? | ★☆☆ | implemente `dentro_da_tolerancia(valor, linha, tolerancias)`. |
| `ex04_contar_votos` | Enquete do refeitório | ★☆☆ | implemente duas funções. |
| `ex05_remover_duplicadas` | Lotes sem repetição | ★☆☆ | implemente `remover_duplicadas(itens)`, que devolve uma lista NOVA: |
| `ex06_fora_da_faixa` | Medições fora da faixa | ★★☆ | implemente duas funções. |
| `ex07_pesos_por_op` | Peso total por OP | ★★☆ | implemente `pesos_por_op(ops, pesos)`. |
| `ex08_leitura_copia_referencia` | Leitura de código: cópia ou referência? | ★★☆ | Um colega escreveu um script de correção de medições e jura que "o Python mudou a lista sozinho". |
| `ex09_ranking_alunos` | Ranking da turma | ★★☆ | implemente duas funções. |
| `ex10_conferir_ops` | OPs pedidas x OPs com resultado | ★★☆ | implemente `conferir_ops(ops_pedidas, ops_com_resultado)`, que devolve um dicionário com três listas, cada uma SEM repetidos e em ordem alfabética: |
| `ex11_resumo_por_linha` | Resumo por linha (o seu primeiro GROUP BY) | ★★★ | implemente duas funções (a segunda usa a primeira). |
| `ex12_revisao_tolerancias` | Revisão: relatório de tolerâncias | ★★★ | implemente quatro funções pequenas, cada uma usando a anterior. |
| `ex13_revisao_juntar_tabelas` | Revisão: juntar pedidos e resultados (o seu primeiro JOIN) | ★★★ | implemente quatro funções. |

**Desafio:** Desafio do módulo 03 — Painel de conferência do lote

## Módulo 04 — Funções: organize, reutilize e decomponha problemas

Pasta: `04-funcoes/`

**Seções da aula:**

- 1. Funções: dar nome a uma ideia
- 2. Parâmetros e argumentos
- 3. Valores padrão (e a armadilha do padrão mutável)
- 4. Vários retornos e retorno antecipado
- 5. Escopo: onde cada nome vive
- 6. Docstrings e type hints
- 7. `*args` e `**kwargs`: quantos argumentos vierem
- 8. Funções são valores
- 9. `lambda` e o parâmetro `key=`
- 10. Funções puras e efeitos colaterais
- 11. Decomposição de problemas
- 12. Recursão (introdução)
- Lendo mensagens de erro deste módulo
- Você domina este módulo se...

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_dividir_lote` | Dividir o lote em bobinas | ★☆☆ | implemente duas funções. |
| `ex02_formatar_medida` | Formatar medidas para o laudo | ★☆☆ | implemente `formatar_medida(valor, unidade="µm", casas=1, decimal=".")`. |
| `ex03_conceito_nota` | Conceito e situação do aluno | ★☆☆ | implemente duas funções usando RETORNO ANTECIPADO (um return por caso, sem if aninhado). |
| `ex04_media_args` | Média com quantos valores vierem | ★☆☆ | implemente duas funções com *args. |
| `ex05_padrao_mutavel` | A armadilha do padrão mutável | ★☆☆ | implemente `adicionar_defeito(defeito, defeitos=None)` do jeito certo. |
| `ex06_funcoes_como_valores` | CONT.SE e SOMASE em Python | ★★☆ | implemente três funções. |
| `ex07_ordenar_com_key` | Ordenar com key e lambda | ★★☆ | implemente três funções, cada uma com UMA chamada a min ou sorted. |
| `ex08_filtrar_kwargs` | Filtros com **kwargs | ★★☆ | implemente duas funções. |
| `ex09_leitura_escopo` | Leitura de código: escopo, padrão mutável e print × return | ★★☆ | Antes de escrever funções, todo programador passa muito tempo LENDO funções dos outros. |
| `ex10_soma_recursiva` | Recursão: pesos aninhados | ★★☆ | implemente duas funções RECURSIVAS (que chamam a si mesmas). |
| `ex11_laudo_decomposto` | Laudo decomposto em funções pequenas | ★★★ | implemente as cinco funções, nesta ordem (de baixo para cima). |
| `ex12_revisao_validar_pedido` | Revisão: validar os pedidos da expedição | ★★★ | implemente cinco funções. |
| `ex13_revisao_pipeline_limpeza` | Revisão: pipeline de limpeza de códigos | ★★★ | implemente três funções. |

**Desafio:** Desafio do módulo 04 — Fila de emissão de certificados

## Módulo 05 — Texto e expressões regulares

Pasta: `05-texto-e-regex/`

**Seções da aula:**

- 1. Strings por dentro
- 2. Procurando dentro do texto
- 3. Limpando e padronizando
- 4. Quebrando e juntando: split, partition e join
- 5. Formatação avançada com f-strings
- 6. Números no formato brasileiro
- 7. Unicode e acentos
- 8. Encodings: o mistério do "ExpediÃ§Ã£o"
- 9. Expressões regulares: a ideia
- 10. Construindo um padrão aos poucos
- 11. search, match, fullmatch, findall e finditer
- 12. Grupos e grupos nomeados
- 13. Substituindo e dividindo: re.sub e re.split
- 14. Flags e re.compile
- 15. Projeto guiado: lendo o e-mail da expedição
- Lendo mensagens de erro deste módulo
- Você domina este módulo se...

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_limpar_nome` | Padronizar nome de cliente | ★☆☆ | implemente `limpar_nome(nome)`, que devolve o nome padronizado: |
| `ex02_formatar_nf` | Formatar número de NF | ★☆☆ | implemente `formatar_nf(numero)`: |
| `ex03_separar_campo` | Separar rótulo e valor | ★☆☆ | implemente `separar_campo(linha)`, que devolve uma tupla (rótulo, valor): |
| `ex04_br_para_float` | Converter número brasileiro | ★☆☆ | implemente `br_para_float(texto)`: |
| `ex05_validar_op` | Validar código de OP | ★☆☆ | implemente `validar_op(codigo)`, que devolve True ou False. |
| `ex06_float_para_br` | Número no formato brasileiro | ★★☆ | implemente `float_para_br(valor, casas=2)`: |
| `ex07_normalizar_chave` | Normalizar nome de coluna | ★★☆ | implemente `normalizar_chave(texto)`, seguindo NESTA ORDEM: |
| `ex08_extrair_ops` | Encontrar OPs num texto | ★★☆ | implemente `extrair_ops(texto)`, que devolve a lista dos números de OP (como texto, 6 dígitos) na ordem em que aparecem, SEM repetir. |
| `ex09_ler_medicao` | Ler uma linha de medição | ★★☆ | implemente `ler_medicao(linha)`. |
| `ex10_padronizar_datas` | Datas no padrão ISO | ★★☆ | implemente `padronizar_datas(texto)`, que troca cada data dia/mês/ano por ano-mês-dia e devolve o texto novo: |
| `ex11_depurar_peso` | Depure a função do estagiário | ★★☆ | sem executar o código, preveja o que `extrair_peso_original` faz em cada caso e complete `previsoes()`, que devolve uma tupla com 3 respostas: |
| `ex12_ler_email_expedicao` | Ler o e-mail da expedição | ★★★ | implemente `ler_email_expedicao(texto)`, que devolve uma lista com um dicionário por pedido, na ordem do e-mail: |
| `ex13_revisao_tolerancias` | Revisão: ler a especificação da OP | ★★★ | implemente `ler_tolerancias(texto)`, que devolve um dicionário {chave_do_ensaio: |
| `ex14_revisao_resumo` | Revisão: resumo para responder a expedição | ★★★ | implemente `montar_resumo(pedidos)`. |

**Desafio:** Desafio do módulo 05 — Leitor de e-mails da expedição

## Módulo 06 — Arquivos e tratamento de erros

Pasta: `06-arquivos-e-erros/`

**Seções da aula:**

- 1. Quando algo dá errado: exceções
- 2. try/except: tratando o erro
- 3. else e finally
- 4. raise: levantando seus próprios erros
- 5. Exceções personalizadas
- 6. Arquivos de texto: open e with
- 7. pathlib: caminhos sem dor
- 8. Encoding na prática: Excel, utf-8-sig e cp1252
- 9. CSV no padrão do Excel brasileiro
- 10. JSON: configurações e regras
- 11. Leitura e escrita segura
- 12. Validação defensiva
- Lendo mensagens de erro deste módulo
- Você domina este módulo se...

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_ler_numero` | Converter sem quebrar | ★☆☆ | implemente `ler_numero(texto, padrao=None)`: |
| `ex02_conferir_tolerancia` | Levantar erro fora da tolerância | ★☆☆ | implemente `conferir_tolerancia(valor, minimo, maximo)`: |
| `ex03_ler_linhas` | Ler um arquivo de texto | ★☆☆ | implemente `ler_linhas(caminho)`: |
| `ex04_registrar_evento` | Escrever um registro (log) | ★☆☆ | implemente `registrar_evento(caminho, momento, mensagem)`: |
| `ex05_listar_planilhas` | Listar as planilhas de uma pasta | ★☆☆ | implemente `listar_planilhas(pasta)`, que devolve a lista com os NOMES (não os caminhos) dos arquivos da pasta que são planilhas: |
| `ex06_ler_texto_excel` | Ler arquivo vindo do Excel | ★★☆ | implemente `ler_texto_excel(caminho)`, que devolve uma tupla (texto, encoding): |
| `ex07_ler_csv_br` | Ler CSV do Excel brasileiro | ★★☆ | implemente `ler_csv_br(caminho, colunas_numericas)`: |
| `ex08_escrever_csv_br` | Gerar CSV que abre certo no Excel | ★★☆ | implemente `escrever_csv_br(caminho, linhas, casas=2)`: |
| `ex09_hierarquia_excecoes` | Suas próprias exceções | ★★☆ | crie TRÊS classes de exceção (seção 5 da aula): |
| `ex10_carregar_config` | Configuração em JSON | ★★☆ | implemente `carregar_config(caminho, padrao)`: |
| `ex11_depurar_media` | Depure a média que mente | ★★☆ | preveja o que a função original devolve em cada caso e complete `previsoes()`, que devolve uma tupla com 4 respostas (números): |
| `ex12_salvar_json_seguro` | Gravação segura de JSON | ★★★ | implemente `salvar_json_seguro(caminho, dados)`: |
| `ex13_revisao_ler_medicoes` | Revisão: leitura validada de medições | ★★★ | implemente `ler_medicoes(caminho)`, que devolve uma lista de dicionários {"lote": |
| `ex14_revisao_conferir_pasta` | Revisão: conferir uma pasta inteira sem parar no erro | ★★★ | implemente `conferir_pasta(pasta, minimo, maximo, saida)`: |

**Desafio:** Desafio do módulo 06 — Conferência de laudos em lote

## Módulo 07 — Módulos, pacotes e biblioteca padrão

Pasta: `07-modulos-e-biblioteca-padrao/`

**Seções da aula:**

- 1. Módulo: um arquivo `.py` que outro arquivo usa
- 2. As formas de importar
- 3. `if __name__ == "__main__":` — script e módulo ao mesmo tempo
- 4. Onde o Python procura módulos
- 5. Pacotes: pastas com `__init__.py`
- 6. Estrutura de projeto profissional: o src layout
- 7. Ambiente virtual e pip a fundo
- 8. Poetry: o gerenciador que já está no seu repositório
- 9. Datas e prazos com `datetime`
- 10. `collections`: Counter, defaultdict e namedtuple
- 11. `itertools`: chain e groupby
- 12. `statistics`: a estatística do laboratório
- 13. `math` e `random`
- 14. `os`, `sys` e `time`
- 15. `argparse`: programas de linha de comando
- Lendo mensagens de erro deste módulo
- Você domina este módulo se...

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_comprimento_bobina` | Comprimento da bobina e bobinas por pedido | ★☆☆ | 1. |
| `ex02_validade_laudo` | Validade do laudo | ★☆☆ | 1. |
| `ex03_datas_brasileiras` | Datas no formato brasileiro | ★☆☆ | 1. |
| `ex04_estatistica_ensaio` | Estatística de um ensaio | ★☆☆ | 1. |
| `ex05_contar_reprovacoes` | Reprovações por linha com Counter | ★☆☆ | 1. |
| `ex06_sorteio_amostras` | Sorteio de bobinas para auditoria | ★★☆ | 1. |
| `ex07_agrupar_expedicao` | Agrupar a expedição por NF | ★★☆ | 1. |
| `ex08_sequencias_groupby` | Sequências de resultados com groupby | ★★☆ | 1. |
| `ex09_corrigir_dias_uteis` | Leitura de código: o prazo que caía no sábado | ★★☆ | 1. |
| `ex10_parser_cli` | Argumentos de linha de comando com argparse | ★★☆ | python validador.py valores.xlsx --linha B --tolerancia 7.5 --desde 01/10/2026 -v Antes de validar qualquer coisa, o programa precisa entender esses argumentos. |
| `ex11_cli_relatorio` | Programa de terminal completo: relatório de CV por linha | ★★★ | 1. |
| `ex12_revisao_expedicao` | Revisão: o e-mail da expedição com datas e agrupamento | ★★★ | 1. |
| `ex13_revisao_relatorio_csv` | Revisão: do CSV do laboratório ao JSON da expedição | ★★★ | 1. |

**Desafio:** Desafio do Módulo 07 — Agenda de validade de laudos

## Módulo 08 — Orientação a objetos

Pasta: `08-orientacao-a-objetos/`

**Seções da aula:**

- 1. O problema: dados soltos
- 2. Classes e objetos
- 3. `__init__` e `self`
- 4. Métodos e atributos de classe
- 5. `__str__` e `__repr__`
- 6. Encapsulamento: o que é de dentro e o que é de fora
- 7. `@property`: atributo com validação
- 8. `@classmethod` e `@staticmethod`
- 9. Herança e `super()`
- 10. Polimorfismo e "duck typing"
- 11. Composição: "tem um" em vez de "é um"
- 12. `dataclasses`: classes de dados sem repetição
- 13. Igualdade: `is`, `==`, `__eq__` e `__hash__`
- 14. `Enum`: conjuntos fechados de valores
- 15. Outros métodos especiais
- 16. Quando NÃO usar classes
- Lendo mensagens de erro deste módulo
- Você domina este módulo se...

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_classe_amostra` | Sua primeira classe: Amostra | ★☆☆ | complete a classe `Amostra`. |
| `ex02_bobina_str_repr` | Bobina com __str__ e __repr__ | ★☆☆ | complete a classe `Bobina`. |
| `ex03_tolerancia` | Tolerância com mínimo, máximo ou os dois | ★☆☆ | complete a classe `Tolerancia`. |
| `ex04_dataclass_resultado` | Resultado de ensaio com @dataclass | ★☆☆ | transforme `ResultadoEnsaio` numa dataclass (apague o __init__ provisório) com os campos, nesta ordem: |
| `ex05_enum_situacao` | Situação de liberação com Enum | ★☆☆ | 1. |
| `ex06_amostra_property` | Amostra protegida com @property | ★★☆ | complete a classe `Amostra`. |
| `ex07_tolerancia_construtores` | Tolerância com construtores alternativos | ★★☆ | complete a classe `Tolerancia`. |
| `ex08_heranca_ensaios` | Tipos de ensaio com herança e polimorfismo | ★★☆ | 1. |
| `ex09_corrigir_lote` | Leitura de código: o lote que pesava demais | ★★☆ | 1. |
| `ex10_dataclass_medicao` | Medições imutáveis e ordenáveis com dataclass | ★★☆ | 1. |
| `ex11_especificacao_linha` | Especificação e linha de produção (composição) | ★★★ | 1. |
| `ex12_revisao_certificado` | Revisão: o certificado de qualidade | ★★★ | transforme `Certificado` numa dataclass com os campos, nesta ordem: |
| `ex13_revisao_fila_emissao` | Revisão: a fila de emissão de certificados | ★★★ | complete a classe `FilaDeEmissao`. |

**Desafio:** Desafio do Módulo 08 — O Validador de Certificados orientado a objetos

## Módulo 09 — Testes e qualidade de código

Pasta: `09-testes-e-qualidade/`

**Seções da aula:**

- 1. Por que testar
- 2. `assert`: a peça mais simples
- 3. pytest: primeiros passos
- 4. Lendo uma falha do pytest
- 5. Anatomia de um bom teste
- 6. Floats e erros: `pytest.approx` e `pytest.raises`
- 7. Vários casos: `@pytest.mark.parametrize`
- 8. Fixtures: preparando o terreno
- 9. Arquivos de verdade em pasta temporária: `tmp_path`
- 10. O que foi impresso e o que foi registrado: `capsys` e `caplog`
- 11. Trocando peças: `monkeypatch`
- 12. Exemplo resolvido: testes para uma função que você não escreveu
- 13. TDD passo a passo: vermelho → verde → refatorar
- 14. Cobertura de testes (conceito)
- 15. ruff: lint e formatação automáticos
- 16. Type hints e mypy (conceito)
- 17. logging: os prints dos profissionais

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_limites_tolerancia` | Limites de tolerância (TDD: os testes vêm primeiro) | ★☆☆ | implemente calcular_limites(nominal, tolerancia_pct), que devolve a tupla (minimo, maximo) de nominal ± tolerancia_pct %. |
| `ex02_conserte_numero_br` | Conserte o bug: número no formato brasileiro | ★☆☆ | este exercício NÃO começa com NotImplementedError. |
| `ex03_testes_media` | Escreva os testes: média das medições | ★☆☆ | complete testar_calcular_media(calcular_media). |
| `ex04_operador_do_laudo` | Operador do laudo (variável de ambiente) | ★☆☆ | implemente as duas funções. |
| `ex05_log_de_inspecao` | Log da inspeção | ★☆☆ | implemente registrar_resultado(logger, op, valor, minimo, maximo). |
| `ex06_conserte_pesos_por_nf` | Conserte o bug: peso total por NF | ★★☆ | a função abaixo já está escrita e tem 2 bugs. |
| `ex07_testes_classificar` | Escreva os testes: classificar uma medição | ★★☆ | complete testar_classificar(classificar), escrevendo asserts que confiram TODAS as regras abaixo. |
| `ex08_ler_medicoes` | Ler o arquivo de medições (TDD com tmp_path) | ★★☆ | implemente ler_medicoes(caminho), que lê o arquivo (UTF-8) e devolve a lista de valores (float), na ordem. |
| `ex09_relatorio_no_terminal` | Relatório no terminal (testado com capsys) | ★★☆ | implemente imprimir_relatorio(resultados). |
| `ex10_conserte_codigos_bobinas` | Conserte o bug: códigos das bobinas | ★★☆ | a função abaixo tem 3 bugs. |
| `ex11_revisao_resumo_por_linha` | Revisão: resumo por linha de produção (conserte os bugs) | ★★★ | leia o código com calma, preveja o que ele faz e corrija os 4 bugs. |
| `ex12_revisao_testes_lotes` | Revisão: escreva os testes de dividir_em_lotes | ★★★ | complete testar_dividir_em_lotes(dividir_em_lotes) com asserts que confiram TODAS as regras abaixo. |

**Desafio:** Desafio do módulo 09 — Do script legado ao código profissional

## Módulo 10 — Análise de dados com pandas, Excel e gráficos

Pasta: `10-dados-com-pandas/`

**Seções da aula:**

- 1. Preparando o terreno
- 2. Series e DataFrame
- 3. Lendo CSV brasileiro
- 4. Lendo Excel: uma aba, várias, todas
- 5. Inspecionando uma base nova
- 6. Selecionando linhas e colunas
- 7. Criando e alterando colunas
- 8. Tipos, texto, ausentes e duplicatas
- 9. Datas
- 10. Ordenando
- 11. Agrupando: groupby e agg
- 12. Juntando tabelas: merge e concat
- 13. Tabela dinâmica: pivot_table
- 14. Vetorização x apply x laço for
- 15. Exportando: CSV e Excel formatado
- 16. Gráficos com matplotlib
- 17. Gráfico de controle (média ± 3σ)
- 18. Laboratório guiado: o mercado de dados em 133 mil salários
- Lendo mensagens de erro deste módulo
- Você domina este módulo se...

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_primeiro_dataframe` | Primeiro DataFrame | ★☆☆ | implemente três funções. |
| `ex02_ler_csv_brasileiro` | Ler CSV brasileiro | ★☆☆ | implemente duas funções. |
| `ex03_filtrar_fora_da_faixa` | Filtrar o que está fora da faixa | ★☆☆ | implemente duas funções. |
| `ex04_nova_coluna_desvio` | Colunas calculadas: desvio e status | ★☆☆ | implemente duas funções. |
| `ex05_ler_abas_excel` | Todas as abas numa tabela só | ★★☆ | implemente ler_todas_as_abas(caminho), que devolve UMA tabela com: |
| `ex06_limpar_medicoes` | Limpar medições digitadas à mão | ★★☆ | implemente limpar_medicoes(bruto). |
| `ex07_corrija_o_relatorio` | Corrija o relatório (leitura de código e depuração) | ★★☆ | escreva a versão correta de percentual_cof_alto(df, cof_max), que devolve uma Series: |
| `ex08_resumo_por_linha` | Resumo por linha de produção | ★★☆ | implemente resumo_por_linha(df). |
| `ex09_conferir_especificacao` | Conferir medições contra a especificação (merge) | ★★★ | implemente conferir_espessura(medicoes, specs). |
| `ex10_tabela_por_mes` | Datas e tabela dinâmica: peso por linha e mês | ★★☆ | implemente duas funções. |
| `ex11_grafico_barras` | Gráfico de barras: peso por linha | ★☆☆ | implemente duas funções. |
| `ex12_grafico_controle` | Gráfico de controle (média ± 3σ) | ★★★ | implemente três funções. |
| `ex13_revisao_emails_expedicao` | Revisão: e-mails da expedição viram tabela | ★★☆ | implemente três funções. |
| `ex14_revisao_relatorio_excel` | Revisão: relatório Excel formatado a partir de objetos | ★★★ | implemente duas funções. |

**Desafio:** Desafio do módulo 10 — Relatório mensal da qualidade

## Módulo 11 — Bancos de dados e SQL (SQLite)

Pasta: `11-banco-de-dados-e-sql/`

**Seções da aula:**

- 1. O que é um banco de dados relacional
- 2. Primeira conexão com sqlite3
- 3. Criando tabelas: tipos e restrições
- 4. Inserindo dados com parâmetros
- 5. O banco do laboratório
- 6. SELECT: escolher, filtrar, ordenar
- 7. Agregação: GROUP BY e HAVING
- 8. JOINs: juntando tabelas
- 9. Subconsultas e CTEs
- 10. UPDATE e DELETE
- 11. Transações: commit, rollback e with
- 12. Linhas com nome: row_factory
- 13. SQL injection na prática
- 14. Índices
- 15. Modelando o banco de regras do projeto final
- 16. SQL e pandas: read_sql e to_sql
- Lendo mensagens de erro deste módulo
- Você domina este módulo se...

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_criar_tabela_bobinas` | Criar a tabela de bobinas | ★☆☆ | implemente criar_tabela_bobinas(conexao), que cria a tabela "bobina" com as colunas, nesta ordem: |
| `ex02_inserir_bobina` | Inserir com parâmetros | ★☆☆ | a tabela já existe: |
| `ex03_inserir_varias` | Inserir vários ensaios de uma vez (tudo ou nada) | ★☆☆ | a tabela já existe: |
| `ex04_buscar_por_op` | Buscar os ensaios de uma OP | ★☆☆ | use o banco do laboratório (tabelas op e ensaio, veja a aula ou dados/laboratorio.sql). |
| `ex05_filtros_where` | Filtros com WHERE | ★☆☆ | use o banco do laboratório. |
| `ex06_agregacoes` | Funções de agregação | ★★☆ | use o banco do laboratório. |
| `ex07_group_by_having` | GROUP BY e HAVING | ★★☆ | use o banco do laboratório. |
| `ex08_joins` | JOINs: juntando OPs, clientes e expedição | ★★☆ | use o banco do laboratório. |
| `ex09_subconsulta` | Subconsultas | ★★☆ | use o banco do laboratório. |
| `ex10_corrija_as_consultas` | Corrija as consultas (leitura de código e depuração) | ★★☆ | escreva as versões corretas (use o banco do laboratório): |
| `ex11_busca_segura` | Busca com filtros, à prova de SQL injection | ★★★ | implemente buscar_ops(conexao, filtros, ordenar_por="numero"), que devolve a lista dos NÚMEROS das OPs (tabela op do banco do laboratório): |
| `ex12_banco_de_regras` | O banco de regras do projeto final | ★★★ | implemente três funções. |
| `ex13_revisao_importar_csv` | Revisão: importar a planilha da expedição para o banco | ★★☆ | implemente importar_expedicao(conexao, caminho), que devolve a tupla (quantidade_inserida, linhas_com_erro). |
| `ex14_revisao_emitir_certificados` | Revisão: emitir certificados numa transação | ★★★ | implemente emitir_certificados(conexao, data), que emite os certificados pendentes e devolve a lista de Certificado (dataclass abaixo, já pronta). |

**Desafio:** Desafio do módulo 11 — Ferramenta do banco de regras

## Módulo 12 — Automação e integração

Pasta: `12-automacao-e-integracao/`

**Seções da aula:**

- 1. O mapa da automação: API, arquivo ou tela?
- 2. HTTP em 10 minutos
- 3. requests: conversando com APIs
- 4. Falhas de rede: timeout, erros e novas tentativas
- 5. Testar sem internet: injeção de dependência e monkeypatch
- 6. Arquivos e pastas em lote (pathlib + shutil)
- 7. Relatórios Excel com openpyxl
- 8. E-mail: montar, salvar e ler mensagens
- 9. Outlook no Windows: clássico, novo e Microsoft Graph
- 10. Agendamento: o Agendador de Tarefas do Windows
- 11. Automação web com Playwright
- 12. O robô de certificados: modo ensaio, log, prints e idempotência
- Lendo mensagens de erro deste módulo
- Você domina este módulo se...

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_classificar_status` | Classificar códigos de status HTTP | ★☆☆ | implemente duas funções. |
| `ex02_montar_url` | Montar a URL de uma consulta | ★☆☆ | implemente montar_url(base, caminho, params=None). |
| `ex03_buscar_tolerancias` | Buscar tolerâncias numa API (com sessão injetada) | ★★☆ | implemente buscar_tolerancias(sessao, base_url, linha, timeout=10). |
| `ex04_com_retentativas` | Tentar de novo com espera crescente (backoff) | ★★★ | implemente com_retentativas(funcao, tentativas=3, espera=1.0, dormir=time.sleep). |
| `ex05_listar_planilhas` | Listar as planilhas de uma pasta | ★☆☆ | implemente listar_planilhas(pasta). |
| `ex06_nome_disponivel` | Nunca sobrescrever um arquivo | ★☆☆ | implemente nome_disponivel(pasta, nome). |
| `ex07_organizar_laudos` | Organizar laudos em pastas (com modo ensaio) | ★★☆ | implemente organizar_laudos(origem, destino, ensaio=True). |
| `ex08_larguras_colunas` | Calcular a largura das colunas de um relatório | ★☆☆ | implemente calcular_larguras(linhas, minimo=8, maximo=50). |
| `ex09_relatorio_excel` | Relatório Excel de medições, pronto para o gerente | ★★★ | implemente gerar_relatorio(medicoes, caminho) com openpyxl. |
| `ex10_montar_email` | Montar o e-mail do certificado (sem enviar) | ★★☆ | implemente montar_email_certificado(remetente, destinatarios, op, nf, anexo=None). |
| `ex11_ler_pedido_eml` | Ler o pedido da expedição num arquivo .eml | ★★☆ | implemente ler_pedido(conteudo), onde `conteudo` são os bytes do .eml. |
| `ex12_corrigir_plano_robo` | Leitura de código: conserte o plano do robô | ★★☆ | um colega separou o robô em duas partes: |
| `ex13_revisao_fila_idempotente` | Revisão: fila de emissão idempotente | ★★★ | implemente processar_fila(pedidos, emitir, registro). |
| `ex14_revisao_resumo_por_dia` | Revisão: resumo diário dos pedidos por e-mail | ★★☆ | implemente resumir_por_dia(emails). |

**Desafio:** Desafio do módulo 12 — Robô da expedição (modo ensaio)

## Módulo 13 — APIs web com FastAPI

Pasta: `13-apis-com-fastapi/`

**Seções da aula:**

- 1. O que é uma API REST
- 2. A primeira API
- 3. Testando com TestClient
- 4. Parâmetros de caminho
- 5. Parâmetros de consulta
- 6. Corpo com Pydantic
- 7. Códigos de status e HTTPException
- 8. Organizando em módulos
- 9. Dependências
- 10. Persistência com SQLite
- 11. Documentação automática
- 12. Rodando de verdade: uvicorn e um cliente requests
- Lendo mensagens de erro deste módulo
- Você domina este módulo se...

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_ola_api` | Olá, API! | ★☆☆ | no `app` abaixo, crie três rotas GET: |
| `ex02_parametros_caminho` | Parâmetros de caminho | ★☆☆ | no `app` abaixo, crie duas rotas GET: |
| `ex03_linhas_404` | Linhas de produção e o erro 404 | ★☆☆ | usando o dicionário LINHAS, crie no `app`: |
| `ex04_parametros_consulta` | Filtros com parâmetros de consulta | ★★☆ | usando a lista BOBINAS, crie GET "/bobinas" com estes parâmetros de consulta, todos opcionais: |
| `ex05_modelos_pydantic` | Modelo Pydantic de uma medição | ★☆☆ | 1. |
| `ex06_validar_medicao` | Rota que valida uma medição contra a tolerância | ★★☆ | 1. |
| `ex07_ocorrencias` | Ocorrências de qualidade: os códigos de status certos | ★★☆ | guarde as ocorrências no dicionário OCORRENCIAS ({id: |
| `ex08_router_e_docs` | APIRouter e documentação automática | ★☆☆ | 1. |
| `ex09_dependencias` | Dependências: chave de acesso, perfil e regras injetadas | ★★☆ | 1. |
| `ex10_leitura_prever_status` | Leitura de código: preveja as respostas da API do colega | ★★☆ | 1. |
| `ex11_revisao_estatisticas_sqlite` | Revisão: API de medições com SQLite e estatística | ★★★ | 1. |
| `ex12_revisao_regras_tolerancia` | Revisão: regras de tolerância (faixa e nominal ± %) na API | ★★★ | 1. |

**Desafio:** Desafio do módulo 13 — API de Certificados do laboratório

## Módulo 14 — Projeto final: Validador de Certificados

Pasta: `14-projeto-final/`

**Seções da aula:**

- 1. O problema, em uma página
- 2. Arquitetura em camadas
- 3. Decisões de projeto (e por quê)
- 4. Os dados de exemplo
- 5. Roteiro de construção
- 6. Domínio e regras (etapas 1 a 6)
- 7. Entradas (etapas 7 a 10)
- 8. Saídas e orquestração (etapas 11 a 14)
- 9. Montagem final: o projeto-completo
- 10. O robô do TOTVS, isolado
- 11. Do curso para o trabalho
- 12. Portfólio no GitHub
- 13. Extensões
- Lendo mensagens de erro deste módulo

**Exercícios:**

| Arquivo | Título | Nível | Tarefa |
|---|---|---|---|
| `ex01_modelos` | Modelos de dados do sistema | ★☆☆ | implemente três coisas. |
| `ex02_carregar_regras` | Carregar as regras do banco SQLite | ★★☆ | implemente `carregar_especificacoes(conexao)`. |
| `ex03_tolerancia_fixa` | Regra de tolerância fixa (mínimo/máximo) | ★☆☆ | implemente `verificar_fixa(caracteristica, valor, minimo, maximo)`. |
| `ex04_tolerancia_nominal` | Regra nominal ± % (espessura e gramatura) | ★☆☆ | implemente duas funções. |
| `ex05_validar_op` | Validar uma OP inteira | ★★☆ | implemente `validar_medicao(medicao, especificacao)` e devolva um ResultadoValidacao(op=medicao.op, especificacao=especificacao.titulo, motivos=[...]). |
| `ex06_liberacao` | Observação de liberação: leia, preveja e conserte | ★★☆ | implemente `prever_v1()` devolvendo uma lista com o que esta_liberado_v1 devolveria para estas observações, nesta ordem. |
| `ex07_ler_planilha` | Ler a planilha de valores (4 abas) com openpyxl | ★★★ | implemente três funções. |
| `ex08_conferir_linha` | A linha digitada bate com a aba? | ★☆☆ | implemente duas funções. |
| `ex09_escolher_especificacao` | Escolher a especificação da OP (sem chutar) | ★★☆ | implemente duas funções. |
| `ex10_emails_expedicao` | Ler os pedidos da expedição (OP, NF e peso) | ★★☆ | implemente três funções. |
| `ex11_fila_emissao` | Montar a fila de emissão (a triagem) | ★★★ | implemente `montar_fila(pedidos, medicoes, especificacoes)` e devolva a tupla (fila, bloqueados): |
| `ex12_emissor_ensaio` | Emissor do TOTVS em modo ensaio (e a emissão da fila) | ★★★ | implemente três coisas. |
| `ex13_relatorio_serie` | Relatório da série (CSV para o Excel brasileiro) | ★☆☆ | implemente duas funções. |
| `ex14_cli` | A linha de comando (argparse) que junta tudo | ★★☆ | implemente duas funções. |

**Desafio:** Desafio do módulo 14 — A API do Validador (extensão FastAPI)
