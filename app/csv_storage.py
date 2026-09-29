import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CSV_FILE = DATA_DIR / "employees.csv"

FIELDNAMES = ["id", "name", "email", "department", "role", "salary"]


def initialize_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not CSV_FILE.exists():
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=FIELDNAMES).writeheader()


def read_all() -> list[dict]:
    initialize_storage()
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_all(rows: list[dict]) -> None:
    initialize_storage()
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def append(row: dict) -> None:
    initialize_storage()
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        csv.DictWriter(file, fieldnames=FIELDNAMES).writerow(row)
