import os
import json
from openai import OpenAI
import google.generativeai as genai

# Configuration
gemini_key = os.environ.get("GEMINI_API_KEY")
openai_key = os.environ.get("OPENAI_API_KEY")

llm_provider = None
openai_client = None

if gemini_key:
    genai.configure(api_key=gemini_key)
    llm_provider = "gemini"
elif openai_key:
    openai_client = OpenAI(api_key=openai_key)
    llm_provider = "openai"
else:
    print("Warning: No API key found (GEMINI_API_KEY or OPENAI_API_KEY). LLM features will fail.")

def get_json_response(prompt: str, system_prompt: str = "You are a helpful assistant that outputs JSON.") -> dict:
    """
    Helper function to get JSON response from the configured LLM provider.
    """
    if llm_provider == "gemini":
        try:
            model = genai.GenerativeModel(
                'gemini-flash-latest', 
                system_instruction=system_prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            response = model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"Gemini error: {e}")
            return {}
            
    elif llm_provider == "openai":
        try:
            if not openai_client:
                return {}
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"OpenAI error: {e}")
            return {}
    
    return {}

def summarize_deck(raw_text: str) -> dict:
    prompt = f"""
    You are a venture capital analyst. Summarize the following pitch deck content into a structured JSON object with these keys:
    - team
    - product
    - market
    - traction
    - financials
    - ask
    - risks

    Content:
    {raw_text[:15000]} 
    """
    # Truncate to avoid token limits if necessary.
    
    return get_json_response(prompt)

def extract_claims(summary_json: dict) -> list[dict]:
    prompt = f"""
    Based on the following summary of a pitch deck, extract important factual claims.
    Return a JSON object with a key "claims" which is a list of objects.
    Each object must have:
    - "text": The claim text
    - "category": One of "traction", "market", "team", "product", "financials", "other"

    Summary:
    {json.dumps(summary_json)}
    """
    
    data = get_json_response(prompt)
    return data.get("claims", [])

def assess_claim(claim_text: str, summary_json: dict) -> tuple[float, str]:
    prompt = f"""
    Assess the plausibility of the following claim based on the context provided in the summary.
    
    Claim: {claim_text}
    
    Context:
    {json.dumps(summary_json)}
    
    Return a JSON object with:
    - "score": A float between 0.0 and 1.0 (1.0 being very plausible/verified, 0.0 being implausible)
    - "notes": A 1-3 sentence explanation.
    """
    
    data = get_json_response(prompt)
    return data.get("score", 0.5), data.get("notes", "No assessment available.")

def generate_questions(claims: list[dict], summary_json: dict) -> list[dict]:
    prompt = f"""
    Generate 8 to 12 specific follow-up questions an investor should ask based on the summary and claims.
    Distribute questions across categories: market, product, traction, financials, team, other.
    
    Return a JSON object with a key "questions" which is a list of objects.
    Each object must have:
    - "text": The question text
    - "category": The category
    
    Summary:
    {json.dumps(summary_json)}
    
    Claims:
    {json.dumps(claims)}
    """
    
    data = get_json_response(prompt)
    return data.get("questions", [])
