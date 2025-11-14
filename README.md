# 🧠 ActuarialMind — Intelligent RAG Platform for Financial & Actuarial Analysis

---

## 📖 Overview
**ActuarialMind** is an **AI-powered platform for actuarial and financial analysis**, designed to provide **fast, accurate, and contextual insights** from actuarial and financial documents.

The system is built on a **RAG (Retrieval-Augmented Generation)** architecture that combines **advanced semantic search**, **vector embeddings**, and **context-aware answer generation**.

---

## 🧩 Project Objectives
- 💬 Build an intelligent **question–answer engine** for financial and actuarial documents.  
- 🔍 Implement **hybrid search** (vector + keyword) using **FAISS**, **Sentence-BERT**, and **Scikit-learn**.  
- 🤖 Integrate an **expert chatbot** powered by **Ollama** and **Flask**, capable of generating contextualized responses.  
- 🗂️ Manage users, histories, and documents using **MongoDB**.  
- 💻 Provide a **modern and user-friendly interface** for seamless interaction.  

---

## 🏗️ System Architecture

### 🔹 1. Data Ingestion & Parsing
- Upload of financial/actuarial reports (PDF, DOCX, text).  
- Automatic extraction and cleaning of text (Regex, custom preprocessing).  
- Chunking and embedding generation using **Sentence-BERT** or **Ollama embeddings**.

### 🔹 2. Vector Indexing & Retrieval
- Storage of embeddings in **FAISS** for high-speed similarity search.  
- Hybrid retrieval combining:
  - **Vector search**
  - **BM25 keyword search**  
- Re-ranking to select the most relevant context.

### 🔹 3. RAG Answer Generation
- Context assembly and prompt creation.  
- Response generation using **Ollama local LLMs**.  
- Quality evaluation + human-in-the-loop correction pipeline.

### 🔹 4. Backend & Database
- REST API built with **Flask**.  
- User, document and history management using **MongoDB**.  

### 🔹 5. Frontend
- Clean and modern UI (HTML/CSS/JS or Streamlit).  
- Document upload, chat interface, history viewer, answer feedback loop.

---

## 🛠️ Technologies Used

| Category | Tools & Technologies |
|----------|----------------------|
| Backend | Flask, Python |
| LLM / RAG | Ollama, Sentence-BERT, FAISS, Scikit-learn |
| NLP Processing | SpaCy, Transformers |
| Data Storage | MongoDB |
| Frontend | HTML/CSS/JS or Streamlit |
| Version Control | Git, GitHub |

---

## 📊 Key Features
- ⚡ Fast semantic search over actuarial & financial reports  
- 🤝 Human-in-the-Loop improvement workflow  
- 📚 Automatic summarization of large documents  
- 🧮 Actuarial-specific question answering  
- 🔐 Multi-user management with document history  

---

