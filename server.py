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

#Grok
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)


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


#Functions:

#Function for querying LLM
def response(question, language):
    prompts = {
        "javascript": """Generate a JSON object that represents a coding question in JavaScript. The object should include:
    - "description" give a concise explanation about the question in about 50 words. DONT MENTION ANYTHING ABOUT THE SOLUTION
    - "steps" as an array where each element is an object with the following keys:
      - "step_id" as a number indicating the step's serial number.
      - "step_title" as a string describing the step.
      - "code" as a string representing the code needed for this step.
      - "desired_output" as a string describing the expected output of the code, if any.
      - "hint" as a string providing a hint to help with the step.

    Ensure that each step's code is executable in isolation, and the final code can be constructed by combining all the steps. Include essential elements like function definitions, return statements, and method calls.

    For example, for the question "How to implement a function to add two numbers in JavaScript?":
    {
      "description": "Create a function that takes two numbers as input parameters and returns their sum. This is a basic mathematical operation implemented as a reusable function.",
      "steps": [
        {
          "step_id": 1,
          "step_title": "Define the function",
          "code": "function addTwoNumbers(num1, num2) {",
          "desired_output": "",
          "hint": "Start by defining the function with parameters for the numbers."
        },
        {
          "step_id": 2,
          "step_title": "Add the numbers",
          "code": "  return num1 + num2;",
          "desired_output": "",
          "hint": "Perform the addition of the two parameters."
        },
        {
          "step_id": 3,
          "step_title": "Close the function",
          "code": "}",
          "desired_output": "",
          "hint": "End the function definition."
        }
      ],
      "language": "JavaScript"
    }
      Now generate for {{QUESTION}}  
    """,
      "cpp": """Generate a JSON object that represents a coding question in C++. The object should include:
    - "description" give a concise explanation about the question in about 50 words. DONT MENTION ANYTHING ABOUT THE SOLUTION
    - "steps" as an array where each element is an object with the following keys:
      - "step_id" as a number indicating the step's serial number.
      - "step_title" as a string describing the step.
      - "code" as a string representing the code needed for this step.
      - "desired_output" as a string describing the expected output of the code, if any.
      - "hint" as a string providing a hint to help with the step.

    Ensure that each step's code is executable in isolation, and the final code can be constructed by combining all the steps. Include elements like function declarations, return statements, and proper use of C++ syntax.

    For example, for the question "How to implement a function to add two numbers in C++?":
    {
      "description": "Create a C++ program that takes two numbers as input and calculates their sum. The program should include proper function declaration and a main function to demonstrate the addition operation.",
      "steps": [
        {
          "step_id": 1,
          "step_title": "Include necessary headers",
          "code": "#include <iostream>",
          "desired_output": "",
          "hint": "Include the necessary headers for input and output operations."
        },
        {
          "step_id": 2,
          "step_title": "Define the function",
          "code": "int addTwoNumbers(int num1, int num2) {",
          "desired_output": "",
          "hint": "Start by defining the function with parameters for the numbers."
        },
        {
          "step_id": 3,
          "step_title": "Add the numbers and return",
          "code": "  return num1 + num2;\n}",
          "desired_output": "",
          "hint": "Perform the addition of the two parameters and return the result."
        },
        {
          "step_id": 4,
          "step_title": "Add main function",
          "code": "int main() {\n  std::cout << addTwoNumbers(5, 3) << std::endl;\n  return 0;\n}",
          "desired_output": "Prints the sum of the numbers.",
          "hint": "Complete the function and provide a main function to test it."
        }
      ],
      "language": "C++"
    }
      Now generate for {{QUESTION}}  
    """,

    "python": """Generate a JSON object that represents a coding question in Python. The object should include:
    - "description" give a concise explanation about the question in about 50 words. DONT MENTION ANYTHING ABOUT THE SOLUTION
    - "steps" as an array where each element is an object with the following keys:
      - "step_id" as a number indicating the step's serial number.
      - "step_title" as a string describing the step.
      - "code" as a string representing the code needed for this step.
      - "desired_output" as a string describing the expected output of the code, if any.
      - "hint" as a string providing a hint to help with the step.

    Ensure that each step's code is executable in isolation, and the final code can be constructed by combining all the steps. Include function definitions, return statements, and proper use of Python syntax.

    For example, for the question "How to implement a function to add two numbers in Python?":
    {
      "description": "Create a Python function that accepts two numbers as input parameters and performs addition. The program should demonstrate basic function definition and arithmetic operations.",
      "steps": [
        {
          "step_id": 1,
          "step_title": "Define the function",
          "code": "def add_two_numbers(num1, num2):",
          "desired_output": "",
          "hint": "Start by defining the function with parameters for the numbers."
        },
        {
          "step_id": 2,
          "step_title": "Add the numbers and return",
          "code": "  return num1 + num2",
          "desired_output": "",
          "hint": "Perform the addition of the two parameters and return the result."
        },
        {
          "step_id": 3,
          "step_title": "Add a test case",
          "code": "print(add_two_numbers(5, 3))",
          "desired_output": "Prints the sum of the numbers.",
          "hint": "Add a test case to check if the function works correctly."
        }
      ],
      "language": "Python"
    }
      Now generate for {{QUESTION}}""",
    }
    
    try:
        language_prompt = prompts[language]
        final_prompt = language_prompt.replace("{{QUESTION}}", question)
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant. Respond only with valid JSON."},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.7,
            max_tokens=8192
        )
        generated_code = completion.choices[0].message.content
        
        print("Raw response:", generated_code)
        
        generated_code = generated_code.strip()
        
        if generated_code.startswith("```"):
            lines = generated_code.split("\n")
            
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            generated_code = "\n".join(lines)
        
        generated_code = generated_code.strip()
        
        try:
            parsed_code = json.loads(generated_code)
            return {"code": parsed_code}
        except json.JSONDecodeError as json_error:
            print("JSON Parse Error:", str(json_error))
            print("Attempted to parse:", generated_code)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse JSON response: {str(json_error)}"
            )
    
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error generating code: {str(e)}"
        )

#Function for fetching qn description from leetcode
def leetcode_description(title_slug):
    url = "https://leetcode.com/graphql"
    
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            title
            content
            difficulty
            topicTags {
                name
            }
        }
    }
    """
    
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com"
    }

    body = {
        "query": query,
        "variables": {
            "titleSlug": title_slug
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status() 
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"LeetCode API error: {str(e)}")
    
#Function for fetching problem from id
def leetcode_problem(frontend_id):
    try:
        problems_response = requests.get("https://leetcode.com/api/problems/algorithms/")
        problems_data = problems_response.json()

        target_problem = None
        for problem in problems_data['stat_status_pairs']:
            if problem['stat']['frontend_question_id'] == frontend_id:
                target_problem = problem
                break
    
        if not target_problem:
            raise HTTPException(status_code=404, detail="Problem not found")
    
        title_slug = target_problem['stat']['question__title_slug']
        result = leetcode_description(title_slug)
        
        if isinstance(result, str):  
            raise HTTPException(status_code=500, detail=result)
            
        return result  

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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