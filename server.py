from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import os
from dotenv import load_dotenv
from groq import Groq
import json
from dotenv import load_dotenv

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
    question_id: str
    language:str


#Functions:

#Function for querying LLM
def response(question, language):
    prompts = {
        "javascript": """Generate a JSON object that represents a coding question in JavaScript. The object should include:
    - "question" as a string describing the coding question.
    - "id" as a unique identifier for the question (string).
    - "steps" as an array where each element is an object with the following keys:
      - "step_id" as a number indicating the step's serial number.
      - "step_title" as a string describing the step.
      - "code" as a string representing the code needed for this step.
      - "desired_output" as a string describing the expected output of the code, if any.
      - "hint" as a string providing a hint to help with the step.
      - "keywords" as an array of objects, where each object contains:
        - "keyword" as a string representing a JavaScript keyword related to the step.
        - "description" as a string explaining the keyword's relevance or usage.

    Ensure that each step's code is executable in isolation, and the final code can be constructed by combining all the steps. Include essential elements like function definitions, return statements, and method calls.

    For example, for the question "How to implement a function to add two numbers in JavaScript?":
    {
      "question": "How to implement a function to add two numbers in JavaScript?",
      "id": "unique-id-123",
      "steps": [
        {
          "step_id": 1,
          "step_title": "Define the function",
          "code": "function addTwoNumbers(num1, num2) {",
          "desired_output": "",
          "hint": "Start by defining the function with parameters for the numbers.",
          "keywords": [
            {"keyword": "function", "description": "Used to declare a function in JavaScript."}
          ]
        },
        {
          "step_id": 2,
          "step_title": "Add the numbers",
          "code": "  return num1 + num2;",
          "desired_output": "",
          "hint": "Perform the addition of the two parameters.",
          "keywords": [
            {"keyword": "return", "description": "Used to return a value from a function."},
            {"keyword": "+", "description": "Addition operator."}
          ]
        },
        {
          "step_id": 3,
          "step_title": "Close the function",
          "code": "}",
          "desired_output": "",
          "hint": "End the function definition.",
          "keywords": [
            {"keyword": "}", "description": "Used to close a block of code."}
          ]
        }
      ],
      "language": "JavaScript"
    }
      Now generate for {{QUESTION}}  
    """,
      "cpp": """Generate a JSON object that represents a coding question in C++. The object should include:
    - "question" as a string describing the coding question.
    - "id" as a unique identifier for the question (string).
    - "steps" as an array where each element is an object with the following keys:
      - "step_id" as a number indicating the step's serial number.
      - "step_title" as a string describing the step.
      - "code" as a string representing the code needed for this step.
      - "desired_output" as a string describing the expected output of the code, if any.
      - "hint" as a string providing a hint to help with the step.
      - "keywords" as an array of objects, where each object contains:
        - "keyword" as a string representing a C++ keyword related to the step.
        - "description" as a string explaining the keyword's relevance or usage.

    Ensure that each step's code is executable in isolation, and the final code can be constructed by combining all the steps. Include elements like function declarations, return statements, and proper use of C++ syntax.

    For example, for the question "How to implement a function to add two numbers in C++?":
    {
      "question": "How to implement a function to add two numbers in C++?",
      "id": "unique-id-123",
      "steps": [
        {
          "step_id": 1,
          "step_title": "Include necessary headers",
          "code": "#include <iostream>",
          "desired_output": "",
          "hint": "Include the necessary headers for input and output operations.",
          "keywords": [
            {"keyword": "#include", "description": "Preprocessor directive to include standard libraries."}
          ]
        },
        {
          "step_id": 2,
          "step_title": "Define the function",
          "code": "int addTwoNumbers(int num1, int num2) {",
          "desired_output": "",
          "hint": "Start by defining the function with parameters for the numbers.",
          "keywords": [
            {"keyword": "int", "description": "Data type for integer values in C++."}
          ]
        },
        {
          "step_id": 3,
          "step_title": "Add the numbers and return",
          "code": "  return num1 + num2;\n}",
          "desired_output": "",
          "hint": "Perform the addition of the two parameters and return the result.",
          "keywords": [
            {"keyword": "return", "description": "Used to return a value from a function."},
            {"keyword": "+", "description": "Addition operator."}
          ]
        },
        {
          "step_id": 4,
          "step_title": "Add main function",
          "code": "int main() {\n  std::cout << addTwoNumbers(5, 3) << std::endl;\n  return 0;\n}",
          "desired_output": "Prints the sum of the numbers.",
          "hint": "Complete the function and provide a main function to test it.",
          "keywords": [
            {"keyword": "main", "description": "The entry point of a C++ program."}
          ]
        }
      ],
      "language": "C++"
    }
      Now generate for {{QUESTION}}  
    """,
      "c": """Generate a JSON object that represents a coding question in C. The object should include:
    - "question" as a string describing the coding question.
    - "id" as a unique identifier for the question (string).
    - "steps" as an array where each element is an object with the following keys:
      - "step_id" as a number indicating the step's serial number.
      - "step_title" as a string describing the step.
      - "code" as a string representing the code needed for this step.
      - "desired_output" as a string describing the expected output of the code, if any.
      - "hint" as a string providing a hint to help with the step.
      - "keywords" as an array of objects, where each object contains:
        - "keyword" as a string representing a C keyword related to the step.
        - "description" as a string explaining the keyword's relevance or usage.

    Ensure that each step's code is executable in isolation, and the final code can be constructed by combining all the steps. Include function definitions, return statements, and main function implementation.

    For example, for the question "How to implement a function to add two numbers in C?":
    {
      "question": "How to implement a function to add two numbers in C?",
      "id": "unique-id-123",
      "steps": [
        {
          "step_id": 1,
          "step_title": "Include necessary headers",
          "code": "#include <stdio.h>",
          "desired_output": "",
          "hint": "Include the necessary headers for input and output operations.",
          "keywords": [
            {"keyword": "#include", "description": "Preprocessor directive to include standard libraries."}
          ]
        },
        {
          "step_id": 2,
          "step_title": "Define the function",
          "code": "int addTwoNumbers(int num1, int num2) {",
          "desired_output": "",
          "hint": "Start by defining the function with parameters for the numbers.",
          "keywords": [
            {"keyword": "int", "description": "Data type for integer values in C."}
          ]
        },
        {
          "step_id": 3,
          "step_title": "Add the numbers and return",
          "code": "  return num1 + num2;\n}",
          "desired_output": "",
          "hint": "Perform the addition of the two parameters and return the result.",
          "keywords": [
            {"keyword": "return", "description": "Used to return a value from a function."},
            {"keyword": "+", "description": "Addition operator."}
          ]
        },
        {
          "step_id": 4,
          "step_title": "Add main function",
          "code": "int main() {\n  printf(\"%d\\n\", addTwoNumbers(5, 3));\n  return 0;\n}",
          "desired_output": "Prints the sum of the numbers.",
          "hint": "Complete the function and provide a main function to test it.",
          "keywords": [
            {"keyword": "main", "description": "The entry point of a C program."}
          ]
        }
      ],
      "language": "C"
    }
      Now generate for {{QUESTION}}  
    """,
      "java": """Generate a JSON object that represents a coding question in Java. The object should include:
    - "question" as a string describing the coding question.
    - "id" as a unique identifier for the question (string).
    - "steps" as an array where each element is an object with the following keys:
      - "step_id" as a number indicating the step's serial number.
      - "step_title" as a string describing the step.
      - "code" as a string representing the code needed for this step.
      - "desired_output" as a string describing the expected output of the code, if any.
      - "hint" as a string providing a hint to help with the step.
      - "keywords" as an array of objects, where each object contains:
        - "keyword" as a string representing a Java keyword related to the step.
        - "description" as a string explaining the keyword's relevance or usage.

    Ensure that each step's code is executable in isolation, and the final code can be constructed by combining all the steps. Include class declarations, method definitions, and proper use of Java syntax.

    For example, for the question "How to implement a function to add two numbers in Java?":
    {
      "question": "How to implement a function to add two numbers in Java?",
      "id": "unique-id-123",
      "steps": [
        {
          "step_id": 1,
          "step_title": "Define the class",
          "code": "public class Main {",
          "desired_output": "",
          "hint": "Start by defining a class.",
          "keywords": [
            {"keyword": "public", "description": "Access modifier that makes the class accessible from other classes."},
            {"keyword": "class", "description": "Keyword to define a class in Java."}
          ]
        },
        {
          "step_id": 2,
          "step_title": "Define the method",
          "code": "  public static int addTwoNumbers(int num1, int num2) {",
          "desired_output": "",
          "hint": "Define the method to add two numbers.",
          "keywords": [
            {"keyword": "public", "description": "Access modifier for the method."},
            {"keyword": "static", "description": "Keyword indicating that the method can be called without an instance."},
            {"keyword": "int", "description": "Data type for integer values in Java."}
          ]
        },
        {
          "step_id": 3,
          "step_title": "Add the numbers and return",
          "code": "    return num1 + num2;\n  }",
          "desired_output": "",
          "hint": "Perform the addition and return the result.",
          "keywords": [
            {"keyword": "return", "description": "Used to return a value from a method."},
            {"keyword": "+", "description": "Addition operator."}
          ]
        },
        {
          "step_id": 4,
          "step_title": "Close the class and add main method",
          "code": "  public static void main(String[] args) {\n    System.out.println(addTwoNumbers(5, 3));\n  }\n}",
          "desired_output": "Prints the sum of the numbers.",
          "hint": "Complete the class and add a main method to test the function.",
          "keywords": [
            {"keyword": "main", "description": "The entry point of a Java application."},
            {"keyword": "System.out.println", "description": "Used to print output to the console."}
          ]
        }
      ],
      "language": "Java"
    }
      Now generate for {{QUESTION}}  
    """,
      "python": """Generate a JSON object that represents a coding question in Python. The object should include:
    - "question" as a string describing the coding question.
    - "id" as a unique identifier for the question (string).
    - "steps" as an array where each element is an object with the following keys:
      - "step_id" as a number indicating the step's serial number.
      - "step_title" as a string describing the step.
      - "code" as a string representing the code needed for this step.
      - "desired_output" as a string describing the expected output of the code, if any.
      - "hint" as a string providing a hint to help with the step.
      - "keywords" as an array of objects, where each object contains:
        - "keyword" as a string representing a Python keyword related to the step.
        - "description" as a string explaining the keyword's relevance or usage.

    Ensure that each step's code is executable in isolation, and the final code can be constructed by combining all the steps. Include function definitions, return statements, and proper use of Python syntax.

    For example, for the question "How to implement a function to add two numbers in Python?":
    {
      "question": "How to implement a function to add two numbers in Python?",
      "id": "unique-id-123",
      "steps": [
        {
          "step_id": 1,
          "step_title": "Define the function",
          "code": "def add_two_numbers(num1, num2):",
          "desired_output": "",
          "hint": "Start by defining the function with parameters for the numbers.",
          "keywords": [
            {"keyword": "def", "description": "Keyword to define a function in Python."}
          ]
        },
        {
          "step_id": 2,
          "step_title": "Add the numbers and return",
          "code": "  return num1 + num2",
          "desired_output": "",
          "hint": "Perform the addition of the two parameters and return the result.",
          "keywords": [
            {"keyword": "return", "description": "Used to return a value from a function."},
            {"keyword": "+", "description": "Addition operator."}
          ]
        },
        {
          "step_id": 3,
          "step_title": "Add a test case",
          "code": "print(add_two_numbers(5, 3))",
          "desired_output": "Prints the sum of the numbers.",
          "hint": "Add a test case to check if the function works correctly.",
          "keywords": [
            {"keyword": "print", "description": "Function used to output data to the console."}
          ]
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


#EndPoints:

#Endpoint for text questions
@app.post('/question')
async def generate_code(request: QuestionDetails):
    return response(question=request.question, language=request.language)
        

#Endpoint for leetcode questions
@app.post('/leetcode')







#Endpoint for health check
@app.get("/health")
async def health():
    return {"200": "OK"}





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")