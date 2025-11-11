# backend/chat_api_rag.py
from flask import Flask, request, jsonify
import ollama
import time
import logging
from datetime import datetime
from knowledge_base import FinanceActuarialKnowledgeBase
from pymongo import MongoClient

# --- Import des nouveaux modules améliorés ---
try:
    from advanced_embeddings import FinancialEmbedder
    from hybrid_search import AdvancedHybridSearch
    from advanced_prompts import AdvancedPromptEngine
    from evaluation_system import RAGEvaluator
    RAG_ENHANCED = True
    print("✅ Tous les modules RAG avancés chargés avec succès")
except ImportError as e:
    print(f"⚠️  Certains modules RAG avancés non disponibles: {e}")
    RAG_ENHANCED = False

# --- MongoDB Setup ---
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["finance_chatbot"]
conversations_collection = mongo_db["conversations"]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

class EnhancedRAGChatbot:
    def __init__(self):
        self.client = ollama.Client()
        self.knowledge_base = FinanceActuarialKnowledgeBase()
        self.available_models = []
        self.current_model = None
        self.ollama_available = False
        
        # Nouveaux composants RAG avancés
        self.rag_enhanced = RAG_ENHANCED
        if self.rag_enhanced:
            try:
                self.embedder = FinancialEmbedder()
                self.search_engine = AdvancedHybridSearch(self.knowledge_base)
                self.prompt_engine = AdvancedPromptEngine()
                self.evaluator = RAGEvaluator()
                print("🔧 Tous les composants RAG avancés initialisés")
            except Exception as e:
                print(f"❌ Erreur initialisation composants RAG: {e}")
                self.rag_enhanced = False
        
        self.initialize_ollama()
        self.conversation_memory = {}  # Mémoire conversationnelle simple
    
    def initialize_ollama(self):
        """Initialise Ollama avec la base de connaissances - VERSION CORRIGÉE"""
        try:
            logger.info("🚀 Initialisation du chatbot RAG amélioré...")
            
            # CORRECTION: Récupérer les modèles disponibles avec gestion d'erreur
            try:
                models_response = self.client.list()
                logger.info(f"📡 Réponse brute d'Ollama: {models_response}")
                
                # CORRECTION: Gérer les différentes structures de réponse
                if isinstance(models_response, dict) and 'models' in models_response:
                    self.available_models = [model['name'] for model in models_response['models']]
                elif isinstance(models_response, list):
                    self.available_models = [model['name'] for model in models_response if 'name' in model]
                else:
                    # Fallback: essayer une autre méthode
                    self.available_models = self._get_models_fallback()
                    
            except Exception as e:
                logger.error(f"❌ Erreur récupération modèles: {e}")
                self.available_models = self._get_models_fallback()
            
            if not self.available_models:
                logger.error("❌ Aucun modèle Ollama trouvé")
                logger.info("💡 Vérifiez qu'Ollama est démarré: ollama serve")
                logger.info("💡 Téléchargez un modèle: ollama pull llama3.2")
                return
            
            logger.info(f"📋 Modèles disponibles: {self.available_models}")
            
            # Sélectionner le meilleur modèle
            self.current_model = self.choose_best_model()
            self.ollama_available = True
            
            # Test de connexion
            test_result = self.test_connection()
            
            logger.info("✅ Chatbot RAG amélioré initialisé")
            logger.info(f"📊 Modèle sélectionné: {self.current_model}")
            logger.info(f"📚 Base de connaissances: {len(self.knowledge_base.chunks)} chunks")
            logger.info(f"🎯 RAG Amélioré: {'ACTIVE' if self.rag_enhanced else 'BASIQUE'}")
            logger.info(f"🔗 Test de connexion: {'Réussi' if test_result else 'Échoué'}")
            
        except Exception as e:
            logger.error(f"❌ Erreur d'initialisation: {e}")
            import traceback
            logger.error(f"🔍 Détails: {traceback.format_exc()}")

