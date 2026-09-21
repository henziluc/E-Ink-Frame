import time
from datetime import datetime

from pathlib import Path

from fetch_data import fetch_all_data
from data.transport.transport import load_transport_data
from layout.dashboard import make_dashbord
from logger import logger

UPDATE_INTERVAL = 15 * 60





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
        "weather_hourly": None,
        "weather_daily": None,
        "departures_seen": None,
        "departures_etzberg": None,
        "health_data": {
            "Luca": None,
            "Jojo": None
        },
        "moon_data": None,
        "news_data": None,
        "quote_data": None,
        "birthday_data": None,
        "status" : {
            'weather' : None,
            'transport' : None,
            'health' : None,
            'moon' : None,
            'news' : None,
            'quote' : None,
            'birthday' : None
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
            logger.info(f"Next update in {wait_time / 60:.1f} minutes")
            time.sleep(wait_time)
        else:
            logger.info("Update took longer than the interval. Starting next update.")   
            
if __name__ == "__main__":
    main()