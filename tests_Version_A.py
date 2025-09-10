# tests.py
# Manual test for get_file_content truncation

from functions.get_file_content import get_file_content

def print_block(title: str, content: str):
    print(title)
    if content.startswith("Error:"):
        print(f"    {content}")
    else:
        # print beginning and ending to keep console tidy but informative
        beginning = content[:200].replace("\n", "\\n")
        ending = content[-200:].replace("\n", "\\n") if len(content) > 200 else ""
        print(f" [BEGIN] {beginning}...")
        if ending:
            print(f" [END] ...{ending}")

    print()

if __name__ == "__main__":
    header = 'get_file_content("calculator", "lorem.txt"):'
    print(header)
    res = get_file_content("calculator", "lorem.txt")
    print_block("Result for lorem.txt:", res)
