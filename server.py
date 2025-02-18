from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import os
from dotenv import load_dotenv
from groq import Groq
import json
from dotenv import load_dotenv
import requests
from Integrations.leetcode import leetcode_problem
from prompt import response




#Initializing FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

#Pydantic Models:

class TextDetails(BaseModel):
    question : str
    language : str

class LeetcodeDetails(BaseModel):
    question_id: int
    language:str


#EndPoints:

#Endpoint for text questions
@app.post('/question')
async def text_qn(details: TextDetails):
    return response(question=details.question, language=details.language)
        

#Endpoint for leetcode questions
@app.post('/leetcode')
async def leetcode_qn(details: LeetcodeDetails):
    description=leetcode_problem(frontend_id=details.question_id)["data"]["question"]["content"]
    return response(description,language=details.language)




#Endpoint for health check
@app.get("/health")
async def health():
    return {"200": "OK"}





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")