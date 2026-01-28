import React, { useState } from 'react';
import './App.css';
import { api, GenerateRequest, ImproveRequest, SEORequest, TranslateRequest } from './services/api';
import { CATEGORIES, TONES, LANGUAGES, LENGTHS, IMPROVEMENT_FOCUS } from './constants';

type TabType = 'generate' | 'improve' | 'seo' | 'translate';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('generate');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');
  const [error, setError] = useState('');
  
  const [generateData, setGenerateData] = useState<GenerateRequest>({
    product_name: '',
    category: 'Autre',
    features: '',
    target_audience: '',
    tone: 'Professionnel',
    language: 'Français',
    length: 'Moyenne (100-200 mots)',
    num_variants: 1,
  });

  const [improveData, setImproveData] = useState<ImproveRequest>({
    original_description: '',
    improvement_focus: ['Clarté et lisibilité', 'Pouvoir de persuasion'],
    tone: 'Professionnel',
    language: 'Français',
  });

  const [seoData, setSeoData] = useState<SEORequest>({
    product_name: '',
    description: '',
    category: 'Autre',
    language: 'Français',
  });

  const [translateData, setTranslateData] = useState<TranslateRequest>({
    description: '',
    source_language: 'Français',
    target_language: 'English',
    adapt_culturally: true,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult('');

    let response;
    switch (activeTab) {
      case 'generate':
        response = await api.generateDescription(generateData);
        break;
      case 'improve':
        response = await api.improveDescription(improveData);
        break;
      case 'seo':
        response = await api.generateSEO(seoData);
        break;
      case 'translate':
        response = await api.translateDescription(translateData);
        break;
    }
    
    setLoading(false);
    
    if (response.success && response.data) {
      setResult(response.data);
    } else {
      setError(response.error || 'Une erreur est survenue');
    }
  };

  const wordCount = result ? result.split(/\s+/).length : 0;
  const charCount = result.length;

  const renderForm = () => {
    switch (activeTab) {
      case 'generate':
        return (
          <>
            <div className="form-group">
              <label htmlFor="product_name">Nom du produit *</label>
              <input
                type="text"
                id="product_name"
                value={generateData.product_name}
                onChange={(e) => setGenerateData({...generateData, product_name: e.target.value})}
                placeholder="Ex: Casque Bluetooth Premium"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="category">Catégorie</label>
              <select
                id="category"
                value={generateData.category}
                onChange={(e) => setGenerateData({...generateData, category: e.target.value})}
              >
                {CATEGORIES.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="features">Caractéristiques clés</label>
              <textarea
                id="features"
                value={generateData.features}
                onChange={(e) => setGenerateData({...generateData, features: e.target.value})}
                placeholder="Ex: Sans fil, autonomie 30h, réduction de bruit active..."
                rows={3}
              />
            </div>

            <div className="form-group">
              <label htmlFor="target_audience">Public cible</label>
              <input
                type="text"
                id="target_audience"
                value={generateData.target_audience}
                onChange={(e) => setGenerateData({...generateData, target_audience: e.target.value})}
                placeholder="Ex: Professionnels, gamers, audiophiles..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="tone">Ton</label>
                <select
                  id="tone"
                  value={generateData.tone}
                  onChange={(e) => setGenerateData({...generateData, tone: e.target.value})}
                >
                  {TONES.map(tone => (
                    <option key={tone} value={tone}>{tone}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="language">Langue</label>
                <select
                  id="language"
                  value={generateData.language}
                  onChange={(e) => setGenerateData({...generateData, language: e.target.value})}
                >
                  {LANGUAGES.map(lang => (
                    <option key={lang} value={lang}>{lang}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="length">Longueur</label>
              <select
                id="length"
                value={generateData.length}
                onChange={(e) => setGenerateData({...generateData, length: e.target.value})}
              >
                {LENGTHS.map(len => (
                  <option key={len} value={len}>{len}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="num_variants">
                Nombre de variantes: {generateData.num_variants}
              </label>
              <input
                type="range"
                id="num_variants"
                min="1"
                max="3"
                value={generateData.num_variants}
                onChange={(e) => setGenerateData({...generateData, num_variants: parseInt(e.target.value)})}
              />
            </div>
          </>
        );

      case 'improve':
        return (
          <>
            <div className="form-group">
              <label htmlFor="original_description">Description originale *</label>
              <textarea
                id="original_description"
                value={improveData.original_description}
                onChange={(e) => setImproveData({...improveData, original_description: e.target.value})}
                placeholder="Collez votre description actuelle ici..."
                rows={6}
                required
              />
            </div>

            <div className="form-group">
              <label>Axes d'amélioration</label>
              {IMPROVEMENT_FOCUS.map((focus) => (
                <div key={focus} className="checkbox-item">
                  <input
                    type="checkbox"
                    id={`focus-${focus}`}
                    checked={improveData.improvement_focus.includes(focus)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setImproveData({...improveData, improvement_focus: [...improveData.improvement_focus, focus]});
                      } else {
                        setImproveData({...improveData, improvement_focus: improveData.improvement_focus.filter(f => f !== focus)});
                      }
                    }}
                  />
                  <label htmlFor={`focus-${focus}`}>{focus}</label>
                </div>
              ))}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="tone">Ton souhaité</label>
                <select
                  id="tone"
                  value={improveData.tone}
                  onChange={(e) => setImproveData({...improveData, tone: e.target.value})}
                >
                  {TONES.map(tone => (
                    <option key={tone} value={tone}>{tone}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="language">Langue</label>
                <select
                  id="language"
                  value={improveData.language}
                  onChange={(e) => setImproveData({...improveData, language: e.target.value})}
                >
                  {LANGUAGES.map(lang => (
                    <option key={lang} value={lang}>{lang}</option>
                  ))}
                </select>
              </div>
            </div>
          </>
        );

      case 'seo':
        return (
          <>
            <div className="form-group">
              <label htmlFor="seo_product_name">Nom du produit *</label>
              <input
                type="text"
                id="seo_product_name"
                value={seoData.product_name}
                onChange={(e) => setSeoData({...seoData, product_name: e.target.value})}
                placeholder="Ex: Montre connectée sportive"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="seo_category">Catégorie</label>
              <select
                id="seo_category"
                value={seoData.category}
                onChange={(e) => setSeoData({...seoData, category: e.target.value})}
              >
                {CATEGORIES.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="seo_description">Description (optionnel)</label>
              <textarea
                id="seo_description"
                value={seoData.description}
                onChange={(e) => setSeoData({...seoData, description: e.target.value})}
                placeholder="Entrez une description existante pour une analyse plus précise..."
                rows={4}
              />
            </div>

            <div className="form-group">
              <label htmlFor="seo_language">Langue cible</label>
              <select
                id="seo_language"
                value={seoData.language}
                onChange={(e) => setSeoData({...seoData, language: e.target.value})}
              >
                {LANGUAGES.map(lang => (
                  <option key={lang} value={lang}>{lang}</option>
                ))}
              </select>
            </div>
          </>
        );

      case 'translate':
        return (
          <>
            <div className="form-group">
              <label htmlFor="translate_description">Description à traduire *</label>
              <textarea
                id="translate_description"
                value={translateData.description}
                onChange={(e) => setTranslateData({...translateData, description: e.target.value})}
                placeholder="Entrez la description de produit à traduire..."
                rows={6}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="source_language">Langue source</label>
                <select
                  id="source_language"
                  value={translateData.source_language}
                  onChange={(e) => setTranslateData({...translateData, source_language: e.target.value})}
                >
                  {LANGUAGES.map(lang => (
                    <option key={lang} value={lang}>{lang}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="target_language">Langue cible</label>
                <select
                  id="target_language"
                  value={translateData.target_language}
                  onChange={(e) => setTranslateData({...translateData, target_language: e.target.value})}
                >
                  {LANGUAGES.map(lang => (
                    <option key={lang} value={lang}>{lang}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
              <div className="checkbox-item">
                <input
                  type="checkbox"
                  id="adapt_culturally"
                  checked={translateData.adapt_culturally}
                  onChange={(e) => setTranslateData({...translateData, adapt_culturally: e.target.checked})}
                />
                <label htmlFor="adapt_culturally">Adaptation culturelle</label>
              </div>
              <p className="field-info">Adapter les références culturelles et expressions pour le marché cible</p>
            </div>
          </>
        );
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Générateur de Descriptions pour Produits E-commerce</h1>
        <p>Créez des descriptions de produits professionnelles et optimisées SEO avec l'IA.</p>
        <p className="powered-by">Propulsé par Qwen2.5-7B via Hugging Face Inference API</p>
      </header>

      <nav className="navigation">
        <button
          className={`nav-btn ${activeTab === 'generate' ? 'active' : ''}`}
          onClick={() => { setActiveTab('generate'); setResult(''); setError(''); }}
        >
          📝 Générer
        </button>
        <button
          className={`nav-btn ${activeTab === 'improve' ? 'active' : ''}`}
          onClick={() => { setActiveTab('improve'); setResult(''); setError(''); }}
        >
          ✨ Améliorer
        </button>
        <button
          className={`nav-btn ${activeTab === 'seo' ? 'active' : ''}`}
          onClick={() => { setActiveTab('seo'); setResult(''); setError(''); }}
        >
          🔍 SEO
        </button>
        <button
          className={`nav-btn ${activeTab === 'translate' ? 'active' : ''}`}
          onClick={() => { setActiveTab('translate'); setResult(''); setError(''); }}
        >
          🌍 Traduire
        </button>
      </nav>

      <main className="App-main">
        <div className="container">
          <div className="form-section">
            <form onSubmit={handleSubmit}>
              {renderForm()}

              <div className="button-group">
                <button type="submit" disabled={loading} className="btn-primary">
                  {loading ? '⏳ En cours...' : '🚀 Soumettre'}
                </button>
              </div>
            </form>
          </div>

          <div className="result-section">
            <h2>Résultat</h2>
            
            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}
            
            {loading && (
              <div className="loading">
                <div className="spinner"></div>
                <p>Génération en cours...</p>
              </div>
            )}
            
            {result && (
              <>
                <textarea
                  className="result-text"
                  value={result}
                  readOnly
                  rows={18}
                />
                <div className="stats">
                  📊 <strong>Statistiques:</strong> {wordCount} mots | {charCount} caractères
                </div>
              </>
            )}

            {!result && !loading && !error && (
              <div className="placeholder">
                💡 Remplissez le formulaire et cliquez sur "Soumettre" pour obtenir votre résultat.
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="App-footer">
        <p>💡 <strong>Conseil:</strong> Pour de meilleurs résultats, fournissez des informations détaillées sur votre produit.</p>
        <p>Made with ❤️ by <a href="https://www.linkedin.com/in/ibrahimdayende" target="_blank" rel="noopener noreferrer">Dayende</a></p>
      </footer>
    </div>
  );
}

export default App;
