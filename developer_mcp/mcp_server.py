
from mcp.server.fastmcp import FastMCP

from developer_mcp.project_analyzer import ProjectAnalyzer
mcp = FastMCP("Employee CRUD Developer Assistant")


def analyzer(project_path):
    return ProjectAnalyzer(project_path)


@mcp.tool()
def project_summary(project_path: str) -> dict:
    """Understand the overall Python project."""
    return analyzer(project_path).project_summary()


@mcp.tool()
def project_structure(project_path: str) -> list:
    """Show the Python project structure."""
    return analyzer(project_path).project_structure()


@mcp.tool()
def search_code(project_path: str, query: str) -> list:
    """Search source code for a keyword or implementation."""
    return analyzer(project_path).search_code(query)


@mcp.tool()
def find_function(project_path: str, function_name: str) -> list:
    """Find where a function is defined."""
    return analyzer(project_path).find_function(function_name)


@mcp.tool()
def find_class(project_path: str, class_name: str) -> list:
    """Find where a class is defined."""
    return analyzer(project_path).find_class(class_name)


@mcp.tool()
def find_function_usages(project_path: str, function_name: str) -> list:
    """Find where a function is called."""
    return analyzer(project_path).find_function_usages(function_name)


@mcp.tool()
def read_file(project_path: str, file_path: str) -> str:
    """Read a source file from the project."""
    return analyzer(project_path).read_file(file_path)


@mcp.tool()
def find_imports(project_path: str) -> list:
    """Find Python imports throughout the project."""
    return analyzer(project_path).find_imports()


@mcp.tool()
def find_csv_files(project_path: str) -> list:
    """Find CSV storage files."""
    return analyzer(project_path).find_csv_files()


if __name__ == "__main__":
    mcp.run(transport="stdio")
