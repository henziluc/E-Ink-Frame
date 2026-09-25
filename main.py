import time
from datetime import datetime, timedelta
from pathlib import Path

from fetch_data import fetch_all_data
from data.transport.transport import load_transport_data
from layout.dashboard import make_dashbord
from logger import logger

UPDATE_INTERVAL = 15 * 60





def main():
    logger.info("E-Ink Dashboard started")
    counter = 0
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
        "quote_data": [],
        "birthday_data": None,
        "status" : {
            'weather' : None,
            'weather_timestamp' : None,
            'transport' : None,
            'transport_timestamp' : None,
            'health' : None,
            'health_timestamp' : None,
            'moon' : None,
            'moon_timestamp' : None,
            'news' : None,
            'news_timestamp' : None,
            'quote' : None,
            'quote_timestamp' : None,
            'birthday' : None,
            'birthday_timestamp' : None,
        }}
        
        
        
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
            
            for key, value in data.items():
                print(f"{key}: {value} \n")
            
            logger.info(f"Status: {data['status']}")
            
            # 2. Create and display dashboard
            data = make_dashbord(data)
            counter += 1
            logger.info(f"Dashboard updated successfully for the {counter} time")

        except Exception as e:
            logger.exception("Update failed")

        sleep_until_next_update()





def sleep_until_next_update():
    now = datetime.now()
    process_time = 60
    # Find the next 15-minute boundary
    minutes_to_next = 15 - (now.minute % 15) - process_time / 60
    if minutes_to_next < 5:
        minutes_to_next + 15

    next_update = now.replace(
        second=0,
        microsecond=0
    ) + timedelta(minutes=minutes_to_next)

    sleep_seconds = (next_update - now).total_seconds()

    logger.info(f"Next update: {next_update.strftime('%H:%M:%S')}")

    time.sleep(sleep_seconds)



if __name__ == "__main__":
    main()