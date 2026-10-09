import json
from pathlib import Path
from datetime import datetime
import pandas as pd

def save_data_to_file(data, file_path):
    
    #convert datetime objects to string for JSON serialization
    data["health_data"]["Luca"]["last updated"] = datetime.isoformat(data["health_data"]["Luca"]["last updated"])
    data["health_data"]["Jojo"]["last updated"] = datetime.isoformat(data["health_data"]["Jojo"]["last updated"])
    
    data["status"]["weather_timestamp"] = datetime.isoformat(data["status"]["weather_timestamp"]) if data["status"]["weather_timestamp"] else None
    data["status"]["transport_timestamp"] = datetime.isoformat(data["status"]["transport_timestamp"]) if data["status"]["transport_timestamp"] else None
    data["status"]["health_timestamp"] = datetime.isoformat(data["status"]["health_timestamp"]) if data["status"]["health_timestamp"] else None
    data["status"]["moon_timestamp"] = datetime.isoformat(data["status"]["moon_timestamp"]) if data["status"]["moon_timestamp"] else None
    data["status"]["news_timestamp"] = datetime.isoformat(data["status"]["news_timestamp"]) if data["status"]["news_timestamp"] else None
    data["status"]["quote_timestamp"] = datetime.isoformat(data["status"]["quote_timestamp"]) if data["status"]["quote_timestamp"] else None
    data["status"]["birthday_timestamp"] = datetime.isoformat(data["status"]["birthday_timestamp"]) if data["status"]["birthday_timestamp"] else None

    data["weather_hourly"]["date"] = data["weather_hourly"]["date"].apply(lambda x: x.isoformat() if pd.notna(x) else None)
    data["weather_hourly"] = data["weather_hourly"].to_dict(orient='records')
    
    data["weather_daily"]["date"] = data["weather_daily"]["date"].apply(lambda x: x.isoformat() if pd.notna(x) else None)
    data["weather_daily"]["sunrise"] = data["weather_daily"]["sunrise"].apply(lambda x: x.isoformat() if pd.notna(x) else None)
    data["weather_daily"]["sunset"] = data["weather_daily"]["sunset"].apply(lambda x: x.isoformat() if pd.notna(x) else None)
    data["weather_daily"] = data["weather_daily"].to_dict(orient='records')
    
    for birthday in data["birthday_data"]:
        birthday["date"] = birthday["date"].isoformat() if pd.notna(birthday["date"]) else None
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
        
        
def load_data_from_file(file_path):
 
    if file_path.exists():
        # Load existing data
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            
        # Restore health timestamps
        data["health_data"]["Luca"]["last updated"] = datetime.fromisoformat(
            data["health_data"]["Luca"]["last updated"]
        ) if data["health_data"]["Luca"]["last updated"] else None

        data["health_data"]["Jojo"]["last updated"] = datetime.fromisoformat(
            data["health_data"]["Jojo"]["last updated"]
        ) if data["health_data"]["Jojo"]["last updated"] else None


        # Restore status timestamps
        for key in [
            "weather_timestamp",
            "transport_timestamp",
            "health_timestamp",
            "moon_timestamp",
            "news_timestamp",
            "quote_timestamp",
            "birthday_timestamp"
        ]:
            data["status"][key] = (
                datetime.fromisoformat(data["status"][key])
                if data["status"][key] else None
            )


        # Restore weather DataFrames
        data["weather_hourly"] = pd.DataFrame(data["weather_hourly"])
        data["weather_hourly"]["date"] = pd.to_datetime(
            data["weather_hourly"]["date"]
        )

        data["weather_daily"] = pd.DataFrame(data["weather_daily"])

        for column in ["date", "sunrise", "sunset"]:
            data["weather_daily"][column] = pd.to_datetime(
                data["weather_daily"][column]
            )


        # Restore birthday dates
        for birthday in data["birthday_data"]:
            birthday["date"] = (
                datetime.fromisoformat(birthday["date"])
                if birthday["date"] else None
            )    
        
    else:
        # Initialize data
        data = {
            "weather_hourly": None,
            "weather_daily": None,
            "departures_seen": None,
            "departures_etzberg": None,
            "health_data": {
                "Luca": {
                    "last updated": datetime(2000, 1, 1, 0, 0),
                    "activity_distance": None,
                    "activity_pace": None,
                    },
                "Jojo": {
                    "last updated": datetime(2000, 1, 1, 0, 0),
                    "activity_distance": None,
                    "activity_pace": None,
                    }
            },
            "moon_data": None,
            "news_data": None,
            "quote_data": [],
            "birthday_data": None,
            "status" : {
                'weather' : None,
                'weather_timestamp' : None,
                'transport' : None,
                'transport_timestamp' : None,
                'health' : None,
                'health_timestamp' : None,
                'moon' : None,
                'moon_timestamp' : None,
                'news' : None,
                'news_timestamp' : None,
                'quote' : None,
                'quote_timestamp' : None,
                'birthday' : None,
                'birthday_timestamp' : None,
            }}
        
    return data