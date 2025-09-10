from functions.write_file import write_file


def print_result(title: str, result: str):
    print(title)
    if isinstance(result, str) and result.startswith("Error:"):
        print(f"    {result}")
    else:
        print(f" {result}")
    print()


if __name__ == "__main__":
    # 1) overwrite lorem.txt
    header = 'write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum"):'
    print(header)
    res = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print_result("Result for lorem.txt:", res)

    # 2) write into pkg/morelorem.txt
    header = 'write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"):'
    print(header)
    res = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print_result("Result for pkg/morelorem.txt:", res)

    # 3) attempt to write outside permitted dir
    header = 'write_file("calculator", "/tmp/temp.txt", "this should not be allowed"):'
    print(header)
    res = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print_result("Result for /tmp/temp.txt:", res)
