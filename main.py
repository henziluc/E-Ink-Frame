import config
from data.weather import get_weather


def main():

    print("Getting weather data...")

    weather_hourly, weather_daily = get_weather(config.location)

    if weather_hourly is None or weather_daily is None:
        print("Could not get weather data.")
        return


if __name__ == "__main__":
    main()