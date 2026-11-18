"""Run the Week 1 employee analysis with the Python standard library."""

import csv
from pathlib import Path


def bonus(salary, rate=0.1, *extras, **options):
    total = salary * rate + sum(extras)
    return min(total, options["cap"]) if "cap" in options else total


class InvalidSalaryError(ValueError):
    """Raised when an employee has a negative monthly salary."""


class Employee:
    def __init__(self, name, salary):
        if salary < 0:
            raise InvalidSalaryError(f"{name} has a negative salary ({salary}).")
        self.name = name
        self.salary = salary

    def annual_salary(self):
        return self.salary * 12

    def get_details(self):
        return f"{self.name}, monthly salary {self.salary:,}"


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def get_details(self):
        return f"{super().get_details()}, team size {self.team_size}"


def load_employees(path):
    with path.open(newline="", encoding="utf-8") as source:
        return [dict(row, salary=int(row["salary"])) for row in csv.DictReader(source)]


def scan_salaries(employees):
    visited = []
    for row in employees:
        if row["salary"] == 0:
            continue
        visited.append(row["name"])
        if row["salary"] > 85000:
            break
    return visited


def main():
    employees = load_employees(Path(__file__).with_name("employees.csv"))
    high_earners = [row["name"] for row in employees if row["salary"] > 50000]
    raised_salaries = map(lambda row: (row["name"], row["salary"] + bonus(row["salary"])), employees)
    chennai = filter(lambda row: row["city"] == "Chennai", employees)

    print("Salary above 50,000:", ", ".join(high_earners))
    print("Monthly salaries after a 10% raise:")
    for name, salary in raised_salaries:
        print(f"  {name}: {salary:,.2f}")
    print("Chennai employees:", ", ".join(row["name"] for row in chennai))
    print("Salary scan:", ", ".join(scan_salaries(employees)))

    first = employees[0]
    employee = Employee(first["name"], first["salary"])
    print(employee.get_details(), f"(annual salary {employee.annual_salary():,})")
    print("Default bonus:", bonus(employee.salary))
    print("Bonus with 800 extra and a 3,500 cap:", bonus(employee.salary, 0.1, 800, cap=3500))
    print("Example manager:", Manager("Demo manager", 80000, 4).get_details())

    try:
        Employee("Demo employee", -1)
    except InvalidSalaryError as error:
        print("Caught InvalidSalaryError:", error)
    finally:
        print("Salary validation demo complete.")


if __name__ == "__main__":
    main()
