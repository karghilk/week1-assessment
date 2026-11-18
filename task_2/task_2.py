import csv
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
USERS_URL = "https://jsonplaceholder.typicode.com/users"


def save_json(filename, rows):
    with (HERE / filename).open("w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2, ensure_ascii=False)
        file.write("\n")


def export_employees():
    with (HERE / "employees.csv").open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fields = reader.fieldnames
        employees = [
            dict(row, id=int(row["id"]), salary=int(row["salary"]))
            for row in reader
        ]

    save_json("employees.json", employees)
    high_earners = [row for row in employees if row["salary"] > 50000]
    with (HERE / "high_earners.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(high_earners)
    print(f"Saved {len(employees)} employees and {len(high_earners)} high earners.")


def fetch_users():
    response = requests.get(USERS_URL, timeout=5)
    response.raise_for_status()
    users = []
    for item in response.json():
        users.append({
            "id": item["id"],
            "name": item["name"],
            "email": item["email"],
            "city": (item.get("address") or {}).get("city"),
        })
    save_json("users.json", users)
    for user in users[:3]:
        print(user["id"], user["name"], user["email"], sep=" | ")


def check_missing_user():
    response = requests.get(f"{USERS_URL}/9999", timeout=5)
    if response.status_code == 404:
        print("Expected 404: user 9999 was not found.")
    else:
        response.raise_for_status()
        raise ValueError(f"Expected 404, received {response.status_code}.")


def main():
    load_dotenv(HERE.parent / ".env")
    if not os.getenv("API_KEY"):
        raise SystemExit("Set API_KEY in the project .env file.")
    print("API_KEY loaded.")
    export_employees()

    failed = False
    for action in (fetch_users, check_missing_user):
        try:
            action()
        except requests.exceptions.Timeout:
            print(f"{action.__name__}: request timed out.")
        except requests.exceptions.ConnectionError:
            print(f"{action.__name__}: connection failed.")
        except (requests.exceptions.RequestException, ValueError) as error:
            print(f"{action.__name__}: {error}")
        else:
            continue
        failed = True
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
