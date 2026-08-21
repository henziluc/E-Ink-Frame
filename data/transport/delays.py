import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from google.transit import gtfs_realtime_pb2


# ============================================================
# Configuration
# ============================================================

# Project root:
# E-Ink-Frame/
#
# delays.py:
# E-Ink-Frame/data/transport/delays.py
#
# Therefore we need to go up three levels:
# transport -> data -> E-Ink-Frame
PROJECT_ROOT = Path(__file__).resolve().parents[2]

ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)


# Open Transport Data API
API_URL = (
    "https://api.opentransportdata.swiss/la/gtfs-rt"
)


# ============================================================
# Get realtime feed
# ============================================================

def get_realtime_feed():
    """
    Download and parse the Swiss public transport
    GTFS-Realtime feed.
    """

    token = os.getenv("OTD_API_TOKEN")

    if not token:
        raise RuntimeError(
            "OTD_API_TOKEN environment variable is not set"
        )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    

    response = requests.get(
        API_URL,
        headers=headers,
        timeout=30
    )

    

    response.raise_for_status()

    # Parse protobuf
    feed = gtfs_realtime_pb2.FeedMessage()

    feed.ParseFromString(response.content)



    return feed


# ============================================================
# Get all realtime delays
# ============================================================

def get_delays():
    """
    Return realtime delays indexed by:

        (trip_id, stop_id)

    Example:

        {
            (
                ".ojp-91-26-A.1.TA.526.j26",
                "ch:1:sloid:6002:1:1"
            ): 30,

            (
                ".ojp-91-26-A.1.TA.200.j26",
                "ch:1:sloid:6002:2:2"
            ): 90
        }

    Delay values are in seconds.
    """

    feed = get_realtime_feed()

    delays = {}

    for entity in feed.entity:

        # We are only interested in TripUpdates
        if not entity.HasField("trip_update"):
            continue

        trip_update = entity.trip_update

        # ----------------------------------------------------
        # Get trip ID
        # ----------------------------------------------------

        if not trip_update.HasField("trip"):
            continue

        trip_id = trip_update.trip.trip_id

        if not trip_id:
            continue

        # ----------------------------------------------------
        # Get stop updates
        # ----------------------------------------------------

        for stop_update in trip_update.stop_time_update:

            stop_id = stop_update.stop_id

            if not stop_id:
                continue

            # ------------------------------------------------
            # Departure delay
            # ------------------------------------------------

            if stop_update.HasField("departure"):

                delay = (
                    stop_update.departure.delay
                )

            # ------------------------------------------------
            # Some feeds may only provide arrival delay
            # ------------------------------------------------

            elif stop_update.HasField("arrival"):

                delay = (
                    stop_update.arrival.delay
                )

            else:
                continue

            delays[(trip_id, stop_id)] = delay


    return delays


# ============================================================
# Get delays for a specific station
# ============================================================

def get_station_delays(
    stop_id,
    stops
):
    """
    Get realtime delays for a station including
    its child stops.

    Example:

        stop_id = "ch:1:sloid:6002"

    will also check:

        ch:1:sloid:6002:1:1
        ch:1:sloid:6002:2:2
    """

    delays = get_delays()

    # --------------------------------------------------------
    # Find parent station
    # --------------------------------------------------------

    parent_id = "Parent" + stop_id

    child_stops = stops[
        stops["parent_station"] == parent_id
    ]["stop_id"].tolist()

    station_stops = [stop_id] + child_stops

    print("\n========== STATION REALTIME ==========")

    station_delays = {}

    for (trip_id, realtime_stop_id), delay in delays.items():

        if realtime_stop_id not in station_stops:
            continue

        station_delays[
            (trip_id, realtime_stop_id)
        ] = delay

        print(
            f"Trip: {trip_id} | "
            f"Stop: {realtime_stop_id} | "
            f"Delay: {delay} sec"
        )

    print("======================================\n")

    return station_delays


# ============================================================
# Helper
# ============================================================

def get_delay(
    trip_id,
    stop_id,
    delays
):
    """
    Get the delay for a specific trip and stop.

    Returns 0 if no realtime information exists.
    """

    return delays.get(
        (trip_id, stop_id),
        0
    )