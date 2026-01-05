# Arquiteturas de Retrieval-Augmented Generation (RAG)

---

### 1. Standard RAG
<p align="justify">
É a arquitetura mais simples e direta, ideal para começar. Ela trata a recuperação como uma busca única (one-shot lookup) e assume que o mecanismo de recuperação funcionará perfeitamente na primeira tentativa.
</p>

* **Prós:** Latência baixa (<1s), custo mínimo, fácil de debugar.
* **Contras:** Suscetível a ruído, sem autocorreção.
* **Melhor para:** FAQs, bases pequenas e estruturadas.

---

### 2. Conversational RAG
<p align="justify">
Adiciona memória para conversas naturais, evitando repetições e permitindo que o modelo compreenda o contexto de interações passadas para manter a fluidez.
</p>

* **Prós:** Experiência natural, evita repetições.
* **Contras:** Memory drift, custo de tokens maior.
* **Melhor para:** Chatbots, assistentes conversacionais.

---

### 3. Corrective RAG
<p align="justify">
Valida a qualidade dos documentos recuperados antes de gerar a resposta, reduzindo drasticamente as alucinações ao conferir a relevância dos dados coletados.
</p>

* **Prós:** Reduz alucinações, preenche lacunas de dados.
* **Contras:** Latência alta (2-4s), custo de APIs.
* **Melhor para:** Saúde, legal, compliance crítico.

---

### 4. Adaptive RAG
<p align="justify">
Gerencia recursos computacionais de forma inteligente, roteando consultas para diferentes mecanismos de recuperação baseando-se na complexidade da pergunta detectada.
</p>

* **Prós:** Economia massiva, latência ótima para queries simples.
* **Contras:** Risco de classificação incorreta.
* **Melhor para:** Alta variação de complexidade, orçamento limitado.

---

### 5. Self-RAG
<p align="justify">
O modelo critica seu próprio raciocínio em tempo real, gerando tokens de reflexão especiais para validar se a resposta está devidamente fundamentada nas fontes.
</p>

* **Prós:** Máxima fundamentação, transparência total.
* **Contras:** Requer fine-tuning, overhead extremo.
* **Melhor para:** Pesquisa acadêmica, citação crítica.

---

### 6. Hybrid RAG
<p align="justify">
Combina busca vetorial e lexical para um recall excepcional, garantindo que termos técnicos específicos e o sentido semântico sejam ambos capturados.
</p>

* **Prós:** Recall excepcional, robustez a fraseado ruim.
* **Contras:** Custo 3x-5x, latência aumentada.
* **Melhor para:** Pesquisa científica, terminologia técnica.

---

### 7. HyDE
<p align="justify">
Gera uma resposta hipotética antes de buscar a real, melhorando a busca conceitual ao alinhar o espaço vetorial da pergunta com o da resposta esperada.
</p>

* **Prós:** Melhora busca conceitual, não requer fine-tuning.
* **Contras:** Risco de viés, ineficiente para lookups simples.
* **Melhor para:** Consultas vagas, busca conceitual.

---

### 8. Agentic RAG
<p align="justify">
Lida com consultas multi-partes e dados em tempo real usando orquestração de ferramentas. O agente decide autonomamente quais passos tomar para resolver o problema.
</p>

* **Prós:** Lida com multi-partes, dados em tempo real.
* **Contras:** Latência alta (5-15s), custo significativo.
* **Melhor para:** Análise multi-fonte, consultoria estratégica.

---

### 9. GraphRAG
<p align="justify">
Usa um grafo de conhecimento para raciocínio causal e análise de redes. É ideal para conectar informações entre documentos que não possuem ligação direta aparente.
</p>

* **Prós:** Raciocínio causal, precisão ~99% em domínios estruturados.
* **Contras:** Alto custo de construção, computacionalmente caro.
* **Melhor para:** Análise de redes, detecção de fraude, pesquisa científica.
