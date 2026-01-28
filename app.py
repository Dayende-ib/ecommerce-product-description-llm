"""
E-commerce Product Description Generator
A chatbot using Hugging Face Inference API with Mistral-7B
"""

import os
import gradio as gr
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Global history storage
generation_history = []

# Configuration
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
HF_TOKEN = os.getenv("HF_API_TOKEN")

# Initialize the inference client
client = None
if HF_TOKEN:
    client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

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

# Product categories
CATEGORIES = [
    "Mode & Vêtements",
    "Électronique",
    "Maison & Décoration",
    "Beauté & Soins",
    "Sport & Loisirs",
    "Alimentation",
    "Jouets & Enfants",
    "Autre",
]

# Tone options
TONES = [
    "Professionnel",
    "Convivial",
    "Luxueux",
    "Technique",
    "Jeune & Dynamique",
    "Écologique",
]

# Examples for quick start
EXAMPLES_GENERATE = [
    [
        "Casque Bluetooth Premium XSound",
        "Électronique",
        "Réduction de bruit active, autonomie 30h, Bluetooth 5.0, confortable",
        "Professionnels et audiophiles",
        "Professionnel",
        "Français",
        "Moyenne (100-200 mots)"
    ],
    [
        "Crème Anti-Âge Lumière d'Or",
        "Beauté & Soins",
        "Acide hyaluronique, collagène marin, protection SPF 30, texture légère",
        "Femmes 35-55 ans",
        "Luxueux",
        "Français",
        "Longue (200-300 mots)"
    ],
    [
        "Chaussures de Running ProSpeed",
        "Sport & Loisirs",
        "Semelle amortissante, respirant, léger (280g), grip optimal",
        "Coureurs réguliers",
        "Jeune & Dynamique",
        "Français",
        "Moyenne (100-200 mots)"
    ],
]


def check_api_token():
    """Check if API token is configured."""
    if not HF_TOKEN or not client:
        return False, "⚠️ Token API Hugging Face non configuré. Veuillez définir HF_API_TOKEN dans votre fichier .env"
    return True, None


def call_llm(prompt: str, max_tokens: int = 1024) -> str:
    """Call the LLM via Hugging Face Inference API."""
    is_valid, error_msg = check_api_token()
    if not is_valid:
        return error_msg

    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur lors de l'appel à l'API: {str(e)}"


def generate_description(
    product_name: str,
    category: str,
    features: str,
    target_audience: str,
    tone: str,
    language: str,
    length: str,
    num_variants: int = 1,
) -> str:
    """Generate a product description from basic information."""
    if not product_name.strip():
        return "⚠️ Veuillez entrer un nom de produit.", ""

    length_instruction = {
        "Courte (50-100 mots)": "50 to 100 words",
        "Moyenne (100-200 mots)": "100 to 200 words",
        "Longue (200-300 mots)": "200 to 300 words",
    }.get(length, "100 to 200 words")

    lang = LANGUAGES.get(language, "French")

    results = []
    for i in range(num_variants):
        variant_instruction = f" (Variant {i+1})" if num_variants > 1 else ""
        prompt = f"""You are an expert e-commerce copywriter. Generate a compelling product description{variant_instruction}.

Product Name: {product_name}
Category: {category}
Key Features: {features if features.strip() else "Not specified"}
Target Audience: {target_audience if target_audience.strip() else "General audience"}
Tone: {tone}
Language: Write the description in {lang}
Length: {length_instruction}

Requirements:
- Create an engaging, persuasive description
- Highlight benefits, not just features
- Use the specified tone consistently
- Include a call to action
- Make it SEO-friendly with natural keyword usage
{"- Make this variant unique and different from others" if num_variants > 1 else ""}

Generate only the product description, no additional commentary."""

        result = call_llm(prompt)
        if num_variants > 1:
            results.append(f"=== VARIANTE {i+1} ===\n\n{result}")
        else:
            results.append(result)
    
    if num_variants > 1:
        final_result = "\n\n".join(results)
    else:
        final_result = results[0]
    
    # Add to history
    if not final_result.startswith("⚠️") and not final_result.startswith("❌"):
        generation_history.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "product": product_name,
            "type": "Génération",
            "content": final_result
        })
        # Keep only last 10
        if len(generation_history) > 10:
            generation_history.pop()
    
    return final_result, update_history_display()


