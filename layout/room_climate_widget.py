import math
import pandas as pd
from datetime import datetime, timedelta
import random
from pathlib import Path
from PIL import Image

from .helpers import draw_smooth_curve
from .fonts import font_very_small, font_small, font_normal, font_medium, font_large, fill_main, fill_gray, spacing_small, spacing_normal, spacing_medium, spacing_large

BASE_DIR = Path(__file__).resolve().parent.parent
path_temperatur = BASE_DIR / "assets" / "weather_symbol" / "thermometer.png"
path_humidity = BASE_DIR / "assets" / "weather_symbol" / "waterdrop.png"
path_CO2 = BASE_DIR / "assets" / "weather_symbol" / "leaf.png"
path_arrow_right = BASE_DIR / "assets" / "weather_symbol" / "arrow-right.png"
path_arrow_right_up = BASE_DIR / "assets" / "weather_symbol" / "arrow-up-right.png"
path_arrow_right_down = BASE_DIR / "assets" / "weather_symbol" / "arrow-down-right.png"

def display_room_climate_widget(draw, image, x_start, y_start, df):
    df = generate_test_data()
    y = y_start
    x = x_start
    icon_size = 40
    icon_size_small = 20
    graph_height = 100
    graph_width = 1200 - x_start - 30  # Adjust the width based on your layout
        
    draw.text((x, y), "Room Climate", font=font_large, fill=fill_main)
    y += spacing_large + 5
    y_stored = y
    latest_values = df[-1]
    compare_values = df[-5]
    
    # Draw temperature
    icon_temperature = Image.open(path_temperatur).convert("RGBA")
    icon_temperature = icon_temperature.resize((icon_size, icon_size))
    image.paste(icon_temperature, (x, y), icon_temperature)
    y += icon_size + 5
    draw.text((x, y), str(latest_values["temperature"]) + '°C', font=font_normal, fill=fill_main)
    y += spacing_normal
    draw.text((x, y), "Temp.", font=font_small, fill=fill_main)
    y += spacing_small
    diff_temperature = round(latest_values["temperature"] - compare_values ["temperature"])
    if diff_temperature > 0:
        icon_temperature_arrow = Image.open(path_arrow_right_up).convert("RGBA")
        diff_temperature = '+' + str(diff_temperature) + '°C'
    elif diff_temperature < 0:
        icon_temperature_arrow = Image.open(path_arrow_right_down).convert("RGBA")
        diff_temperature = str(diff_temperature) + '°C'
    else:
        icon_temperature_arrow = Image.open(path_arrow_right).convert("RGBA")
        diff_temperature = str(diff_temperature) + '°C'
        
    icon_temperature_arrow = icon_temperature_arrow.resize((icon_size_small, icon_size_small))
    image.paste(icon_temperature_arrow, (x, y + 2), icon_temperature_arrow)    
    draw.text((x + icon_size_small, y), diff_temperature, font=font_small, fill=fill_main)
    y += spacing_small
    draw.line([(x + 90, y_stored), (x + 90, y)], fill= fill_gray, width = 1) 
    x += 100
    y = y_stored
    
    # Draw Humidity
    icon_humidity = Image.open(path_humidity).convert("RGBA")
    icon_humidity = icon_humidity.resize((icon_size, icon_size))
    image.paste(icon_humidity, (x, y), icon_humidity)
    y += icon_size + 5
    draw.text((x, y), str(latest_values["humidity"]) + '%', font=font_small, fill=fill_main)
    y += spacing_normal
    draw.text((x, y), "Humidity", font=font_small, fill=fill_main)
    y += spacing_small
    diff_humidity = round(latest_values["humidity"] - compare_values ["humidity"])
    if diff_humidity > 0:
        icon_humidity_arrow = Image.open(path_arrow_right_up).convert("RGBA")
        diff_humidity = '+' + str(diff_humidity) + '%'
    elif diff_humidity < 0:
        icon_humidity_arrow = Image.open(path_arrow_right_down).convert("RGBA")
        diff_humidity = str(diff_humidity) + '%'
    else:
        icon_humidity_arrow = Image.open(path_arrow_right).convert("RGBA")
        diff_humidity = str(diff_humidity) + '%'
        
    icon_humidity_arrow = icon_humidity_arrow.resize((icon_size_small, icon_size_small))
    image.paste(icon_humidity_arrow, (x, y + 2), icon_humidity_arrow)    
    draw.text((x + icon_size_small, y), diff_humidity, font=font_small, fill=fill_main)
    y += spacing_small
    draw.line([(x + 90, y_stored), (x + 90, y)], fill= fill_gray, width = 1) 
    x += 100
    y = y_stored
   
        
    # Draw CO2
    icon_CO2 = Image.open(path_CO2).convert("RGBA")
    icon_CO2 = icon_CO2.resize((icon_size, icon_size))
    image.paste(icon_CO2, (x, y), icon_CO2)
    y += icon_size + 5
    draw.text((x, y), str(latest_values["co2"]) + 'ppm', font=font_small, fill=fill_main)
    y += spacing_normal
    draw.text((x, y), "CO2", font=font_small, fill=fill_main)
    y += spacing_small
    diff_co2 = round(latest_values["co2"] - compare_values ["co2"])
    if diff_co2 > 0:
        icon_co2_arrow = Image.open(path_arrow_right_up).convert("RGBA")
        diff_co2 = '+' + str(diff_co2) + 'ppm'
    elif diff_co2 < 0:
        icon_co2_arrow = Image.open(path_arrow_right_down).convert("RGBA")
        diff_co2 = str(diff_co2) + 'ppm'
    else:
        icon_co2_arrow = Image.open(path_arrow_right).convert("RGBA")
        diff_co2 = str(diff_co2) + 'ppm'
        
    icon_co2_arrow = icon_co2_arrow.resize((icon_size_small, icon_size_small))
    image.paste(icon_co2_arrow, (x, y + 2), icon_co2_arrow)    
    draw.text((x + icon_size_small, y), diff_co2, font=font_small, fill=fill_main)
    y += spacing_small
    #y += spacing_normal + graph_height
    #draw_room_climate_graph(draw, x_start, y, graph_width, graph_height, df, "co2", fill_main)
    
    
    
    
