import os
import socket
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

HOSTNAME = socket.gethostname()

class GenerateRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    prompt: str
    response: str
    container: str

@app.get("/health")
async def health_check():
    return {"status": "healthy", "container": HOSTNAME}


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured")
    
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(request.prompt)
        
        return GenerateResponse(
            prompt=request.prompt,
            response=response.text,
            container=HOSTNAME
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
