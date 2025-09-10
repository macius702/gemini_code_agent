# tests.py
# Manual test runner for get_file_content

from functions.get_file_content import get_file_content

def print_block(title: str, content: str):
    print(title)
    if isinstance(content, str) and content.startswith("Error:"):
        print(f"    {content}")
    else:
        # Show a short preview to avoid flooding stdout
        preview = (content[:2200] + ("..." if len(content) > 200 else "")).replace("\n", "\\n")
        print(f" {preview}")
    print()

if __name__ == "__main__":
    header = 'get_file_content("calculator", "main.py"):'
    print(header)
    res = get_file_content("calculator", "main.py")
    print_block("Result for main.py:", res)

    header = 'get_file_content("calculator", "pkg/calculator.py"):'
    print(header)
    res = get_file_content("calculator", "pkg/calculator.py")
    print_block("Result for pkg/calculator.py:", res)

    header = 'get_file_content("calculator", "/bin/cat"):'
    print(header)
    res = get_file_content("calculator", "/bin/cat")
    print_block("Result for /bin/cat:", res)

    header = 'get_file_content("calculator", "pkg/does_not_exist.py"):'
    print(header)
    res = get_file_content("calculator", "pkg/does_not_exist.py")
    print_block("Result for missing file:", res)
