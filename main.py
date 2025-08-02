from dotenv import load_dotenv
import os
import asyncio
import requests
import json

load_dotenv(".env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def make_gemini_request(prompt_text):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt_text
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "No response generated"
            
    except requests.exceptions.RequestException as e:
        return f"Error making request: {e}"
    except KeyError as e:
        return f"Error parsing response: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

async def main():
    prompt = "Ali razumeš slovensko? povej mi kratko zgodbico v slovenščini da vidim kako ti gre slovenščina. Zgodba naj bo o dečku ki rad igra košarko."
    print("Making request to Gemini API...")
    result = make_gemini_request(prompt)
    print("\nResponse from Gemini:")
    print("=" * 50)
    print(result)
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
