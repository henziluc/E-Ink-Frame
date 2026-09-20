import time
from datetime import datetime

from fetch_data import fetch_all_data
from data.transport.transport import load_transport_data
from layout.dashboard import make_dashbord

UPDATE_INTERVAL = 15 * 60  # 15 minutes





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
    
    data = {'health_data' : {
        'Luca' : None,
        'Jojo' : None
    }
        }
    # --------------------------------------------------------
    # Main loop
    # --------------------------------------------------------

    while True:
        print(f"\n[{datetime.now()}] Starting update...")
        try:
            # 1. Fetch all data
            data = fetch_all_data(stop_times,
                    calendar,
                    calendar_dates,
                    transport_info,
                    data)
            
            print(data)

            # 2. Display the data
            make_dashbord(data)

            print(f"[{datetime.now()}] Update completed successfully.")

        except Exception as e:
            print(f"[{datetime.now()}] ERROR: {e}")
        
        
        
        
        print(f"Waiting {UPDATE_INTERVAL // 60} minutes...")
        time.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    main()