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

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

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
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
   
    if args.verbose:
        print(f'User prompt: {user_prompt}')
        print('Prompt tokens:', response.usage_metadata.prompt_token_count)
        print('Response tokens:', response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()
