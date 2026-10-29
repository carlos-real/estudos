# Guia de carreira: do laboratório de qualidade à programação

> Escrito para quem trabalha em laboratório de qualidade numa indústria de embalagens
> plásticas e quer trabalhar com programação. Números e rankings conferidos em
> **outubro de 2026**. Mercado muda: confira as fontes antes de decisões grandes.

Neste guia, cada afirmação vem marcada:

- 📊 **Fato:** dado com fonte (link no texto e na lista de fontes no fim).
- 💬 **Opinião:** minha leitura do mercado e conselho prático. Pode e deve ser questionada.

Quando não achei fonte confiável para um número, **não dei número**.

---

## Resumo em 1 minuto

- **Fique com Python.** Para dados e automação, que são os seus objetivos, ele é a
  escolha certa. Some **SQL** a ele desde já.
- **O caminho mais rápido é o híbrido "qualidade + dados"** dentro da própria indústria.
  Você já conhece o processo, os dados e as pessoas. Isso vale muito.
- **Prova vale mais que certificado.** Uma automação real funcionando no laboratório,
  com horas economizadas medidas, abre mais portas que dez cursos concluídos.
- **Portfólio no GitHub** com os projetos do curso + **LinkedIn** contando essa história.
- No fim deste guia há um **plano de 6 meses** e um **de 12 meses**.

---

## 1. Python vale a pena ou devo mudar de linguagem?

### 1.1 O que os dados dizem

