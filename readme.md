# CodeSH

A powerful AI-powered code generation and project scaffolding tool.

## Overview

CodeSH is an intelligent command-line tool that helps developers:
- Generate code in multiple programming languages
- Create project structures and scaffolds
- Execute and manage file operations
- Explain and improve existing code
- Generate tests for code

The tool uses natural language processing to understand your intentions and automatically generates and executes the appropriate commands.

## Features

- **Intelligent Command Generation**: Describe what you want in plain English, and CodeSH will generate the appropriate shell commands.
- **Project Scaffolding**: Quickly create new projects with proper structure and configurations.
- **Real-time Feedback**: See command execution progress in real-time, especially useful for long-running operations like dependency installation.
- **Code Generation**: Generate code snippets or complete files based on natural language descriptions.
- **Code Explanation**: Get detailed explanations of existing code.
- **Code Improvement**: Suggestions for improving code quality, performance, and readability.
- **Test Generation**: Automatically generate test cases for your code.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mukulpythondev/codesh.git
cd codesh
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
Create a `.env` file in the project root with:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start CodeSH:
```bash
python cli/codesh.py
```

2. At the prompt, describe what you want to do:
```
> Create a React app with Vite in a folder called my-app
```

3. CodeSH will analyze your request, create a plan, and execute the necessary commands with real-time feedback.

### Example Commands

Here are some examples of what you can ask CodeSH to do:

#### File Operations
```
> List files in the current directory
> Create a new folder called projects
> Create a file called app.py with a simple Flask hello world app
```

#### Project Generation
```
> Create a React todo app with Vite and Tailwind CSS in ./todo-app
> Generate a Django REST API project with user authentication
> Create a Node.js Express server with MongoDB connection
```

#### Code Generation
```
> Generate a Python function to calculate Fibonacci numbers
> Create a JavaScript class to manage a shopping cart
> Write a CSS grid layout for a responsive dashboard
```

#### Code Explanation & Improvement
```
> Explain this code: [paste code here]
> Improve this code for better performance: [paste code here]
> Optimize this SQL query: [paste query here]
```

#### Test Generation
```
> Write tests for: [paste code here]
> Generate Jest tests for this React component: [paste component here]
```

## Architecture

CodeSH works in a four-step process:
1. **Start**: Parse the user's request.
2. **Plan**: Create a plan to fulfill the request.
3. **Action**: Execute the appropriate tool or command.
4. **Observe**: Analyze the results and provide feedback.

### Available Tools

- `execute_command`: Executes a shell command directly.
- `execute_long_running_command`: Executes commands with real-time feedback.
- `generate_command`: Converts a description into a shell command.
- `generate_code`: Creates code based on descriptions.
- `generate_project`: Builds complete project structures.
- `explain_code`: Provides detailed code explanations.
- `improve_code`: Suggests improvements for existing code.
- `generate_test`: Creates test cases for code.

## Dependencies

- Python 3.7+
- OpenAI API (GPT-4o model)
- python-dotenv

## Security Notes

- CodeSH checks commands for potentially dangerous operations
- Avoids executing sudo or system-modifying commands
- Always reviews generated commands before execution

## Limitations

- Requires an active OpenAI API key and internet connection
- Generated code may need adjustment for specific use cases
- Limited to operations allowed by the system's user permissions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

