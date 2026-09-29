
# Employee CRUD + Developer MCP

A Python employee CRUD application that stores records in CSV, plus an MCP server that helps an AI assistant explore the project source code.

## Requirements

- Windows with Python 3.10 or newer
- Visual Studio Code with MCP support to use the developer tools from chat

## Setup (PowerShell)

Run these commands from the project directory, the folder containing `requirements.txt`:

```powershell
cd E:\employee-crud-mcp
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run this once in that terminal, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run the CRUD application

With the virtual environment active and the current directory set to the project root:

```powershell
python -m app.main
```

The application reads and writes employee records in `data/employees.csv`. Use `7` in the menu to exit.

## Run the MCP server in VS Code

The server implementation is `developer_mcp/mcp_server.py`. It uses stdio transport, so normally let VS Code start it:

1. Open the project in VS Code. The workspace folder should be the folder containing `requirements.txt`.
2. Ensure setup above is complete so `.venv` exists and contains the `mcp` package.
3. Open the Command Palette with `Ctrl+Shift+P` and run **MCP: List Servers**.
4. Start or restart `employee-developer-assistant`.
5. Ask the assistant a question about the project. The tools receive the project root as `project_path`.

The MCP configuration must be named `mcp.json` and be located in a `.vscode` folder at the VS Code workspace root. For this repository, the project-level config is `.vscode/mcp.json`. If you open the parent folder instead of the project folder, use the parent workspace config at `../.vscode/mcp.json`; it points into the nested project directory.

The project-level configuration should look like this:

```json
{
    "servers": {
        "employee-developer-assistant": {
            "type": "stdio",
            "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
            "args": [
                "-m",
                "developer_mcp.mcp_server"
            ]
        }
    }
}
```

Important configuration details:

- `command` should point to the Python executable inside this project's `.venv`.
- `args` launches the server as a Python module from the workspace root.
- Use the parent-folder config if the VS Code workspace is `E:\employee-crud-mcp`; its Python and `cwd` paths include the nested `employee-crud-mcp` directory.
- Do not type shell commands into a running MCP server terminal. Its standard input carries MCP messages, not PowerShell commands.

For a manual startup check, open a fresh PowerShell terminal at the project root and run:

```powershell
python -m developer_mcp.mcp_server
```

The process will wait without displaying a prompt. That is expected for stdio; press `Ctrl+C` to stop it. Manual startup alone does not connect it to a VS Code chat client.

## Test

Install pytest into the active virtual environment, then run the tests from the project root:

```powershell
python -m pip install pytest
python -m pytest -q
```

## MCP tools

- `project_summary`: counts files, classes, and functions and lists CSV files.
- `project_structure`: lists Python files.
- `search_code`: searches source lines for text.
- `find_function` and `find_class`: locate definitions.
- `find_function_usages`: finds calls by function name.
- `read_file`: reads a project file.
- `find_imports`: lists imports in Python files.
- `find_csv_files`: lists CSV files.

## Example questions

- Summarize this project and explain its architecture.
- Where is employee creation implemented? Show the relevant function.
- Where is employee data stored, and how is the CSV file accessed?
- Find the definition and usages of `delete_employee`.
- Walk through the update-employee flow from the CLI to CSV storage.
- Which files import the employee repository?
- Which files would need changes to add a phone number field?

## Architecture

```text
app/main.py
  -> app/employee_service.py
  -> app/employee_repository.py
  -> app/csv_storage.py
  -> data/employees.csv

developer_mcp/mcp_server.py
  -> developer_mcp/project_analyzer.py
```
