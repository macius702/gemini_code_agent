import os

def write_file(working_directory, file_path, content):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(wd_abs, file_path))

        # Resolve symlinks for security
        wd_real = os.path.realpath(wd_abs)
        target_real = os.path.realpath(target_abs)

        try:
            if os.path.commonpath([wd_real, target_real]) != wd_real:
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        except Exception as e:
            return f"Error: {e}"

        # Ensure parent directories exist
        os.makedirs(os.path.dirname(target_real), exist_ok=True)

        # Write content to the file (create or overwrite)
        try:
            with open(target_real, "w", encoding="utf-8", errors="replace") as f:
                f.write(content)
        except Exception as e:
            return f"Error: {e}"

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
