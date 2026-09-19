from pathlib import Path
import datetime
import pandas as pd

from .delays import get_delays


# ============================================================
# GTFS DATA PREPARATION
# ============================================================

def prepare_gtfs():
    """
    Load and prepare all static GTFS data.

    This function should only be called ONCE when the program
    starts.
    """

    BASE_DIR = Path(__file__).resolve().parents[2]
    GTFS_DIR = BASE_DIR / "assets" / "gtfs"

    print("Loading GTFS data...")

    # --------------------------------------------------------
    # Load GTFS files
    # --------------------------------------------------------

    stops = pd.read_csv(
        GTFS_DIR / "stops.txt"
    )

    stop_times = pd.read_csv(
        GTFS_DIR / "stop_times.txt"
    )

    trips = pd.read_csv(
        GTFS_DIR / "trips.txt"
    )

    routes = pd.read_csv(
        GTFS_DIR / "routes.txt"
    )

    calendar = pd.read_csv(
        GTFS_DIR / "calendar.txt"
    )

    calendar_dates = pd.read_csv(
        GTFS_DIR / "calendar_dates.txt"
    )

    # --------------------------------------------------------
    # Convert calendar dates ONCE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Convert departure times ONCE
    # --------------------------------------------------------

    print("Converting departure times...")

    time_parts = stop_times["departure_time"].str.split(
        ":",
        expand=True
    ).astype(int)

    stop_times["departure_seconds"] = (
        time_parts[0] * 3600
        + time_parts[1] * 60
        + time_parts[2]
    )

    # --------------------------------------------------------
    # Add trip information ONCE
    # --------------------------------------------------------

    print("Merging trips...")

    stop_times = stop_times.merge(
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

    # --------------------------------------------------------
    # Add route information ONCE
    # --------------------------------------------------------

    print("Merging routes...")

    stop_times = stop_times.merge(
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

    # --------------------------------------------------------
    # Index stop_times by stop_id
    # --------------------------------------------------------

    print("Indexing stop times...")

    stop_times = stop_times.set_index("stop_id")

    print("GTFS preparation finished.")

    return (
        stops,
        stop_times,
        calendar,
        calendar_dates
    )


# ============================================================
# ACTIVE SERVICES
# ============================================================

def get_active_services(
    calendar,
    calendar_dates,
    date
):
    """
    Get all services operating on a specific date.
    """

    weekday = date.strftime("%A").lower()

    # --------------------------------------------------------
    # Normal weekly services
    # --------------------------------------------------------

    active_services = set(
        calendar.loc[
            (
                (calendar["start_date"] <= date)
                &
                (calendar["end_date"] >= date)
                &
                (calendar[weekday] == 1)
            ),
            "service_id"
        ]
    )

    # --------------------------------------------------------
    # Apply exceptions
    # --------------------------------------------------------

    exceptions = calendar_dates[
        calendar_dates["date"] == date
    ]

    for row in exceptions.itertuples(index=False):

        if row.exception_type == 1:
            active_services.add(
                row.service_id
            )

        elif row.exception_type == 2:
            active_services.discard(
                row.service_id
            )

    return active_services


# ============================================================
# DEPARTURE SCHEDULE
# ============================================================

def departure_schedule(
    stop_id,
    stop_times,
    active_services,
    stops,
    delays
):
    """
    Get the next 5 departures for a station.
    """

    # --------------------------------------------------------
    # Current time
    # --------------------------------------------------------

    now = datetime.datetime.now()

    current_seconds = (
        now.hour * 3600
        + now.minute * 60
        + now.second
    )

    # --------------------------------------------------------
    # Find child stops
    # --------------------------------------------------------

    station_id = "Parent" + stop_id

    child_stops = stops.loc[
        stops["parent_station"] == station_id,
        "stop_id"
    ].tolist()

    relevant_stop_ids = [
        stop_id
    ] + child_stops

    # --------------------------------------------------------
    # Find stop IDs that actually exist
    # --------------------------------------------------------

    available_stop_ids = (
        stop_times.index.intersection(
            relevant_stop_ids
        )
    )

    if len(available_stop_ids) == 0:
        return pd.DataFrame()

    # --------------------------------------------------------
    # Get departures
    # --------------------------------------------------------

    departures = stop_times.loc[
        available_stop_ids
    ]

    # --------------------------------------------------------
    # Filter active services
    # --------------------------------------------------------

    departures = departures[
        departures["service_id"].isin(
            active_services
        )
    ]

    if departures.empty:
        return pd.DataFrame()

    # --------------------------------------------------------
    # Filter future departures
    # --------------------------------------------------------

    departures = departures[
        departures["departure_seconds"]
        >= current_seconds
    ]

    if departures.empty:
        return pd.DataFrame()

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    departures = departures.sort_values(
        "departure_seconds"
    )

    # --------------------------------------------------------
    # Take only next 5
    # --------------------------------------------------------

    next_departures = departures.head(
        5
    ).copy()

    # --------------------------------------------------------
    # Add realtime delays
    # --------------------------------------------------------

    next_departures["delay"] = [
        delays.get(
            (trip_id, current_stop_id),
            0
        )
        for trip_id, current_stop_id in zip(
            next_departures["trip_id"],
            next_departures.index
        )
    ]

    # --------------------------------------------------------
    # Realtime departure
    # --------------------------------------------------------

    next_departures[
        "realtime_departure_seconds"
    ] = (
        next_departures["departure_seconds"]
        + next_departures["delay"]
    )

    # --------------------------------------------------------
    # Reset index
    # --------------------------------------------------------

    next_departures = (
        next_departures
        .reset_index()
    )

    # --------------------------------------------------------
    # Return only required data
    # --------------------------------------------------------

    return next_departures[
        [
            "stop_id",
            "departure_time",
            "realtime_departure_seconds",
            "route_short_name",
            "trip_headsign",
            "delay"
        ]
    ]


# ============================================================
# TRANSPORT
# ============================================================

def get_transport(
    stops,
    stop_times,
    calendar,
    calendar_dates
):
    """
    Get transport data for the dashboard.

    GTFS data is already prepared and stays in memory.
    Only realtime delays are downloaded here.
    """

    stop_id_seen = "ch:1:sloid:6002"
    stop_id_etzberg = "ch:1:sloid:90937"

    # --------------------------------------------------------
    # Get realtime delays
    # --------------------------------------------------------

    delays = get_delays()

    # --------------------------------------------------------
    # Get active services ONCE
    # --------------------------------------------------------

    now = datetime.datetime.now()

    today = pd.Timestamp(
        now.year,
        now.month,
        now.day
    )

    active_services = get_active_services(
        calendar,
        calendar_dates,
        today
    )

    # --------------------------------------------------------
    # Get departures
    # --------------------------------------------------------

    departures_seen = departure_schedule(
        stop_id_seen,
        stop_times,
        active_services,
        stops,
        delays
    )

    departures_etzberg = departure_schedule(
        stop_id_etzberg,
        stop_times,
        active_services,
        stops,
        delays
    )

    return (
        departures_seen,
        departures_etzberg
    )