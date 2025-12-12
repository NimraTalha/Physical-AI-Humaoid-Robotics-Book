from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.config import settings
import google.generativeai as genai
import os

router = APIRouter()

# Configure the Gemini API client
genai.configure(api_key=settings.gemini_api_key)

class TranslateRequest(BaseModel):
    content: str

@router.post("/translate")
async def translate_content(request: TranslateRequest):
    """
    Translates the content to Urdu using the Gemini API.
    """
    prompt = f"""
    Translate the following English technical text from a book on robotics and AI into clear, high-quality, and natural-sounding Urdu.
    The output should be in HTML format.

    Original English Text:
    ---
    {request.content}
    ---

    Translated Urdu Text (in HTML format):
    """

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        translated_text = response.text
    except Exception as e:
        print(f"Error calling Gemini API for translation: {e}")
        raise HTTPException(status_code=500, detail="Failed to translate content with AI.")

    return {"translated_content": translated_text}
