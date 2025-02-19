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
from prompt import response,send_evaluation,get_latest_qn
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime,UTC

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["Questions"]
collection = db["Elab_Questions"]

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

class Evaluate(BaseModel):
    steps: str
    language: str
    code: str

class QuestionModel(BaseModel):
    question: str
    
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

@app.post('/evaluate')
async def evaluate_qn(content: Evaluate):    
    return send_evaluation(steps=content.steps,language=content.language,code=content.code)


@app.post("/saveqn")
async def save_content(question_data: QuestionModel):
    try:
        qn = ' '.join(question_data.question.split("Constraints")[0].split())
        result = collection.insert_one({
            "question": qn,
            "timestamp": datetime.utcnow()  # Add this line
        })
        return {
            "success": True,
            "message": "Content saved successfully",
            "id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/elab")
async def elab_qn(language):
    try:
        latest_question = get_latest_qn()
        if latest_question:
            return response(question=latest_question,language=language)
        return {"error": "No questions found"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
            




try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



#Endpoint for health check
@app.get("/health")
async def health():
    return {"200": "OK"}





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")