import requests
import json
import os
from datetime import datetime, timedelta


# =========================================================
# CONFIGURATION
# =========================================================

API_URL = "https://www.thesportsdb.com/api/v1/json/123"

BAYERN_ID = "133664"
WINTERTHUR_ID = "138984"

CACHE_FILE = "data/sport_cache.json"

# Cache sport data for this many hours
CACHE_HOURS = 6


# =========================================================
# API REQUEST
# =========================================================

def api_request(endpoint, params=None):

    url = f"{API_URL}/{endpoint}"

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    # Too many requests
    if response.status_code == 429:

        print("TheSportsDB rate limit reached.")
        print("Wait about 1 minute before trying again.")

        return None

    response.raise_for_status()

    return response.json()


# =========================================================
# GET EVENTS FOR ONE DAY
# =========================================================

def get_events_on_day(day):

    data = api_request(
        "eventsday.php",
        {
            "d": day.strftime("%Y-%m-%d"),
            "s": "Soccer"
        }
    )

    if data is None:
        return None

    return data.get("events") or []


# =========================================================
# EVENT DATETIME
# =========================================================

def get_event_datetime(event):

    timestamp = event.get("strTimestamp")

    if timestamp:

        try:
            return datetime.fromisoformat(timestamp)

        except ValueError:
            pass

    date_value = event.get("dateEventLocal")
    time_value = event.get("strTimeLocal")

    if date_value and time_value:

        try:
            return datetime.strptime(
                f"{date_value} {time_value}",
                "%Y-%m-%d %H:%M:%S"
            )

        except ValueError:
            pass

    return None


# =========================================================
# CHECK TEAM
# =========================================================

def is_team_event(event, team_id):

    return (
        str(event.get("idHomeTeam")) == str(team_id)
        or
        str(event.get("idAwayTeam")) == str(team_id)
    )


# =========================================================
# FORMAT EVENT
# =========================================================

def format_event(event):

    event_datetime = get_event_datetime(event)

    return {

        "id": event.get("idEvent"),

        # Convert datetime to string so json.dumps() works
        "date": (
            event_datetime.strftime("%Y-%m-%d %H:%M")
            if event_datetime
            else None
        ),

        "home": event.get("strHomeTeam"),

        "away": event.get("strAwayTeam"),

        "home_score": event.get("intHomeScore"),

        "away_score": event.get("intAwayScore"),

        "league": event.get("strLeague"),

        "status": event.get("strStatus"),

        "venue": event.get("strVenue"),

        "home_badge": event.get("strHomeTeamBadge"),

        "away_badge": event.get("strAwayTeamBadge"),
    }


# =========================================================
# NEXT GAME
# =========================================================

def get_next_game(team_id):

    data = api_request(
        "eventsnext.php",
        {
            "id": team_id
        }
    )

    if data is None:
        return None

    events = data.get("events") or []

    now = datetime.now()

    future_events = []

    for event in events:

        if not is_team_event(event, team_id):
            continue

        event_datetime = get_event_datetime(event)

        if event_datetime is None:
            continue

        if event_datetime <= now:
            continue

        if event.get("strPostponed") == "yes":
            continue

        future_events.append(event)

    if not future_events:
        return None

    future_events.sort(
        key=get_event_datetime
    )

    return format_event(future_events[0])


# =========================================================
# LAST GAME
# =========================================================

def get_last_game(team_id):

    data = api_request(
        "eventslast.php",
        {
            "id": team_id
        }
    )

    if data is None:
        return None

    events = (
        data.get("results")
        or data.get("events")
        or []
    )

    now = datetime.now()

    finished_events = []

    for event in events:

        if not is_team_event(event, team_id):
            continue

        event_datetime = get_event_datetime(event)

        if event_datetime is None:
            continue

        if event_datetime > now:
            continue

        status = event.get("strStatus")

        if status not in [
            "FT",
            "AET",
            "PEN"
        ]:
            continue

        finished_events.append(event)

    if not finished_events:
        return None

    finished_events.sort(
        key=get_event_datetime,
        reverse=True
    )

    return format_event(finished_events[0])


