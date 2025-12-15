import logging
import os
import google.generativeai as genai
from app.config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        if not settings.gemini_api_key:
            logger.error("GEMINI_API_KEY is not set in environment variables.")
            raise ValueError("GEMINI_API_KEY is not configured.")
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        logger.info("GeminiService initialized with gemini-1.5-flash-latest model.")

    async def generate_content(self, prompt: str) -> str:
        """
        Generates content using the Gemini model based on the given prompt.
        """
        try:
            response = await self.model.generate_content_async(prompt)
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                return ''.join(part.text for part in response.candidates[0].content.parts if part.text)
            logger.warning("No content generated or response format is unexpected.")
            return "No content generated."
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {e}", exc_info=True)
            raise

    async def translate(self, content: str, target_language: str, source_language: str = "English") -> str:
        """
        Translates the given content to the target language using Gemini,
        preserving structure and without translating code blocks.
        """
        prompt = f"""
You are a professional technical translator.
TASK: Translate the provided technical book chapter from {source_language} into clear, simple, professional {target_language}.

STRICT RULES:
- Preserve ALL headings and subheadings exactly as they are in the source.
- DO NOT translate content inside code blocks (```...```).
- DO NOT modify code formatting.
- Preserve all markdown formatting, including lists, bold, italics, and links.
- Keep technical terms accurate and beginner-friendly.
- Maintain the original paragraph structure.
- Use neutral, modern {target_language}.
- Do not add or remove content.
- Do not explain anything.
- Output ONLY the translated content.

CONTENT TO TRANSLATE:
{content}
"""
        return await self.generate_content(prompt)

    async def chat_completion(self, history: list, message: str) -> str:
        """
        Conducts a chat completion using the Gemini model.
        `history` should be a list of dicts, e.g., [{"role": "user", "parts": ["Hello."]}, {"role": "model", "parts": ["Hi there!"]}]
        """
        try:
            chat = self.model.start_chat(history=history)
            response = await chat.send_message_async(message)
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                return ''.join(part.text for part in response.candidates[0].content.parts if part.text)
            logger.warning("No chat response generated or response format is unexpected.")
            return "No chat response generated."
        except Exception as e:
            logger.error(f"Error in Gemini chat completion: {e}", exc_info=True)
            raise

gemini_service = GeminiService()