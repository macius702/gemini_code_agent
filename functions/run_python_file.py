import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(wd_abs, file_path))

        # Resolve symlinks for security
        wd_real = os.path.realpath(wd_abs)
        target_real = os.path.realpath(target_abs)

        try:
            if os.path.commonpath([wd_real, target_real]) != wd_real:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        except Exception as e:
            return f"Error: {e}"

        # Ensure file exists
        if not os.path.exists(target_real):
            return f'Error: File "{file_path}" not found.'

        # Ensure it's a Python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        try:
            completed = subprocess.run(
                ["python", target_real] + list(args),
                cwd=wd_real,
                capture_output=True,
                text=True,
                timeout=30,
            )

            output_parts = []
            if completed.stdout:
                output_parts.append("STDOUT:\n" + completed.stdout.strip())
            if completed.stderr:
                output_parts.append("STDERR:\n" + completed.stderr.strip())

            if completed.returncode != 0:
                output_parts.append(f"Process exited with code {completed.returncode}")

            if not output_parts:
                return "No output produced."

            return "\n".join(output_parts)

        except Exception as e:
            return f"Error: executing Python file: {e}"

    except Exception as e:
        return f"Error: {e}"