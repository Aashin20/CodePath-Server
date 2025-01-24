from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import os
from groq import Groq

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/health")
async def health():
    return {"200": "OK"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")