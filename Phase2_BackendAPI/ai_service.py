import os
from google import genai
import json
from dotenv import load_dotenv

load_dotenv()

def generate_recommendation_rationale(user_prefs: dict, candidates: list) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "I found some great restaurants for you based on the database, but my AI chef module is offline (Missing GEMINI_API_KEY) so I cannot provide a detailed rationale right now!"
        
    if not candidates:
        return "I'm sorry, but I couldn't find any restaurants that match those exact preferences. Try broadening your search or adjusting the price/rating constraints."

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an AI restaurant recommendation expert acting as a friendly digital concierge. 
    A user has asked for recommendations based on these preferences: {json.dumps(user_prefs)}
    
    I have queried the database and found these exact top candidates that match their criteria:
    {json.dumps(candidates, indent=2)}
    
    Your job is to write a warm, engaging, and highly personalized recommendation rationale. 
    Acknowledge their preferences briefly, and explicitly mention 2-3 of the top restaurants from the list provided, explaining *why* they are perfect choices based on the data (cost, rating, cuisine).
    Make it sound natural and enthusiastic. Do not hallucinate restaurants that aren't in the provided list.
    **CRITICAL STYLISTIC INSTRUCTION**: Output the rationale as **short, crisp HTML bullet points** (`<ul><li>...</li></ul>`) rather than a long paragraph. Keep each point highly concise and easy to read quickly. Do not include markdown code block syntax like ```html, just return the raw HTML tags.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "I found some matches, but my AI generator encountered an issue creating the summary."
