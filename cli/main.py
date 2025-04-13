import json
import os
import subprocess
import threading
import time
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def execute_command(command: str, show_realtime_output: bool = False) -> str:
    """
    Execute a shell command and return its output.
    Optionally show real-time output for long-running commands.
    """
    try:
        if show_realtime_output:
            # For real-time output display during command execution
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            output_lines = []
            print("\nExecuting command: ", command)
            print("Command output:")
            print("-" * 40)
            
            for line in iter(process.stdout.readline, ''):
                print(f"  {line.rstrip()}")
                output_lines.append(line)
                sys.stdout.flush()  # Ensure output is displayed in real-time
            
            process.stdout.close()
            return_code = process.wait()
            print("-" * 40)
            
            if return_code != 0:
                return f"Command completed with non-zero exit code: {return_code}\nOutput:\n{''.join(output_lines)}"
            
            return f"Command completed successfully.\nOutput:\n{''.join(output_lines)}"
        else:
            # Standard execution for simple commands
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                return f"Command failed with error code {result.returncode}:\n{result.stderr}"
            
            return result.stdout.strip() or "Command executed successfully."
    except Exception as e:
        return f"Error executing command: {str(e)}"

def execute_long_running_command(command: str) -> str:
    """
    Execute a command that might take a while, with real-time feedback.
    Used for project creation, npm installs, etc.
    """
    # Start a spinner in a separate thread to show activity
    stop_spinner = threading.Event()
    
    def spinner():
        spinner_chars = "|/-\\"
        i = 0
        while not stop_spinner.is_set():
            i = (i + 1) % len(spinner_chars)
            sys.stdout.write(f"\r[{spinner_chars[i]}] Command running...")
            sys.stdout.flush()
            time.sleep(0.1)
    
    # Only start spinner if not showing real-time output
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()
    
    try:
        result = execute_command(command, show_realtime_output=True)
        return result
    finally:
        # Stop spinner thread when command completes
        stop_spinner.set()
        spinner_thread.join()
        sys.stdout.write("\r" + " " * 30 + "\r")  # Clear spinner line
        sys.stdout.flush()

def generate_command(operation_description: str) -> str:
    """
    Generate a shell command based on the operation description.
    """
    try:
        prompt = f"""
        Convert the following operation into a safe shell command:
        "{operation_description}"
        
        Rules:
        1. NEVER generate dangerous commands (rm -rf /, sudo, etc.)
        2. Only generate file/directory operations (ls, mkdir, cat, touch, echo, cd, pwd, cp, mv, etc.)
        3. Make the command as simple as possible
        4. For writing file content, use echo with redirection or cat with heredoc when appropriate
        5. Return ONLY the command, no explanations or markdown

        Example input: "List files in current directory"
        Example output: ls -la
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract command from response
        generated_command = response.choices[0].message.content.strip()
        
        # Basic safety check
        dangerous_patterns = ['sudo', 'rm -rf /', '> /dev/', '| rm', '& rm', '; rm', '&& rm']
        if any(pattern in generated_command.lower() for pattern in dangerous_patterns):
            return "Error: Potentially dangerous command detected."
        
        return generated_command
    except Exception as e:
        return f"Error generating command: {str(e)}"

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

def create_project_using_cli(project_info, project_path):
    """
    Create a project using CLI commands based on the project info.
    Now with improved real-time feedback for long-running commands.
    """
    try:
        # Extract information from project_info
        project_type = project_info.get("project_type", "unknown")
        cli_commands = project_info.get("cli_commands", [])
        
        results = []
        
        print(f"\n📦 Creating {project_type} project in {project_path}...\n")
        
        # Execute each CLI command with real-time feedback
        for i, command in enumerate(cli_commands):
            print(f"\n[{i+1}/{len(cli_commands)}] Running: {command}\n")
            result = execute_long_running_command(command)
            results.append(f"Command: {command}\nResult: {result}")
            print(f"\n✅ Command completed\n")
        
        return "\n\nProject creation completed successfully!"
    except Exception as e:
        return f"Error creating project using CLI: {str(e)}"

def generate_project(project_description: str, project_path: str = ".") -> str:
    """
    Generates a complete project structure based on the description.
    Now with support for using CLI commands for frameworks like React, Vue, etc.
    And improved real-time feedback for long-running operations.
    """
    try:
        # Detect project type to determine if CLI commands should be used
        project_info = detect_project_type(project_description)
        
        print("\n🔍 Analyzing project requirements...")
        
        # If we should use CLI commands (like npm create vite@latest)
        if isinstance(project_info, dict) and project_info.get("use_cli", False):
            print(f"\n🚀 This appears to be a {project_info.get('project_type', 'framework')} project. Using CLI tools...")
            return create_project_using_cli(project_info, project_path)
        
        print("\n📂 Generating project structure...")
        
        # Otherwise, generate a series of commands to create the project structure
        prompt = f"""
        For the project described as and use the Standard command(eg for express npm init then all deps): "{project_description}" to be created in path "{project_path}"
        
        Generate a series of shell commands to:
        1. Create the necessary directory structure
        2. Create all required files with their content
        3. Include appropriate configuration files
        
        Format the response as a list of commands, one per line.
        Each file content should be created using echo with heredoc or similar techniques.
        
        Only provide the commands without any explanations or markdown.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Get the commands
        commands = response.choices[0].message.content.strip().split('\n')
        
        # Execute each command with progress indicator
        results = []
        for i, command in enumerate(commands):
            if command.strip():
                print(f"\n[{i+1}/{len(commands)}] Executing: {command}")
                result = execute_command(command)
                results.append(f"Command: {command}\nResult: {result}")
                print(f"  Result: {result}")
        
        return "\n\nProject creation completed successfully!"
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

