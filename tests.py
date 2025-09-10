from functions.run_python_file import run_python_file


def print_result(title: str, result: str):
    print(title)
    if isinstance(result, str):
        print(result)
    else:
        print(str(result))
    print()


if __name__ == "__main__":
    # 1) run calculator main.py with no args
    header = 'run_python_file("calculator", "main.py"):'
    print(header)
    res = run_python_file("calculator", "main.py")
    print_result("Result for main.py:", res)

    # 2) run calculator main.py with expression arg
    header = 'run_python_file("calculator", "main.py", ["3 + 5"]):'
    print(header)
    res = run_python_file("calculator", "main.py", ["3 + 5"])
    print_result("Result for main.py with arg:", res)

    # 3) run tests.py itself
    header = 'run_python_file("calculator", "tests.py"):'
    print(header)
    res = run_python_file("calculator", "tests.py")
    print_result("Result for tests.py:", res)

    # 4) attempt to run outside directory
    header = 'run_python_file("calculator", "../main.py"):'
    print(header)
    res = run_python_file("calculator", "../main.py")
    print_result("Result for ../main.py:", res)

    # 5) attempt to run nonexistent file
    header = 'run_python_file("calculator", "nonexistent.py"):'
    print(header)
    res = run_python_file("calculator", "nonexistent.py")
    print_result("Result for nonexistent.py:", res)
