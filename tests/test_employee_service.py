from app.employee_service import EmployeeService


def test_service_can_be_created():
    service = EmployeeService()
    assert service is not None
