import requests

def get_moon_phase(icon_dir="assets/icons/moon"):
    """
    Get the current moon phase from CycleCalcs and return
    the phase name, illumination and corresponding icon path.
    """

    url = "https://www.cyclecalcs.com/v2/moon"
    for attempt in range(2):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()["data"]["phase"]

            phase = data["name"]
            waxing = data["waxing"]
            illumination = data["illumination_percent"]



            return {
                "phase": phase,
                "waxing": waxing,
                "illumination": illumination,
            }

        except requests.RequestException as e:
            print(f"Moon API error: {e}")
            return {
                "phase": 'unkown',
                "waxing": False,
                "illumination": 0,
            }
        except (KeyError, ValueError) as e:
            print(f"Invalid moon API response: {e}")
        return {
                "phase": 'unkown',
                "waxing": False,
                "illumination": 0,
            }