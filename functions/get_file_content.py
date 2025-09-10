import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    """
    Read a file within `working_directory` and return its contents as a string.

    Rules:
    - If `file_path` is outside `working_directory`, return:
      f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    - If `file_path` is not a regular file, return:
      f'Error: File not found or is not a regular file: "{file_path}"'
    - Truncate results to MAX_CHARS and append:
      [...File "{file_path}" truncated at MAX_CHARS characters]
    - Catch any stdlib errors and return them as strings prefixed with "Error:".
    """
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(wd_abs, file_path))

        # Resolve symlinks and do a robust containment check
        wd_real = os.path.realpath(wd_abs)
        target_real = os.path.realpath(target_abs)

        try:
            if os.path.commonpath([wd_real, target_real]) != wd_real:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        except Exception as e:
            return f"Error: {e}"

        # Ensure it's a regular file
        if not os.path.isfile(target_real):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read up to MAX_CHARS + 1 to detect truncation cleanly
        try:
            with open(target_real, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(MAX_CHARS + 1)
        except Exception as e:
            return f"Error: {e}"

        if len(content) > MAX_CHARS:
            result = content[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return result
        return content

    except Exception as e:
        return f"Error: {e}"