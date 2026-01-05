<div style="text-align: justify;">

# Arquiteturas de Retrieval-Augmented Generation (RAG)

---

### 1. Standard RAG
**Descrição:** É a arquitetura mais simples e direta, ideal para começar. Ela trata a recuperação como uma busca única (one-shot lookup) e assume que o mecanismo de recuperação funcionará perfeitamente na primeira tentativa.
* **Prós:** Latência baixa (<1s), custo mínimo, fácil de debugar.
* **Contras:** Suscetível a ruído, sem autocorreção.
* **Melhor para:** FAQs, bases pequenas e estruturadas.

---

### 2. Conversational RAG
**Descrição:** Adiciona memória para conversas naturais, evitando repetições. Permite que o modelo entenda o contexto de perguntas anteriores para manter a fluidez do diálogo.
* **Prós:** Experiência natural, evita repetições.
* **Contras:** Memory drift, custo de tokens maior.
* **Melhor para:** Chatbots, assistentes conversacionais.

---

### 3. Corrective RAG
**Descrição:** Valida a qualidade dos documentos recuperados antes de gerar a resposta, reduzindo alucinações. Garante que apenas informações pertinentes alimentem o modelo.
* **Prós:** Reduz alucinações, preenche lacunas de dados.
* **Contras:** Latência alta (2-4s), custo de APIs.
* **Melhor para:** Saúde, legal, compliance crítico.

---

### 4. Adaptive RAG
**Descrição:** Gerencia recursos computacionais de forma inteligente, roteando consultas para diferentes mecanismos de recuperação conforme a complexidade detectada.
* **Prós:** Economia massiva, latência ótima para queries simples.
* **Contras:** Risco de classificação incorreta.
* **Melhor para:** Alta variação de complexidade, orçamento limitado.

---

### 5. Self-RAG
**Descrição:** O modelo critica seu próprio raciocínio em tempo real, gerando tokens de reflexão especiais para validar se a resposta está devidamente fundamentada.
* **Prós:** Máxima fundamentação, transparência total.
* **Contras:** Requer fine-tuning, overhead extremo.
* **Melhor para:** Pesquisa acadêmica, citação crítica.

---

### 6. Hybrid RAG
**Descrição:** Combina busca vetorial e lexical para recall excepcional. É capaz de entender o sentido da frase e também encontrar termos técnicos específicos.
* **Prós:** Recall excepcional, robustez a fraseado ruim.
* **Contras:** Custo 3x-5x, latência aumentada.
* **Melhor para:** Pesquisa científica, terminologia técnica.

---

### 7. HyDE
**Descrição:** Gera uma resposta hipotética antes de buscar a real, melhorando a busca conceitual ao alinhar o espaço vetorial da pergunta com o da resposta.
* **Prós:** Melhora busca conceitual, não requer fine-tuning.
* **Contras:** Risco de viés, ineficiente para lookups simples.
* **Melhor para:** Consultas vagas, busca conceitual.

---

### 8. Agentic RAG
**Descrição:** Lida com consultas multi-partes e dados em tempo real usando orquestração de ferramentas. O agente decide quais passos tomar para resolver o problema.
* **Prós:** Lida com multi-partes, dados em tempo real.
* **Contras:** Latência alta (5-15s), custo significativo.
* **Melhor para:** Análise multi-fonte, consultoria estratégica.

---

### 9. GraphRAG
**Descrição:** Usa um grafo de conhecimento para raciocínio causal e análise de redes. Excelente para conectar pontos entre documentos distantes.
* **Prós:** Raciocínio causal, precisão ~99% em domínios estruturados.
* **Contras:** Alto custo de construção, computacionalmente caro.
* **Melhor para:** Análise de redes, detecção de fraude, pesquisa científica.

</div>
