# Arquiteturas de Retrieval-Augmented Generation (RAG)

Este guia resume as principais abordagens para sistemas RAG, detalhando suas características, vantagens, limitações e casos de uso ideais.

---

### 1. Standard RAG
* **Descrição:** É a arquitetura mais simples e direta, ideal para começar. Ela trata a recuperação como uma busca única (one-shot lookup) e assume que o mecanismo de recuperação funcionará perfeitamente na primeira tentativa.
* **Prós:** Latência baixa (<1s), custo mínimo, fácil de debugar.
* **Contras:** Suscetível a ruído, sem autocorreção.
* **Melhor para:** FAQs, bases pequenas e estruturadas.



### 2. Conversational RAG
* **Descrição:** Adiciona memória para manter o contexto de conversas naturais, permitindo que o modelo entenda referências a mensagens anteriores e evite repetições desnecessárias.
* **Prós:** Experiência natural, evita repetições.
* **Contras:** Risco de "memory drift" e custo de tokens progressivamente maior conforme o histórico cresce.
* **Melhor para:** Chatbots e assistentes conversacionais dinâmicos.

### 3. Corrective RAG (C-RAG)
* **Descrição:** Valida a qualidade e a relevância dos documentos recuperados antes de gerar a resposta. Se os dados forem irrelevantes, o sistema pode buscar fontes externas ou ignorar o conteúdo para reduzir alucinações.
* **Prós:** Reduz drasticamente as alucinações e preenche lacunas de dados.
* **Contras:** Latência mais alta (2-4s) e maior custo de APIs devido às camadas de validação.
* **Melhor para:** Setores de saúde, legal e compliance crítico.



### 4. Adaptive RAG
* **Descrição:** Gerencia recursos computacionais de forma inteligente, utilizando um classificador para rotear consultas para diferentes mecanismos de recuperação (dos mais simples aos mais complexos).
* **Prós:** Economia massiva de recursos e latência ótima para queries simples.
* **Contras:** Risco de classificação incorreta da complexidade da pergunta.
* **Melhor para:** Sistemas com alta variação de complexidade e orçamentos limitados.

### 5. Self-RAG
* **Descrição:** O modelo critica seu próprio raciocínio e a utilidade dos documentos em tempo real, gerando tokens de reflexão especiais para decidir se deve continuar ou buscar mais informações.
* **Prós:** Máxima fundamentação (grounding) e transparência total no processo de pensamento.
* **Contras:** Requer fine-tuning específico do modelo e possui um overhead computacional extremo.
* **Melhor para:** Pesquisa acadêmica e cenários de citação crítica.

### 6. Hybrid RAG
* **Descrição:** Combina a busca vetorial (semântica) com a busca lexical (palavras-chave/BM25) para garantir um recall excepcional, unindo contexto e precisão de termos.
* **Prós:** Recall excepcional e alta robustez a fraseados ruins ou termos técnicos específicos.
* **Contras:** Custo de infraestrutura 3x-5x maior e latência ligeiramente aumentada.
* **Melhor para:** Pesquisa científica e domínios com terminologia técnica densa.

### 7. HyDE (Hypothetical Document Embeddings)
* **Descrição:** O modelo gera uma resposta hipotética primeiro e utiliza essa resposta "fictícia" para buscar documentos reais semanticamente similares no banco de dados.
* **Prós:** Melhora significativamente a busca conceitual; não requer fine-tuning.
* **Contras:** Risco de viés inicial e ineficiente para consultas de fatos simples (lookups).
* **Melhor para:** Consultas vagas ou busca puramente conceitual.

### 8. Agentic RAG
* **Descrição:** Utiliza agentes de IA para lidar com consultas multi-partes e dados em tempo real, orquestrando diferentes ferramentas, navegadores ou bases de dados conforme a necessidade.
* **Prós:** Capacidade de resolver problemas complexos e acessar dados em tempo real.
* **Contras:** Latência alta (5-15s) e custo significativo por execução.
* **Melhor para:** Análise multi-fonte e consultoria estratégica.

### 9. GraphRAG
* **Descrição:** Utiliza um Grafo de Conhecimento (Knowledge Graph) em vez de apenas vetores, permitindo o raciocínio sobre relações causais e análise de redes complexas.
* **Prós:** Excelente raciocínio causal e precisão próxima de 99% em domínios altamente estruturados.
* **Contras:** Altíssimo custo de construção do grafo e processamento caro.
* **Melhor para:** Detecção de fraude, análise de redes e pesquisa científica avançada.
