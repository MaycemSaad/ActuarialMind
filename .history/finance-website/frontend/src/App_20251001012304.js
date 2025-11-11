// src/App.js
import React, { useState, useEffect } from 'react';
import './App.css';

// Composants
import Header from './components/Header/Header';
import Chatbot from './components/Chatbot/Chatbot';
import ServiceCard from './components/ServiceCard/ServiceCard';
import DocumentCard from './components/DocumentCard/DocumentCard';
import StatsCounter from './components/StatsCounter/StatsCounter';

function App() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const services = [
    {
      icon: '🎯',
      title: 'Risk Management',
      description: 'Analyse et modélisation des risques financiers avec IA avancée',
      features: ['Bâle III/IV Compliance', 'Value at Risk (VaR)', 'Stress Testing', 'Capital Allocation'],
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    },
    {
      icon: '📋',
      title: 'Conformité Réglementaire',
      description: 'Surveillance complète des régulations financières internationales',
      features: ['IFRS 17 Implementation', 'Solvability II Reporting', 'Regulatory Monitoring', 'Audit Automation'],
      gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
    },
    {
      icon: '📊',
      title: 'Analyse Actuarielle',
      description: 'Modélisation actuarielle précise et calcul de réserves optimisés',
      features: ['Pricing & Reserving', 'Mortality Modeling', 'Pension Valuation', 'ALM Strategies'],
      gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
    },
    {
      icon: '🤖',
      title: 'Chatbot Expert',
      description: 'Assistant IA spécialisé disponible 24/7 pour vos questions techniques',
      features: ['24/7 Availability', 'Technical Expertise', 'Multi-language', 'RAG Powered'],
      gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
    }
  ];

  const documents = [
    {
      icon: '📄',
      title: 'Bâle III/IV Framework',
      description: 'Analyse exhaustive des exigences de capital renforcées et des nouveaux ratios de liquidité',
      meta: { type: 'AI Generated', pages: '45 pages', category: 'Régulation' },
      badge: 'Nouveau'
    },
    {
      icon: '📊',
      title: 'IFRS 17 Implementation',
      description: 'Guide pratique de mise en œuvre avec études de cas et modèles financiers',
      meta: { type: 'AI Enhanced', pages: '32 pages', category: 'Comptabilité' },
      badge: 'Populaire'
    },
    {
      icon: '🎯',
      title: 'Risk Management Strategies',
      description: 'Stratégies avancées de gestion des risques financiers et opérationnels',
      meta: { type: 'Expert Analysis', pages: '28 pages', category: 'Risk Management' }
    }
  ];

  const stats = [
    { number: '250+', label: 'Documents Analysés' },
    { number: '15+', label: 'Domaines Experts' },
    { number: '99.7%', label: 'Précision IA' },
    { number: '24/7', label: 'Disponibilité' }
  ];

  return (
    <div className="App">
      <Header />
      
      <main className="main-content">
        {/* Section Hero avec animations */}
        <section className={`hero ${isVisible ? 'visible' : ''}`}>
          <div className="hero-background">
            <div className="hero-gradient"></div>
          </div>
          <div className="container">
            <div className="hero-content">
              <div className="hero-badge">
                <span>🚀 Plateforme IA Avancée</span>
              </div>
              <h1 className="hero-title">
                Intelligence Artificielle pour la
                <span className="hero-highlight"> Finance & Actuariat</span>
              </h1>
              <p className="hero-subtitle">
                Solutions IA de pointe pour l'analyse de risques, la conformité réglementaire 
                et l'optimisation actuariale. Transformez vos données en avantage compétitif.
              </p>
              
              <div className="hero-stats">
                {stats.map((stat, index) => (
                  <StatsCounter 
                    key={index}
                    number={stat.number}
                    label={stat.label}
                    delay={index * 200}
                  />
                ))}
              </div>

              <div className="hero-buttons">
                <button className="btn btn-primary">
                  <span>Découvrir nos Services</span>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </button>
                <button className="btn btn-secondary">
                  <span>Consulter les Documents</span>
                </button>
              </div>
            </div>
            
            <div className="hero-visual">
              <div className="floating-cards">
                <div className="floating-card card-1">
                  <div className="card-icon">📈</div>
                  <span>Risk Analysis</span>
                </div>
                <div className="floating-card card-2">
                  <div className="card-icon">🔒</div>
                  <span>Compliance</span>
                </div>
                <div className="floating-card card-3">
                  <div className="card-icon">💰</div>
                  <span>Valuation</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Section Services avec hover effects */}
        <section className="services-section">
          <div className="container">
            <div className="section-header">
              <h2>Nos Domaines d'Expertise</h2>
              <p className="section-subtitle">
                Des solutions IA spécialisées pour chaque aspect de la finance et de l'actuariat
              </p>
            </div>
            
            <div className="services-grid">
              {services.map((service, index) => (
                <ServiceCard 
                  key={index}
                  {...service}
                  delay={index * 100}
                />
              ))}
            </div>
          </div>
        </section>

        {/* Section Documents avec carousel effect */}
        <section className="documents-section">
          <div className="container">
            <div className="section-header">
              <h2>Base de Connaissances Technique</h2>
              <p className="section-subtitle">
                Documents spécialisés analysés et enrichis par notre intelligence artificielle
              </p>
            </div>
            
            <div className="documents-grid">
              {documents.map((doc, index) => (
                <DocumentCard 
                  key={index}
                  {...doc}
                  delay={index * 150}
                />
              ))}
            </div>
            
            <div className="section-actions">
              <button className="btn btn-outline">
                <span>Explorer la Base Complète</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </button>
            </div>
          </div>
        </section>

        {/* Section CTA avec gradient */}
        <section className="cta-section">
          <div className="cta-background">
            <div className="cta-gradient"></div>
          </div>
          <div className="container">
            <div className="cta-content">
              <h2>Prêt à révolutionner votre approche financière ?</h2>
              <p>
                Rejoignez les leaders qui utilisent déjà notre plateforme IA 
                pour optimiser leurs processus et prendre des décisions éclairées.
              </p>
              
              <div className="cta-features">
                <div className="feature-item">
                  <div className="feature-icon">⚡</div>
                  <span>Déploiement en 24h</span>
                </div>
                <div className="feature-item">
                  <div className="feature-icon">🛡️</div>
                  <span>Certifié RGPD</span>
                </div>
                <div className="feature-item">
                  <div className="feature-icon">🎯</div>
                  <span>Sur-mesure</span>
                </div>
              </div>
              
              <div className="cta-buttons">
                <button className="btn btn-primary btn-large">
                  <span>Démarrer une Démonstration</span>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" fill="currentColor"/>
                    <path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" strokeWidth="2"/>
                  </svg>
                </button>
                <button className="btn btn-secondary btn-large">
                  <span>Tester le Chatbot Expert</span>
                </button>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Chatbot intégré */}
      <Chatbot />
      
      {/* Footer moderne */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-main">
              <div className="footer-brand">
                <h3>FinanceActuarial AI</h3>
                <p>L'intelligence artificielle au service de l'excellence financière et actuarielle</p>
                <div className="social-links">
                  <a href="#" aria-label="LinkedIn">💼</a>
                  <a href="#" aria-label="Twitter">🐦</a>
                  <a href="#" aria-label="GitHub">🔗</a>
                </div>
              </div>
              
              <div className="footer-links">
                <div className="link-group">
                  <h4>Solutions</h4>
                  <a href="#">Risk Management</a>
                  <a href="#">Compliance</a>
                  <a href="#">Actuarial Analysis</a>
                  <a href="#">Chatbot Expert</a>
                </div>
                
                <div className="link-group">
                  <h4>Ressources</h4>
                  <a href="#">Documentation</a>
                  <a href="#">Cas d'Usage</a>
                  <a href="#">Blog Technique</a>
                  <a href="#">API</a>
                </div>
                
                <div className="link-group">
                  <h4>Entreprise</h4>
                  <a href="#">À propos</a>
                  <a href="#">Carrières</a>
                  <a href="#">Contact</a>
                  <a href="#">Presse</a>
                </div>
                
                <div className="link-group">
                  <h4>Légal</h4>
                  <a href="#">Confidentialité</a>
                  <a href="#">Conditions</a>
                  <a href="#">Cookies</a>
                  <a href="#">Sécurité</a>
                </div>
              </div>
            </div>
            
            <div className="footer-bottom">
              <div className="footer-info">
                <p>&copy; 2024 Finance & Actuarial AI. Tous droits réservés.</p>
                <div className="footer-meta">
                  <span>🏢 Paris, France</span>
                  <span>📧 contact@finance-actuarial.ai</span>
                  <span>📞 +33 1 23 45 67 89</span>
                </div>
              </div>
              
              <div className="footer-badges">
                <div className="badge">ISO 27001</div>
                <div className="badge">RGPD Compliant</div>
                <div className="badge">SOC 2 Type II</div>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;