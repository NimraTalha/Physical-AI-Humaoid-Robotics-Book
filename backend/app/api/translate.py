from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.services.gemini_service import gemini_service
from app.security import get_current_user
from app.schemas import User

router = APIRouter()

class TranslateRequest(BaseModel):
    content: str
    target_language: str = "Urdu"

@router.post("/translate", tags=["Translation"])
async def translate_content(
    request: TranslateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Translates the given content to the target language.
    """
    if not request.content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content cannot be empty.",
        )
    
    try:
        translated_text = await gemini_service.translate(
            content=request.content,
            target_language=request.target_language
        )
        return {"translated_text": translated_text}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during translation: {e}",
        )