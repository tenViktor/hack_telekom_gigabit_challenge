# backend/services/vector_store.py
import faiss
import numpy as np
from typing import List, Dict
import pickle
import os
from transformers import AutoTokenizer, AutoModel
import torch

class VectorStore:
    def __init__(self):
        self.index_file = "/data/faiss/vulnerability_index.idx"
        self.mapping_file = "/data/faiss/id_mapping.pkl"
        self.embedding_dim = 768  # BERT embedding dimension
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.model = AutoModel.from_pretrained('bert-base-uncased')
        
        # Load or create index
        if os.path.exists(self.index_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.mapping_file, 'rb') as f:
                self.id_mapping = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.id_mapping = {}

    def get_embedding(self, text: str) -> np.ndarray:
        inputs = self.tokenizer(text, return_tensors="pt", 
                              max_length=512, truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).numpy()

    async def add_vulnerability(self, vuln_id: int, description: str):
        embedding = self.get_embedding(description)
        self.index.add(embedding)
        self.id_mapping[self.index.ntotal - 1] = vuln_id
        await self._save_index()

    async def find_similar(self, query: str, k: int = 5) -> List[int]:
        query_vector = self.get_embedding(query)
        D, I = self.index.search(query_vector, k)
        return [self.id_mapping[i] for i in I[0]]

    async def _save_index(self):
        os.makedirs("/data/faiss", exist_ok=True)
        faiss.write_index(self.index, self.index_file)
        with open(self.mapping_file, 'wb') as f:
            pickle.load(self.id_mapping, f)

# Initial data loading script
async def load_vulnerability_data():
    store = VectorStore()
    
    # Load from various sources
    vulnerabilities = [
        {"id": 1, "description": "SQL injection vulnerability in login form"},
        {"id": 2, "description": "Cross-site scripting in user profile"},
        # ... more vulnerabilities
    ]
    
    for vuln in vulnerabilities:
        await store.add_vulnerability(vuln["id"], vuln["description"])
