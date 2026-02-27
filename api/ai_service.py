import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()

def generate_recommendation_rationale(user_prefs: dict, candidates: list) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "I found some great restaurants for you based on the database, but my AI chef module is offline (Missing GEMINI_API_KEY) so I cannot provide a detailed rationale right now!"
        
    if not candidates:
        return "I'm sorry, but I couldn't find any restaurants that match those exact preferences. Try broadening your search or adjusting the price/rating constraints."

    # Configure the library
    genai.configure(api_key=api_key)
    
    # Proactively find a model that supports generation
    try:
        models = list(genai.list_models())
        gemini_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods and 'gemini' in m.name]
        
        if not gemini_models:
            print("CRITICAL: No Gemini models found with generateContent support for this key!")
            # Try a blind guess if list fails
            model_name = "gemini-1.5-flash"
        else:
            # Prefer 1.5-flash if available, otherwise just pick the first one
            preferred = [m for m in gemini_models if 'gemini-1.5-flash' in m]
            if preferred:
                model_name = preferred[0]
            else:
                model_name = gemini_models[0]
            
        print(f"DEBUG: Using model -> {model_name}")
        model = genai.GenerativeModel(model_name)
    except Exception as e:
        print(f"Error during model discovery: {e}")
        model = genai.GenerativeModel('gemini-1.5-flash') # Ultimate fallback
    
    prompt = f"""
    You are an AI restaurant recommendation expert acting as a friendly digital concierge. 
    A user has asked for recommendations based on these preferences: {json.dumps(user_prefs)}
    
    I have queried the database and found these exact top candidates that match their criteria:
    {json.dumps(candidates, indent=2)}
    
    Your job is to write a warm, engaging, and highly personalized recommendation rationale. 
    Acknowledge their preferences briefly, and explicitly mention 2-3 of the top restaurants from the list provided, explaining *why* they are perfect choices based on the data (cost, rating, cuisine).
    Make it sound natural and enthusiastic. Do not hallucinate restaurants that aren't in the provided list.
    **CRITICAL STYLISTIC INSTRUCTION**: Output the rationale as **short, crisp HTML bullet points** (<ul><li>...</li></ul>) rather than a long paragraph. Keep each point highly concise and easy to read quickly. Do not include markdown code block syntax like ```html, just return the raw HTML tags.
    """
    
    try:
        response = model.generate_content(prompt)
        if not response or not response.text:
            print("Gemini returned empty response")
            return "I found some matches, but the AI chef's notes were empty this time."
        return response.text
    except Exception as e:
        import traceback
        print(f"DEBUG - Model Name: {model_name}")
        traceback.print_exc()
        return "I found some matches, but my AI generator encountered an issue creating the summary."
