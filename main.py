import time
from datetime import datetime

from fetch_data import fetch_all_data
from data.transport.transport import load_transport_data
from layout.dashboard import make_dashbord

UPDATE_INTERVAL = 15 * 60


def main():
    print("E-Ink Dashboard started")

    # --------------------------------------------------------
    # Prepare GTFS ONCE
    # --------------------------------------------------------
    (
        stop_times,
        calendar,
        calendar_dates,
        transport_info
    ) = load_transport_data()

    data = {
        "health_data": {
            "Luca": None,
            "Jojo": None
        }
    }

    # --------------------------------------------------------
    # Main loop
    # --------------------------------------------------------
    next_update = time.monotonic()

    while True:
        print(f"\n[{datetime.now()}] Starting update...")

        try:
            # 1. Fetch all data
            data = fetch_all_data(
                stop_times,
                calendar,
                calendar_dates,
                transport_info,
                data
            )

            # 2. Create and display dashboard
            make_dashbord(data)

            print(f"[{datetime.now()}] Update completed successfully.")

        except Exception as e:
            print(f"[{datetime.now()}] ERROR: {e}")

        # Schedule next update
        next_update += UPDATE_INTERVAL

        # Calculate remaining time
        wait_time = next_update - time.monotonic()

        if wait_time > 0:
            print(f"Waiting {wait_time / 60:.1f} minutes...")
            time.sleep(wait_time)
        else:
            print("Update took longer than the interval. Starting next update.")    