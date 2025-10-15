# documind
AI-powered document question answering with semantic search and vector embeddings


# ⚙️ Setup Instructions

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