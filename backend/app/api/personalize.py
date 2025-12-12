from fastapi import APIRouter, Depends, HTTPException
from app.schemas import User
from app.security import get_current_user
from pydantic import BaseModel
from app.config import settings # Import settings
import google.generativeai as genai # Import gemini client
import os # To ensure GEMINI_API_KEY is loaded correctly

router = APIRouter()

# Configure the Gemini API client
genai.configure(api_key=settings.gemini_api_key)

class PersonalizeRequest(BaseModel):
    content: str

@router.post("/personalize")
async def personalize_content(
    request: PersonalizeRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Personalizes the content based on the user's background using the Gemini API.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Access user background information
    software_background = current_user.get('software_background', 'not specified')
    hardware_background = current_user.get('hardware_background', 'not specified')
    username = current_user.get('username', 'User')

    # Construct a detailed prompt for Gemini
    prompt = f"""
    You are an AI assistant specialized in Physical AI and Humanoid Robotics. Your task is to personalize the provided chapter content for a user with specific technical backgrounds.

    User's Background:
    - Username: {username}
    - Software Background: {software_background}
    - Hardware Background: {hardware_background}

    Original Chapter Content:
    ---
    {request.content}
    ---

    Instructions for Personalization:
    1.  Tailor the explanation of concepts to best resonate with the user's stated software and hardware background.
    2.  Provide examples or analogies that relate to their background.
    3.  Suggest practical applications or next steps relevant to their skills.
    4.  Maintain the core information and academic rigor of the original content.
    5.  Present the personalized content in clear, readable HTML format, suitable for a technical textbook. Ensure all content is within appropriate HTML tags (e.g., <p>, <h2>, <ul>, <ol>, <code>, <pre>).
    6.  The output should only be the personalized content, without any conversational filler or introductory/concluding remarks.
    """

    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-pro')

        # Generate personalized content
        response = model.generate_content(prompt)
        personalized_text = response.text

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        raise HTTPException(status_code=500, detail="Failed to personalize content with AI.")

    return {"personalized_content": personalized_text}