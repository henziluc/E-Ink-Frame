from pathlib import Path
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

GTFS_DIR = BASE_DIR / "assets" / "gtfs"

OUTPUT_DIR = BASE_DIR / "assets" / "transport"

OUTPUT_FILE = OUTPUT_DIR / "transport_static.pkl"


# Your stations
STOP_IDS = [
    "ch:1:sloid:6002",   # Seen
    "ch:1:sloid:90937",  # Etzberg
]


# ============================================================
# HELPER
# ============================================================

def convert_gtfs_time(series):
    """
    Convert GTFS HH:MM:SS times to seconds.

    GTFS can contain times > 24:00:00, so we don't use
    datetime parsing here.
    """

    parts = series.str.split(":", expand=True).astype("int32")

    return (
        parts[0] * 3600
        + parts[1] * 60
        + parts[2]
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("GTFS PREPROCESSING")
    print("=" * 60)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # 1. Load stops
    # --------------------------------------------------------

    print("\n1. Loading stops...")

    stops = pd.read_csv(
        GTFS_DIR / "stops.txt",
        usecols=[
            "stop_id",
            "parent_station"
        ],
        dtype={
            "stop_id": "string",
            "parent_station": "string"
        }
    )

    # --------------------------------------------------------
    # 2. Find all relevant stops
    # --------------------------------------------------------

    print("\n2. Finding station child stops...")

    relevant_stop_ids = set(STOP_IDS)

    for stop_id in STOP_IDS:

        # Your GTFS structure uses Parent + stop_id
        station_id = "Parent" + stop_id

        children = stops.loc[
            stops["parent_station"] == station_id,
            "stop_id"
        ]

        relevant_stop_ids.update(
            children.dropna().tolist()
        )

    print(
        f"Relevant stops: {len(relevant_stop_ids)}"
    )

    for stop_id in relevant_stop_ids:
        print(f"  {stop_id}")

    # --------------------------------------------------------
    # 3. Load only required trip information
    # --------------------------------------------------------

    print("\n3. Loading trips...")

    trips = pd.read_csv(
        GTFS_DIR / "trips.txt",
        usecols=[
            "trip_id",
            "route_id",
            "service_id",
            "trip_headsign"
        ],
        dtype={
            "trip_id": "string",
            "route_id": "string",
            "service_id": "string",
            "trip_headsign": "string"
        }
    )

    # --------------------------------------------------------
    # 4. Load routes
    # --------------------------------------------------------

    print("\n4. Loading routes...")

    routes = pd.read_csv(
        GTFS_DIR / "routes.txt",
        usecols=[
            "route_id",
            "route_short_name",
            "route_long_name"
        ],
        dtype={
            "route_id": "string",
            "route_short_name": "string",
            "route_long_name": "string"
        }
    )

    # --------------------------------------------------------
    # 5. Read stop_times in chunks
    #
    # IMPORTANT:
    # We DON'T load the giant stop_times.txt into memory.
    # We process it in chunks and keep only your stations.
    # --------------------------------------------------------

    print("\n5. Processing stop_times.txt...")

    required_stop_times_columns = [
        "trip_id",
        "stop_id",
        "departure_time",
        "stop_sequence",
        "pickup_type",
        "drop_off_type"
    ]

    chunks = []

    chunk_number = 0
    total_rows = 0
    matching_rows = 0

    for chunk in pd.read_csv(
        GTFS_DIR / "stop_times.txt",
        usecols=required_stop_times_columns,
        dtype={
            "trip_id": "string",
            "stop_id": "string",
            "departure_time": "string",
            "stop_sequence": "int32",
            "pickup_type": "string",
            "drop_off_type": "string"
        },
        chunksize=250_000
    ):

        chunk_number += 1
        total_rows += len(chunk)

        # Only keep our stations
        filtered = chunk[
            chunk["stop_id"].isin(
                relevant_stop_ids
            )
        ].copy()

        if not filtered.empty:

            matching_rows += len(filtered)

            # Convert time now, on the laptop
            filtered["departure_seconds"] = (
                convert_gtfs_time(
                    filtered["departure_time"]
                )
            )

            chunks.append(filtered)

        print(
            f"  Chunk {chunk_number}: "
            f"{total_rows:,} rows processed, "
            f"{matching_rows:,} relevant rows"
        )

    if not chunks:
        raise RuntimeError(
            "No stop_times found for the requested stations."
        )

    stop_times = pd.concat(
        chunks,
        ignore_index=True
    )

    print(
        f"\nFound {len(stop_times):,} relevant departures."
    )

    # --------------------------------------------------------
    # 6. Merge trip information
    # --------------------------------------------------------

    print("\n6. Adding trip information...")

    stop_times = stop_times.merge(
        trips,
        on="trip_id",
        how="left"
    )

    # --------------------------------------------------------
    # 7. Merge route information
    # --------------------------------------------------------

    print("\n7. Adding route information...")

    stop_times = stop_times.merge(
        routes,
        on="route_id",
        how="left"
    )

    # --------------------------------------------------------
    # 8. Keep only columns required by Raspberry Pi
    # --------------------------------------------------------

    stop_times = stop_times[
        [
            "stop_id",
            "trip_id",
            "departure_time",
            "departure_seconds",
            "service_id",
            "route_short_name",
            "route_long_name",
            "trip_headsign"
        ]
    ]

    # --------------------------------------------------------
    # 9. Sort
    # --------------------------------------------------------

    print("\n8. Sorting departures...")

    stop_times = stop_times.sort_values(
        [
            "stop_id",
            "departure_seconds"
        ]
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # 10. Load calendar
    # --------------------------------------------------------

    print("\n9. Loading calendar...")

    calendar = pd.read_csv(
        GTFS_DIR / "calendar.txt",
        dtype={
            "service_id": "string"
        }
    )

    # Convert dates once
    calendar["start_date"] = pd.to_datetime(
        calendar["start_date"].astype(str),
        format="%Y%m%d"
    )

    calendar["end_date"] = pd.to_datetime(
        calendar["end_date"].astype(str),
        format="%Y%m%d"
    )

    # --------------------------------------------------------
    # 11. Load calendar exceptions
    # --------------------------------------------------------

    print("\n10. Loading calendar exceptions...")

    calendar_dates = pd.read_csv(
        GTFS_DIR / "calendar_dates.txt",
        dtype={
            "service_id": "string"
        }
    )

    calendar_dates["date"] = pd.to_datetime(
        calendar_dates["date"].astype(str),
        format="%Y%m%d"
    )

    # --------------------------------------------------------
    # 12. Create transport object
    # --------------------------------------------------------

    transport_data = {
        "stop_times": stop_times,
        "calendar": calendar,
        "calendar_dates": calendar_dates,
        "stations": {
            "seen": "ch:1:sloid:6002",
            "etzberg": "ch:1:sloid:90937"
        }
    }

    # --------------------------------------------------------
    # 13. Save
    # --------------------------------------------------------

    print("\n11. Saving preprocessed data...")

    stop_times_memory = stop_times.memory_usage(
        deep=True
    ).sum()

    print(
        f"Processed stop_times RAM size: "
        f"{stop_times_memory / 1024 / 1024:.2f} MB"
    )

    stop_times.to_pickle(
        OUTPUT_DIR / "stop_times.pkl"
    )

    calendar.to_pickle(
        OUTPUT_DIR / "calendar.pkl"
    )

    calendar_dates.to_pickle(
        OUTPUT_DIR / "calendar_dates.pkl"
    )

    # Small metadata file
    import pickle

    with open(
        OUTPUT_DIR / "transport_info.pkl",
        "wb"
    ) as file:

        pickle.dump(
            transport_data["stations"],
            file
        )

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)

    print(
        f"\nOutput directory:\n"
        f"{OUTPUT_DIR}"
    )

    print(
        "\nFiles created:"
    )

    print(
        "  stop_times.pkl"
    )

    print(
        "  calendar.pkl"
    )

    print(
        "  calendar_dates.pkl"
    )

    print(
        "  transport_info.pkl"
    )


if __name__ == "__main__":
    main()