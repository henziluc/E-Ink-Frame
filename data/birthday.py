import json
from datetime import date
from pathlib import Path


def get_birthday_data():

    file_path = Path(__file__).resolve().parent / 'assets' / 'birthdays' / "birthday_data.json"

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    birthday_data = [
        {
            "name": person["name"],
            "birthday": date.fromisoformat(person["birthday"])
        }
        for person in data["birthdays"]
    ]

    return birthday_data