import config
from data.weather import get_weather
from data.transport.transport import get_transport
from data.garmin import get_health_data
from data.moon import get_moon_phase
from data.news import get_news


def main():

    # Get weather data from open-meteo.com. The data is returned as two pandas dataframes, one for hourly data and one for daily data.
    print("Getting weather data...")
    weather_hourly, weather_daily = get_weather(config.location)

    if weather_hourly is None or weather_daily is None:
       print("Could not get weather data.")
       return

    
    print("Getting transport data...")
    #departures_seen, departures_etzberg = get_transport()

    #if departures_seen is None or departures_etzberg is None:
    #    print("Could not get transport data.")
    #    return
    
    print("Gettin health data...")
    #health_data = get_health_data()
    #if health_data is None:
        #print("Could not get health data.")
        #return
    
 
    print("Getting moon phase data...")
    #moon_data = get_moon_phase()
    #if moon_data is None:
        #print("Could not get moon phase data.")
        #return
    
    print("Getting news data...")
    news_data = get_news()
    if news_data is None:
        print("Could not get news data.")
        return
    print(news_data)
    
if __name__ == "__main__":
    main()