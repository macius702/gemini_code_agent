import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

import argparse

parser= argparse.ArgumentParser(description="Use prompt and --verbose")

parser.add_argument("-v", "--verbose", action="store_true", help = "Enable verbose output")


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
        model='gemini-2.0-flash-001', contents=messages)
    print(response.text)
    if args.verbose:
        print(f'User prompt: {user_prompt}')
        print('Prompt tokens:', response.usage_metadata.prompt_token_count)
        print('Response tokens:', response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()
