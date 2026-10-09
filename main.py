import time
from datetime import datetime, timedelta
from pathlib import Path

from fetch_data import fetch_all_data
from data.transport.transport import load_transport_data
from data.data_saver import save_data_to_file, load_data_from_file
from data.holiday_photo import prepare_holiday_photos
from assets.holiday_data import holidays
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
    try:
        prepare_holiday_photos(holidays)
    except:
        logger.exception("Getting holiday pictures failed")
        
    data = load_data_from_file(Path("assets/projectdata/data.json"))
        
        
        
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
                print(f"{key}:")

                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        print(f"  {subkey}: {subvalue}")

                elif isinstance(value, list):
                    for element in value:
                        if isinstance(element, dict):
                            for subkey, subvalue in element.items():
                                print(f"  {subkey}: {subvalue}")
                        else:
                            print(f"  {element}")

                else:
                    print(f"  {value}")
            
            logger.info(f"Status: {data['status']}")
            
            save_data_to_file(data, Path("assets/projectdata/data.json"))
            
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
    minutes_to_next = 15 - process_time / 60 - (now.minute % 15)
    if minutes_to_next < 5:
        minutes_to_next += 15
    
    next_update = now.replace(
        second=0,
        microsecond=0
    ) + timedelta(minutes=minutes_to_next)

    sleep_seconds = (next_update - now).total_seconds()

    logger.info(f"Next update: {next_update.strftime('%H:%M:%S')}")

    time.sleep(sleep_seconds)



if __name__ == "__main__":
    main()