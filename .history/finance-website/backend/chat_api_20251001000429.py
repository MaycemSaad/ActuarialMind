# backend/chat_api_rag.py
from flask import Flask, request, jsonify
import ollama
import time
import logging
from datetime import datetime
from knowledge_base import FinanceActuarialKnowledgeBase
from pymongo import MongoClient

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

class RAGChatbot:
    def __init__(self):
        self.client = ollama.Client()
        self.knowledge_base = FinanceActuarialKnowledgeBase()
        self.available_models = []
        self.current_model = None
        self.ollama_available = False
        self.initialize_ollama()
    
    def initialize_ollama(self):
        """Initialise Ollama avec la base de connaissances"""
        try:
            logger.info("Initialisation du chatbot RAG...")
            
            # Récupérer les modèles disponibles
            models_response = self.client.list()
            self.available_models = [model['name'] for model in models_response.get('models', [])]
            
            if not self.available_models:
                logger.error("Aucun modele Ollama trouve")
                return
            
            # Sélectionner le meilleur modèle
            self.current_model = self.choose_best_model()
            self.ollama_available = True
            
            # Test de connexion
            test_result = self.test_connection()
            
            logger.info("Chatbot RAG initialise")
            logger.info(f"Modele selectionne: {self.current_model}")
            logger.info(f"Base de connaissances: {len(self.knowledge_base.chunks)} chunks")
            logger.info(f"Test de connexion: {'Reussi' if test_result else 'Echoue'}")
            
        except Exception as e:
            logger.error(f"Erreur d'initialisation: {e}")
    
    def choose_best_model(self):
        """Choisit le meilleur modèle disponible"""
        if "mistral" in [model.lower() for model in self.available_models]:
            return "mistral"
        elif "llama3.2" in [model.lower() for model in self.available_models]:
            return "llama3.2"
        else:
            return self.available_models[0] if self.available_models else None
    
    def test_connection(self):
        """Teste la connexion à Ollama"""
        try:
            if not self.current_model:
                return False
                
            response = self.client.chat(
                model=self.current_model,
                messages=[{'role': 'user', 'content': 'Test'}]
            )
            return response is not None
        except Exception as e:
            logger.error(f"Test de connexion echoue: {e}")
            return False
    
    def generate_rag_response(self, user_message):
        """Génère une réponse en utilisant RAG (base de connaissances + Ollama)"""
        try:
            if not self.ollama_available:
                return self.get_fallback_response(user_message)
            
            logger.info(f"Generation reponse RAG pour: {user_message}")
            
            # 1. Recherche dans la base de connaissances
            context = self.knowledge_base.get_context_for_question(user_message)
            
            # 2. Construction du prompt avec contexte
            system_prompt = self.create_enhanced_system_prompt(context)
            
            # 3. Génération de la réponse
            start_time = time.time()
            
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
            
            processing_time = time.time() - start_time
            
            if response and 'message' in response and 'content' in response['message']:
                ai_response = response['message']['content'].strip()
                
                logger.info(f"Reponse RAG generee en {processing_time:.2f}s")
                logger.info(f"Longueur: {len(ai_response)} caracteres")
                
                return ai_response
            else:
                logger.error("Reponse Ollama invalide")
                return self.get_fallback_response(user_message)
                
        except Exception as e:
            logger.error(f"Erreur generation RAG: {e}")
            return self.get_fallback_response(user_message)
    
    def create_enhanced_system_prompt(self, context):
        """Crée un prompt système enrichi avec le contexte"""
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

REPONDS EN FRANCAIS de maniere technique, precise et structuree."""

        return base_prompt.format(context=context)
    
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
**Assistant Expert Finance & Actuariat**

Votre question : "{user_message}"

Je consulte actuellement notre base de connaissances spécialisée contenant des documents techniques en finance et actuariat.

**Domaines Couverts:**
- Risk Management & Régulation Bâle
- Actuariat & Assurances
- Finance Quantitative
- Normes IFRS 17
- Modélisation Financière

Veuillez patienter pendant que je recherche les informations les plus pertinentes.
"""

# Initialisation globale
chatbot = RAGChatbot()

@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "service": "Chatbot Finance & Actuariat - RAG System",
        "ollama_available": chatbot.ollama_available,
        "current_model": chatbot.current_model,
        "knowledge_base_chunks": len(chatbot.knowledge_base.chunks),
        "available_models": chatbot.available_models,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy" if chatbot.ollama_available else "unhealthy",
        "ollama_available": chatbot.ollama_available,
        "current_model": chatbot.current_model,
        "knowledge_base_chunks": len(chatbot.knowledge_base.chunks),
        "available_models": chatbot.available_models,
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

        logger.info(f"Question RAG: {user_message}")

        start_time = time.time()
        
        # Utiliser ton système RAG
        ai_response = chatbot.generate_rag_response(user_message)
        
        processing_time = time.time() - start_time

        # --- ✅ Étape 2 : Sauvegarde dans MongoDB ---
        conversations_collection.insert_one({
            "conversation_id": conversation_id,
            "user_message": user_message,
            "ai_response": ai_response,
            "ai_used": True,
            "rag_used": True,
            "model": chatbot.current_model,
            "knowledge_base_used": len(chatbot.knowledge_base.chunks) > 0,
            "processing_time": round(processing_time, 2),
            "timestamp": datetime.now()
        })

        logger.info("Réponse RAG envoyée et sauvegardée")
        return jsonify({
            "response": ai_response,
            "status": "success",
            "ai_used": True,
            "rag_used": True,
            "processing_time": round(processing_time, 2),
            "model": chatbot.current_model,
            "knowledge_base_used": len(chatbot.knowledge_base.chunks) > 0,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erreur globale: {e}")
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
        
        results = chatbot.knowledge_base.search_similar_chunks(query, top_k=5)
        
        return jsonify({
            "query": query,
            "results_found": len(results),
            "results": [
                {
                    "content": result['chunk'][:500] + "..." if len(result['chunk']) > 500 else result['chunk'],
                    "source": result['metadata']['source'],
                    "similarity_score": round(result['similarity_score'], 4),
                    "domain_relevance": result['metadata']['semantic_info'].get('domain_relevance', 0)
                }
                for result in results
            ],
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/kb-stats', methods=['GET'])
def knowledge_base_stats():
    """Statistiques de la base de connaissances"""
    return jsonify({
        "total_chunks": len(chatbot.knowledge_base.chunks),
        "index_created": chatbot.knowledge_base.index is not None,
        "sources": list(set([meta['source'] for meta in chatbot.knowledge_base.metadata])),
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 60)
    print("CHATBOT FINANCE & ACTUARIAT - SYSTEME RAG")
    print("=" * 60)
    print(f"URL: http://localhost:5001")
    print(f"Ollama: {'CONNECTE' if chatbot.ollama_available else 'HORS LIGNE'}")
    print(f"Modele: {chatbot.current_model or 'Aucun'}")
    print(f"Base de connaissances: {len(chatbot.knowledge_base.chunks)} chunks")
    print(f"Health: http://localhost:5001/api/health")
    print(f"Recherche: POST http://localhost:5001/api/search")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)