def draw_room_climate_graph(draw, x_start, y_start, graph_width, graph_height, data, value_key, color):
    offset = 3
    positions = []
    datapoints = 12
    data = data[-(datapoints + 1):]  # Get the last 12 data points

    if len(data) < 2:
        return  # Not enough data to draw a graph
    
    min_value = math.floor(data[value_key].min())  # Ensure the minimum value is at least 0
    max_value = math.ceil(data[value_key].max())  # Ensure the maximum value is at least 1 to avoid division by zero
    delta = max_value - min_value
    y_spacing = (graph_height - offset * 2) / delta
    x_spacing = graph_width / datapoints
    
    if min_value == max_value:
        return  # Avoid division by zero
    
    draw.line((x_start, y_start, x_start, y_start - graph_height), fill=fill_main, width=2)
    draw.line((x_start, y_start, x_start + graph_width, y_start), fill=fill_main, width=2)
    draw.text((x_start - 2, y_start - offset), str(min_value), font=font_small, fill=fill_main, anchor= 'rm')
    draw.text((x_start - 2, y_start - graph_height - offset), str(max_value), font=font_small, fill=fill_main, anchor= 'rm')
    
    start_time = data.iloc[0]["date"].strftime("%H:%M")
    end_time = data.iloc[-1]["date"].strftime("%H:%M")
    draw.text((x_start , y_start + 5), str(start_time), font=font_small, fill=fill_main, anchor= 'mt')
    draw.text((x_start + graph_width , y_start + 5), str(end_time), font=font_small, fill=fill_main, anchor= 'mt')
    x_increment = 0    
    
    for i in range(len(data)):
        value = data.iloc[i][value_key]
        
        x = x_start + x_increment * x_spacing
        y = y_start - offset - (value - min_value) * y_spacing
        positions.append((x, y))
        x_increment += 1
    
    # Draw the graph line
    draw_smooth_curve(draw, positions, fill_main, 2)
        

def generate_test_data():
    """
    Generate 24 hours of test data at 30-minute intervals.

    Returns:
        list[dict]: Data in the same format as the real sensor data.
    """

    data = []

    # Start 24 hours ago, rounded to the nearest 30 minutes
    now = datetime.now()
    now = now.replace(
        minute=30 if now.minute >= 30 else 0,
        second=0,
        microsecond=0
    )

    start = now - timedelta(hours=24)

    # Starting values
    co2 = 500
    humidity = 58.0
    temperature = 21.5

    for i in range(49):  # 24 hours = 48 intervals + current value
        timestamp = start + timedelta(minutes=30 * i)

        hour = timestamp.hour + timestamp.minute / 60

        # -------------------------
        # CO2
        # -------------------------
        # Higher during daytime/evening, lower during the night
        if 7 <= hour < 18:
            target_co2 = 700
        elif 18 <= hour < 23:
            target_co2 = 800
        else:
            target_co2 = 480

        co2 += (target_co2 - co2) * 0.15
        co2 += random.uniform(-15, 15)
        co2 = max(400, min(1200, co2))

        # -------------------------
        # Humidity
        # -------------------------
        # Slightly higher at night
        target_humidity = 60 if hour < 7 or hour >= 22 else 52

        humidity += (target_humidity - humidity) * 0.08
        humidity += random.uniform(-0.3, 0.3)
        humidity = max(40, min(70, humidity))

        # -------------------------
        # Temperature
        # -------------------------
        # Cooler at night, warmer during the afternoon
        temperature = (
            22.5
            + 2.5 * max(0, __import__("math").sin(
                ((hour - 7) / 24) * 2 * __import__("math").pi
            ))
        )

        temperature += random.uniform(-0.15, 0.15)

        data.append({
            "date": timestamp.strftime("%Y-%m-%d %H:%M"),
            "co2": round(co2),
            "humidity": round(humidity, 1),
            "temperature": round(temperature, 1)
        })

    return data
