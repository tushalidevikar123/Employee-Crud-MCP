from app.employee_repository import EmployeeRepository
from app.validators import validate_employee


class EmployeeService:

    def __init__(self):
        self.repository = EmployeeRepository()

    def create_employee(self, name, email, department, role, salary) -> dict:
        validate_employee(name, email, department, role, salary)
        employees = self.repository.get_all()
        if any(e["email"].lower() == email.lower() for e in employees):
            raise ValueError("Employee with this email already exists.")
        employee_id = max((int(e["id"]) for e in employees), default=0) + 1
        employee = {
            "id": employee_id, "name": name.strip(), "email": email.strip(),
            "department": department.strip(), "role": role.strip(), "salary": salary
        }
        return self.repository.create(employee)

    def get_all_employees(self) -> list[dict]:
        return self.repository.get_all()

    def get_employee(self, employee_id: int) -> dict:
        employee = self.repository.get_by_id(employee_id)
        if employee is None:
            raise ValueError(f"Employee {employee_id} not found.")
        return employee

    def update_employee(self, employee_id, name, email, department, role, salary) -> dict:
        validate_employee(name, email, department, role, salary)
        if self.repository.get_by_id(employee_id) is None:
            raise ValueError(f"Employee {employee_id} not found.")
        employee = {
            "id": employee_id, "name": name.strip(), "email": email.strip(),
            "department": department.strip(), "role": role.strip(), "salary": salary
        }
        return self.repository.update(employee_id, employee)

    def delete_employee(self, employee_id: int) -> bool:
        self.get_employee(employee_id)
        return self.repository.delete(employee_id)

    def search_employees(self, keyword: str) -> list[dict]:
        keyword = keyword.lower()
        return [
            e for e in self.repository.get_all()
            if keyword in " ".join(
                [e["name"], e["email"], e["department"], e["role"]
            ]).lower()
        ]
