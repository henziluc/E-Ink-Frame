import config
from data.weather import get_weather
from data.transport.transport import get_transport

def main():

    # Get weather data from open-meteo.com. The data is returned as two pandas dataframes, one for hourly data and one for daily data.
    print("Getting weather data...")
    weather_hourly, weather_daily = get_weather(config.location)

    if weather_hourly is None or weather_daily is None:
       print("Could not get weather data.")
       return

    
    print("Getting transport data...")
    departures_seen, departures_etzberg = get_transport()
    
    if departures_seen is None or departures_etzberg is None:
        print("Could not get transport data.")
        return
    
if __name__ == "__main__":
    main()