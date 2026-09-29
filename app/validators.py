import re


def validate_name(name: str) -> None:
    if not name or not name.strip():
        raise ValueError("Employee name cannot be empty.")


def validate_email(email: str) -> None:
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(pattern, email):
        raise ValueError("Invalid email address.")


def validate_department(department: str) -> None:
    if not department or not department.strip():
        raise ValueError("Department cannot be empty.")


def validate_role(role: str) -> None:
    if not role or not role.strip():
        raise ValueError("Role cannot be empty.")


def validate_salary(salary: float) -> None:
    if salary < 0:
        raise ValueError("Salary cannot be negative.")


def validate_employee(name, email, department, role, salary) -> None:
    validate_name(name)
    validate_email(email)
    validate_department(department)
    validate_role(role)
    validate_salary(salary)
