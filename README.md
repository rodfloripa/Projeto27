# Projeto27
RAG usando busca semantica+bm25

Esta implementação é um sistema de **RAG Adaptativo e Híbrido** bastante sofisticado e moderno. Ela abandona padrões rígidos e utiliza técnicas avançadas para garantir que a recuperação de dados seja eficiente tanto para buscas semânticas quanto para buscas por palavras-chave.

Abaixo, detalho as características principais e as decisões de projeto tomadas:

---

## 1. Mudança para LCEL (LangChain Expression Language)

Uma das evoluções mais importantes no código é o uso de **LCEL** na linha:
`chain = prompt | self.llm | StrOutputParser()`.

* **Por que abandonar as chains antigas?** As classes antigas (como `RetrievalQA`) eram "caixas pretas" difíceis de customizar. O LCEL usa o operador pipe (`|`), tornando o fluxo de dados explícito.
* **Componibilidade:** É muito mais fácil adicionar um parser de saída ou modificar o prompt sem precisar herdar classes complexas.
* **Streaming e Async:** O LCEL suporta nativamente execução assíncrona e streaming de tokens, o que facilita escalar o sistema no futuro.

---

## 2. Configuração Adaptativa de Hiperparâmetros

O método `_setup_adaptive_params` é um diferencial raro em implementações básicas. O sistema analisa o volume total de texto antes de indexar.

* **Decisão de Projeto:** * **Documentos pequenos:** Usa chunks menores () para precisão cirúrgica.
* **Documentos grandes:** Usa chunks maiores () e recupera mais documentos ().


* **Objetivo:** Evitar a perda de contexto em bases de dados extensas e economizar processamento em bases pequenas.

---

## 3. Arquitetura de Recuperação Híbrida

A classe utiliza dois motores de busca simultâneos no método `hybrid_retrieve`:

1. **Milvus (Busca Vetorial):** Utiliza o modelo `text-embedding-3-large` para entender o **conceito** da pergunta (busca semântica). Usa o modo `mmr` (Maximal Marginal Relevance) para garantir que os resultados sejam diversos e não repetitivos.
2. **BM25 (Busca de Palavras-chave):** Um algoritmo estatístico que foca em termos exatos. É excelente para encontrar nomes próprios, códigos ou termos técnicos que os embeddings podem "confundir".

* **Deduplicação:** O código combina os resultados e remove duplicatas baseando-se no conteúdo, garantindo que o contexto enviado ao LLM seja único e rico.

---

## 4. Rastreabilidade e Citação (O "Pé de Página")

Uma decisão crítica de design foi a implementação manual de um sistema de citações.

* **Mapeamento `id_to_source`:** Durante a recuperação, o código cria um dicionário que vincula o número da fonte ao arquivo e página originais.
* **Regex de Captura:** O sistema usa `re.findall(r'Fonte\s?(\d+)')` para varrer a resposta do GPT. Ele só lista no rodapé as fontes que a IA **realmente citou** no texto.
* **Agrupamento Inteligente:** Se a IA citar a [Fonte 1] e a [Fonte 2] e ambas forem do mesmo arquivo "Contrato.pdf", o rodapé agrupa essas informações para uma leitura mais limpa.

---

## 5. Escolhas Tecnológicas (Stack)

* **Milvus:** Escolhido como banco vetorial por ser focado em produção e suportar milhões de vetores com baixa latência.
* **text-embedding-3-large:** É o modelo de embedding mais potente da OpenAI atualmente, oferecendo uma representação matemática muito precisa do texto.
* **GPT-4o:** Utilizado com `temperature=0` para garantir que a resposta seja factual e não criativa (alucinação mínima).
* **RecursiveCharacterTextSplitter:** Diferente de um splitter simples, ele tenta manter parágrafos e frases juntos, respeitando a estrutura semântica do texto.

---
O Problema das Chains Antigas vs. A Solução LCEL

As chains antigas funcionavam como uma "caixa preta". Quando ocorria um erro de tipagem ou de conexão entre o banco de dados e o modelo, era quase impossível rastrear em qual etapa o dado se perdia.
1. Transparência e Depuração

    Nas Chains Antigas: O fluxo era interno. Se o Milvus retornasse um formato de dado levemente diferente, a chain quebrava com erros genéricos.

    No  código (LCEL): Com a estrutura prompt | self.llm | StrOutputParser(), cada etapa é um objeto independente. Você consegue ver exatamente o que sai do prompt e entra no modelo, facilitando a correção de erros de entrada/saída.

2. Controle do Contexto

    Erro comum: As chains padrão tentavam injetar o contexto automaticamente, o que frequentemente estourava o limite de tokens ou formatava as fontes de maneira confusa.

    Sua decisão: Você optou por montar o context_parts manualmente em uma lista e injetá-lo no dicionário do invoke. Isso garante que você tenha controle total sobre como as fontes aparecem para a IA, evitando os erros de formatação que as chains automáticas causavam.

Arquitetura de Fluxo da RAG

Para visualizar como essas decisões de projeto se conectam e evitam os erros das chains tradicionais, veja o fluxo de dados implementado:
Outras Decisões de Projeto Relevantes

*   Tratamento de Exceções no Milvus: Você adicionou um loop de 5 tentativas (for i in range(5)) com time.sleep(5) ao conectar ao banco. Isso é uma decisão de engenharia para lidar com problemas de rede ou tempo de subida do container Docker ("standalone"), algo que as chains prontas não fazem sozinhas.

*  Deduplicação Manual: No método hybrid_retrieve, você usa um set() para garantir que o mesmo conteúdo não seja enviado duas vezes para o GPT. Isso economiza dinheiro (tokens) e evita que a IA fique confusa com informações repetidas.

*  Pós-processamento de Resposta: O uso de re.findall para extrair as fontes após a geração da resposta permite que o sistema seja honesto. Ele não lista todas as fontes recuperadas, apenas aquelas que a IA realmente utilizou para formular o texto.

## Resumo das Características

| Característica | Implementação no Código |
| --- | --- |
| **Recuperação** | Híbrida (Vetor + BM25) |
| **Processamento** | Adaptativo (ajusta chunk size via volume de dados) |
| **Interface** | LCEL (moderno e modular) |
| **Fidelidade** | Prompt restritivo ("Use APENAS o contexto") |
| **Transparência** | Rodapé dinâmico com arquivo e página |

**Deseja que eu ajude a implementar uma lógica de "Re-ranking" para melhorar ainda mais a ordem desses resultados antes de enviar para o GPT?**