def _get_models_fallback(self):
    """Méthode de fallback pour récupérer les modèles"""
    try:
        import requests
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'models' in data:
                return [model['name'] for model in data['models']]
        return []
    except Exception as e:
        logger.error(f"❌ Fallback échoué: {e}")
        return []
    def choose_best_model(self):
        """Choisit le meilleur modèle disponible"""
        preferred_models = ["llama3.2", "mistral", "llama2", "codellama"]
        
        for model_name in preferred_models:
            for available_model in self.available_models:
                if model_name in available_model.lower():
                    return available_model
        
        return self.available_models[0] if self.available_models else None
    
    def test_connection(self):
        """Teste la connexion à Ollama"""
        try:
            if not self.current_model:
                return False
                
            response = self.client.chat(
                model=self.current_model,
                messages=[{'role': 'user', 'content': 'Test de connexion - reponds OK'}]
            )
            return response is not None
        except Exception as e:
            logger.error(f"❌ Test de connexion echoue: {e}")
            return False

    def get_conversation_history(self, conversation_id, max_turns=3):
        """Récupère l'historique de conversation"""
        if conversation_id not in self.conversation_memory:
            return ""
        
        history = self.conversation_memory[conversation_id][-max_turns:]
        context = "\n## Historique récent de la conversation:\n"
        
        for turn in history:
            context += f"**Utilisateur**: {turn['user']}\n"
            context += f"**Assistant**: {turn['assistant'][:200]}...\n\n"
        
        return context

    def add_to_conversation_history(self, conversation_id, user_message, ai_response):
        """Ajoute une interaction à l'historique"""
        if conversation_id not in self.conversation_memory:
            self.conversation_memory[conversation_id] = []
        
        self.conversation_memory[conversation_id].append({
            'user': user_message,
            'assistant': ai_response,
            'timestamp': datetime.now()
        })
        
        # Garder seulement les 10 dernières interactions
        if len(self.conversation_memory[conversation_id]) > 10:
            self.conversation_memory[conversation_id] = self.conversation_memory[conversation_id][-10:]

    def enhanced_search(self, query, top_k=5):
        """Recherche améliorée avec le système hybride si disponible"""
        if self.rag_enhanced:
            try:
                logger.info("🔍 Utilisation de la recherche hybride avancée")
                results = self.search_engine.hybrid_search(query, top_k=top_k)
                return results
            except Exception as e:
                logger.error(f"❌ Recherche hybride echouee, fallback basique: {e}")
        
        # Fallback à la recherche basique
        logger.info("🔍 Utilisation de la recherche basique")
        return self.knowledge_base.search_similar_chunks(query, top_k=top_k)

    def build_enhanced_context(self, search_results):
        """Construit un contexte enrichi à partir des résultats de recherche"""
        if not search_results:
            return "Aucun contexte spécifique disponible dans la base de connaissances."
        
        context_parts = ["## Contexte documentaire (sources spécialisées):"]
        
        for i, result in enumerate(search_results[:3]):  # Top 3 résultats
            source = result.get('metadata', {}).get('source', 'Document technique')
            content = result['chunk'][:800] + "..." if len(result['chunk']) > 800 else result['chunk']
            
            context_parts.append(f"**Source {i+1}** ({source}):\n{content}")
        
        return "\n\n".join(context_parts)

    def create_enhanced_system_prompt(self, context, query, conversation_history=""):
        """Crée un prompt système enrichi avec les nouveaux composants"""
        if self.rag_enhanced:
            try:
                # Détection du domaine avec le nouveau moteur
                domain = self.prompt_engine.detect_domain(query, context)
                return self.prompt_engine.create_dynamic_prompt(query, context, conversation_history, domain)
            except Exception as e:
                logger.error(f"❌ Prompt engine echoue, fallback basique: {e}")
        
        # Fallback au prompt basique
        base_prompt = """Tu es un expert senior en finance et actuariat avec accès à une base de connaissances spécialisée.

DOMAINES D'EXPERTISE:
- Actuariat et assurances (vie, dommages, reassurance)
- Risk Management et regulation Bale III/IV
- Finance quantitative et produits derives
- IFRS 17 et normes comptables
- Modelisation financiere et ALM

INSTRUCTIONS IMPORTANTES:
1. Base tes reponses sur le contexte fourni provenant de documents specialises
2. Sois precis et technique dans tes explications
3. Structure tes reponses de maniere claire
4. Mentionne les concepts specifiques quand c'est pertinent
5. Si le contexte ne couvre pas completement la question, utilise tes connaissances generales
6. Reponds toujours en francais

CONTEXTE DOCUMENTAIRE:
{context}

HISTORIQUE CONVERSATIONNEL:
{history}

REPONDS EN FRANCAIS de maniere technique, precise et structuree."""

        return base_prompt.format(context=context, history=conversation_history)

    def generate_rag_response(self, user_message, conversation_id=None):
        """Génère une réponse en utilisant RAG amélioré"""
        try:
            if not self.ollama_available:
                return self.get_fallback_response(user_message), {}
            
            logger.info(f"🎯 Generation reponse RAG pour: {user_message}")
            
            # Récupérer l'historique de conversation
            conversation_history = ""
            if conversation_id:
                conversation_history = self.get_conversation_history(conversation_id)
            
            # 1. Recherche améliorée dans la base de connaissances
            start_search = time.time()
            search_results = self.enhanced_search(user_message, top_k=5)
            search_time = time.time() - start_search
            
            # 2. Construction du contexte
            context = self.build_enhanced_context(search_results)
            
            # 3. Construction du prompt amélioré
            system_prompt = self.create_enhanced_system_prompt(context, user_message, conversation_history)
            
            # 4. Génération de la réponse
            start_generation = time.time()
            
            response = self.client.chat(
                model=self.current_model,
                messages=[
                    {
                        'role': 'system',
                        'content': system_prompt
                    },
                    {
                        'role': 'user', 
                        'content': user_message
                    }
                ],
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'num_predict': 2000
                }
            )
            
            generation_time = time.time() - start_generation
            total_time = search_time + generation_time
            
            if response and 'message' in response and 'content' in response['message']:
                ai_response = response['message']['content'].strip()
                
                # 5. Évaluation de la réponse (si disponible)
                if self.rag_enhanced:
                    try:
                        self.evaluator.log_interaction(user_message, ai_response, context)
                    except Exception as e:
                        logger.error(f"⚠️  Erreur evaluation: {e}")
                
                # 6. Mise à jour de l'historique
                if conversation_id:
                    self.add_to_conversation_history(conversation_id, user_message, ai_response)
                
                logger.info(f"✅ Reponse RAG generee en {total_time:.2f}s (recherche: {search_time:.2f}s)")
                logger.info(f"📊 Longueur: {len(ai_response)} caracteres")
                
                metadata = {
                    'search_time': round(search_time, 2),
                    'generation_time': round(generation_time, 2),
                    'total_time': round(total_time, 2),
                    'search_results_count': len(search_results),
                    'rag_enhanced': self.rag_enhanced,
                    'context_length': len(context)
                }
                
                return ai_response, metadata
            else:
                logger.error("❌ Reponse Ollama invalide")
                return self.get_fallback_response(user_message), {}
                
        except Exception as e:
            logger.error(f"❌ Erreur generation RAG: {e}")
            return self.get_fallback_response(user_message), {}
    
    def get_fallback_response(self, user_message):
        """Réponse de fallback si RAG échoue"""
        fallback_responses = {
            'actuariat': """
**L'ACTUARIAT - Science des Risques et Assurances**

L'actuariat est une discipline qui applique des méthodes mathématiques et statistiques pour évaluer les risques financiers dans les domaines de l'assurance, de la finance et de la prévoyance sociale.

**Domaines Principaux:**
• **Assurance Vie** : Calcul des primes, réserves mathématiques, tables de mortalité
• **Assurance Dommages** : Tarification IARD, provisionnement des sinistres
• **Régimes de Retraite** : Gestion des pensions, financement
• **Risk Management** : Solvabilité II, capital économique, stress testing

*Réponse basée sur notre base de connaissances spécialisée*
""",
            'bâle': """
**RÉGULATION BÂLE III/IV**

**Bâle III** renforce les exigences de capital après la crise de 2008:
• Ratio CET1 minimum : 4.5% + 2.5% buffer = 7%
• Ratio de levier : 3% minimum
• Liquidité : LCR (100%) et NSFR (100%)

**Bâle IV** (finalisation de Bâle III):
• Sortie des approches standardisées
• Restrictions sur les modèles internes
• Meilleure comparabilité internationale

*Réponse basée sur notre base de connaissances réglementaire*
""",
            'ifrs': """
**IFRS 17 - Contrats d'Assurance**

Nouvelle norme comptable internationale pour les contrats d'assurance:

**Principales Caractéristiques:**
• Modèle de mesure unique (VFA, PAA, BBA)
• Reconnaissance des profits sur la durée du contrat
• Meilleure comparabilité internationale
• Transparence accrue sur la performance

*Réponse basée sur notre base de connaissances comptables*
"""
        }
        
        user_lower = user_message.lower()
        for keyword, response in fallback_responses.items():
            if keyword in user_lower:
                return response
        
        return f"""
**🤖 Assistant Expert Finance & Actuariat**

Votre question : "{user_message}"

Je consulte actuellement notre base de connaissances spécialisée contenant des documents techniques en finance et actuariat.

**Domaines Couverts:**
- Risk Management & Régulation Bâle
- Actuariat & Assurances (vie, non-vie, santé)
- Finance Quantitative & Produits Dérivés
- Normes IFRS 17 & Comptabilité
- Modélisation Financière & ALM

Veuillez patienter pendant que je recherche les informations les plus pertinentes dans nos documents techniques.
"""

