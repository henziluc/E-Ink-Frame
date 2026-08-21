from pathlib import Path
import pandas as pd
from data.transport.departures import departure_schedule




def get_transport():
    BASE_DIR = Path(__file__).resolve().parents[2]
    stop_id_seen ="ch:1:sloid:6002"
    stop_id_etzberg = "ch:1:sloid:90937"

    stops = pd.read_csv(BASE_DIR / "assets" / "gtfs" / "stops.txt")
    stop_times = pd.read_csv(BASE_DIR / "assets" / "gtfs" / "stop_times.txt")
    trips = pd.read_csv(BASE_DIR / "assets" / "gtfs" / "trips.txt")
    routes = pd.read_csv(    BASE_DIR / "assets" / "gtfs" / "routes.txt")
    calendar = pd.read_csv(BASE_DIR / "assets" / "gtfs" / "calendar.txt")
    calendar_dates = pd.read_csv(BASE_DIR / "assets" / "gtfs" / "calendar_dates.txt")

    #print("Station Seen:", stop_id_seen)
    departures_seen = departure_schedule(stop_id_seen, stop_times, trips, routes, calendar, calendar_dates, stops)
    #print(departures_seen.to_string(index=False))
    
    #print("Station Etzberg:", stop_id_etzberg)
    departures_etzberg = departure_schedule(stop_id_etzberg, stop_times, trips, routes, calendar, calendar_dates, stops)
    #print(departures_etzberg.to_string(index=False))

    return departures_seen, departures_etzberg