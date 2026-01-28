# Guide de déploiement sur Hugging Face Spaces

## 📦 Architecture créée

Votre projet contient maintenant :

```
ecommerce-product-description-llm/
├── frontend/              # Application React (en cours d'installation)
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/               # API FastAPI ✅ CRÉÉ
│   ├── main.py
│   └── requirements.txt
│
├── Dockerfile             # Configuration Docker ✅ CRÉÉ
├── nginx.conf             # Configuration Nginx ✅ CRÉÉ
├── .dockerignore          # Fichiers à ignorer ✅ CRÉÉ
└── README.md              # Documentation ✅ MIS À JOUR
```

## 🚀 Étapes de déploiement

### 1. Préparer le projet

Une fois que `create-react-app` aura terminé (en cours...), vous devrez :

- Personnaliser le frontend React selon vos besoins
- Tester localement avec `npm start` (frontend) et `uvicorn main:app` (backend)

### 2. Créer un Space sur Hugging Face

1. Allez sur https://huggingface.co/new-space
2. Choisissez un nom pour votre Space
3. Sélectionnez **Docker** comme SDK
4. Choisissez **CPU Basic** (gratuit)

### 3. Configurer les secrets

Dans les paramètres de votre Space :
- Ajoutez `HF_API_TOKEN` comme variable d'environnement secrète
- Collez votre token Hugging Face

### 4. Uploader les fichiers

Vous pouvez uploader via :

**Option A : Interface web**
- Glissez-déposez tous les dossiers et fichiers

**Option B : Git**
```bash
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE
git push space main
```

### 5. Déploiement automatique

Hugging Face va automatiquement :
1. Construire l'image Docker
2. Compiler le frontend React
3. Démarrer Nginx + FastAPI
4. Exposer l'application sur le port 7860

### 6. Accéder à votre application

Votre app sera disponible à :
```
https://YOUR_USERNAME-YOUR_SPACE.hf.space
```

## 🧪 Test local avant déploiement

### Backend seul :
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# Testez sur http://localhost:8000/docs
```

### Frontend seul :
```bash
cd frontend
npm start
# Testez sur http://localhost:3000
```

### Docker complet :
```bash
docker build -t test-app .
docker run -p 7860:7860 -e HF_API_TOKEN=your_token test-app
# Testez sur http://localhost:7860
```

## ✅ Points à vérifier avant déploiement

- [ ] Le frontend React compile sans erreur (`npm run build`)
- [ ] L'API FastAPI fonctionne localement
- [ ] Votre `HF_API_TOKEN` est valide
- [ ] Tous les fichiers nécessaires sont présents
- [ ] Le Dockerfile est correctement configuré

## 🔧 Personnalisation du frontend

Une fois React installé, vous pourrez :
- Créer des composants React pour chaque fonctionnalité
- Utiliser votre design préféré (Material-UI, Tailwind, etc.)
- Appeler l'API FastAPI via `fetch()` ou `axios`

## 📚 Documentation API

Une fois déployé, votre API sera documentée automatiquement à :
- `https://your-space.hf.space/docs` (Swagger UI)
- `https://your-space.hf.space/redoc` (ReDoc)

## 🎯 Prochaines étapes

1. ⏳ Attendre la fin de l'installation de React
2. 🎨 Personnaliser le frontend selon vos besoins
3. 🧪 Tester localement
4. 🚀 Déployer sur Hugging Face Spaces

---

Made with ❤️ by Dayende