def improve_description(
    original_description: str,
    improvement_focus: list,
    tone: str,
    language: str,
) -> str:
    """Improve an existing product description."""
    if not original_description.strip():
        return "⚠️ Veuillez entrer une description à améliorer.", ""

    focus_text = ", ".join(improvement_focus) if improvement_focus else "general improvement"
    lang = LANGUAGES.get(language, "French")

    prompt = f"""You are an expert e-commerce copywriter. Improve the following product description.

Original Description:
{original_description}

Improvement Focus: {focus_text}
Desired Tone: {tone}
Language: Write in {lang}

Requirements:
- Maintain the core product information
- Enhance readability and engagement
- Apply the specified improvements
- Keep the specified tone
- Make it more persuasive

Provide the improved description only, no explanations."""

    result = call_llm(prompt)
    
    # Add to history
    if not result.startswith("⚠️") and not result.startswith("❌"):
        generation_history.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "product": "Amélioration",
            "type": "Amélioration",
            "content": result
        })
        if len(generation_history) > 10:
            generation_history.pop()
    
    return result, update_history_display()


def update_history_display():
    """Update the history display."""
    if not generation_history:
        return "📋 Aucune génération récente"
    
    history_text = "📋 **Historique des générations** (dernières 10)\n\n"
    for item in generation_history:
        history_text += f"**[{item['time']}] {item['type']}** - {item['product']}\n"
        preview = item['content'][:100].replace('\n', ' ') + "..."
        history_text += f"_{preview}_\n\n---\n\n"
    
    return history_text


def copy_to_clipboard(text):
    """Helper to show copy notification."""
    if text and not text.startswith("⚠️") and not text.startswith("❌"):
        return "✅ Texte prêt à être copié ! Utilisez Ctrl+C après avoir sélectionné le texte."
    return "⚠️ Aucun texte à copier"


def count_words(text):
    """Count words in text."""
    if not text:
        return "0 mots | 0 caractères"
    words = len(text.split())
    chars = len(text)
    return f"{words} mots | {chars} caractères"


def generate_seo_keywords(
    product_name: str,
    description: str,
    category: str,
    language: str,
) -> str:
    """Generate SEO keywords and optimization suggestions."""
    if not product_name.strip() and not description.strip():
        return "⚠️ Veuillez entrer un nom de produit ou une description."

    lang = LANGUAGES.get(language, "French")

    prompt = f"""You are an SEO expert for e-commerce. Analyze the following product and provide SEO recommendations.

Product Name: {product_name}
Category: {category}
Description: {description if description.strip() else "Not provided"}
Target Language: {lang}

Provide:
1. **Primary Keywords** (5-7 high-value keywords)
2. **Long-tail Keywords** (5-7 specific phrases)
3. **Meta Title Suggestion** (max 60 characters)
4. **Meta Description Suggestion** (max 155 characters)
5. **SEO Tips** (3-4 specific recommendations for this product)

Format your response clearly with headers."""

    return call_llm(prompt, max_tokens=1500)


def translate_description(
    description: str,
    source_language: str,
    target_language: str,
    adapt_culturally: bool,
) -> str:
    """Translate and optionally adapt a product description."""
    if not description.strip():
        return "⚠️ Veuillez entrer une description à traduire."

    if source_language == target_language:
        return "⚠️ Les langues source et cible sont identiques."

    source_lang = LANGUAGES.get(source_language, "French")
    target_lang = LANGUAGES.get(target_language, "English")

    adaptation_instruction = ""
    if adapt_culturally:
        adaptation_instruction = """
- Adapt cultural references, idioms, and expressions for the target market
- Adjust measurements, sizes, or formats if relevant
- Consider local preferences and buying habits"""

    prompt = f"""You are a professional translator specialized in e-commerce content.

Original Description ({source_lang}):
{description}

Task: Translate to {target_lang}

Requirements:
- Maintain the persuasive tone and marketing appeal
- Preserve all product information accurately
- Keep the same structure and formatting{adaptation_instruction}

Provide only the translated description."""

    return call_llm(prompt)


