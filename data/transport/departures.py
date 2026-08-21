import datetime
import pandas as pd
from .delays import get_delays

def departure_schedule(
    stop_id,
    stop_times,
    trips,
    routes,
    calendar,
    calendar_dates,
    stops,
    delays
):
    # --------------------------------------------------
    # 1. Get current date and time
    # --------------------------------------------------
    now = datetime.datetime.now()

    today = pd.Timestamp(
        now.year,
        now.month,
        now.day
    )

    # --------------------------------------------------
    # 2. Find station and child stops
    # --------------------------------------------------
    station_id = "Parent" + stop_id

    # Find child stops belonging to this station
    child_stops = stops[
        stops["parent_station"] == station_id
    ]["stop_id"].tolist()


    # Include the station itself AND all child stops
    relevant_stop_ids = [stop_id] + child_stops

    # --------------------------------------------------
    # 3. Get all departures from station + child stops
    # --------------------------------------------------
    departures = stop_times[
        stop_times["stop_id"].isin(relevant_stop_ids)
    ].copy()

    # --------------------------------------------------
    # 4. Add trip information
    # --------------------------------------------------
    departures = departures.merge(
        trips[
            [
                "trip_id",
                "route_id",
                "service_id",
                "trip_headsign"
            ]
        ],
        on="trip_id",
        how="left"
    )

    # --------------------------------------------------
    # 5. Add route information
    # --------------------------------------------------
    departures = departures.merge(
        routes[
            [
                "route_id",
                "route_short_name",
                "route_long_name"
            ]
        ],
        on="route_id",
        how="left"
    )

    # --------------------------------------------------
    # 6. Find services operating today
    # --------------------------------------------------
    active_services = get_active_services(
        calendar,
        calendar_dates,
        today
    )

    # --------------------------------------------------
    # 7. Debug service IDs
    # --------------------------------------------------
    station_service_ids = set(
        departures["service_id"].dropna()
    )

    matching_ids = station_service_ids & active_services

    # --------------------------------------------------
    # 8. Keep only services operating today
    # --------------------------------------------------
    departures_today = departures[
        departures["service_id"].isin(active_services)
    ].copy()

    # --------------------------------------------------
    # 9. Convert GTFS time to seconds
    # --------------------------------------------------
    departures_today["departure_seconds"] = (
        departures_today["departure_time"]
        .apply(gtfs_time_to_seconds)
    )

    # --------------------------------------------------
    # 10. Get current time in seconds
    # --------------------------------------------------
    current_seconds = (
        now.hour * 3600 +
        now.minute * 60 +
        now.second
    )

    # --------------------------------------------------
    # 11. Find next departures
    # --------------------------------------------------
    next_departures = departures_today[
        departures_today["departure_seconds"] >= current_seconds
    ].sort_values("departure_seconds")

    # --------------------------------------------------
    # 12. Add realtime delays
    # --------------------------------------------------


    next_departures["delay"] = next_departures.apply(
        lambda row: delays.get(
            (row["trip_id"], row["stop_id"]),
            0
        ),
        axis=1
    )

    # --------------------------------------------------
    # 13. Calculate realtime departure time
    # --------------------------------------------------

    next_departures["realtime_departure_seconds"] = (
        next_departures["departure_seconds"]
        + next_departures["delay"]
    )
    # --------------------------------------------------
    # 14. Drop not needed columns
    # --------------------------------------------------
    
    next_departures = next_departures.drop(columns=[
        "route_long_name",
        "trip_id",
        "stop_id",
        "stop_sequence",
        "pickup_type",
        "drop_off_type",
        "route_id",
        "service_id"
        ])
    
    
    # --------------------------------------------------
    # 15. Return next 5
    # --------------------------------------------------

    return next_departures.head(5)


def gtfs_time_to_seconds(time_string):
    hours, minutes, seconds = map(
        int,
        time_string.split(":")
    )

    return (
        hours * 3600 +
        minutes * 60 +
        seconds
    )


def get_active_services(calendar, calendar_dates, date):

    calendar = calendar.copy()
    calendar_dates = calendar_dates.copy()

    # --------------------------------------------------
    # Convert dates
    # --------------------------------------------------
    calendar["start_date"] = pd.to_datetime(
        calendar["start_date"].astype(str),
        format="%Y%m%d"
    )

    calendar["end_date"] = pd.to_datetime(
        calendar["end_date"].astype(str),
        format="%Y%m%d"
    )

    calendar_dates["date"] = pd.to_datetime(
        calendar_dates["date"].astype(str),
        format="%Y%m%d"
    )

    # --------------------------------------------------
    # Get weekday
    # --------------------------------------------------
    weekday = date.strftime("%A").lower()

    # --------------------------------------------------
    # Normal weekly services
    # --------------------------------------------------
    active_services = set(
        calendar[
            (calendar["start_date"] <= date) &
            (calendar["end_date"] >= date) &
            (calendar[weekday] == 1)
        ]["service_id"]
    )

    # --------------------------------------------------
    # Apply exceptions
    # --------------------------------------------------
    exceptions = calendar_dates[
        calendar_dates["date"] == date
    ]

    for _, row in exceptions.iterrows():

        if row["exception_type"] == 1:
            active_services.add(row["service_id"])

        elif row["exception_type"] == 2:
            active_services.discard(row["service_id"])

    return active_services