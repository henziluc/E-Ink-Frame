import config
import os

from data.weather import get_weather
from data.transport.transport import get_transport
from data.garmin import get_health_data
from data.moon import get_moon_phase
from data.news import get_news
from data.quote import get_quote
from data.birthday import get_birthday_data
from logger import logger


def fetch_all_data(stop_times, calendar, calendar_dates, transport_info, data):
    
    weather_hourly = None
    weather_daily = None
    departures_seen = None
    departures_etzberg = None
    health_data = None
    moon_data = None
    news_data = None
    quote_data = None
    birthday_data = None


    # Get weather data from open-meteo.com. The data is returned as two pandas dataframes, one for hourly data and one for daily data.
    print("Getting weather data...")
    try:
        weather_hourly, weather_daily = get_weather(config.location)
        data["status"]["weather"] = True
    except:
        logger.exception("Weather data request failed")
        data["status"]["weather"] = False

    
    print("Getting transport data...")
    try:
        departures_seen, departures_etzberg = get_transport(stop_times, calendar, calendar_dates, transport_info)
        data["status"]["transport"] = True
    except:
        logger.exception("Transport request failed")
        data["status"]["transport"] = False


    print("Gettin health data...")
    try:
        health_data = get_health_data(data['health_data'])
        data["status"]["health"] = True
    except:
        logger.exception("Health request failed")
        data["status"]["health"] = False

 
    print("Getting moon phase data...")
    try:
        moon_data = get_moon_phase()
        data["status"]["moon"] = True
    except:
        logger.exception("Moon request failed")
        data["status"]["moon"] = False

    
    print("Getting news data...")
    try:
        news_data = get_news()
        data["status"]["news"] = True        
    except:
        logger.exception("News request failed")
        data["status"]["news"] = False        
    
    
    print("Getting quote data...")
    try:
        quote_data = get_quote()
        data["status"]["quote"] = True   
    except:
        logger.exception("Quote request failed")
        data["status"]["quote"] = False         

    
    print('Gettin birthdays...')
    try:
        birthday_data = get_birthday_data()
        data["status"]["birthday"] = True            
    except:
        logger.exception("Birthday request failed")
        data["status"]["birthday"] = False            
   
   
    return {
        "weather_hourly": weather_hourly,
        "weather_daily": weather_daily,
        "departures_seen": departures_seen,
        "departures_etzberg": departures_etzberg,
        "health_data": health_data,
        "moon_data": moon_data,
        "news_data": news_data,
        "quote_data": quote_data,
        "birthday_data": birthday_data
    }
