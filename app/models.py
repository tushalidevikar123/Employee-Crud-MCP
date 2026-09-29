from dataclasses import dataclass


@dataclass
class Employee:
    id: int
    name: str
    email: str
    department: str
    role: str
    salary: float
