import logging
import os
import google.generativeai as genai
from app.config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        # Ensure the Gemini API key is set in environment variables
        if not settings.gemini_api_key:
            logger.error("GEMINI_API_KEY is not set in environment variables.")
            raise ValueError("GEMINI_API_KEY is not configured.")
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        logger.info("GeminiService initialized with gemini-pro model.")

    async def generate_content(self, prompt: str) -> str:
        """
        Generates content using the Gemini Pro model based on the given prompt.
        """
        try:
            response = await self.model.generate_content_async(prompt)
            # Access the text from the candidate's content parts
            if response.candidates:
                full_text = ""
                for part in response.candidates[0].content.parts:
                    if part.text:
                        full_text += part.text
                return full_text
            return "No content generated."
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {e}", exc_info=True)
            raise

    async def chat_completion(self, history: list, message: str) -> str:
        """
        Conducts a chat completion using the Gemini Pro model.
        `history` should be a list of dicts, e.g., [{"role": "user", "parts": ["Hello."]}, {"role": "model", "parts": ["Hi there!"]}]
        """
        try:
            chat = self.model.start_chat(history=history)
            response = await chat.send_message_async(message)
            if response.candidates:
                full_text = ""
                for part in response.candidates[0].content.parts:
                    if part.text:
                        full_text += part.text
                return full_text
            return "No chat response generated."
        except Exception as e:
            logger.error(f"Error in Gemini chat completion: {e}", exc_info=True)
            raise

gemini_service = GeminiService()