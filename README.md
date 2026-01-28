# E-commerce Product Description Generator

A chatbot that generates professional e-commerce product descriptions using Hugging Face Inference API with Mistral-7B.

## Features

- **Product Description Generation**: Create compelling descriptions from basic product information
- **Description Improvement**: Enhance existing descriptions for better engagement
- **SEO Optimization**: Generate keywords, meta titles, and descriptions
- **Multi-language Support**: Translate and culturally adapt descriptions across 7 languages

## Supported Languages

- French, English, Spanish, German, Italian, Portuguese, Dutch

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ecommerce-product-description-llm.git
cd ecommerce-product-description-llm

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Get your Hugging Face API token from https://huggingface.co/settings/tokens
2. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

3. Edit `.env` and add your token:

```
HF_API_TOKEN=your_huggingface_token_here
```

## Usage

```bash
python app.py
```

The application will start and open in your browser at `http://localhost:7860`.

## Interface Tabs

### 1. Generate Description
Enter product details (name, category, features, target audience) and get a professional description.

### 2. Improve Description
Paste an existing description and select improvement areas (clarity, persuasion, SEO, etc.).

### 3. SEO & Keywords
Get keyword suggestions, meta titles, and SEO recommendations for your products.

### 4. Multi-language
Translate descriptions with optional cultural adaptation for target markets.

## Model

This application uses **Mistral-7B-Instruct-v0.2** via Hugging Face Inference API, known for excellent multilingual support and high-quality text generation.

## License

MIT License
