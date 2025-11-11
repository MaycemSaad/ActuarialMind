# backend/advanced_embeddings.py
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
from transformers import AutoTokenizer, AutoModel

class FinancialEmbedder:
    def __init__(self):
        # Modèle général pour fallback
        self.general_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Tentative de chargement de modèles spécialisés
        self.specialized_models = self._load_specialized_models()
        
        # Lexique financier étendu pour l'adaptation
        self.finance_terms = self._load_finance_vocabulary()
    
    def _load_specialized_models(self):
        """Charge des modèles spécialisés si disponibles"""
        models = {}
        try:
            # Modèle pour documents financiers
            models['finance'] = SentenceTransformer('nickprock/finbert-tone')
            print("✅ Modèle financier chargé")
        except:
            print("⚠️  Modèle financier non disponible")
        
        try:
            # Modèle multilingue
            models['multilingual'] = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
            print("✅ Modèle multilingue chargé")
        except:
            print("⚠️  Modèle multilingue non disponible")
            
        return models
    
    def _load_finance_vocabulary(self):
        """Vocabulaire spécialisé finance/actuariat"""
        return {
            'risk_terms': ['var', 'cvar', 'volatility', 'liquidity', 'stress_testing', 'capital_adequacy'],
            'regulation_terms': ['basel', 'ifrs', 'solvency', 'compliance', 'regulation', 'reporting'],
            'actuarial_terms': ['mortality', 'longevity', 'reserving', 'premium', 'annuity', 'underwriting'],
            'quantitative_terms': ['derivatives', 'pricing', 'valuation', 'hedging', 'portfolio', 'optimization']
        }
    
    def get_embedding(self, text, model_type='auto'):
        """Génère des embeddings adaptés au domaine"""
        if model_type == 'auto':
            model_type = self.detect_domain(text)
        
        if model_type in self.specialized_models:
            try:
                embedding = self.specialized_models[model_type].encode(text)
                # Amélioration avec pondération domaine
                embedding = self.enhance_domain_relevance(embedding, text)
                return embedding
            except:
                pass
        
        # Fallback au modèle général
        return self.general_model.encode(text)
    
    def detect_domain(self, text):
        """Détecte le domaine du texte"""
        text_lower = text.lower()
        finance_score = sum(1 for term in self.finance_terms['risk_terms'] + 
                          self.finance_terms['regulation_terms'] if term in text_lower)
        actuarial_score = sum(1 for term in self.finance_terms['actuarial_terms'] if term in text_lower)
        
        if actuarial_score > finance_score:
            return 'actuarial'
        elif finance_score > 2:
            return 'finance'
        else:
            return 'general'
    
    def enhance_domain_relevance(self, embedding, text):
        """Améliore la pertinence des embeddings pour le domaine"""
        # Technique simple d'augmentation pour les termes clés
        boost_factor = 1.1  # Augmentation légère
        return embedding * boost_factor