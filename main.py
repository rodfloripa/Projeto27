import os
import time
import re
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_milvus import Milvus
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.retrievers import BM25Retriever

class FinalAdaptiveRAG:
    def __init__(self):
        self.milvus_host = os.getenv('MILVUS_HOST', 'standalone')
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        self.chunk_size = 600
        self.chunk_overlap = 150
        self.k_retrieval = 5
        self.search_type = "mmr"
        
        self.vectorstore = None
        self.bm25 = None

    def _setup_adaptive_params(self, docs):
        total_chars = sum(len(d.page_content) for d in docs)
        if total_chars < 15000:
            self.chunk_size, self.chunk_overlap, self.k_retrieval = 450, 80, 4
        elif total_chars < 120000:
            self.chunk_size, self.chunk_overlap, self.k_retrieval = 800, 150, 6
        else:
            self.chunk_size, self.chunk_overlap, self.k_retrieval = 1200, 250, 10
        print(f"[INFO] Configuração Adaptativa: {total_chars} chars. K={self.k_retrieval}")

    def index_documents(self):
        if not os.path.exists('docs'): return False
        loader = DirectoryLoader('docs/', glob="**/*.pdf", loader_cls=PyPDFLoader)
        docs = loader.load()
        if not docs: return False

        self._setup_adaptive_params(docs)
        splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        chunks = splitter.split_documents(docs)

        self.bm25 = BM25Retriever.from_documents(chunks)
        self.bm25.k = self.k_retrieval

        for i in range(5):
            try:
                self.vectorstore = Milvus.from_documents(
                    chunks, self.embeddings, 
                    connection_args={"uri": f"http://{self.milvus_host}:19530"},
                    drop_old=True
                )
                break
            except Exception as e:
                time.sleep(5)
        return True

    def hybrid_retrieve(self, question):
        if not self.vectorstore or not self.bm25: return []
        vec_res = self.vectorstore.search(question, search_type=self.search_type, k=self.k_retrieval, fetch_k=self.k_retrieval*2)
        kw_res = self.bm25.invoke(question)
        
        seen, combined = set(), []
        for d in (vec_res + kw_res):
            if d.page_content not in seen:
                combined.append(d)
                seen.add(d.page_content)
        return combined[:(5 if self.k_retrieval > 5 else 3)]

    def ask(self, question):
        results = self.hybrid_retrieve(question)
        if not results: return "Sem informações."

        context_parts = []
        id_to_source = {} # Mapeia o número da fonte para os metadados
        
        for i, d in enumerate(results):
            ref_id = str(i + 1)
            fname = os.path.basename(d.metadata.get('source', 'Doc'))
            page = str(d.metadata.get('page', '0'))
            context_parts.append(f"[Fonte {ref_id} | Arquivo: {fname} | Pág: {page}]\n{d.page_content}")
            id_to_source[ref_id] = {"file": fname, "page": page}
        
        template = """Responda à pergunta usando APENAS o contexto abaixo.
        Para cada informação usada, você DEVE citar o número da fonte no formato [Fonte X].
        CONTEXTO:
        {context}
        PERGUNTA: {question}
        RESPOSTA:"""
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm | StrOutputParser()
        resposta_llm = chain.invoke({"context": "\n\n".join(context_parts), "question": question})
        
        # --- Lógica de Rodapé Corrigida ---
        # Captura todos os números após a palavra 'Fonte'
        citacoes = re.findall(r'Fonte\s?(\d+)', resposta_llm)
        fontes_unicas = sorted(list(set(citacoes)))
        
        # Agrupamento por arquivo para evitar repetição
        agrupado = {}
        for n in fontes_unicas:
            if n in id_to_source:
                info = id_to_source[n]
                arq, pag = info["file"], info["page"]
                if arq not in agrupado: agrupado[arq] = {"paginas": set(), "numeros": set()}
                agrupado[arq]["paginas"].add(pag)
                agrupado[arq]["numeros"].add(n)

        footer = "\n\n--- FONTES CITADAS NA RESPOSTA ---"
        if not agrupado:
            footer += "\nNenhuma fonte detectada no texto."
        else:
            for arq, dados in agrupado.items():
                pags = ", ".join(sorted(list(dados["paginas"]), key=int))
                nums = ", ".join(sorted(list(dados["numeros"]), key=int))
                footer += f"\n- [Fonte {nums}] {arq} (Páginas: {pags}) "
            
        return f"{resposta_llm}{footer}"

if __name__ == "__main__":
    rag = FinalAdaptiveRAG()
    if rag.index_documents():
        while True:
            q = input("\nPergunta: ")
            if q.lower() in ['sair', 'exit']: break
            print(rag.ask(q))