# =========================================================
# FIND AWAY GAME
# =========================================================

def find_away_game(
    team_id,
    days=7,
    future=True
):

    today = datetime.now().date()

    if future:

        dates = [
            today + timedelta(days=i)
            for i in range(1, days + 1)
        ]

    else:

        dates = [
            today - timedelta(days=i)
            for i in range(1, days + 1)
        ]

    for check_date in dates:

        events = get_events_on_day(check_date)

        # Stop immediately if rate limit was reached
        if events is None:
            return None

        for event in events:

            # We specifically want an away game
            if str(event.get("idAwayTeam")) != str(team_id):
                continue

            event_datetime = get_event_datetime(event)

            if event_datetime is None:
                continue

            # -----------------------------------------
            # FUTURE
            # -----------------------------------------

            if future:

                if event_datetime <= datetime.now():
                    continue

                if event.get("strPostponed") == "yes":
                    continue

                return format_event(event)

            # -----------------------------------------
            # PAST
            # -----------------------------------------

            else:

                if event_datetime > datetime.now():
                    continue

                if event.get("strStatus") not in [
                    "FT",
                    "AET",
                    "PEN"
                ]:
                    continue

                return format_event(event)

    return None


# =========================================================
# TEAM DATA
# =========================================================

def get_team_data(team_id, team_name):

    print(f"Getting data for {team_name}...")

    # -----------------------------------------------------
    # NEXT GAME
    # -----------------------------------------------------

    next_game = get_next_game(team_id)

    # The free API only returns home events.
    # Therefore search for an away game if necessary.

    if next_game is None:

        print(
            f"Searching away games for {team_name}..."
        )

        next_game = find_away_game(
            team_id,
            days=7,
            future=True
        )

    # -----------------------------------------------------
    # LAST GAME
    # -----------------------------------------------------

    last_game = get_last_game(team_id)

    # Again, search for an away game if necessary.

    if last_game is None:

        print(
            f"Searching previous away games for {team_name}..."
        )

        last_game = find_away_game(
            team_id,
            days=7,
            future=False
        )

    return {

        "name": team_name,

        "next": next_game,

        "last": last_game
    }


# =========================================================
# CACHE
# =========================================================

def load_cache():

    if not os.path.exists(CACHE_FILE):
        return None

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            cache = json.load(file)

        timestamp = datetime.fromisoformat(
            cache["timestamp"]
        )

        age = datetime.now() - timestamp

        if age < timedelta(
            hours=CACHE_HOURS
        ):

            print("Using cached sport data.")

            return cache["data"]

    except Exception as e:

        print(
            f"Could not load sport cache: {e}"
        )

    return None


def save_cache(data):

    cache = {

        "timestamp":
            datetime.now().isoformat(),

        "data": data
    }

    cache_directory = os.path.dirname(
        CACHE_FILE
    )

    if cache_directory:

        os.makedirs(
            cache_directory,
            exist_ok=True
        )

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            cache,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# MAIN SPORT FUNCTION
# =========================================================

def get_sport_data():

    # -----------------------------------------------------
    # Try cache first
    # -----------------------------------------------------

    cached_data = load_cache()

    if cached_data is not None:

        return cached_data

    # -----------------------------------------------------
    # Get Bayern
    # -----------------------------------------------------

    bayern = get_team_data(
        BAYERN_ID,
        "Bayern München"
    )

    # -----------------------------------------------------
    # Get Winterthur
    # -----------------------------------------------------

    winterthur = get_team_data(
        WINTERTHUR_ID,
        "FC Winterthur"
    )

    # -----------------------------------------------------
    # Build result
    # -----------------------------------------------------

    data = {

        "football": [

            bayern,

            winterthur
        ]
    }

    # -----------------------------------------------------
    # Save cache
    # -----------------------------------------------------

    save_cache(data)

    return data


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    sport_data = get_sport_data()

    print()

    print(
        json.dumps(
            sport_data,
            indent=4,
            ensure_ascii=False
        )
    )