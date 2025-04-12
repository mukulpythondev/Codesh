import os
import subprocess

# Global variable to track current working directory
current_working_directory = os.getcwd()

# ---------------------------
# File Operations Functions
# ---------------------------

def create_file(file_path: str, content: str = "") -> str:
    """
    Create a new file with provided content.
    """
    global current_working_directory
    try:
        abs_file_path = os.path.join(current_working_directory, file_path)
        # Create directory if it doesn't exist
        directory = os.path.dirname(abs_file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        with open(abs_file_path, 'w') as file:
            file.write(content)
        return f"File '{file_path}' created successfully."
    except Exception as e:
        return f"Error creating file: {str(e)}"

def read_file(file_path: str) -> str:
    """
    Read the contents of a file.
    """
    global current_working_directory
    try:
        abs_file_path = os.path.join(current_working_directory, file_path)
        if not os.path.exists(abs_file_path):
            return f"Error: File '{file_path}' does not exist."
        with open(abs_file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

def update_file(file_path: str, content: str) -> str:
    """
    Update the contents of an existing file.
    """
    global current_working_directory
    try:
        abs_file_path = os.path.join(current_working_directory, file_path)
        if not os.path.exists(abs_file_path):
            return f"Error: File '{file_path}' does not exist."
        with open(abs_file_path, 'w') as file:
            file.write(content)
        return f"File '{file_path}' updated successfully."
    except Exception as e:
        return f"Error updating file: {str(e)}"

def list_directory(directory_path: str = ".") -> str:
    """
    List contents of a directory.
    """
    global current_working_directory
    try:
        abs_dir_path = os.path.join(current_working_directory, directory_path)
        if not os.path.exists(abs_dir_path):
            return f"Error: Directory '{directory_path}' does not exist."
        contents = os.listdir(abs_dir_path)
        if not contents:
            return f"Directory '{directory_path}' is empty."
        result = f"Contents of '{directory_path}':\n"
        for item in contents:
            full_path = os.path.join(abs_dir_path, item)
            if os.path.isdir(full_path):
                result += f"📁 {item}/\n"
            else:
                result += f"📄 {item}\n"
        return result
    except Exception as e:
        return f"Error listing directory: {str(e)}"

def create_directory(directory_path: str) -> str:
    """
    Create a new directory.
    """
    global current_working_directory
    try:
        abs_dir_path = os.path.join(current_working_directory, directory_path)
        if os.path.exists(abs_dir_path):
            return f"Error: Directory '{directory_path}' already exists."
        os.makedirs(abs_dir_path)
        return f"Directory '{directory_path}' created successfully."
    except Exception as e:
        return f"Error creating directory: {str(e)}"

def change_directory(directory_path: str) -> str:
    """
    Change the current working directory.
    """
    global current_working_directory
    try:
        target_dir = os.path.join(current_working_directory, directory_path) \
            if not os.path.isabs(directory_path) else directory_path
        if not os.path.exists(target_dir):
            return f"Error: Directory '{directory_path}' does not exist."
        if not os.path.isdir(target_dir):
            return f"Error: '{directory_path}' is not a directory."
        current_working_directory = os.path.abspath(target_dir)
        return f"Changed directory to: {current_working_directory}"
    except Exception as e:
        return f"Error changing directory: {str(e)}"

def get_current_directory() -> str:
    """
    Get the current working directory.
    """
    global current_working_directory
    return f"Current directory: {current_working_directory}"

# ----------------------------------
# CLI Automation & Tool Execution
# ----------------------------------

def create_project_using_cli(project_info: dict, project_path: str) -> str:
    """
    Create a project using CLI commands (such as 'npm create vite@latest') with automated handling.
    """
    global current_working_directory
    results = {
        "success": True,
        "commands_executed": [],
        "output": [],
        "errors": []
    }
    
    try:
        # Create or navigate to project directory
        project_abs_path = os.path.join(current_working_directory, project_path)
        if not os.path.exists(project_abs_path):
            os.makedirs(project_abs_path)
        
        old_dir = current_working_directory
        current_working_directory = os.path.abspath(project_abs_path)
        
        # Define CLI templates for common tools
        cli_templates = {
            "vite": {
                "command": f"npm create vite@latest {project_info.get('project_type', 'my-app')} -- --template react",
                "post": [
                    f"cd {project_info.get('project_type', 'my-app')}",
                    "npm install",
                    "npm install -D tailwindcss postcss autoprefixer",
                    "npx tailwindcss init -p"
                ]
            },
            "create-react-app": {
                "command": f"npx create-react-app {project_info.get('project_type', 'my-app')} --template typescript",
                "post": [f"cd {project_info.get('project_type', 'my-app')}"]
            },
            "next": {
                "command": f"npx create-next-app@latest {project_info.get('project_type', 'my-app')} --ts --app --tailwind --eslint --src-dir --import-alias '@/*'",
                "post": [f"cd {project_info.get('project_type', 'my-app')}"]
            },
            "nuxt": {
                "command": f"npx nuxi init {project_info.get('project_type', 'my-app')}",
                "post": [
                    f"cd {project_info.get('project_type', 'my-app')}",
                    "npm install"
                ]
            }
        }
        
        # For simplicity, choose a template based on project type if available.
        tool_key = project_info.get("project_type", "vite").lower()
        steps = cli_templates.get(tool_key)
        if not steps:
            return f"Tool '{tool_key}' is not yet supported for automation."
        
        # Execute the primary CLI command.
        command = steps["command"]
        # Append non-interactive flags if they are missing.
        if "vite" in command and "--template" not in command:
            command = f"{command} --template react"
        if "--yes" not in command and "-y" not in command:
            command = f"{command} --yes"
        
        print(f"Executing command: {command}")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=current_working_directory,
                capture_output=True, 
                text=True,
                input="yes\n",
                timeout=300
            )
        except subprocess.TimeoutExpired:
            results["errors"].append(f"Command timed out: {command}")
            return f"Timeout during execution."
        
        if result.stdout:
            results["output"].append(result.stdout)
        if result.stderr and "npm WARN" not in result.stderr:
            results["errors"].append(result.stderr)
        
        # Execute any post-commands.
        for cmd in steps.get("post", []):
            print(f"Executing: {cmd}")
            subprocess.run(cmd, shell=True)
        
        current_working_directory = old_dir
        
        return f"Project created successfully in '{project_path}' using CLI commands. Details: {results}"
    except Exception as e:
        current_working_directory = old_dir
        return f"Error creating project using CLI: {str(e)}"

def process_function_input(function_name: str, input_data):
    """
    Process the function input based on its type and call the corresponding tool.
    """
    # If input_data is a dict, pass as keyword arguments; else, as a single argument.
    from app.executor import available_tools  # Import our tool registry
    if isinstance(input_data, dict):
        return available_tools[function_name]["fn"](**input_data)
    else:
        return available_tools[function_name]["fn"](input_data)

# ----------------------------------
# Tool Registry: Map tool names to functions
# ----------------------------------
from app.gpt_service import (
    generate_code, detect_project_type, generate_project,
    explain_code, improve_code, generate_test
)

available_tools = {
    "create_file": {
        "fn": create_file,
        "description": "Creates a new file with content. Parameters: file_path, content."
    },
    "read_file": {
        "fn": read_file,
        "description": "Reads and returns the contents of a file. Parameters: file_path."
    },
    "update_file": {
        "fn": update_file,
        "description": "Updates the contents of an existing file. Parameters: file_path, content."
    },
    "list_directory": {
        "fn": list_directory,
        "description": "Lists the contents of a directory. Parameters: directory_path (optional, defaults to current directory)."
    },
    "create_directory": {
        "fn": create_directory,
        "description": "Creates a new directory. Parameters: directory_path."
    },
    "change_directory": {
        "fn": change_directory,
        "description": "Changes the current working directory. Parameters: directory_path."
    },
    "get_current_directory": {
        "fn": get_current_directory,
        "description": "Gets the current working directory."
    },
    "generate_code": {
        "fn": generate_code,
        "description": "Generates code based on the provided prompt and language. Parameters: prompt, language (optional, defaults to python)."
    },
    "generate_project": {
        "fn": generate_project,
        "description": "Generates a complete project structure based on the description. Parameters: project_description, project_path (optional)."
    },
    "explain_code": {
        "fn": explain_code,
        "description": "Provides an explanation for the given code. Parameters: code."
    },
    "improve_code": {
        "fn": improve_code,
        "description": "Improves the given code based on the improvement prompt. Parameters: code, improvement_prompt (optional)."
    },
    "generate_test": {
        "fn": generate_test,
        "description": "Generates tests for the given code. Parameters: code, test_framework (optional, defaults to pytest)."
    }
}