📊 **Fato:** na pesquisa do Stack Overflow de 2026 (mais de 30 mil participantes de 169
países), as linguagens mais usadas por todos os respondentes foram JavaScript (62,0%),
SQL (58,4%), HTML/CSS (58,2%) e Python (58,0%). Depois vêm Bash/Shell (51,3%), TypeScript
(43,8%), Java (27,6%) e C# (27,1%).
([Stack Overflow Developer Survey 2026, Technology](https://survey.stackoverflow.co/2026/technology);
[anúncio dos resultados](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/))

📊 **Fato:** na edição anterior, o uso de Python tinha subido 7 pontos percentuais de 2024
para 2025, um dos maiores saltos da pesquisa.
([Stack Overflow Developer Survey 2025, Technology](https://survey.stackoverflow.co/2025/technology))

📊 **Fato:** Python segue em 1º lugar no índice TIOBE de outubro de 2026. O TIOBE mede
popularidade por buscas na internet, não vagas de emprego.
([TechRepublic sobre o TIOBE de outubro de 2026](https://www.techrepublic.com/article/news-tiobe-october-2026-java-closes-cpp-gap/);
[índice oficial](https://www.tiobe.com/tiobe-index/))

📊 **Fato:** no relatório Octoverse 2025 do GitHub, o TypeScript passou Python e
JavaScript como linguagem mais usada **no GitHub** (agosto de 2025). O mesmo relatório
aponta Python como líder em projetos de IA e ciência de dados.
([GitHub Octoverse 2025](https://github.blog/2025-10-28-octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/))

📊 **Fato:** no Brasil, entre profissionais de dados, Python e SQL aparecem como as
ferramentas mais usadas nas análises da pesquisa State of Data Brazil, feita pela
comunidade Data Hackers com a Bain & Company.
([State of Data Brazil 2025-2026, Bain](https://www.bain.com/pt-br/insights/state-of-data-2025/);
[dados abertos da pesquisa](https://github.com/data-hackers-br/state-of-data-brazil))

📊 **Fato:** o relatório da Brasscom sobre o mercado de trabalho de tecnologia aponta que,
entre 2019 e 2024, a demanda foi de 665.403 profissionais, enquanto 464.569 pessoas se
formaram em cursos da área entre 2018 e 2023.
([Brasscom, Perspectivas do Mercado de Trabalho do Macrossetor TIC](https://brasscom.org.br/wp-content/uploads/2025/02/Relatorio-Perspectivas-do-Mercado-de-Trabalho.pdf))

💬 **Opinião:** a falta de profissionais é real nas vagas experientes. Na vaga de entrada
(júnior), a disputa ficou mais dura em 2025 e 2026, em parte porque ferramentas de IA
fazem tarefas simples que antes iam para iniciantes. Não encontrei uma estatística oficial
e confiável sobre vagas júnior no Brasil, então trate isso como tendência, não como
número. A consequência prática: **quem chega com conhecimento de um negócio real (como
você chega com a indústria) se destaca de quem só fez cursos.**

### 1.2 Comparação honesta das linguagens

| Linguagem | Onde é usada | Para você |
|---|---|---|
| **Python** | Dados, automação, IA, scripts, backend (FastAPI, Django) | 💬 Melhor encaixe. Curva de aprendizado mais suave, e é a língua dos dados. |
| **JavaScript / TypeScript** | Web (obrigatória no navegador), backend com Node.js | 💬 Muitas vagas, mas muita concorrência de iniciantes. Só faz sentido se você quiser criar sites e telas. |
| **Java** | Sistemas corporativos, bancos, grandes empresas | 💬 Mercado sólido no Brasil para backend corporativo. Mais verbosa, mais distante de dados. |
| **C# (.NET)** | Sistemas corporativos no ecossistema Microsoft, jogos (Unity) | 💬 Boa opção em empresas "100% Microsoft". Mesma observação do Java sobre dados. |
| **SQL** | Bancos de dados: **todo** trabalho com dados | 💬 Não é alternativa ao Python: é **complemento obrigatório**. Comece já. |

Um nicho que pouca gente lembra: o TOTVS Protheus, que você usa no trabalho, é
customizado com linguagens próprias da TOTVS, o AdvPL e o TLPP.
([TDN TOTVS: TLPP x AdvPL](https://tdn.totvs.com/display/tec/TLPP+x+AdvPL))
💬 **Opinião:** é um mercado real de desenvolvedor de ERP no Brasil, mas pequeno e preso a
um fornecedor. Vale como curiosidade e como ponte com a TI da sua empresa, não como
primeira linguagem.

### 1.3 Recomendação

💬 **Opinião, com convicção:** **não mude de linguagem. Fique com Python e some SQL.**

1. Seus objetivos (dados e automação) são o território do Python.
2. O projeto que você quer construir (validar planilhas, ler e-mails, gerar certificados)
   é Python puro: pandas, openpyxl, Playwright.
3. A segunda linguagem é muito mais fácil que a primeira. Se um dia uma vaga pedir Java
   ou C#, com a base deste curso você aprende em semanas, não em anos.
4. Trocar de linguagem no começo é a forma mais comum de nunca sair do começo.

Quando reconsiderar: se você descobrir que gosta mesmo é de construir telas e sites, aí
JavaScript/TypeScript entra. Mas descubra isso **depois** de terminar o curso.

---

## 2. As trilhas possíveis

### 2.1 Híbrido "qualidade + dados" (a transição mais rápida)

**Cargos com esse perfil** (os nomes variam por empresa): analista de qualidade com foco
em dados, analista de melhoria contínua, analista de processos, analista de dados
industriais, analista de BI da área industrial.

**No dia a dia:** automatizar relatórios do laboratório, montar painéis de CEP (gráficos
de controle), cruzar dados do ERP com resultados de ensaio, investigar a causa de
reclamações com dados, calcular capacidade de processo (Cp, Cpk).

**Por que é mais rápida** (💬 opinião): você não precisa convencer um recrutador
desconhecido. Você já está dentro, conhece o processo, fala a língua da produção e sabe
onde estão as dores. Um analista de dados vindo de fora leva meses para aprender o que
você já sabe sobre espessura, gramatura, COF e selagem.

**O que exige além do curso:** Excel avançado, Power BI, SQL, estatística aplicada à
qualidade (CEP, capacidade, análise do sistema de medição).

### 2.2 Analista de Dados / BI

**No dia a dia:** responder perguntas de negócio com dados. Consultas SQL, limpeza de
dados, painéis no Power BI, relatórios, apresentações.

**O que exige:** SQL (a habilidade número um), Excel, Power BI, Python com pandas,
estatística básica, comunicação ("contar a história" dos números).

📊 **Fato:** a Robert Half publica, no Guia Salarial 2026, faixas mensais brutas para
Analista de BI: pleno de R$ 7.650 a R$ 12.850 e sênior de R$ 10.900 a R$ 18.250 (no nível
júnior, a mesma fonte indica R$ 5.600 a R$ 9.000).
([Robert Half: Analista de BI Pleno](https://www.roberthalf.com/br/pt/vagas-detalhes/analista-de-bi-pleno);
[Analista de BI Sênior](https://www.roberthalf.com/br/pt/vagas-detalhes/analista-de-bi-senior))

⚠️ Leia com cuidado: consultorias de recrutamento como a Robert Half trabalham mais com
empresas médias e grandes, e os valores variam muito por cidade e porte da empresa. Em
indústrias do interior, espere valores menores. Sites como o
[Glassdoor](https://www.glassdoor.com.br/Sal%C3%A1rios/desenvolvedor-python-junior-sal%C3%A1rio-SRCH_KO0,27.htm)
trazem relatos de profissionais, mas muitas vezes com amostras pequenas (às vezes menos de
20 salários), e os números oscilam bastante de uma página para outra.

### 2.3 Engenheiro de Dados

**No dia a dia:** construir e manter os "encanamentos" de dados (pipelines): levar dados
do ERP, de sensores e de planilhas para um banco ou data lake, limpos e no horário.

**O que exige:** SQL avançado, Python, modelagem de dados, uma nuvem (Azure, AWS ou
Google Cloud), Docker, ferramentas como Spark, Airflow ou dbt, Git no dia a dia.

📊 **Fato:** na pesquisa State of Data Brazil 2025-2026, 43,5% dos engenheiros de dados e
de machine learning declararam ganhar acima de R$ 12 mil por mês, contra 11,6% dos
analistas de dados. Entre os respondentes de nível sênior, 52,2% estavam acima de
R$ 12 mil. A amostra é de quem escolheu responder, não um censo.
([relatório State of Data Brazil 2025-2026, PDF](https://www.bain.com/contentassets/aaff7ea7a43944dbac97232329c3c1b6/baincompany-e-data-hackers_state-of-data-2025-2026.pdf))

💬 **Opinião:** raramente é a primeira vaga. O caminho comum é analista de dados →
engenheiro de dados, depois de 1 a 3 anos lidando com dados de verdade.

### 2.4 Desenvolvedor Backend Python

**No dia a dia:** criar e manter sistemas: APIs, regras de negócio, integrações com
bancos de dados e outros sistemas.

**O que exige:** Python sólido, FastAPI ou Django, SQL, testes automatizados, Git com
branches e pull requests, HTTP, Docker, noções de nuvem e Linux.

📊 **Fato:** o Guia Salarial 2026 da Robert Half traz, para Desenvolvedor(a) Back-End
Júnior, faixa nacional de R$ 6.050 a R$ 8.750 (mediana de R$ 6.850). Por cidade, a
variação é grande: São Paulo de R$ 5.750 a R$ 8.300, Rio de Janeiro de R$ 7.050 a
R$ 10.200.
([Robert Half: Back-End Júnior](https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-junior);
[São Paulo](https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-junior/sao-paulo);
[Rio de Janeiro](https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-junior/rio-de-janeiro))

💬 **Opinião:** no Brasil, boa parte das vagas de backend pede Java, C# ou
JavaScript/TypeScript. Vagas de backend **em Python** existem, mas são menos numerosas
que as de dados em Python. É uma trilha ótima, só que mais competitiva para quem vem de
outra área.

### 2.5 Automação / RPA

**No dia a dia:** robôs que fazem tarefas repetitivas: baixar relatórios, preencher
sistemas, mandar e-mails, consolidar planilhas. Exatamente o que o seu projeto final faz
com o TOTVS.

**O que exige:** Python para scripts, automação de navegador (Playwright, Selenium),
APIs, Excel e Outlook, boas práticas de robô (log, modo ensaio, tratamento de falhas).
Muitas empresas também usam ferramentas próprias de RPA (como Power Automate ou UiPath).

💬 **Opinião:** é a trilha mais fácil de **provar** dentro da empresa, porque o resultado
é medido em horas economizadas. Combina muito bem com o híbrido "qualidade + dados".
Não encontrei uma fonte salarial confiável e específica para essa trilha no Brasil.

### 2.6 Quadro comparativo

| Trilha | Distância a partir do curso (💬) | O que mais falta | Primeira vaga típica |
|---|---|---|---|
| Qualidade + dados | Curta | Power BI, SQL, estatística de qualidade | Transição interna |
| Analista de Dados/BI | Curta a média | SQL todo dia, Power BI | Analista júnior, assistente de dados |
| Automação/RPA | Curta a média | Projetos de automação provados | Analista de automação júnior |
| Backend Python | Média | Docker, nuvem, mais projetos de API | Desenvolvedor júnior |
| Engenheiro de Dados | Longa | Nuvem, pipelines, modelagem | Geralmente depois de ser analista |

---

## 3. O que estudar além deste curso

| Habilidade | Por quê | Para quais trilhas | Quanto (💬) |
|---|---|---|---|
| **SQL** | Está em praticamente toda vaga de dados | Todas | Desde já, 3 vezes por semana, exercícios curtos |
| **Excel avançado** | Tabela dinâmica, PROCX, Power Query: a língua da empresa | Híbrido, dados | O suficiente para não depender de ninguém |
| **Power BI** | Ferramenta de painel mais pedida no Brasil (💬) | Híbrido, dados | 1 a 2 meses de prática com dados reais anonimizados |
| **Estatística** | CEP, capacidade, média × mediana, desvio, testes de hipótese | Híbrido, dados | Você já tem a base do laboratório: formalize |
| **Git** | Todo time de tecnologia usa | Todas | O curso cobre (módulos 00 e 09) |
| **Docker** | Rodar o mesmo sistema em qualquer máquina | Backend, eng. de dados | Depois do curso, 2 a 4 semanas |
| **Nuvem** | Onde os sistemas e os dados vivem hoje | Backend, eng. de dados | Uma nuvem só, o básico, depois do curso |
| **Inglês técnico** | Documentação, erros e respostas estão em inglês | Todas | Leitura: um pouco todo dia |

📊 **Fato:** a certificação de Power BI da Microsoft (exame PL-300) cobre preparação de
dados com Power Query, modelagem, DAX, visualização e gestão de relatórios, e a Microsoft
oferece trilhas de estudo e um simulado gratuitos.
([guia de estudo do PL-300](https://learn.microsoft.com/pt-br/credentials/certifications/resources/study-guides/pl-300))

💬 **Opinião:** certificação ajuda a passar por filtros de RH, mas não substitui
portfólio. Faça a do Power BI só se mirar vagas de dados e depois de já usar a ferramenta
de verdade.

Links para estudar cada item: [recursos.md](recursos.md).

---

## 4. Portfólio com os projetos do curso

O `PLANO-DE-ESTUDOS.md` define 4 marcos. Cada um vira um repositório próprio no GitHub:

| Marco | Projeto | O que mostra para um recrutador |
|---|---|---|
| 1 | Desafio do módulo 04 | Lógica, funções, código organizado |
| 2 | Desafio do módulo 08 | Orientação a objetos, uma ferramenta útil |
| 3 | Desafio do módulo 11 + laboratório de salários do módulo 10 | SQL, pandas, análise de dados: o "kit" de vaga de dados |
| 4 | Validador de Certificados (módulo 14) | Sistema completo, com testes, de um problema real da indústria |

**Como transformar um projeto do curso em projeto de portfólio:**

1. **Repositório próprio**, com nome claro (`validador-certificados`, não `projeto-final`).
2. **README que vende o projeto**: o problema (em 2 frases), o que o programa faz, como
   rodar (comandos copiáveis), um print ou GIF, como rodar os testes, o que você aprendeu.
3. **Testes rodando** e, se possível, rodando sozinhos a cada push (GitHub Actions,
   módulo 14).
4. **Dados fictícios.** Nunca dados reais da empresa, nem anonimizados "mais ou menos".
5. **Commits com boas mensagens.** Recrutador técnico olha o histórico.

Sobre o `salaries.csv` do seu repositório: ele traz salários de profissões de dados em
dólar, de vários países. 💬 É ótimo para praticar e para portfólio, mas não use como
referência de salário no Brasil.

**Ideias de projeto extra com o seu domínio** (💬 diferenciam muito):

- Painel de CEP de espessura com limites de controle, a partir de um CSV.
- Comparador de laudos: lê dois arquivos de resultados e destaca diferenças fora da
  tolerância.
- API de tolerâncias: consulta a especificação de um produto por código (módulo 13).
- Robô em "modo ensaio" que preenche um formulário de teste no navegador (módulo 12).

---

## 5. GitHub e LinkedIn

### 5.1 GitHub

- **Foto e nome reais**, bio de uma linha ("Qualidade industrial → dados e automação com
  Python").
- **README de perfil** (um repositório com o mesmo nome do seu usuário): quem você é, o
  que está estudando, links para os 4 projetos.
- **Fixe (pin) os 4 melhores repositórios.** O resto pode ficar, mas não é vitrine.
- 💬 Os "quadradinhos verdes" de atividade ajudam a mostrar constância, mas qualidade dos
  projetos pesa mais. Não faça commits vazios só para pintar o gráfico.
- README em português serve para vagas no Brasil. Um parágrafo em inglês no topo é um
  bônus.

### 5.2 LinkedIn

- **Título:** o que você é + para onde vai. Exemplo:
  "Laboratório de Qualidade | Python, SQL e Power BI | Dados na indústria de embalagens".
- **Sobre:** sua história em 5 linhas. Do laboratório para os dados, o que já automatizou,
  o que procura.
- **Projetos:** cada marco do portfólio com link para o GitHub e o resultado.
- **Publique de vez em quando** (💬 uma vez a cada 2 semanas já basta): um aprendizado, um
  antes/depois de uma automação (sem dados da empresa), um gráfico do seu projeto.
- **Conecte-se** com pessoas de dados e qualidade da sua região e do seu setor, e com
  recrutadores de tecnologia.
- **Honestidade sempre:** escreva "estudando" no que você está estudando. Exagero aparece
  na primeira entrevista técnica.

---

## 6. Como conseguir a primeira oportunidade

### 6.1 Transição interna (💬 a melhor aposta)

1. **Escolha uma dor real e pequena** do laboratório: o relatório semanal que leva 2
   horas, a planilha consolidada à mão, a conferência de tolerâncias.
2. **Automatize** com o que o curso já ensinou (a partir do módulo 06 dá para muita coisa).
3. **Meça**: quanto tempo levava, quanto leva agora, quantos erros evitou. "Economiza 6
   horas por mês" convence qualquer gestor.
4. **Converse com a TI antes de colocar em uso**: acesso a sistemas, segurança, LGPD e
   onde o código vai ficar. Isso mostra maturidade e evita problemas.
5. **Apresente ao gestor** o antes/depois e proponha: "posso dedicar X horas por semana a
   isso?".
6. **Aproxime-se** de quem já trabalha com dados ou TI na empresa (BI, engenharia de
   processos, TI). Pergunte como eles trabalham. Ofereça ajuda.
7. **Fique de olho no recrutamento interno.** Muitas vagas de analista são preenchidas
   por gente de dentro que já provou valor.

O seu projeto final (o Validador de Certificados) foi pensado para isso: rodar primeiro
em **modo ensaio**, sem gravar nada no TOTVS, comparando com o processo manual.

### 6.2 Estágio e trainee

Estágio exige estar matriculado em curso técnico ou superior. 💬 Se você ainda não tem
graduação, um tecnólogo (Análise e Desenvolvimento de Sistemas, Ciência de Dados, Gestão
da Produção com ênfase em dados) abre a porta do estágio e passa pelo filtro de RH de
indústrias grandes. Não é obrigatório para trabalhar com programação, mas ajuda,
principalmente em empresas tradicionais.

### 6.3 Freelas e projetos pequenos

💬 Automatizar planilhas e relatórios para pequenos negócios (de conhecidos, de
fornecedores) dá experiência e história para contar. Cuidados: escopo por escrito,
começar pequeno, não usar o tempo nem os dados do seu emprego, e não cobrar barato demais
só para "pegar experiência".

### 6.4 Busca externa

- Onde: LinkedIn e plataformas de recrutamento usadas pelas empresas da sua região.
- Termos de busca: "analista de dados júnior", "analista de BI júnior", "assistente de
  dados", "analista de melhoria contínua", "analista de automação", "desenvolvedor Python
  júnior", "RPA".
- 💬 Candidate-se mesmo sem cumprir 100% dos requisitos. A lista da vaga costuma ser um
  desejo, não um filtro rígido.
- 💬 Indústrias do seu setor (embalagens, plásticos, alimentos, bens de consumo) valorizam
  quem entende chão de fábrica. Comece por elas.

---

## 7. Como se preparar para entrevistas técnicas

### 7.1 O formato mais comum (💬)

1. **Triagem com RH:** sua história, motivação, pretensão salarial.
2. **Teste técnico:** online ou para fazer em casa. Para dados: SQL, um caso em Excel ou
   Power BI, às vezes pandas. Para desenvolvimento: um exercício de lógica ou uma pequena
   API.
3. **Entrevista técnica:** você explica um projeto seu e resolve um problema pensando em
   voz alta.
4. **Conversa com o gestor:** como você trabalha, como lida com erro e prazo.

### 7.2 Como treinar

- **SQL:** `SELECT`, `WHERE`, `GROUP BY`, `HAVING`, `JOIN`, subconsultas. Um exercício por
  dia nas plataformas de [recursos.md](recursos.md).
- **Python:** listas, dicionários, funções, ler CSV, pandas (`groupby`, `merge`, filtros).
  Os exercícios do curso são um ótimo treino: refaça os de revisão sem olhar.
- **Seu projeto em 2 minutos:** problema → o que você fez → resultado (com número).
  Treine em voz alta.
- **Histórias no formato STAR** (Situação, Tarefa, Ação, Resultado). Exemplo: "o
  relatório de liberação levava 2 horas (S); eu precisava reduzir erros de digitação (T);
  escrevi um script em Python que lê a planilha e confere as tolerâncias (A); hoje leva 5
  minutos e não tivemos mais erro de transcrição (R)".
- **Estatística de conversa:** média × mediana, desvio padrão, o que é um outlier, o que
  um gráfico de controle mostra. Você vive isso no laboratório: use a seu favor.
- **Simulado com IA:** peça para a IA ser o entrevistador, fazer uma pergunta por vez e
  avaliar suas respostas no fim.

### 7.3 Na hora

- Pense em voz alta. O entrevistador avalia o raciocínio, não só a resposta.
- Não sabe? Diga o que sabe e como descobriria. "Não sei, mas eu procuraria na
  documentação do pandas por..." vale mais que inventar.
- Faça perguntas sobre o time, os dados e as ferramentas. Mostra interesse real.

---

## 8. Plano de 6 meses e plano de 12 meses

💬 Os dois planos são sugestões, não garantias. Eles seguem o `PLANO-DE-ESTUDOS.md`, que
leva cerca de 31 semanas com 1 hora por dia.

### 8.1 Plano de 6 meses: transição híbrida "qualidade + dados"

Ritmo: **1h30 por dia, 5 dias por semana** (1h de curso + 30 min de SQL ou Power BI).
Objetivo: assumir tarefas de dados no seu próprio trabalho e ter os 3 primeiros marcos
do portfólio.

| Mês | Curso | Além do curso | Entrega do mês |
|---|---|---|---|
| 1 | Módulos 00 a 02 | SQL básico (SELECT, WHERE) 3x por semana | Ambiente pronto, LinkedIn atualizado, `DIARIO.md` começado |
| 2 | Módulos 03 e 04 | SQL com GROUP BY; Power BI: primeiros painéis | Marco 1 no GitHub; lista de 3 tarefas do laboratório para automatizar |
| 3 | Módulos 05 e 06 | Power BI com dados fictícios do laboratório | Primeira automação real (ler planilha/CSV e gerar resumo), com tempo economizado medido |
| 4 | Módulos 07 e 08 | Estatística de qualidade (CEP, Cp/Cpk) | Marco 2; apresentação da automação ao gestor |
| 5 | Módulos 09 e 10 | SQL com JOIN; Excel avançado | Painel de CEP em Python ou Power BI; conversa com a TI sobre acesso e governança |
| 6 | Módulo 11 | Revisão de SQL para entrevista | Marco 3; proposta formal de horas dedicadas a dados, ou primeiras candidaturas internas |

Ao fim dos 6 meses o curso ainda não acabou (faltam os módulos 12 a 14). Tudo bem: o
objetivo aqui é a **primeira oportunidade**, não o diploma do curso.

### 8.2 Plano de 12 meses: curso completo + trilha escolhida

Ritmo: **1 hora por dia, 5 dias por semana**.

| Período | Foco | Entrega |
|---|---|---|
| Meses 1 a 7 | Curso completo, seguindo o `PLANO-DE-ESTUDOS.md`; SQL 2x por semana a partir do mês 2 | Os 4 marcos no GitHub; ao menos uma automação em uso no trabalho |
| Mês 8 | Escolher a trilha (dados ou automação/backend) com base no que você mais gostou | Validador rodando em modo ensaio no laboratório; LinkedIn reescrito para a trilha |
| Meses 9 e 10 | **Dados:** Power BI a fundo, estatística, SQL avançado (PL-300 opcional). **Automação/backend:** Docker, publicar a API do módulo 13 numa nuvem, mais um robô | Um projeto extra completo da trilha |
| Meses 11 e 12 | Candidaturas internas e externas, simulados de entrevista, ajustes no portfólio | Entrevistas acontecendo; meta: primeira posição na área |

### 8.3 Sinais de que você está no caminho

- Você resolve exercícios novos sem abrir a solução na maioria das vezes.
- Alguém no trabalho já te procurou para "fazer aquela planilha automática".
- Você consegue explicar o seu Validador em 2 minutos para alguém de fora da área.
- Você tem pelo menos um número para contar: horas economizadas, erros evitados.

---

## Fontes

Consultadas em outubro de 2026.

- Stack Overflow Developer Survey 2026, Technology:
  <https://survey.stackoverflow.co/2026/technology>
- Stack Overflow, anúncio dos resultados de 2026:
  <https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/>
- Stack Overflow Developer Survey 2025, Technology:
  <https://survey.stackoverflow.co/2025/technology>
- TechRepublic, TIOBE Index de outubro de 2026:
  <https://www.techrepublic.com/article/news-tiobe-october-2026-java-closes-cpp-gap/>
- Índice TIOBE (página oficial): <https://www.tiobe.com/tiobe-index/>
- GitHub Octoverse 2025:
  <https://github.blog/2025-10-28-octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/>
- Bain & Company e Data Hackers, State of Data Brazil 2025-2026:
  <https://www.bain.com/pt-br/insights/state-of-data-2025/> e relatório em PDF:
  <https://www.bain.com/contentassets/aaff7ea7a43944dbac97232329c3c1b6/baincompany-e-data-hackers_state-of-data-2025-2026.pdf>
- Data Hackers, dados abertos do State of Data Brazil:
  <https://github.com/data-hackers-br/state-of-data-brazil>
- Brasscom, Perspectivas do Mercado de Trabalho do Macrossetor TIC:
  <https://brasscom.org.br/wp-content/uploads/2025/02/Relatorio-Perspectivas-do-Mercado-de-Trabalho.pdf>
- Robert Half, Guia Salarial 2026, páginas de cargo:
  <https://www.roberthalf.com/br/pt/vagas-detalhes/analista-de-bi-pleno>,
  <https://www.roberthalf.com/br/pt/vagas-detalhes/analista-de-bi-senior>,
  <https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-junior>
  (e as variações por cidade citadas no texto)
- Glassdoor, salários de Desenvolvedor Python Júnior:
  <https://www.glassdoor.com.br/Sal%C3%A1rios/desenvolvedor-python-junior-sal%C3%A1rio-SRCH_KO0,27.htm>
- Microsoft Learn, guia de estudo do exame PL-300:
  <https://learn.microsoft.com/pt-br/credentials/certifications/resources/study-guides/pl-300>
- TOTVS TDN, TLPP x AdvPL: <https://tdn.totvs.com/display/tec/TLPP+x+AdvPL>
