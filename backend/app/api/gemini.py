from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import logging

from app.services.gemini_service import gemini_service
from app.schemas import ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter()

class GeminiGenerateRequest(BaseModel):
    prompt: str = Field(..., description="The text prompt to send to the Gemini model.")

class GeminiChatRequest(BaseModel):
    history: List[Dict[str, Any]] = Field(..., description="Chat history in Gemini format.")
    message: str = Field(..., description="The current message from the user.")

class GeminiResponse(BaseModel):
    response_text: str = Field(..., description="The generated content from the Gemini model.")

@router.post(
    "/gemini/generate",
    response_model=GeminiResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    tags=["Gemini"]
)
async def generate_gemini_content(request: GeminiGenerateRequest):
    """
    Generates text content using the Gemini Pro model based on a given prompt.
    """
    try:
        logger.info(f"Received Gemini generate request for prompt: {request.prompt[:50]}...")
        content = await gemini_service.generate_content(request.prompt)
        return GeminiResponse(response_text=content)
    except Exception as e:
        logger.error(f"Gemini content generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "gemini_generation_error",
                "message": "Failed to generate content with Gemini. Please try again.",
                "details": str(e)
            }
        )

@router.post(
    "/gemini/chat",
    response_model=GeminiResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    tags=["Gemini"]
)
async def gemini_chat_completion(request: GeminiChatRequest):
    """
    Conducts a chat completion using the Gemini Pro model based on chat history and a new message.
    """
    try:
        logger.info(f"Received Gemini chat request for message: {request.message[:50]}...")
        response = await gemini_service.chat_completion(request.history, request.message)
        return GeminiResponse(response_text=response)
    except Exception as e:
        logger.error(f"Gemini chat completion failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "gemini_chat_error",
                "message": "Failed to get chat completion from Gemini. Please try again.",
                "details": str(e)
            }
        )
