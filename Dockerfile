# Dockerfile para app Streamlit + LangChain + Playwright

FROM python:3.13-slim

# Evita prompts do Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y curl gnupg unzip git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala Playwright e bibliotecas Python
RUN pip install --no-cache-dir \
    streamlit \
    langchain \
    requests \
    faiss-cpu \
    langchain-text-splitters \
    playwright \
    nest_asyncio \
    langchain-community \
    python-dotenv \
    openai \
    tiktoken

# Instala os navegadores do Playwright
RUN python -m playwright install --with-deps

# Cria diretório da app
WORKDIR /app
COPY . /app

# Porta padrão do Streamlit
EXPOSE 8501

# Comando para iniciar o app
CMD ["streamlit", "run", "model/ai.py"]
