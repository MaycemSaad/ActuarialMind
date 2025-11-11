# backend/advanced_prompts.py
class AdvancedPromptEngine:
    def __init__(self):
        self.domain_experts = {
            'risk_management': {
                'persona': "Expert en Risk Management certifié FRM avec 15 ans d'expérience",
                'style': "Technique et prudent, focus sur les mesures quantitatives",
                'key_topics': ['VaR', 'CVaR', 'stress testing', 'capital allocation', 'liquidity risk']
            },
            'actuarial': {
                'persona': "Actuaire Fellow avec expertise en modélisation actuarielle",
                'style': "Précis et méthodique, utilisation de modèles stochastiques", 
                'key_topics': ['mortality', 'reserving', 'pricing', 'Solvency II', 'IFRS 17']
            },
            'regulation': {
                'persona': "Spécialiste en conformité réglementaire financière",
                'style': "Structuré et normatif, référence aux textes officiels",
                'key_topics': ['Bâle III/IV', 'IFRS', 'reporting', 'compliance', 'audit']
            },
            'quantitative': {
                'persona': "Quantitative Analyst expert en modèles financiers",
                'style': "Mathématique et technique, utilisation de formules et algorithmes",
                'key_topics': ['derivatives', 'pricing models', 'monte carlo', 'optimization']
            }
        }
    
    def detect_domain(self, query, context):
        """Détecte le domaine dominant de la requête"""
        domain_scores = {}
        
        for domain, info in self.domain_experts.items():
            score = 0
            for topic in info['key_topics']:
                if topic.lower() in query.lower():
                    score += 2
                if topic.lower() in context.lower():
                    score += 1
            domain_scores[domain] = score
        
        return max(domain_scores, key=domain_scores.get) if domain_scores else 'general'
    
    def create_dynamic_prompt(self, query, context, conversation_history, domain):
        """Crée un prompt dynamique et contextuel"""
        expert_info = self.domain_experts.get(domain, self.domain_experts['general'])
        
        prompt_template = """
# IDENTITÉ PROFESSIONNELLE
Tu es {persona}. Tu réponds exclusivement en français.

# STYLE DE RÉPONSE ATTENDU
{style}

# CONTEXTE DOCUMENTAIRE (Sources spécialisées)
{context}

# HISTORIQUE DE LA CONVERSATION
{history}

# QUESTION ACTUELLE
{query}

# INSTRUCTIONS DE RÉPONSE
1. Structure avec des sections claires (Analyse, Recommandations, Considérations)
2. Utilise une terminologie technique exacte
3. Inclus des exemples concrets quand c'est pertinent
4. Mentionne les implications pratiques
5. Sois précis et évite les généralités
6. Si le contexte est insuffisant, indique-le clairement

# FORMAT DE SORTIE
**Analyse Technique** : [Analyse détaillée basée sur le contexte]
**Recommandations Opérationnelles** : [Conseils pratiques d'implémentation]  
**Aspects Réglementaires** : [Considérations conformité le cas échéant]
**Risques & Limites** : [Points de vigilance importants]
"""
        return prompt_template.format(
            persona=expert_info['persona'],
            style=expert_info['style'],
            context=context[:6000],  # Limiter la taille
            history=conversation_history[-1000:],  # Historique récent
            query=query
        )