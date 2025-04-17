# 📚 Crawler Inteligente para Documentações de Projetos com LangChain + OpenAI

Este projeto é um **crawler especializado para documentações técnicas**. Ele utiliza **Playwright** para renderizar e navegar entre páginas de uma documentação, extrai o conteúdo textual e transforma em vetores semânticos com embeddings da OpenAI. Em seguida, você pode **consultar essa base com perguntas em linguagem natural**, como se estivesse conversando com a documentação.

---

## 📌 O que este projeto faz?

- Acessa documentações web.
- Rastreia links internos e coleta o conteúdo textual renderizado.
- Cria uma base vetorial local usando FAISS com embeddings da OpenAI.
- Permite fazer **perguntas em linguagem natural sobre a documentação**, com respostas geradas via LangChain + GPT-3.5.

---

## 📁 Estrutura Esperada da Documentação

Este crawler é ideal para:

- Documentações hospedadas como Single Page Applications (ex: `https://meuprojeto.dev/docs/#/`)
- Estrutura de links internos usando `#` ou caminhos relativos (`/docs/intro`, `/docs/api`, etc)
- Documentações com conteúdo acessível diretamente no DOM (sem carregamento assíncrono excessivo via JS)

---

## 🚀 Como Usar

⚠️ O código principal está no arquivo `model/ai.ipynb`, que deve ser executado em um ambiente Jupyter (Notebook ou Lab).

1. **Abra o notebook:**

```bash
jupyter notebook model/ai.ipynb
```

ou, se preferir:

```bash
jupyter lab model/ai.ipynb
```

2. **Configure a URL base da documentação e o caminho inicial** no notebook:

```python
BASE_URL = "https://meuprojeto.github.io"
START_PATH = "/docs/#/"
```

3. **Execute as células do notebook passo a passo** e edite a variável `query` no final para fazer perguntas como:

```python
query = "Quais são os parâmetros obrigatórios para criar um usuário na API?"
```

---

## 🧠 O que o crawler faz

1. Carrega a chave da OpenAI do `.env`
2. Usa Playwright para acessar a documentação e renderizar as páginas
3. Extrai o conteúdo textual de cada página visitada
4. Usa `RecursiveCharacterTextSplitter` para dividir o conteúdo em pedaços manejáveis
5. Gera vetores semânticos com `OpenAIEmbeddings`
6. Indexa os dados com FAISS
7. Usa `RetrievalQA` para responder perguntas com base no conteúdo indexado

---

## 💡 Exemplo de Pergunta/Resposta

```bash
Pergunta:
Quais headers são obrigatórios na API para adicionar o produto no carrinho?

Resposta:
Os headers obrigatórios são Authorization e Content-Type: application/json.
```

---
