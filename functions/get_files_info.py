import os

def get_files_info(working_directory, directory="."):
    try:
        # Get absolute paths
        working_directory = os.path.abspath(working_directory)
        target_directory = os.path.abspath(os.path.join(working_directory, directory))

        # Check if the target_directory is inside the working_directory
        if not target_directory.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the path is a directory
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        # Build directory contents string
        items = []
        for entry in os.listdir(target_directory):
            try:
                path = os.path.join(target_directory, entry)
                is_dir = os.path.isdir(path)
                size = os.path.getsize(path)
                items.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as inner_e:
                return f"Error: {str(inner_e)}"
        return "\n".join(items)

    except Exception as e:
        return f"Error: {str(e)}"
