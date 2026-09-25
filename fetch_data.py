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
    weather_timestamp = None
    departures_seen = None
    departures_etzberg = None
    transport_timestamp = None
    health_data = None
    healt_timestamp = None
    moon_data = None
    moon_timestamp = None
    news_data = None
    news_timestamp = None
    quote_data = None
    quote_timestamp = None
    birthday_data = None
    birthday_timestamp = None
    


    # Get weather data from open-meteo.com. The data is returned as two pandas dataframes, one for hourly data and one for daily data.
    print("Getting weather data...")
    try:
        weather_hourly, weather_daily, weather_timestamp = get_weather(config.location)
        weather_status = True
    except:
        logger.exception("Weather data request failed")
        weather_status = False

    if weather_timestamp is None:
            weather_timestamp = data['status']['weather_timestamp']
    
    
    print("Getting transport data...")
    try:
        departures_seen, departures_etzberg, transport_timestamp = get_transport(stop_times, calendar, calendar_dates, transport_info)
        transport_status = True
    except:
        logger.exception("Transport request failed")
        transport_status = False
        
    if transport_timestamp is None:
        transport_timestamp = data['status']['transport_timestamp']


    print("Gettin health data...")
    try:
        health_data, health_timestamp = get_health_data(data['health_data'])
        health_status = True
    except:
        logger.exception("Health request failed")
        health_status = False

    if health_timestamp is None:
        health_timestamp = data['status']['health_timestamp']
            
            
    print("Getting moon phase data...")
    try:
        moon_data, moon_timestamp = get_moon_phase()
        moon_status = True
    except:
        logger.exception("Moon request failed")
        moon_status = False

    if moon_timestamp is None:
        moon_timestamp = data['status']['moon_timestamp']
        
    
    print("Getting news data...")
    try:
        news_data, news_timestamp = get_news()
        news_status = True        
    except:
        logger.exception("News request failed")
        news_status = False        
    
    if news_timestamp is None:
        news_timestamp = data['status']['news_timestamp']
            
    
    print("Getting quote data...")
    try:
        quote_data, quote_timestamp = get_quote(data['quote_data'])
        quote_status = True   
    except:
        logger.exception("Quote request failed")
        quote_status = False         

    if quote_timestamp is None:
        quote_timestamp = data['status']['quote_timestamp']
    
    
    print('Gettin birthdays...')
    try:
        birthday_data, birthday_timestamp = get_birthday_data()
        birthday_status = True            
    except:
        logger.exception("Birthday request failed")
        birthday_status = False            
   
    if birthday_timestamp is None:
        birthday_timestamp = data['status']['birthday_timestamp']    
        
        
    
    return {
        "weather_hourly": weather_hourly,
        "weather_daily": weather_daily,
        "departures_seen": departures_seen,
        "departures_etzberg": departures_etzberg,
        "health_data": health_data,
        "moon_data": moon_data,
        "news_data": news_data,
        "quote_data": quote_data,
        "birthday_data": birthday_data,
        "status" : {
            'weather' : weather_status,
            'weather_timestamp' : weather_timestamp,
            'transport' : transport_status,
            'transport_timestamp' : transport_timestamp,
            'health' : health_status,
            'health_timestamp' : health_timestamp,
            'moon' : moon_status,
            'moon_timestamp' : moon_timestamp,
            'news' : news_status,
            'news_timestamp' : news_timestamp,
            'quote' : quote_status,
            'quote_timestamp' : quote_timestamp,
            'birthday' : birthday_status,
            'birthday_timestamp' : birthday_timestamp,
        }
    }
