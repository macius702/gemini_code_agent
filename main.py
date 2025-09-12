import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt


import argparse

parser= argparse.ArgumentParser(description="Use prompt and --verbose")

parser.add_argument("-v", "--verbose", action="store_true", help = "Enable verbose output")



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory."
            ),
        },
        required=["file_path"],
    ),
)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the working directory with optional arguments and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the working directory. Creates or overwrites the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write into the file."
            ),
        },
        required=["file_path", "content"],
    ),
)



available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

# Import actual implementations
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def call_function(function_call_part, verbose=False):
    args = dict(function_call_part.args or {})
    args["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {function_call_part.name}({args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name == "get_files_info":
        result = get_files_info(**args)
    elif function_call_part.name == "get_file_content":
        result = get_file_content(**args)
    elif function_call_part.name == "run_python_file":
        result = run_python_file(**args)
    elif function_call_part.name == "write_file":
        result = write_file(**args)
    else:
        raise ValueError(f"Unknown function name: {function_call_part.name}")

    return result

def main():

    args, rest = parser.parse_known_args()

    if not rest:
        print('Error: Prompt argument needed')
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])

    messages = [ types.Content(role='user', parts = [types.Part(text=user_prompt)])]

    # print(f'{messages=}')


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            )
        )

    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        result = call_function(function_call_part, verbose=args.verbose)
        if args.verbose:
            print("Result:", result)
   
    if args.verbose:
        print(f'User prompt: {user_prompt}')
        print('Prompt tokens:', response.usage_metadata.prompt_token_count)
        print('Response tokens:', response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()