def create_interface():
    """Create the Gradio interface with all features."""
    
    custom_css = """
    .highlight-box {border: 2px solid #4CAF50; border-radius: 8px; padding: 10px;}
    .stat-box {background: #f0f0f0; padding: 10px; border-radius: 5px; margin: 5px 0;}
    """
    
    with gr.Blocks(
        title="E-commerce Product Description Generator",
    ) as app:
        gr.Markdown(
            """
            # Générateur de Descriptions Produits E-commerce
            
            Créez des descriptions de produits professionnelles et optimisées SEO avec l'IA.
            
            *Propulsé par Qwen2.5-7B via Hugging Face Inference API*
            """
        )

        with gr.Tabs():
            # Tab 1: Generate Description (ENHANCED)
            with gr.TabItem("📝 Générer une description"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gen_product_name = gr.Textbox(
                            label="Nom du produit",
                            placeholder="Ex: Casque Bluetooth Premium",
                            info="💡 Soyez précis et descriptif"
                        )
                        gen_category = gr.Dropdown(
                            choices=CATEGORIES,
                            label="Catégorie",
                            value="Autre",
                            info="🎯 Sélectionnez la catégorie appropriée"
                        )
                        
                        with gr.Accordion("⚙️ Options avancées", open=True):
                            gen_features = gr.Textbox(
                                label="Caractéristiques clés",
                                placeholder="Ex: Sans fil, autonomie 30h, réduction de bruit active...",
                                lines=3,
                            )
                            gen_target = gr.Textbox(
                                label="Public cible",
                                placeholder="Ex: Professionnels, gamers, audiophiles...",
                            )
                            gen_tone = gr.Dropdown(
                                choices=TONES,
                                label="Ton",
                                value="Professionnel",
                            )
                            gen_language = gr.Dropdown(
                                choices=list(LANGUAGES.keys()),
                                label="Langue",
                                value="Français",
                            )
                            gen_length = gr.Radio(
                                choices=["Courte (50-100 mots)", "Moyenne (100-200 mots)", "Longue (200-300 mots)"],
                                label="Longueur",
                                value="Moyenne (100-200 mots)",
                            )
                            gen_num_variants = gr.Slider(
                                minimum=1,
                                maximum=3,
                                step=1,
                                value=1,
                                label="Nombre de variantes",
                                info="🔄 Générer plusieurs versions différentes"
                            )
                        
                        with gr.Row():
                            gen_button = gr.Button("✨ Générer", variant="primary", scale=2)
                            gen_clear = gr.Button("🗑️ Effacer", scale=1)
                        
                        # Examples
                        gr.Examples(
                            examples=EXAMPLES_GENERATE,
                            inputs=[gen_product_name, gen_category, gen_features, gen_target, gen_tone, gen_language, gen_length],
                            label="💡 Exemples rapides"
                        )

                    with gr.Column(scale=1):
                        gen_output = gr.Textbox(
                            label="Description générée",
                            lines=18,
                        )
                        gen_word_count = gr.Textbox(
                            label="📊 Statistiques",
                            interactive=False,
                            lines=1
                        )
                        gen_history_display = gr.Markdown(value="📋 Aucune génération récente")

                # Button actions
                gen_button.click(
                    fn=generate_description,
                    inputs=[gen_product_name, gen_category, gen_features, gen_target, gen_tone, gen_language, gen_length, gen_num_variants],
                    outputs=[gen_output, gen_history_display],
                )
                
                gen_output.change(
                    fn=count_words,
                    inputs=[gen_output],
                    outputs=[gen_word_count]
                )
                
                gen_clear.click(
                    fn=lambda: ["", "", "", "", "Professionnel", "Français", "Moyenne (100-200 mots)", 1],
                    outputs=[gen_product_name, gen_category, gen_features, gen_target, gen_tone, gen_language, gen_length, gen_num_variants]
                )

            # Tab 2: Improve Description (ENHANCED)
            with gr.TabItem("✨ Améliorer une description"):
                with gr.Row():
                    with gr.Column(scale=1):
                        imp_original = gr.Textbox(
                            label="Description originale",
                            placeholder="Collez votre description actuelle ici...",
                            lines=8,
                            info="📝 Entrez le texte à améliorer"
                        )
                        
                        with gr.Accordion("⚙️ Options d'amélioration", open=True):
                            imp_focus = gr.CheckboxGroup(
                                choices=[
                                    "Clarté et lisibilité",
                                    "Pouvoir de persuasion",
                                    "Optimisation SEO",
                                    "Appel à l'action",
                                    "Mise en avant des bénéfices",
                                    "Ton et style",
                                ],
                                label="Axes d'amélioration",
                                value=["Clarté et lisibilité", "Pouvoir de persuasion"],
                            )
                            imp_tone = gr.Dropdown(
                                choices=TONES,
                                label="Ton souhaité",
                                value="Professionnel",
                            )
                            imp_language = gr.Dropdown(
                                choices=list(LANGUAGES.keys()),
                                label="Langue",
                                value="Français",
                            )
                        
                        with gr.Row():
                            imp_button = gr.Button("🔄 Améliorer", variant="primary", scale=2)
                            imp_clear = gr.Button("🗑️ Effacer", scale=1)

                    with gr.Column(scale=1):
                        imp_output = gr.Textbox(
                            label="Description améliorée",
                            lines=18,
                        )
                        imp_word_count = gr.Textbox(
                            label="📊 Statistiques",
                            interactive=False,
                            lines=1
                        )
                        imp_history_display = gr.Markdown(value="📋 Aucune amélioration récente")

                imp_button.click(
                    fn=improve_description,
                    inputs=[imp_original, imp_focus, imp_tone, imp_language],
                    outputs=[imp_output, imp_history_display],
                )
                
                imp_output.change(
                    fn=count_words,
                    inputs=[imp_output],
                    outputs=[imp_word_count]
                )
                
                imp_clear.click(
                    fn=lambda: ["", ["Clarté et lisibilité", "Pouvoir de persuasion"], "Professionnel", "Français"],
                    outputs=[imp_original, imp_focus, imp_tone, imp_language]
                )

            # Tab 3: SEO Keywords (ENHANCED)
            with gr.TabItem("🔍 SEO & Mots-clés"):
                with gr.Row():
                    with gr.Column(scale=1):
                        seo_product_name = gr.Textbox(
                            label="Nom du produit",
                            placeholder="Ex: Montre connectée sportive",
                            info="🎯 Nom du produit pour l'analyse SEO"
                        )
                        seo_category = gr.Dropdown(
                            choices=CATEGORIES,
                            label="Catégorie",
                            value="Autre",
                        )
                        seo_description = gr.Textbox(
                            label="Description (optionnel)",
                            placeholder="Entrez une description existante pour une analyse plus précise...",
                            lines=5,
                        )
                        seo_language = gr.Dropdown(
                            choices=list(LANGUAGES.keys()),
                            label="Langue cible",
                            value="Français",
                        )
                        
                        with gr.Row():
                            seo_button = gr.Button("🎯 Analyser SEO", variant="primary", scale=2)
                            seo_clear = gr.Button("🗑️ Effacer", scale=1)

                    with gr.Column(scale=1):
                        seo_output = gr.Textbox(
                            label="Analyse SEO et mots-clés",
                            lines=20,
                        )

                seo_button.click(
                    fn=generate_seo_keywords,
                    inputs=[seo_product_name, seo_description, seo_category, seo_language],
                    outputs=seo_output,
                )
                
                seo_clear.click(
                    fn=lambda: ["", "Autre", "", "Français"],
                    outputs=[seo_product_name, seo_category, seo_description, seo_language]
                )

            # Tab 4: Multi-language Translation (ENHANCED)
            with gr.TabItem("🌍 Multi-langue"):
                with gr.Row():
                    with gr.Column(scale=1):
                        trans_description = gr.Textbox(
                            label="Description à traduire",
                            placeholder="Entrez la description de produit à traduire...",
                            lines=8,
                            info="🌐 Texte source pour traduction"
                        )
                        trans_source = gr.Dropdown(
                            choices=list(LANGUAGES.keys()),
                            label="Langue source",
                            value="Français",
                        )
                        trans_target = gr.Dropdown(
                            choices=list(LANGUAGES.keys()),
                            label="Langue cible",
                            value="English",
                        )
                        trans_adapt = gr.Checkbox(
                            label="Adaptation culturelle",
                            value=True,
                            info="Adapter les références culturelles et expressions pour le marché cible",
                        )
                        
                        with gr.Row():
                            trans_button = gr.Button("🔄 Traduire", variant="primary", scale=2)
                            trans_clear = gr.Button("🗑️ Effacer", scale=1)

                    with gr.Column(scale=1):
                        trans_output = gr.Textbox(
                            label="Description traduite",
                            lines=18,
                        )
                        trans_word_count = gr.Textbox(
                            label="📊 Statistiques",
                            interactive=False,
                            lines=1
                        )

                trans_button.click(
                    fn=translate_description,
                    inputs=[trans_description, trans_source, trans_target, trans_adapt],
                    outputs=trans_output,
                )
                
                trans_output.change(
                    fn=count_words,
                    inputs=[trans_output],
                    outputs=[trans_word_count]
                )
                
                trans_clear.click(
                    fn=lambda: ["", "Français", "English", True],
                    outputs=[trans_description, trans_source, trans_target, trans_adapt]
                )

        gr.Markdown(
            """
            ---
            💡 **Conseil**: Pour de meilleurs résultats, fournissez des informations détaillées sur votre produit.
            
            Made with ❤️ by [Dayende](https://www.linkedin.com/in/ibrahimdayende)
            """
        )

    return app


if __name__ == "__main__":
    app = create_interface()
    custom_css = """
    .highlight-box {border: 2px solid #4CAF50; border-radius: 8px; padding: 10px;}
    .stat-box {background: #f0f0f0; padding: 10px; border-radius: 5px; margin: 5px 0;}
    """
    app.launch(theme=gr.themes.Soft(), css=custom_css)