# Initialisation globale
chatbot = EnhancedRAGChatbot()

@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "service": "Chatbot Finance & Actuariat - Enhanced RAG System",
        "ollama_available": chatbot.ollama_available,
        "current_model": chatbot.current_model,
        "knowledge_base_chunks": len(chatbot.knowledge_base.chunks),
        "available_models": chatbot.available_models,
        "rag_enhanced": chatbot.rag_enhanced,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    # Rapport de performance si disponible
    performance_report = {}
    if chatbot.rag_enhanced:
        try:
            performance_report = chatbot.evaluator.get_performance_report()
        except:
            pass
    
    return jsonify({
        "status": "healthy" if chatbot.ollama_available else "unhealthy",
        "ollama_available": chatbot.ollama_available,
        "current_model": chatbot.current_model,
        "knowledge_base_chunks": len(chatbot.knowledge_base.chunks),
        "available_models": chatbot.available_models,
        "rag_enhanced": chatbot.rag_enhanced,
        "performance_metrics": performance_report,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat_endpoint():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"})
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id', f"conv_{int(time.time())}")

        if not user_message:
            return jsonify({"error": "Message vide"}), 400

        logger.info(f"💬 Question RAG: {user_message}")

        start_time = time.time()
        
        # Utiliser le système RAG amélioré
        ai_response, metadata = chatbot.generate_rag_response(user_message, conversation_id)
        
        processing_time = time.time() - start_time

        # Sauvegarde dans MongoDB
        conversations_collection.insert_one({
            "conversation_id": conversation_id,
            "user_message": user_message,
            "ai_response": ai_response,
            "ai_used": True,
            "rag_used": True,
            "rag_enhanced": chatbot.rag_enhanced,
            "model": chatbot.current_model,
            "knowledge_base_used": len(chatbot.knowledge_base.chunks) > 0,
            "processing_time": round(processing_time, 2),
            "search_time": metadata.get('search_time', 0),
            "generation_time": metadata.get('generation_time', 0),
            "search_results_count": metadata.get('search_results_count', 0),
            "timestamp": datetime.now()
        })

        logger.info("✅ Réponse RAG envoyée et sauvegardée")
        
        response_data = {
            "response": ai_response,
            "status": "success",
            "ai_used": True,
            "rag_used": True,
            "rag_enhanced": chatbot.rag_enhanced,
            "processing_time": round(processing_time, 2),
            "search_time": metadata.get('search_time', 0),
            "generation_time": metadata.get('generation_time', 0),
            "search_results_count": metadata.get('search_results_count', 0),
            "model": chatbot.current_model,
            "knowledge_base_used": len(chatbot.knowledge_base.chunks) > 0,
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"❌ Erreur globale: {e}")
        return jsonify({
            "error": "Erreur interne du serveur",
            "details": str(e)
        }), 500

@app.route('/api/search', methods=['POST'])
def search_knowledge_base():
    """Endpoint pour rechercher directement dans la base de connaissances"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({"error": "Requête vide"}), 400
        
        # Utiliser la recherche améliorée
        results = chatbot.enhanced_search(query, top_k=5)
        
        return jsonify({
            "query": query,
            "results_found": len(results),
            "rag_enhanced": chatbot.rag_enhanced,
            "results": [
                {
                    "content": result['chunk'][:500] + "..." if len(result['chunk']) > 500 else result['chunk'],
                    "source": result.get('metadata', {}).get('source', 'Document'),
                    "similarity_score": round(result.get('similarity_score', result.get('combined_score', 0)), 4),
                    "search_type": result.get('search_type', 'hybrid')
                }
                for result in results
            ],
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/system-status', methods=['GET'])
def system_status():
    """Statut détaillé du système"""
    performance_report = {}
    improvements = []
    
    if chatbot.rag_enhanced:
        try:
            performance_report = chatbot.evaluator.get_performance_report()
            improvements = chatbot.evaluator.identify_improvement_areas()
        except Exception as e:
            logger.error(f"Erreur récupération statut: {e}")
    
    return jsonify({
        "ollama_available": chatbot.ollama_available,
        "current_model": chatbot.current_model,
        "knowledge_base_chunks": len(chatbot.knowledge_base.chunks),
        "rag_components_operational": chatbot.rag_enhanced,
        "performance_metrics": performance_report,
        "improvement_suggestions": improvements,
        "conversations_in_memory": len(chatbot.conversation_memory),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/kb-stats', methods=['GET'])
def knowledge_base_stats():
    """Statistiques de la base de connaissances"""
    return jsonify({
        "total_chunks": len(chatbot.knowledge_base.chunks),
        "index_created": chatbot.knowledge_base.index is not None,
        "rag_enhanced": chatbot.rag_enhanced,
        "sources": list(set([meta.get('source', 'Unknown') for meta in chatbot.knowledge_base.metadata])),
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🤖 CHATBOT FINANCE & ACTUARIAT - SYSTÈME RAG AMÉLIORÉ")
    print("=" * 70)
    print(f"🌐 URL: http://localhost:5001")
    print(f"🔗 Ollama: {'CONNECTÉ' if chatbot.ollama_available else 'HORS LIGNE'}")
    print(f"🧠 Modèle: {chatbot.current_model or 'Aucun'}")
    print(f"📚 Base de connaissances: {len(chatbot.knowledge_base.chunks)} chunks")
    print(f"🎯 RAG Amélioré: {'ACTIVÉ' if chatbot.rag_enhanced else 'DÉSACTIVÉ'}")
    print(f"💊 Health: http://localhost:5001/api/health")
    print(f"🔍 Recherche: POST http://localhost:5001/api/search")
    print(f"📊 Statut: GET http://localhost:5001/api/system-status")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)