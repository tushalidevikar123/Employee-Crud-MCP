from pathlib import Path
import ast

IGNORED_DIRECTORIES = {".git", ".venv", "venv", "__pycache__", ".pytest_cache"}


class ProjectAnalyzer:
    def __init__(self, project_path: str):
        self.root = Path(project_path).resolve()
        if not self.root.exists():
            raise ValueError(f"Project does not exist: {project_path}")

    def get_python_files(self):
        return [
            f for f in self.root.rglob("*.py")
            if not any(x in f.parts for x in IGNORED_DIRECTORIES)
        ]

    def project_structure(self):
        return sorted(str(f.relative_to(self.root)) for f in self.get_python_files())

    def search_code(self, query):
        results = []
        for file in self.get_python_files():
            try:
                lines = file.read_text(encoding="utf-8", errors="ignore").splitlines()
            except Exception:
                continue
            for line_no, line in enumerate(lines, 1):
                if query.lower() in line.lower():
                    results.append({
                        "file": str(file.relative_to(self.root)),
                        "line": line_no,
                        "code": line.strip()
                    })
        return results

    def read_file(self, file_path):
        root = self.root.resolve()
        target = (root / file_path).resolve()
        if not str(target).startswith(str(root)):
            raise ValueError("Access outside project denied.")
        if not target.exists():
            raise ValueError("File not found.")
        return target.read_text(encoding="utf-8", errors="ignore")

    def find_symbols(self):
        results = []
        for file in self.get_python_files():
            try:
                tree = ast.parse(file.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    results.append({
                        "type": "function", "name": node.name,
                        "file": str(file.relative_to(self.root)), "line": node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                    results.append({
                        "type": "class", "name": node.name,
                        "file": str(file.relative_to(self.root)), "line": node.lineno
                    })
        return results

    def find_function(self, name):
        return [s for s in self.find_symbols() if s["type"] == "function" and s["name"] == name]

    def find_class(self, name):
        return [s for s in self.find_symbols() if s["type"] == "class" and s["name"] == name]

    def find_function_usages(self, name):
        results = []
        for file in self.get_python_files():
            try:
                tree = ast.parse(file.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    called = None
                    if isinstance(node.func, ast.Name):
                        called = node.func.id
                    elif isinstance(node.func, ast.Attribute):
                        called = node.func.attr
                    if called == name:
                        results.append({
                            "file": str(file.relative_to(self.root)),
                            "line": node.lineno,
                            "function": name
                        })
        return results

    def find_imports(self):
        results = []
        for file in self.get_python_files():
            try:
                tree = ast.parse(file.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.append(node.module)
            results.append({
                "file": str(file.relative_to(self.root)),
                "imports": imports
            })
        return results

    def find_csv_files(self):
        return sorted(str(f.relative_to(self.root)) for f in self.root.rglob("*.csv"))

    def project_summary(self):
        symbols = self.find_symbols()
        return {
            "project": self.root.name,
            "python_files": len(self.get_python_files()),
            "functions": sum(s["type"] == "function" for s in symbols),
            "classes": sum(s["type"] == "class" for s in symbols),
            "csv_files": self.find_csv_files(),
            "python_files_list": self.project_structure()
        }
