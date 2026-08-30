import os
from garminconnect import Garmin


def get_health_data():
    email = os.getenv("garmin_mail")
    password = os.getenv("garmin_password")
    
    client = Garmin(email, password)
    client.login()
    
    return {
        "steps": client.get_steps(),
        "heart_rate": client.get_heart_rates(),
        "sleep": client.get_sleep_data(),
    }