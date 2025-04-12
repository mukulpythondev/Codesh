import json
import os
import subprocess
from typing import Dict, Any, List, Union
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Keep track of current working directory
current_working_directory = os.getcwd()

def create_file(file_path: str, content: str = "") -> str:
    """
    Create a new file with provided content.
    """
    global current_working_directory
    try:
        # Convert relative path to absolute path
        abs_file_path = os.path.join(current_working_directory, file_path)
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(abs_file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Create the file with content
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
        # Convert relative path to absolute path
        abs_file_path = os.path.join(current_working_directory, file_path)
        
        # Check if file exists
        if not os.path.exists(abs_file_path):
            return f"Error: File '{file_path}' does not exist."
        
        # Read the file
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
        # Convert relative path to absolute path
        abs_file_path = os.path.join(current_working_directory, file_path)
        
        # Check if file exists
        if not os.path.exists(abs_file_path):
            return f"Error: File '{file_path}' does not exist."
        
        # Update the file
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
        # Convert relative path to absolute path
        abs_dir_path = os.path.join(current_working_directory, directory_path)
        
        # Check if directory exists
        if not os.path.exists(abs_dir_path):
            return f"Error: Directory '{directory_path}' does not exist."
        
        # List directory contents
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
        # Convert relative path to absolute path
        abs_dir_path = os.path.join(current_working_directory, directory_path)
        
        # Check if directory already exists
        if os.path.exists(abs_dir_path):
            return f"Error: Directory '{directory_path}' already exists."
        
        # Create the directory
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
        # Convert relative path to absolute path if not already absolute
        if not os.path.isabs(directory_path):
            target_dir = os.path.join(current_working_directory, directory_path)
        else:
            target_dir = directory_path
        
        # Check if directory exists
        if not os.path.exists(target_dir):
            return f"Error: Directory '{directory_path}' does not exist."
        
        # Check if it's a directory
        if not os.path.isdir(target_dir):
            return f"Error: '{directory_path}' is not a directory."
        
        # Change directory
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

def generate_code(prompt: str, language: str = "python") -> str:
    """
    Generate code based on the provided prompt and language.
    """
    try:
        code_prompt = f"Generate {language} code for: {prompt}\n\nOnly provide the code without any explanations or markdown formatting."
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": code_prompt}]
        )
        
        # Extract code from response
        generated_code = response.choices[0].message.content.strip()
        
        return generated_code
    except Exception as e:
        return f"Error generating code: {str(e)}"

