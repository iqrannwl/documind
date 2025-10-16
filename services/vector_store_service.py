import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Any
from datetime import datetime
import uuid
from openai import AsyncOpenAI
from app.settings import settings


class VectorStoreService:    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.dimension = 1536
        self.index = None
        self.metadata = []
        self.documents = {}
        self.index_file = "data/faiss_index.bin"
        self.metadata_file = "data/metadata.pkl"
        self.documents_file = "data/documents.pkl"
        
        os.makedirs("data", exist_ok=True)
        
        self._load_index()
    
    def _load_index(self):
        """Load existing FAISS index and metadata"""
        try:
            if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
                self.index = faiss.read_index(self.index_file)
                with open(self.metadata_file, 'rb') as f:
                    self.metadata = pickle.load(f)
                with open(self.documents_file, 'rb') as f:
                    self.documents = pickle.load(f)
                print(f"Loaded existing index with {len(self.metadata)} vectors")
            else:
                self.index = faiss.IndexFlatL2(self.dimension)
                self.metadata = []
                self.documents = {}
                print("Initialized new FAISS index")
        except Exception as e:
            print(f"Error loading index: {e}. Initializing new index.")
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
            self.documents = {}
    
    def _save_index(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, 'wb') as f:
            pickle.dump(self.metadata, f)
        with open(self.documents_file, 'wb') as f:
            pickle.dump(self.documents, f)
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    async def _get_embedding(self, text: str) -> np.ndarray:
        response = await self.client.embeddings.create(
            model=settings.EMBEDDING_MODEL,
            input=text
        )
        return np.array(response.data[0].embedding, dtype=np.float32)
    
    async def index_documents(self, documents: List[Dict[str, str]]) -> Dict[str, Any]:
        document_ids = []
        total_chunks = 0
        
        for doc in documents:
            doc_id = str(uuid.uuid4())
            title = doc.get('title', 'Untitled')
            content = doc.get('content', '')
            
            # Split into chunks
            chunks = self._chunk_text(content)
            
            # Store document metadata
            self.documents[doc_id] = {
                'title': title,
                'chunks_count': len(chunks),
                'created_at': datetime.utcnow().isoformat()
            }
            
            # Get embeddings and add to index
            for i, chunk in enumerate(chunks):
                embedding = await self._get_embedding(chunk)
                
                # Add to FAISS index
                self.index.add(embedding.reshape(1, -1))
                
                # Store metadata
                self.metadata.append({
                    'doc_id': doc_id,
                    'title': title,
                    'chunk_index': i,
                    'content': chunk
                })
                
                total_chunks += 1
            
            document_ids.append(doc_id)
        
        # Save index to disk
        self._save_index()
        
        return {
            'document_ids': document_ids,
            'chunks_created': total_chunks
        }
    
    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if self.index.ntotal == 0:
            return []
        
        # Get query embedding
        query_embedding = await self._get_embedding(query)
        
        # Search in FAISS
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1),
            min(top_k, self.index.ntotal)
        )
        
        # Prepare results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata):
                meta = self.metadata[idx]
                results.append({
                    'doc_id': meta['doc_id'],
                    'title': meta['title'],
                    'content': meta['content'],
                    'score': float(1 / (1 + dist))
                })
        
        return results
    
    def list_documents(self) -> List[Dict[str, Any]]:
        return [
            {
                'doc_id': doc_id,
                'title': info['title'],
                'chunks_count': info['chunks_count'],
                'created_at': info['created_at']
            }
            for doc_id, info in self.documents.items()
        ]
    
    def delete_document(self, doc_id: str) -> bool:
        if doc_id not in self.documents:
            return False
        
        # Find indices to remove
        indices_to_keep = [
            i for i, meta in enumerate(self.metadata)
            if meta['doc_id'] != doc_id
        ]
        
        if len(indices_to_keep) == len(self.metadata):
            return False
        
        # Rebuild index with remaining vectors
        new_index = faiss.IndexFlatL2(self.dimension)
        new_metadata = []
        
        for idx in indices_to_keep:
            # Get vector from old index
            vector = self.index.reconstruct(idx)
            new_index.add(vector.reshape(1, -1))
            new_metadata.append(self.metadata[idx])
        
        # Update index and metadata
        self.index = new_index
        self.metadata = new_metadata
        del self.documents[doc_id]
        
        # Save updated index
        self._save_index()
        
        return True
    
    def is_initialized(self) -> bool:
        """Check if vector store is initialized"""
        return self.index is not None
