# E-commerce Product Description Generator

An AI-powered tool to generate professional product descriptions for e-commerce.

## Features

- 🎯 Generate product descriptions with AI
- ✨ Improve existing descriptions
- 🔍 SEO keyword analysis
- 🌍 Multi-language translation
- 🔄 Generate multiple variants

## Architecture

- **Frontend**: React + TypeScript
- **Backend**: FastAPI + Python
- **AI Model**: Qwen2.5-7B via Hugging Face Inference API
- **Deployment**: Docker (single deployment)

## Deployment on Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Select **Docker** as the SDK
3. Upload the following files/folders:
   - `frontend/` (React app)
   - `backend/` (FastAPI server)
   - `Dockerfile`
   - `nginx.conf`
   - `.dockerignore`
4. Add your `HF_API_TOKEN` as a secret in Space settings
5. Deploy!

## Local Development

### Backend API

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

API will be available at: http://localhost:8000

API Documentation: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm start
```

Frontend will be available at: http://localhost:3000

### Full Docker Build (Production)

```bash
docker build -t ecommerce-desc-gen .
docker run -p 7860:7860 -e HF_API_TOKEN=your_token ecommerce-desc-gen
```

Application will be available at: http://localhost:7860

## Environment Variables

- `HF_API_TOKEN`: Your Hugging Face API token (required)

## API Endpoints

- `POST /api/generate` - Generate product description
- `POST /api/improve` - Improve existing description
- `POST /api/seo` - Generate SEO keywords
- `POST /api/translate` - Translate description
- `GET /health` - Health check

## Tech Stack

- React 18 + TypeScript
- FastAPI
- Hugging Face Inference API
- Nginx (reverse proxy)
- Docker

## Credits

Made with ❤️ by [Dayende](https://www.linkedin.com/in/ibrahimdayende)

## License

MIT