def detect_project_type(project_description: str) -> str:
    """
    Detect the project type from the description to determine if CLI commands should be used.
    """
    try:
        prompt = f"""
        Based on this project description, determine what type of project it is and how it should be created.
        Project description: "{project_description}"
        
        Return a JSON object with the following structure:
        {{
            "project_type": "react|vue|angular|nextjs|nuxt|express|flask|django|...",
            "use_cli": true|false,
            "cli_commands": ["command 1", "command 2", ...] if use_cli is true,
            "package_manager": "npm|yarn|pnpm",
        }}
        
        Only provide the JSON without any explanations or additional text.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]
        )
        
        project_info = json.loads(response.choices[0].message.content)
        return project_info
    except Exception as e:
        return {"project_type": "unknown", "use_cli": False, "error": str(e)}

def create_project_using_cli(tool_name, project_name, additional_options=None):

    # Set up common CLI templates and flags
    cli_templates = {
        "vite": {
            "command": f"npm create vite@latest {project_name} -- --template react",
            "post": [
                f"cd {project_name}",
                "npm install",
                "npm install -D tailwindcss postcss autoprefixer",
                "npx tailwindcss init -p"
            ]
        },
        "create-react-app": {
            "command": f"npx create-react-app {project_name} --template typescript",
            "post": [f"cd {project_name}"]
        },
        "next": {
            "command": f"npx create-next-app@latest {project_name} --ts --app --tailwind --eslint --src-dir --import-alias '@/*'",
            "post": [f"cd {project_name}"]
        },
        "nuxt": {
            "command": f"npx nuxi init {project_name}",
            "post": [
                f"cd {project_name}",
                "npm install"
            ]
        },
    
    }

    tool_key = tool_name.lower()
    if tool_key not in cli_templates:
        print(f"Tool '{tool_name}' is not yet supported for automation.")
        return

    steps = cli_templates[tool_key]

    if "expect_script" in steps:
        script_path = "temp_script.exp"
        with open(script_path, "w") as f:
            f.write(steps["expect_script"])
        subprocess.run(["expect", script_path])
        os.remove(script_path)
    else:
        print(f"Running: {steps['command']}")
        subprocess.run(steps["command"], shell=True)

    for cmd in steps.get("post", []):
        print(f"Running: {cmd}")
        subprocess.run(cmd, shell=True)

def generate_project(project_description: str, project_path: str = ".") -> str:
    """
    Generates a complete project structure based on the description.
    Now with support for using CLI commands for frameworks like React, Vue, etc.
    """
    global current_working_directory
    try:
        # Detect project type to determine if CLI commands should be used
        project_info = detect_project_type(project_description)
        
        # If we should use CLI commands (like npm create vite@latest)
        if isinstance(project_info, dict) and project_info.get("use_cli", False):
            return create_project_using_cli(project_info, project_path)
        
        # Otherwise, fall back to the manual file creation approach
        # Create project directory if it doesn't exist
        if not os.path.exists(os.path.join(current_working_directory, project_path)):
            os.makedirs(os.path.join(current_working_directory, project_path))
            
        # Generate project structure based on description
        prompt = f"""
        For the project described as: "{project_description}"
        
        1. Create a detailed project structure with necessary files
        2. For each file, provide the complete code content
        3. Include appropriate configuration files
        4. Format the response as a JSON object with the following structure:
        
        {{
            "project_name": "name of the project",
            "description": "brief description of what the project does",
            "files": [
                {{
                    "path": "relative/path/to/file.ext",
                    "content": "full content of the file"
                }},
                ...
            ]
        }}
        
        Only provide the JSON without any explanations or additional text.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse the response
        project_data = json.loads(response.choices[0].message.content)
        
        # Create the files
        files_created = []
        for file_info in project_data.get("files", []):
            file_path = os.path.join(current_working_directory, project_path, file_info["path"])
            file_content = file_info["content"]
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Create the file
            with open(file_path, 'w') as f:
                f.write(file_content)
                
            files_created.append(file_info["path"])
        
        return {
            "message": f"Project '{project_data.get('project_name')}' created successfully.",
            "description": project_data.get("description"),
            "files_created": files_created
        }
    except Exception as e:
        return f"Error generating project: {str(e)}"

def explain_code(code: str) -> str:
    """
    Provide an explanation for the given code.
    """
    try:
        prompt = f"Explain the following code in detail:\n\n```\n{code}\n```\n\nProvide a clear, line-by-line explanation."
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error explaining code: {str(e)}"

def improve_code(code: str, improvement_prompt: str = "") -> str:
    """
    Improve the given code based on the improvement prompt.
    """
    try:
        prompt = f"Improve the following code:\n\n```\n{code}\n```\n\n"
        
        if improvement_prompt:
            prompt += f"Specifically focus on: {improvement_prompt}\n\n"
        else:
            prompt += "Focus on improving: performance, readability, and best practices.\n\n"
            
        prompt += "Only provide the improved code without explanations."
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error improving code: {str(e)}"

