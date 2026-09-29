from app import csv_storage


class EmployeeRepository:

    def get_all(self) -> list[dict]:
        return csv_storage.read_all()

    def get_by_id(self, employee_id: int) -> dict | None:
        for employee in self.get_all():
            if int(employee["id"]) == employee_id:
                return employee
        return None

    def create(self, employee: dict) -> dict:
        csv_storage.append(employee)
        return employee

    def update(self, employee_id: int, updated_employee: dict) -> dict | None:
        employees = self.get_all()
        for index, employee in enumerate(employees):
            if int(employee["id"]) == employee_id:
                employees[index] = updated_employee
                csv_storage.write_all(employees)
                return updated_employee
        return None

    def delete(self, employee_id: int) -> bool:
        employees = self.get_all()
        filtered = [e for e in employees if int(e["id"]) != employee_id]
        if len(filtered) == len(employees):
            return False
        csv_storage.write_all(filtered)
        return True
