// src/components/Auth/Signup.js
import React, { useState } from 'react';
import './Auth.css';

const Signup = ({ onSwitchToLogin, onSignup }) => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    company: '',
    password: '',
    confirmPassword: '',
    profession: '',
    acceptTerms: false
  });

  const professions = [
    'Actuaire',
    'Risk Manager',
    'Analyste Financier',
    'Compliance Officer',
    'Directeur Financier',
    'Consultant',
    'Autre'
  ];

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      alert('Les mots de passe ne correspondent pas');
      return;
    }
    onSignup(formData);
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2>Inscription</h2>
          <p>Rejoignez notre communauté d'experts</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="firstName">Prénom</label>
              <input
                type="text"
                id="firstName"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                placeholder="Votre prénom"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="lastName">Nom</label>
              <input
                type="text"
                id="lastName"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                placeholder="Votre nom"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="email">Email professionnel</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="votre@entreprise.com"
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="company">Entreprise</label>
              <input
                type="text"
                id="company"
                name="company"
                value={formData.company}
                onChange={handleChange}
                placeholder="Nom de votre entreprise"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="profession">Profession</label>
              <select
                id="profession"
                name="profession"
                value={formData.profession}
                onChange={handleChange}
                required
              >
                <option value="">Sélectionnez...</option>
                {professions.map(prof => (
                  <option key={prof} value={prof}>{prof}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password">Mot de passe</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Minimum 8 caractères"
              minLength="8"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirmer le mot de passe</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="Retapez votre mot de passe"
              required
            />
          </div>

          <div className="form-options">
            <label className="checkbox-label">
              <input 
                type="checkbox" 
                name="acceptTerms"
                checked={formData.acceptTerms}
                onChange={handleChange}
                required
              />
              <span>
                J'accepte les <a href="#">conditions d'utilisation</a> et la <a href="#">politique de confidentialité</a>
              </span>
            </label>
          </div>

          <button type="submit" className="btn btn-primary btn-full">
            Créer mon compte
          </button>
        </form>

        <div className="auth-divider">
          <span>Ou</span>
        </div>

        <div className="social-auth">
          <button className="btn btn-outline btn-full">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              {/* Icône Google identique à Login */}
            </svg>
            S'inscrire avec Google
          </button>
        </div>

        <div className="auth-switch">
          <p>
            Déjà inscrit ? 
            <button onClick={onSwitchToLogin} className="switch-link">
              Se connecter
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signup;