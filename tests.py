# tests.py
# Example manual test runner for get_files_info
# If your function is inside a subdirectory, import it like this:
# from DIRNAME.FILENAME import FUNCTION_NAME
# For example, if you have utils/files_info.py exporting get_files_info:
# from utils.files_info import get_files_info



# Fallback import patterns (adjust to your project layout)
try:
    # Try common subdirectory layout first
    from functions.get_files_info import get_files_info  # noqa: F401
except Exception:
    try:
        # Try same-directory module name
        from get_files_info import get_files_info  # noqa: F401
    except Exception:
        try:
            # Try the code cell/document name if used
            from files_info_checker import get_files_info  # noqa: F401
        except Exception:  # As a last resort, define a placeholder
            def get_files_info(*args, **kwargs):
                return 'Error: get_files_info not found. Ensure the function is importable.'


def print_block(header: str, result: str):
    print(header)
    print(result)


def print_result(title: str, result: str):
    print(title)
    if isinstance(result, str) and result.startswith("Error:"):
        # Indent the error line by 4 spaces as per example
        print(f"    {result}")
    else:
        # Each entry should be on its own line and begin with a single leading space before '-'
        lines = result.splitlines() if isinstance(result, str) else []
        for line in lines:
            # Ensure exactly one leading space before '-'
            line = line.strip()
            if line.startswith('-'):
                print(f" {line}")
            elif line.startswith(' -'):
                print(line)
            else:
                print(f" - {line}")
    print()  # blank line between blocks


if __name__ == "__main__":
    # 1) Current directory
    header = 'get_files_info("calculator", "."):'
    print(header)
    res = get_files_info("calculator", ".")
    print_result("Result for current directory:", res)

    # 2) pkg directory
    header = 'get_files_info("calculator", "pkg"):'
    print(header)
    res = get_files_info("calculator", "pkg")
    print_result("Result for 'pkg' directory:", res)

    # 3) absolute /bin (should error)
    header = 'get_files_info("calculator", "/bin"):'
    print(header)
    res = get_files_info("calculator", "/bin")
    print_result("Result for '/bin' directory:", res)

    # 4) parent directory via relative path (should error)
    header = 'get_files_info("calculator", "../"):'
    print(header)
    res = get_files_info("calculator", "../")
    print_result("Result for '../' directory:", res)
