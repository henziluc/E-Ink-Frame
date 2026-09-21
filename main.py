import time
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from fetch_data import fetch_all_data
from data.transport.transport import load_transport_data
from layout.dashboard import make_dashbord

UPDATE_INTERVAL = 15 * 60


BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("E-Ink-Dashboard")
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    LOG_DIR / "dashboard.log",
    maxBytes=2 * 1024 * 1024,  # 2 MB
    backupCount=5,
    encoding="utf-8"
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)



def main():
    logger.info("E-Ink Dashboard started")

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
        logger.info("Start fetching data")

        try:
            # 1. Fetch all data
            data = fetch_all_data(
                stop_times,
                calendar,
                calendar_dates,
                transport_info,
                data
            )

            logger.info("Data fetched successfully")
            
            # 2. Create and display dashboard
            make_dashbord(data)

            logger.info("Dashboard displayed successfully")

        except Exception as e:
            logger.exception("Update failed")

        # Schedule next update
        next_update += UPDATE_INTERVAL

        # Calculate remaining time
        wait_time = next_update - time.monotonic()

        if wait_time > 0:
            print(f"Waiting {wait_time / 60:.1f} minutes...")
            logger.info(f"Next update in {wait_time / 60:.1f} minutes")
            time.sleep(wait_time)
        else:
            print("Update took longer than the interval. Starting next update.")
            logger.info("Update took longer than the interval. Starting next update.")   
            
if __name__ == "__main__":
    main()