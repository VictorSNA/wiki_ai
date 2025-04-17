# Requisitos:
# pip install streamlit langchain requests faiss-cpu langchain-text-splitters playwright nest_asyncio
# playwright install

import streamlit as st
import requests
import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List
import nest_asyncio
import asyncio
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# CONFIGURAÇÕES
MODEL = "mistral:latest"
OLLAMA_URL = "http://ollama:11434/api/generate"
BASE_URL = "https://victorsna.github.io"
START_PATH = "/wiki_ai/#/"

load_dotenv()

# Interface personalizada
st.set_page_config(page_title="RAG com LLM Local", layout="wide")
st.markdown("""
    <style>
    .main { padding: 2rem; font-family: 'Segoe UI', sans-serif; }
    .stTextInput > div > input { font-size: 1.1rem; padding: 0.6rem; }
    .stButton > button { font-size: 1.1rem; background-color: #4CAF50; color: white; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Chat com a Documentação Online - RAG + Ollama")
st.markdown("Buscando conteúdo da documentação em tempo real usando Playwright.")

nest_asyncio.apply()

# Função para fazer crawling com JS (Playwright)
async def crawl_docs(base_url, start_path, max_pages=5):
    visited = set()
    to_visit = [start_path]
    documents = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        while to_visit and len(visited) < max_pages:
            path = to_visit.pop(0)
            if path in visited:
                continue

            url = urljoin(base_url, path)
            try:
                await page.goto(url, timeout=60000)
                await page.wait_for_timeout(2000)
                text = await page.inner_text("body")
                documents.append(Document(page_content=text, metadata={"source": url}))

                hrefs = await page.eval_on_selector_all("a", "els => els.map(el => el.href)")
                for href in hrefs:
                    parsed = urlparse(href)
                    if parsed.netloc == "" or parsed.netloc == urlparse(base_url).netloc:
                        rel_path = parsed.path + (f"#{parsed.fragment}" if parsed.fragment else "")
                        if rel_path not in visited and rel_path not in to_visit:
                            to_visit.append(rel_path)
            except Exception as e:
                print(f"Erro ao acessar {url}: {e}")
            visited.add(path)
        await browser.close()
    return documents

# Carregar e criar FAISS
@st.cache_resource(show_spinner=True)
def get_vectorstore():
    docs = asyncio.run(crawl_docs(BASE_URL, START_PATH, max_pages=5))
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(chunks, embeddings)

# Função para recuperar contexto relevante
def recuperar_contexto(vectorstore, pergunta, k=3):
    resultados = vectorstore.similarity_search(pergunta, k=k)
    contexto = "\n\n".join([doc.page_content for doc in resultados])
    return contexto

# Função para gerar resposta com o modelo local
def consultar_modelo_ollama(contexto, pergunta):
    prompt = f"""
Use the following context to answer the question.

Context:
{contexto}

Question: {pergunta}
Answer:
"""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "[No response from model]")
    except Exception as e:
        return f"Erro ao consultar o modelo: {e}"

# Input do usuário
pergunta = st.text_input("💬 Digite sua pergunta:")

vectorstore = get_vectorstore()

# Processamento da pergunta
if pergunta:
    with st.spinner("Buscando resposta..."):
        contexto = recuperar_contexto(vectorstore, pergunta)
        resposta = consultar_modelo_ollama(contexto, pergunta)

    st.subheader("📘 Resposta:")
    st.write(resposta)

    with st.expander("🔎 Contexto usado"):
        st.code(contexto)
