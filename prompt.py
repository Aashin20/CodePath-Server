from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import os
from dotenv import load_dotenv
from groq import Groq
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["Questions"]
collection = db["Elab_Questions"]


def get_latest_qn():
    try:
        latest_doc = collection.find_one(
            {},
            sort=[("timestamp", -1)]
        )
        if latest_doc and "question" in latest_doc:
            return str(latest_doc["question"])
        raise HTTPException("No Questions Found")
    except Exception as e:
        print(f"Error fetching latest question: {e}")


def response(question, language):
    prompts = {
        "javascript": """Generate a JSON object that represents a coding question in JavaScript. The object should include:
    - "description" give a concise explanation about the question in about 50 words. DONT MENTION ANYTHING ABOUT THE SOLUTION
    - "steps" as an array where each element is an object with the following keys:
      - "completed" a integer value which is 0 for the first step and -1 for all other steps
      - "step_title" as a string describing the step.
      - "code" as a string representing the code needed for this step.
      - "desired_output" as a string describing the expected output of the code, if any.
      - "hint" as a string providing a hint to help with the step.

    Ensure that each step is indepth, detailed and code is executable in isolation, and the final code can be constructed by combining all the steps. Atleast create 5 steps. Include essential elements like function definitions, return statements, and method calls.

    For example, for the question "How to implement a function to add two numbers in JavaScript?":
    {
      "description": "Create a function that takes two numbers as input parameters and returns their sum. This is a basic mathematical operation implemented as a reusable function.",
      "steps": [
        {
          "completed":0,
          "step_title": "Define the function",
          "code": "function addTwoNumbers(num1, num2) {",
          "desired_output": "",
          "hint": "Start by defining the function with parameters for the numbers."
        },
        {
          "completed":-1,
          "step_title": "Add the numbers",
          "code": "  return num1 + num2;",
          "desired_output": "",
          "hint": "Perform the addition of the two parameters."
        },
        {
          "completed":-1,
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
      - "completed" a integer value which is 0 for the first step and -1 for all other steps
      - "step_title" as a string describing the step.
      - "code" as a string representing the code needed for this step.
      - "desired_output" as a string describing the expected output of the code, if any.
      - "hint" as a string providing a hint to help with the step.


    Ensure that each step is indepth, detailed and code is executable in isolation, and the final code can be constructed by combining all the steps. Atleast create more than 5 steps depending on complexity. Include essential elements like function definitions, return statements, and method calls.

    For example, for the question "How to implement a function to add two numbers in C++?":
    {
      "description": "Create a C++ program that takes two numbers as input and calculates their sum. The program should include proper function declaration and a main function to demonstrate the addition operation.",
      "steps": [
        {
          "completed":0,
          "step_title": "Include necessary headers",
          "code": "#include <iostream>",
          "desired_output": "",
          "hint": "Include the necessary headers for input and output operations."
        },
        {
          "completed":-1,
          "step_title": "Define the function",
          "code": "int addTwoNumbers(int num1, int num2) {",
          "desired_output": "",
          "hint": "Start by defining the function with parameters for the numbers."
        },
        {
          "completed":-1,
          "step_title": "Add the numbers and return",
          "code": "  return num1 + num2;\n}",
          "desired_output": "",
          "hint": "Perform the addition of the two parameters and return the result."
        },
        {
          "completed":-1,
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
      - "completed" a integer value which is 0 for the first step and -1 for all other steps
      - "step_title" as a string describing the step.
      - "code" as a string representing the code needed for this step.
      - "desired_output" as a string describing the expected output of the code, if any.
      - "hint" as a string providing a hint to help with the step.


    Ensure that each step is indepth, detailed and code is executable in isolation, and the final code can be constructed by combining all the steps. Atleast create 5 steps. Include essential elements like function definitions, return statements, and method calls.

    For example, for the question "How to implement a function to add two numbers in Python?":
    {
      "description": "Create a Python function that accepts two numbers as input parameters and performs addition. The program should demonstrate basic function definition and arithmetic operations.",
      "steps": [
        {
          "completed":0,
          "step_title": "Define the function",
          "code": "def add_two_numbers(num1, num2):",
          "desired_output": "",
          "hint": "Start by defining the function with parameters for the numbers."
        },
        {
          "completed":-1,
          "step_title": "Add the numbers and return",
          "code": "  return num1 + num2",
          "desired_output": "",
          "hint": "Perform the addition of the two parameters and return the result."
        },
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


def evaluate(steps, language, code):
    try:

        steps_array = json.loads(steps)

        prompt = f"""Here is a NEW coding exercise to evaluate (ignore any previous exercises):

Language: {language}
steps: {steps}

User's Code:
{code}

Please evaluate ONLY THIS specific code submission for the steps in the specified language and return feedback in the following structured JSON format:

{{
  "feedback": "Provide detailed feedback about the correctness and quality of the user's code, including any issues related to logic, syntax, or code structure.",
  "success": "If users code feedback is positive,ie success then complete=1 else complete=0"
}}

The evaluation should consider:
1. The programming language and its conventions.
2. Syntax correctness and adherence to the language's rules.
3. The logic and overall structure of the code provided by the user.
4. Do not mind about variable names as it can be anything. Just evaluate the logic.

Return {steps} as it is after adding the above JSON and updating the completed value. DO NOT ADD OR REMOVE ANY STEPS
Note: Evaluate the user's code against all steps and mark each step as:
1: completed step
0: current step (partially complete or in progress)
-1: upcoming step (not started)

"""
        return prompt
    except Exception as e:
        raise Exception(f"Error in evaluate function: {str(e)}")

def send_evaluation(steps, language, code):
    try:
        evaluation_prompt = evaluate(steps, language, code)
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a code evaluation assistant. Return only a single valid JSON object with feedback, complete status, and steps. No additional text or formatting."},
                {"role": "user", "content": evaluation_prompt}
            ],
            temperature=0.7,
            max_tokens=8192,
        )
        evaluation_response = completion.choices[0].message.content

        print("Raw evaluation response:", evaluation_response)

        # Clean up the response
        evaluation_response = evaluation_response.strip()

      
        if evaluation_response.startswith("```json"):
            evaluation_response = evaluation_response[7:]
        elif evaluation_response.startswith("```"):
            evaluation_response = evaluation_response[3:]
        if evaluation_response.endswith("```"):
            evaluation_response = evaluation_response[:-3]

        evaluation_response = evaluation_response.strip()

        try:
           
            start = evaluation_response.find('{')
            end = evaluation_response.rindex('}') + 1
            if start != -1 and end != -1:
                evaluation_response = evaluation_response[start:end]

            parsed_evaluation = json.loads(evaluation_response)

         
            final_response = {
                "feedback": parsed_evaluation.get("feedback", ""),
                "complete": parsed_evaluation.get("complete", 0),
                "steps": parsed_evaluation.get("steps", json.loads(steps))
            }

            return final_response

        except json.JSONDecodeError as json_error:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse evaluation response: {str(json_error)}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in send_evaluation: {str(e)}"
        )