"""
E-commerce Product Description Generator API
FastAPI backend for React frontend
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()

# Configuration
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
HF_TOKEN = os.getenv("HF_API_TOKEN")

# Initialize the inference client
client = None
if HF_TOKEN:
    client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

# Initialize FastAPI
app = FastAPI(
    title="E-commerce Product Description Generator API",
    description="Generate product descriptions using AI",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Available languages
LANGUAGES = {
    "Français": "French",
    "English": "English",
    "Español": "Spanish",
    "Deutsch": "German",
    "Italiano": "Italian",
    "Português": "Portuguese",
    "Nederlands": "Dutch",
}

# Pydantic models for request validation
class GenerateDescriptionRequest(BaseModel):
    product_name: str
    category: str
    features: Optional[str] = ""
    target_audience: Optional[str] = ""
    tone: str = "Professionnel"
    language: str = "Français"
    length: str = "Moyenne (100-200 mots)"
    num_variants: int = 1

class ImproveDescriptionRequest(BaseModel):
    original_description: str
    improvement_focus: List[str] = []
    tone: str = "Professionnel"
    language: str = "Français"

class SEOKeywordsRequest(BaseModel):
    product_name: str
    description: Optional[str] = ""
    category: str
    language: str = "Français"

class TranslateDescriptionRequest(BaseModel):
    description: str
    source_language: str = "Français"
    target_language: str = "English"
    adapt_culturally: bool = True

class APIResponse(BaseModel):
    success: bool
    data: Optional[str] = None
    error: Optional[str] = None


def check_api_token():
    """Check if API token is configured."""
    if not HF_TOKEN or not client:
        return False, "Token API Hugging Face non configuré"
    return True, None


def call_llm(prompt: str, max_tokens: int = 1024) -> str:
    """Call the LLM via Hugging Face Inference API."""
    is_valid, error_msg = check_api_token()
    if not is_valid:
        raise HTTPException(status_code=500, detail=error_msg)

    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'appel à l'API: {str(e)}")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "E-commerce Product Description Generator API", "status": "running"}


@app.get("/health")
async def health():
    """Health check with API token verification."""
    is_valid, error_msg = check_api_token()
    return {
        "status": "healthy" if is_valid else "error",
        "api_configured": is_valid,
        "error": error_msg
    }


@app.post("/api/generate", response_model=APIResponse)
async def generate_description(request: GenerateDescriptionRequest):
    """Generate product description from basic information."""
    try:
        if not request.product_name.strip():
            return APIResponse(success=False, error="Veuillez entrer un nom de produit")

        length_instruction = {
            "Courte (50-100 mots)": "50 to 100 words",
            "Moyenne (100-200 mots)": "100 to 200 words",
            "Longue (200-300 mots)": "200 to 300 words",
        }.get(request.length, "100 to 200 words")

        lang = LANGUAGES.get(request.language, "French")

        results = []
        for i in range(request.num_variants):
            variant_instruction = f" (Variant {i+1})" if request.num_variants > 1 else ""
            prompt = f"""You are an expert e-commerce copywriter. Generate a compelling product description{variant_instruction}.

Product Name: {request.product_name}
Category: {request.category}
Key Features: {request.features if request.features.strip() else "Not specified"}
Target Audience: {request.target_audience if request.target_audience.strip() else "General audience"}
Tone: {request.tone}
Language: Write the description in {lang}
Length: {length_instruction}

Requirements:
- Create an engaging, persuasive description
- Highlight benefits, not just features
- Use the specified tone consistently
- Include a call to action
- Make it SEO-friendly with natural keyword usage
{"- Make this variant unique and different from others" if request.num_variants > 1 else ""}

