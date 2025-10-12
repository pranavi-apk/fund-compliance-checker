
#Simple vector store for semantic search using sentence transformers.

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import json
from typing import List, Dict, Tuple, Optional
from sentence_transformers import SentenceTransformer
from .pdf_parser import DocumentChunk


class VectorStore:
    """Simple in-memory vector store for document chunks."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize vector store with embedding model.
        
        Args:
            model_name: Name of the sentence-transformer model to use
        """
        print(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        self.chunks: List[DocumentChunk] = []
        self.embeddings: Optional[np.ndarray] = None
        
    def add_documents(self, chunks: List[DocumentChunk]):
        """
        Add document chunks to the vector store.
        
        Args:
            chunks: List of DocumentChunk objects to add
        """
        if not chunks:
            return
            
        print(f"Generating embeddings for {len(chunks)} chunks...")
        texts = [chunk.text for chunk in chunks]
        new_embeddings = self.embedding_model.encode(
            texts, 
            show_progress_bar=True,
            batch_size=32
        )
        
        if self.embeddings is None:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
            
        self.chunks.extend(chunks)
        print(f"Total chunks in store: {len(self.chunks)}")
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[DocumentChunk, float]]:
        """
        Search for most similar chunks to query.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            
        Returns:
            List of tuples (DocumentChunk, similarity_score)
        """
        if self.embeddings is None or len(self.chunks) == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0]
        
        # Calculate cosine similarity
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Get top k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Return chunks with scores
        results = [
            (self.chunks[idx], float(similarities[idx]))
            for idx in top_indices
        ]
        
        return results
    
    def save(self, filepath: str):
        """
        Save vector store to disk.
        
        Args:
            filepath: Path to save the vector store
        """
        data = {
            'chunks': [
                {
                    'text': chunk.text,
                    'page_number': chunk.page_number,
                    'chunk_id': chunk.chunk_id,
                    'source_file': chunk.source_file
                }
                for chunk in self.chunks
            ],
            'embeddings': self.embeddings.tolist() if self.embeddings is not None else None
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f)
        print(f"Vector store saved to {filepath}")
    
    def load(self, filepath: str):
        """
        Load vector store from disk.
        
        Args:
            filepath: Path to load the vector store from
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.chunks = [
            DocumentChunk(
                text=c['text'],
                page_number=c['page_number'],
                chunk_id=c['chunk_id'],
                source_file=c['source_file']
            )
            for c in data['chunks']
        ]
        
        if data['embeddings']:
            self.embeddings = np.array(data['embeddings'])
        
        print(f"Vector store loaded with {len(self.chunks)} chunks")
