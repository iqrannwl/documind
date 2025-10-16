# documind
AI-powered document question answering with semantic search and vector embeddings

# How to set up and run the project
## ⚙️ Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/iqrannwl/documind.git
cd documind
```

### 2. Create Virtual Environment

```
python3 -m venv venv
source venv/bin/activate   # on macOS/Linux
venv\Scripts\activate      # on Windows
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the project root:
```
OPENAI_API_KEY=sk-your-key
VECTOR_STORE_PATH=vectorstore.faiss
CHUNK_SIZE=500
```


### 5. Run the Server

```
uvicorn main:app --reload
```


# How to test each endpoint

```
http://127.0.0.1:8000/docs
```

# What tools or libraries you used and why

## 🧠 Tools & Libraries Used
### FastAPI

* Why: A modern, high-performance web framework for building APIs quickly with automatic OpenAPI documentation, async support, and Pydantic-based validation.

* Usage: Defines and exposes RESTful endpoints for document ingestion, querying, and health checks.

### Pydantic / Pydantic Settings

* Why: Provides powerful data validation and settings management using Python type hints.

* Usage: Handles request validation (e.g., document and query models) and environment configuration via .env for API keys and constants.

### OpenAI API

* Why: Provides access to powerful LLMs (like GPT-3.5 and GPT-4) for generating natural language answers from retrieved document context.

* Usage: Used in the LLMService to generate context-aware answers to user queries.

### FAISS (Facebook AI Similarity Search)

* Why: A fast and efficient library for vector similarity search and clustering at scale.

* Usage: Used as the vector store to index and retrieve document embeddings for semantic search.

### OpenAI Embeddings (text-embedding-ada-002)

* Why: Converts text into numerical vector representations that capture semantic meaning.

* Usage: Used to embed document chunks and user queries for similarity comparison in the vector database.

### LangChain (optional / utility layer)

* Why: Simplifies chaining together LLM calls and vector search for context-aware Q&A workflows.

* Usage: Used as an optional abstraction layer for query pipeline and retrieval-augmented generation (RAG).

### Uvicorn

* Why: A lightning-fast ASGI server ideal for serving FastAPI applications.

* Usage: Used to run the API locally and in production.

### PyPDF2 / Markdown / TextLoader (Utils)

* why: Enables reading and parsing of multiple file formats like PDF, TXT, and Markdown.

* Usage: Used in the file_loader.py utility to extract text from uploaded documents for indexing.

### FAISS / Chroma (Vector Database)

* Why: Both are efficient local vector databases that allow similarity searches across embeddings.

* Usage: Stores and retrieves embeddings for the document search pipeline.