Generate only the product description, no additional commentary."""

            result = call_llm(prompt)
            if request.num_variants > 1:
                results.append(f"=== VARIANTE {i+1} ===\n\n{result}")
            else:
                results.append(result)
        
        final_result = "\n\n".join(results) if request.num_variants > 1 else results[0]
        
        return APIResponse(success=True, data=final_result)
    
    except HTTPException as he:
        return APIResponse(success=False, error=he.detail)
    except Exception as e:
        return APIResponse(success=False, error=str(e))


@app.post("/api/improve", response_model=APIResponse)
async def improve_description(request: ImproveDescriptionRequest):
    """Improve an existing product description."""
    try:
        if not request.original_description.strip():
            return APIResponse(success=False, error="Veuillez entrer une description à améliorer")

        focus_text = ", ".join(request.improvement_focus) if request.improvement_focus else "general improvement"
        lang = LANGUAGES.get(request.language, "French")

        prompt = f"""You are an expert e-commerce copywriter. Improve the following product description.

Original Description:
{request.original_description}

Improvement Focus: {focus_text}
Desired Tone: {request.tone}
Language: Write in {lang}

Requirements:
- Maintain the core product information
- Enhance readability and engagement
- Apply the specified improvements
- Keep the specified tone
- Make it more persuasive

Provide the improved description only, no explanations."""

        result = call_llm(prompt)
        return APIResponse(success=True, data=result)
    
    except HTTPException as he:
        return APIResponse(success=False, error=he.detail)
    except Exception as e:
        return APIResponse(success=False, error=str(e))


@app.post("/api/seo", response_model=APIResponse)
async def generate_seo_keywords(request: SEOKeywordsRequest):
    """Generate SEO keywords and optimization suggestions."""
    try:
        if not request.product_name.strip() and not request.description.strip():
            return APIResponse(success=False, error="Veuillez entrer un nom de produit ou une description")

        lang = LANGUAGES.get(request.language, "French")

        prompt = f"""You are an SEO expert for e-commerce. Analyze the following product and provide SEO recommendations.

Product Name: {request.product_name}
Category: {request.category}
Description: {request.description if request.description.strip() else "Not provided"}
Target Language: {lang}

Provide:
1. **Primary Keywords** (5-7 high-value keywords)
2. **Long-tail Keywords** (5-7 specific phrases)
3. **Meta Title Suggestion** (max 60 characters)
4. **Meta Description Suggestion** (max 155 characters)
5. **SEO Tips** (3-4 specific recommendations for this product)

Format your response clearly with headers."""

        result = call_llm(prompt, max_tokens=1500)
        return APIResponse(success=True, data=result)
    
    except HTTPException as he:
        return APIResponse(success=False, error=he.detail)
    except Exception as e:
        return APIResponse(success=False, error=str(e))


@app.post("/api/translate", response_model=APIResponse)
async def translate_description(request: TranslateDescriptionRequest):
    """Translate and optionally adapt a product description."""
    try:
        if not request.description.strip():
            return APIResponse(success=False, error="Veuillez entrer une description à traduire")

        if request.source_language == request.target_language:
            return APIResponse(success=False, error="Les langues source et cible sont identiques")

        source_lang = LANGUAGES.get(request.source_language, "French")
        target_lang = LANGUAGES.get(request.target_language, "English")

        adaptation_instruction = ""
        if request.adapt_culturally:
            adaptation_instruction = """
- Adapt cultural references, idioms, and expressions for the target market
- Adjust measurements, sizes, or formats if relevant
- Consider local preferences and buying habits"""

        prompt = f"""You are a professional translator specialized in e-commerce content.

Original Description ({source_lang}):
{request.description}

Task: Translate to {target_lang}

Requirements:
- Maintain the persuasive tone and marketing appeal
- Preserve all product information accurately
- Keep the same structure and formatting{adaptation_instruction}

Provide only the translated description."""

        result = call_llm(prompt)
        return APIResponse(success=True, data=result)
    
    except HTTPException as he:
        return APIResponse(success=False, error=he.detail)
    except Exception as e:
        return APIResponse(success=False, error=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
