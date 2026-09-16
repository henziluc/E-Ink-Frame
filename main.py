import time
from datetime import datetime

from fetch_data import fetch_all_data
from layout.dashboard import make_dashbord

UPDATE_INTERVAL = 15 * 60  # 15 minutes


def run_update():
    print(f"\n[{datetime.now()}] Starting update...")

    try:
        # 1. Fetch all data
        data = fetch_all_data()

        # 2. Display the data
        make_dashbord(data)

        print(f"[{datetime.now()}] Update completed successfully.")

    except Exception as e:
        print(f"[{datetime.now()}] ERROR: {e}")


def main():
    print("E-Ink Dashboard started")

    while True:
        run_update()

        print(f"Waiting {UPDATE_INTERVAL // 60} minutes...")
        time.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    main()