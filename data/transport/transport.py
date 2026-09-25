from pathlib import Path
from datetime import datetime
import pandas as pd

from .delays import get_delays


# ============================================================
# LOAD PREPROCESSED DATA
# ============================================================

def load_transport_data():

    BASE_DIR = Path(
        __file__
    ).resolve().parents[2]

    TRANSPORT_DIR = (
        BASE_DIR
        / "assets"
        / "transport"
    )


    stop_times = pd.read_pickle(
        TRANSPORT_DIR
        / "stop_times.pkl"
    )

    calendar = pd.read_pickle(
        TRANSPORT_DIR
        / "calendar.pkl"
    )

    calendar_dates = pd.read_pickle(
        TRANSPORT_DIR
        / "calendar_dates.pkl"
    )
    
    transport_info = pd.read_pickle(
            TRANSPORT_DIR
            / "transport_info.pkl"
        )



    return (
        stop_times,
        calendar,
        calendar_dates,
        transport_info
    )


# ============================================================
# ACTIVE SERVICES
# ============================================================

def get_active_services(
    calendar,
    calendar_dates,
    date
):

    weekday = date.strftime(
        "%A"
    ).lower()

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
    # Calendar exceptions
    # --------------------------------------------------------

    exceptions = calendar_dates[
        calendar_dates["date"] == date
    ]

    for row in exceptions.itertuples(
        index=False
    ):

        if row.exception_type == 1:

            # Service added
            active_services.add(
                row.service_id
            )

        elif row.exception_type == 2:

            # Service removed
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
    delays
):

    # --------------------------------------------------------
    # Current time
    # --------------------------------------------------------

    
    now = datetime.now()

    current_seconds = (
        now.hour * 3600
        + now.minute * 60
        + now.second
    )

    # --------------------------------------------------------
    # Filter station
    # --------------------------------------------------------

    stop_ids = stop_id["children"]
    
    
    departures = stop_times[
    stop_times["stop_id"].isin(stop_ids)
    ].copy()

    
    if departures.empty:
        return pd.DataFrame()

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
    # Take next 5
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
            next_departures["stop_id"]
        )
    ]

    # --------------------------------------------------------
    # Calculate realtime departure
    # --------------------------------------------------------

    next_departures[
        "realtime_departure_seconds"
    ] = (
        next_departures["departure_seconds"]
        + next_departures["delay"]
    )


    
    # --------------------------------------------------------
    # Return
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
    ].reset_index(
        drop=True
    )


# ============================================================
# GET TRANSPORT
# ============================================================

def get_transport(
    stop_times,
    calendar,
    calendar_dates,
    transport_info
):

    # --------------------------------------------------------
    # Station IDs
    # --------------------------------------------------------

    stop_id_seen = transport_info['seen']

    stop_id_etzberg = transport_info['etzberg']

    # --------------------------------------------------------
    # Get realtime delays
    # --------------------------------------------------------

    delays = get_delays()

    # --------------------------------------------------------
    # Current date
    # --------------------------------------------------------

    now = datetime.now()

    today = pd.Timestamp(
        now.year,
        now.month,
        now.day
    )

    # --------------------------------------------------------
    # Determine active services ONCE
    # --------------------------------------------------------

    active_services = get_active_services(
        calendar,
        calendar_dates,
        today
    )

    # --------------------------------------------------------
    # Seen
    # --------------------------------------------------------

    departures_seen = departure_schedule(
        stop_id_seen,
        stop_times,
        active_services,
        delays
    )

    # --------------------------------------------------------
    # Etzberg
    # --------------------------------------------------------

    departures_etzberg = departure_schedule(
        stop_id_etzberg,
        stop_times,
        active_services,
        delays
    )

    now = datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    
    
    return (
        departures_seen,
        departures_etzberg,
        formatted_datetime
    )