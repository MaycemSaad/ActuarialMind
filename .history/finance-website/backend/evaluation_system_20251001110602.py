# backend/evaluation_system.py
import numpy as np
from datetime import datetime, timedelta
import json

class RAGEvaluator:
    def __init__(self):
        self.evaluation_data = []
        self.performance_metrics = {
            'response_relevance': [],
            'context_utilization': [],
            'technical_accuracy': [],
            'user_satisfaction': []
        }
    
    def log_interaction(self, query, response, context_used, user_feedback=None):
        """Log une interaction pour évaluation"""
        metrics = self.calculate_automatic_metrics(query, response, context_used)
        
        interaction_data = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response_preview': response[:500] + '...' if len(response) > 500 else response,
            'context_used': bool(context_used),
            'context_length': len(context_used) if context_used else 0,
            'automatic_metrics': metrics,
            'user_feedback': user_feedback
        }
        
        self.evaluation_data.append(interaction_data)
        
        # Mettre à jour les métriques de performance
        self.update_performance_metrics(metrics, user_feedback)
        
        # Sauvegarder périodiquement
        if len(self.evaluation_data) % 10 == 0:
            self.save_evaluation_data()
    
    def calculate_automatic_metrics(self, query, response, context_used):
        """Calcule des métriques automatiques de qualité"""
        embedder = FinancialEmbedder()
        
        # Similarité sémantique query-réponse
        query_embedding = embedder.get_embedding(query)
        response_embedding = embedder.get_embedding(response)
        relevance_score = np.dot(query_embedding, response_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(response_embedding)
        )
        
        # Utilisation du contexte
        if context_used:
            context_embedding = embedder.get_embedding(context_used)
            response_to_context = np.dot(response_embedding, context_embedding) / (
                np.linalg.norm(response_embedding) * np.linalg.norm(context_embedding)
            )
            context_utilization = min(1.0, response_to_context * 2)  # Amplifier
        else:
            context_utilization = 0
        
        # Score de confiance technique
        technical_terms = ['var', 'cvar', 'basel', 'ifrs', 'solvency', 'mortality', 'premium']
        technical_score = sum(1 for term in technical_terms if term in response.lower()) / len(technical_terms)
        
        return {
            'relevance_score': float(relevance_score),
            'context_utilization': float(context_utilization),
            'technical_accuracy': float(technical_score),
            'response_length': len(response)
        }
    
    def update_performance_metrics(self, metrics, user_feedback):
        """Met à jour les métriques de performance"""
        for key in ['relevance_score', 'context_utilization', 'technical_accuracy']:
            if key in metrics:
                self.performance_metrics[key].append(metrics[key])
        
        if user_feedback:
            self.performance_metrics['user_satisfaction'].append(user_feedback)
    
    def get_performance_report(self):
        """Génère un rapport de performance"""
        report = {}
        
        for metric, values in self.performance_metrics.items():
            if values:
                report[metric] = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'count': len(values),
                    'trend': 'improving' if len(values) > 10 and np.mean(values[-5:]) > np.mean(values[:-5]) else 'stable'
                }
        
        return report
    
    def identify_improvement_areas(self):
        """Identifie les domaines nécessitant des améliorations"""
        report = self.get_performance_report()
        improvements = []
        
        if report.get('relevance_score', {}).get('mean', 0) < 0.6:
            improvements.append("Améliorer la pertinence des réponses - revoir le RAG")
        
        if report.get('context_utilization', {}).get('mean', 0) < 0.4:
            improvements.append("Meilleure utilisation du contexte - optimiser la recherche")
        
        if report.get('technical_accuracy', {}).get('mean', 0) < 0.5:
            improvements.append("Renforcer la précision technique - enrichir la base de connaissances")
        
        return improvements
    
    def save_evaluation_data(self):
        """Sauvegarde les données d'évaluation"""
        try:
            data = {
                'evaluation_data': self.evaluation_data[-1000:],  # Garder les 1000 dernières
                'performance_report': self.get_performance_report(),
                'improvement_suggestions': self.identify_improvement_areas(),
                'last_updated': datetime.now().isoformat()
            }
            
            with open('evaluation_data.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Erreur sauvegarde évaluation: {e}")