# backend/hybrid_search.py
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AdvancedHybridSearch:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.embedder = FinancialEmbedder()
        self.setup_hybrid_index()
    
    def setup_hybrid_index(self):
        """Initialise les index hybrides"""
        # Index sémantique FAISS
        self.semantic_index = faiss.IndexFlatIP(384)  # Dimension des embeddings
        
        # Index lexical TF-IDF avec paramètres optimisés
        self.tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),  # Bigrams et trigrams
            max_features=20000,
            stop_words='english',
            min_df=2,
            max_df=0.8
        )
        
        # Préparation des données
        self.prepare_indices()
    
    def prepare_indices(self):
        """Prépare les indices avec les chunks"""
        if not self.kb.chunks:
            return
        
        # Embeddings sémantiques
        chunk_texts = [chunk['chunk'] for chunk in self.kb.chunks]
        self.embeddings = np.array([self.embedder.get_embedding(text) for text in chunk_texts])
        
        # Ajout à FAISS
        self.semantic_index.add(self.embeddings)
        
        # Index TF-IDF
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(chunk_texts)
    
    def hybrid_search(self, query, top_k=5, semantic_weight=0.7, lexical_weight=0.3):
        """Recherche hybride avancée"""
        # Recherche sémantique
        semantic_results = self.semantic_search(query, top_k * 3)
        
        # Recherche lexicale
        lexical_results = self.lexical_search(query, top_k * 3)
        
        # Fusion intelligente
        fused_results = self.intelligent_fusion(
            semantic_results, lexical_results, 
            semantic_weight, lexical_weight
        )
        
        # Re-ranking
        reranked_results = self.rerank_with_cross_encoder(query, fused_results)
        
        return reranked_results[:top_k]
    
    def semantic_search(self, query, top_k):
        """Recherche sémantique avec FAISS"""
        query_embedding = self.embedder.get_embedding(query).reshape(1, -1)
        
        # Recherche dans FAISS
        scores, indices = self.semantic_index.search(query_embedding, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.kb.chunks):
                results.append({
                    'chunk': self.kb.chunks[idx]['chunk'],
                    'metadata': self.kb.chunks[idx]['metadata'],
                    'similarity_score': float(score),
                    'search_type': 'semantic'
                })
        
        return results
    
    def lexical_search(self, query, top_k):
        """Recherche lexicale avec TF-IDF"""
        query_vector = self.tfidf_vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Obtenir les top_k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:
                results.append({
                    'chunk': self.kb.chunks[idx]['chunk'],
                    'metadata': self.kb.chunks[idx]['metadata'],
                    'similarity_score': float(similarities[idx]),
                    'search_type': 'lexical'
                })
        
        return results
    
    def intelligent_fusion(self, semantic_results, lexical_results, semantic_weight, lexical_weight):
        """Fusion intelligente des résultats"""
        all_results = {}
        
        # Combiner les résultats
        for result in semantic_results:
            chunk_text = result['chunk']
            if chunk_text not in all_results:
                all_results[chunk_text] = {
                    'chunk': chunk_text,
                    'metadata': result['metadata'],
                    'semantic_score': result['similarity_score'] * semantic_weight,
                    'lexical_score': 0,
                    'combined_score': result['similarity_score'] * semantic_weight
                }
        
        for result in lexical_results:
            chunk_text = result['chunk']
            if chunk_text in all_results:
                all_results[chunk_text]['lexical_score'] = result['similarity_score'] * lexical_weight
                all_results[chunk_text]['combined_score'] += result['similarity_score'] * lexical_weight
            else:
                all_results[chunk_text] = {
                    'chunk': chunk_text,
                    'metadata': result['metadata'],
                    'semantic_score': 0,
                    'lexical_score': result['similarity_score'] * lexical_weight,
                    'combined_score': result['similarity_score'] * lexical_weight
                }
        
        # Convertir en liste et trier
        fused_list = list(all_results.values())
        return sorted(fused_list, key=lambda x: x['combined_score'], reverse=True)
    
    def rerank_with_cross_encoder(self, query, candidates):
        """Re-ranking avec modèle cross-encoder"""
        try:
            from sentence_transformers import CrossEncoder
            cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
            
            pairs = [[query, candidate['chunk']] for candidate in candidates]
            scores = cross_encoder.predict(pairs)
            
            for candidate, score in zip(candidates, scores):
                candidate['relevance_score'] = float(score)
            
            return sorted(candidates, key=lambda x: x['relevance_score'], reverse=True)
        except:
            # Fallback sans re-ranking
            return candidates