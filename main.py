from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Union
import telegramify_markdown
import asyncio

app = FastAPI(
    title="Telegramify Markdown API",
    description="API wrapper for telegramify-markdown library with support for markdownify, telegramify, and standardize functions",
    version="1.0.0"
)

class TextRequest(BaseModel):
    text: str

class TextResponse(BaseModel):
    result: str

class TelegramifyResponse(BaseModel):
    result: List[Dict[str, Any]]

@app.post("/markdownify", response_model=TextResponse)
async def markdownify_text(request: TextRequest):
    """
    Convert text to markdown format using the markdownify function.
    """
    try:
        result = telegramify_markdown.markdownify(request.text)
        return TextResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@app.post("/telegramify", response_model=TelegramifyResponse)
async def telegramify_text(request: TextRequest):
    """
    Convert text to Telegram-formatted markdown using the telegramify function.
    Returns a list of content items with different types (TEXT, PHOTO, FILE, etc.).
    """
    try:
        # Check if telegramify function exists, if not fall back to markdownify
        if hasattr(telegramify_markdown, 'telegramify'):
            # Call telegramify function (it might be async)
            result = telegramify_markdown.telegramify(request.text)
            
            # Check if result is a coroutine (async)
            if asyncio.iscoroutine(result):
                result = await result
            
            # Convert result to serializable format
            if isinstance(result, list):
                serializable_result = []
                for item in result:
                    if hasattr(item, '__dict__'):
                        serializable_result.append(item.__dict__)
                    else:
                        serializable_result.append(str(item))
                return TelegramifyResponse(result=serializable_result)
            else:
                return TelegramifyResponse(result=[{"type": "TEXT", "content": str(result)}])
        else:
            # Fallback to markdownify if telegramify is not available
            result = telegramify_markdown.markdownify(request.text)
            return TelegramifyResponse(result=[{"type": "TEXT", "content": result}])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@app.post("/standardize", response_model=TextResponse)
async def standardize_text(request: TextRequest):
    """
    Standardize text formatting using the standardize function.
    """
    try:
        # Check if standardize function exists, if not fall back to markdownify
        if hasattr(telegramify_markdown, 'standardize'):
            result = telegramify_markdown.standardize(request.text)
        else:
            # Fallback to markdownify if standardize is not available
            result = telegramify_markdown.markdownify(request.text)
        return TextResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@app.get("/")
async def root():
    """
    Health check endpoint.
    """
    return {"message": "Telegramify Markdown API is running"}

@app.get("/debug")
async def debug_info():
    """
    Debug endpoint to check available functions in telegramify_markdown module.
    """
    available_functions = [attr for attr in dir(telegramify_markdown) if not attr.startswith('_')]
    return {
        "available_functions": available_functions,
        "has_markdownify": hasattr(telegramify_markdown, 'markdownify'),
        "has_telegramify": hasattr(telegramify_markdown, 'telegramify'),
        "has_standardize": hasattr(telegramify_markdown, 'standardize')
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)