def generate_test(code: str, test_framework: str = "pytest") -> str:
    """
    Generate tests for the given code.
    """
    try:
        prompt = f"""
        Generate tests for the following code using {test_framework}:
        
        ```
        {code}
        ```
        
        Create comprehensive tests that cover different scenarios and edge cases.
        Only provide the test code without any explanations.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating tests: {str(e)}"

# Available tools dictionary
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

system_prompt = f"""
    You are CodeSH, an intelligent code generation assistant that helps users create code, develop projects, and work with files.
    You work in a start, plan, action, observe mode to carefully address user requests.
    
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tools. Based on the tool selection, perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call, resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input.
    - Carefully analyze the user query.
    - NEVER execute sudo commands or any commands that could harm the system.
    - Be helpful and informative about code generation and programming concepts.
    - Give clear explanations of what each action does.
    - If creating a project using a specific framework (React, Vue, etc.), use the generate_project function
      which will detect if CLI commands should be used for proper project setup.
    - When changing directories, always use the change_directory function.
    - Always show each minor step to the user like creating a file, reading a file, etc. 

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - create_file: Creates a new file with content. Parameters: file_path, content.
    - read_file: Reads and returns the contents of a file. Parameters: file_path.
    - update_file: Updates the contents of an existing file. Parameters: file_path, content.
    - list_directory: Lists the contents of a directory. Parameters: directory_path (optional, defaults to current directory).
    - create_directory: Creates a new directory. Parameters: directory_path.
    - change_directory: Changes the current working directory. Parameters: directory_path.
    - get_current_directory: Gets the current working directory.
    - generate_code: Generates code based on the provided prompt and language. Parameters: prompt, language (optional, defaults to python).
    - generate_project: Generates a complete project structure based on the description. Parameters: project_description, project_path (optional).
    - explain_code: Provides an explanation for the given code. Parameters: code.
    - improve_code: Improves the given code based on the improvement prompt. Parameters: code, improvement_prompt (optional).
    - generate_test: Generates tests for the given code. Parameters: code, test_framework (optional, defaults to pytest).
    
    Example:
    User Query: Create a function to calculate factorial
    Output: {{ "step": "plan", "content": "I'll generate a Python function to calculate the factorial of a number." }}
    Output: {{ "step": "action", "function": "generate_code", "input": {{ "prompt": "Write a function to calculate the factorial of a number", "language": "python" }} }}
    Output: {{ "step": "observe", "output": "def factorial(n):\\n    if n == 0 or n == 1:\\n        return 1\\n    else:\\n        return n * factorial(n-1)" }}
    Output: {{ "step": "output", "content": "Here's a Python function to calculate factorial:\\n\\n```python\\ndef factorial(n):\\n    if n == 0 or n == 1:\\n        return 1\\n    else:\\n        return n * factorial(n-1)\\n```\\n\\nThis is a recursive implementation that multiplies n by the factorial of (n-1) until it reaches the base case of 0 or 1." }}
"""

def process_function_input(function_name, input_data):
    """Process the function input based on its type and the expected parameters."""
    if isinstance(input_data, dict):
        # If input is a dictionary, pass it as kwargs
        return available_tools[function_name]["fn"](**input_data)
    else:
        # If input is not a dictionary, pass it as a single argument
        return available_tools[function_name]["fn"](input_data)

messages = [
    {"role": "system", "content": system_prompt}
]

def display_banner():
    """Display a banner for the code generation tool."""
    banner = """
    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║              CODESH                        ║
    ║                                            ║
    ║  Code Generation and File Creation Agent   ║
    ║                                            ║
    ║  Type 'help' for available commands        ║
    ║  Type 'exit' to quit                       ║
    ║                                            ║
    ╚════════════════════════════════════════════╝
    """
    print(banner)

def main():
    display_banner()
    
    while True:
        user_query = input('> ')
        
        if user_query.lower() == 'exit':
            print("Exiting CODESH. Goodbye!")
            break
            
        if user_query.lower() == 'help':
            print("\nAvailable operations:")
            print("  - Generate code: 'Create a function to calculate Fibonacci numbers'")
            print("  - Create files: 'Create a file named app.py with a Flask app'")
            print("  - Generate projects: 'Create a React todo app with Vite and Tailwind in ./todo-app'")
            print("  - Explain code: 'Explain this code: <paste code here>'")
            print("  - Improve code: 'Improve this code for performance: <paste code here>'")
            print("  - Generate tests: 'Write tests for: <paste code here>'")
            print("  - File operations: Create, read, update files")
            print("  - Directory operations: List, create, navigate directories")
            print("    - 'cd projects' to change directory")
            print("    - 'pwd' to show current directory")
            print("\nType 'exit' to quit\n")
            continue
        
        
        messages.append({"role": "user", "content": user_query})

        while True:
            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=messages
            )

            try:
                parsed_output = json.loads(response.choices[0].message.content)
                messages.append({"role": "assistant", "content": json.dumps(parsed_output)})

                if parsed_output.get("step") == "plan":
                    print(f"🧠: {parsed_output.get('content')}")
                    continue
                
                if parsed_output.get("step") == "action":
                    tool_name = parsed_output.get("function")
                    tool_input = parsed_output.get("input")

                    if tool_name in available_tools:
                        output = process_function_input(tool_name, tool_input)
                        messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                        continue
                    else:
                        output = f"Error: Tool '{tool_name}' not found."
                        messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                        continue
                
                if parsed_output.get("step") == "output":
                    print(f"🤖: {parsed_output.get('content')}")
                    break

            except json.JSONDecodeError:
                print("Error: Invalid JSON response from assistant.")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                break

if __name__ == "__main__":
    main()