# Available tools dictionary - now with improved command execution tools
available_tools = {
    "execute_command": {
        "fn": execute_command,
        "description": "Executes a shell command directly. Parameters: command, show_realtime_output (optional)."
    },
    "execute_long_running_command": {
        "fn": execute_long_running_command,
        "description": "Executes a potentially long-running command with real-time feedback. Parameters: command."
    },
    "generate_command": {
        "fn": generate_command,
        "description": "Generates a shell command based on the operation description. Parameters: operation_description."
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
    - For file and directory operations, use generate_command to get the appropriate shell command.
    - For simple commands, use execute_command.
    - For potentially long-running commands, use execute_long_running_command to show real-time progress.
    - Always show each minor step to the user like creating a file, reading a file, etc.

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - execute_command: Executes a shell command directly. Parameters: command, show_realtime_output (optional).
    - execute_long_running_command: Executes a potentially long-running command with real-time feedback. Parameters: command.
    - generate_command: Generates a shell command based on the operation description. Parameters: operation_description.
    - generate_code: Generates code based on the provided prompt and language. Parameters: prompt, language (optional, defaults to python).
    - generate_project: Generates a complete project structure based on the description. Parameters: project_description, project_path (optional).
    - explain_code: Provides an explanation for the given code. Parameters: code.
    - improve_code: Improves the given code based on the improvement prompt. Parameters: code, improvement_prompt (optional).
    - generate_test: Generates tests for the given code. Parameters: code, test_framework (optional, defaults to pytest).
    
    Example:
    User Query: Create a React app with Vite in a folder called my-app
    Output: {{ "step": "plan", "content": "I'll generate a new React application using Vite in a folder called 'my-app'." }}
    Output: {{ "step": "action", "function": "generate_project", "input": {{ "project_description": "React application with Vite", "project_path": "my-app" }} }}
    Output: {{ "step": "observe", "output": "🔍 Analyzing project requirements...\n\n🚀 This appears to be a react project. Using CLI tools...\n\n📦 Creating react project in my-app...\n\n[1/3] Running: npm create vite@latest my-app -- --template react\n\nCommand completed successfully.\nOutput:\n...\n\n✅ Command completed\n\n[2/3] Running: cd my-app && npm install\n\nCommand completed successfully.\nOutput:\n...\n\n✅ Command completed\n\n[3/3] Running: cd my-app && npm install -D tailwindcss postcss autoprefixer\n\nCommand completed successfully.\nOutput:\n...\n\n✅ Command completed\n\nProject creation completed successfully!" }}
    Output: {{ "step": "output", "content": "I've created a new React application using Vite in the 'my-app' folder. The project has been set up with npm and all the necessary dependencies have been installed. You can now navigate to the my-app directory and start the development server with 'npm run dev'." }}
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
        user_query = input('\n> ')
        
        if user_query.lower() == 'exit':
            print("Exiting CODESH. Goodbye!")
            break
            
        if user_query.lower() == 'help':
            print("\nAvailable operations:")
            print("  - File & Directory operations: 'List files in current directory', 'Create a new folder called projects', etc.")
            print("  - Generate code: 'Create a function to calculate Fibonacci numbers'")
            print("  - Create files: 'Create a file named app.py with a Flask app'")
            print("  - Generate projects: 'Create a React todo app with Vite and Tailwind in ./todo-app'")
            print("  - Explain code: 'Explain this code: <paste code here>'")
            print("  - Improve code: 'Improve this code for performance: <paste code here>'")
            print("  - Generate tests: 'Write tests for: <paste code here>'")
            print("\nCommands are automatically generated and executed based on natural language descriptions")
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