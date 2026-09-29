from app.employee_service import EmployeeService

service = EmployeeService()


def print_employee(employee):
    print("\n-----------------------------")
    for key, label in [
        ("id", "ID"), ("name", "Name"), ("email", "Email"),
        ("department", "Department"), ("role", "Role"), ("salary", "Salary")
    ]:
        print(f"{label:<11}: {employee[key]}")
    print("-----------------------------")


def main():
    while True:
        print("\n============================")
        print(" Employee Management System")
        print("============================")
        print("1. Create Employee")
        print("2. List Employees")
        print("3. Get Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Search Employee")
        print("7. Exit")

        choice = input("\nChoose option: ")

        try:
            if choice == "1":
                employee = service.create_employee(
                    input("Name: "), input("Email: "), input("Department: "),
                    input("Role: "), float(input("Salary: "))
                )
                print("Employee created successfully.")
                print_employee(employee)

            elif choice == "2":
                for employee in service.get_all_employees():
                    print_employee(employee)

            elif choice == "3":
                print_employee(service.get_employee(int(input("Employee ID: "))))

            elif choice == "4":
                employee_id = int(input("Employee ID: "))
                current = service.get_employee(employee_id)
                name = input(f"Name [{current['name']}]: ") or current["name"]
                email = input(f"Email [{current['email']}]: ") or current["email"]
                department = input(f"Department [{current['department']}]: ") or current["department"]
                role = input(f"Role [{current['role']}]: ") or current["role"]
                salary_input = input(f"Salary [{current['salary']}]: ")
                salary = float(salary_input) if salary_input else float(current["salary"])
                print_employee(service.update_employee(
                    employee_id, name, email, department, role, salary
                ))

            elif choice == "5":
                service.delete_employee(int(input("Employee ID: ")))
                print("Employee deleted successfully.")

            elif choice == "6":
                for employee in service.search_employees(input("Search keyword: ")):
                    print_employee(employee)

            elif choice == "7":
                break
            else:
                print("Invalid option.")

        except (ValueError, TypeError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
