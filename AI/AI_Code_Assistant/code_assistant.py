from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

load_dotenv(r"C:\Users\prann\OneDrive\เอกสาร\Projects\Essentials\API_KEYS\GROQ_API.env")
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.5,
    groq_api_key=api_key,
)

prompt = PromptTemplate(
    input_variables=[
        "programming_language",
        "code",
        "description",
        "output_format",
        "task_type"
    ],
    template="""
    You are a highly skilled programming expert. Based on the provided details, your task is to perform the requested action in {programming_language}:

    1. *Programming Language:*
       - {programming_language}

    2. *Task Type:*
       - {task_type}

    3. *Code (if applicable):*
       - {code}

    4. *User Request (Description):*
       - {description}

    5. *Desired Output Format:*
       - {output_format}

    *Guidelines:*
    - If the task type is *"Generate Code"*:
      - Generate a code snippet based on the description provided by the user. 
      - The description will specify what the code should do (e.g., "Generate a Java function to find the maximum element in an array").
      - Ensure that the generated code follows best practices, is functional, and meets the described requirement.

    - If the task type is *"Explain Code"*:
      - Provide an explanation for the given code, breaking it down into its components and functionality.
      
    - If the task type is *"Debug Code"*:
      - Identify issues in the provided code, explain the problems, and suggest fixes.

    - If the task type is *"Optimize Code"*:
      - Suggest improvements for the provided code in terms of performance, readability, or efficiency.

    - Tailor the output based on the desired format:
      - Plain Text: Provide a continuous explanation or code in natural language.
      - Step-by-Step: Break down the task or explanation in a sequential manner.
      - Bullet Points: Summarize the key points concisely.

    *Important:*
    - If the user is generating code and the code field is empty, generate the code based on the description.
    - Ensure that the output is relevant, clear, and meets the user's requirements.
    """
)

chain = prompt | llm

def process_code_task(programming_language, task_type, code=None, description=None, output_format=None):
    if not programming_language or not task_type:
        raise ValueError("Programming language and task type are required")
    
    if task_type == "Generate Code" and not code and not description:
        raise ValueError("For Generate Code task, either code or description must be provided")

    result = chain.invoke({
        "programming_language": programming_language,
        "code": code if code else "No code provided",
        "description": description if description else "No description provided",
        "output_format": output_format if output_format else "Plain Text",
        "task_type": task_type
    })
    
    return result.content

def main():
    try:
        programming_language = input("Enter the programming language: ")
        code = input("Enter the code (optional): ").strip() or None
        description = input("Enter a description of the task: ").strip() or None
        output_format = input("Enter the desired output format (Plain Text/Step-by-Step/Bullet Points): ").strip() or None
        task_type = input("Enter the task type (Generate Code/Explain Code/Debug Code/Optimize Code): ")

        result = process_code_task(programming_language, task_type, code, description, output_format)
        print(result)
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()