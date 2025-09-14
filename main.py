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

    function_name = function_call_part.name

    try:
        if function_name == "get_files_info":
            function_result = get_files_info(**args)
        elif function_name == "get_file_content":
            function_result = get_file_content(**args)
        elif function_name == "run_python_file":
            function_result = run_python_file(**args)
        elif function_name == "write_file":
            function_result = write_file(**args)
        else:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": str(e)},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

def main():
    args, rest = parser.parse_known_args()

    if not rest:
        print('Error: Prompt argument needed')
        sys.exit(1)

    user_prompt = " ".join(rest)

    # Initialize conversation with user's message
    messages = [types.Content(role='user', parts=[types.Part(text=user_prompt)])]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    max_steps = 20
    step = 0

    while step < max_steps:
        step += 1
        if args.verbose:
            print(f"\n--- Agent step {step} ---")

        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )

            # In verbose mode, show the model's rationale/explanation text for this step
            if args.verbose:
                try:
                    rationale_lines = []
                    for cand in (getattr(response, "candidates", None) or []):
                        content = getattr(cand, "content", None)
                        if not content:
                            continue
                        for part in getattr(content, "parts", []) or []:
                            txt = getattr(part, "text", None)
                            if txt:
                                rationale_lines.append(txt)
                    if rationale_lines:
                        print("Model rationale:")
                        for line in rationale_lines:
                            print(line)
                except Exception:
                    # Best effort only; ignore any SDK shape differences
                    pass

            # Append model candidates to the conversation so the next call has full context
            try:
                for cand in (response.candidates or []):
                    if getattr(cand, "content", None):
                        messages.append(cand.content)
            except Exception:
                # If the SDK shape differs, fall back to the top-level content if present
                if getattr(response, "content", None):
                    messages.append(response.content)

            # Prefer executing function calls if present (even if text also exists)
            function_calls = list(getattr(response, "function_calls", []) or [])
            for function_call_part in function_calls:
                result_content = call_function(function_call_part, verbose=args.verbose)

                if not result_content.parts or not hasattr(result_content.parts[0], "function_response"):
                    raise RuntimeError("Fatal: function call did not return a function_response")

                function_response = result_content.parts[0].function_response.response

                if args.verbose:
                    print("Function call result:", function_response)

                # Feed tool result back into the conversation as a user message so the model can continue
                messages.append(
                    types.Content(
                        role='user',
                        parts=[
                            types.Part.from_function_response(
                                name=function_call_part.name,
                                response=function_response,
                            )
                        ],
                )
                )

            # If there were any function calls, continue to next iteration to let the model react
            if function_calls:
                continue

            # Otherwise, if model produced final text, print and stop looping
            final_text = getattr(response, "text", "") or ""
            if final_text:
                print(final_text)
                # Token usage (verbose only)
                if args.verbose and getattr(response, "usage_metadata", None):
                    print('Prompt tokens:', response.usage_metadata.prompt_token_count)
                    print('Response tokens:', response.usage_metadata.candidates_token_count)
                break

            # If there were no function calls and no text, nothing else to do
            if not getattr(response, "function_calls", None) and not final_text:
                if args.verbose:
                    print("No function calls or final text; stopping.")
                break

        except Exception as e:
            print(f"Error: {e}")
            break

    # If we get here, we hit the max step limit
    if args.verbose:
        print(f"Reached max steps ({max_steps}) without a final answer.")

if __name__ == "__main__":
    main()
