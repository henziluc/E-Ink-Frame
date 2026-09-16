import datetime
import math
from PIL import Image
from pathlib import Path

from .fonts import font_very_small, font_small, font_medium, font_large, fill_main, fill_rain_graph, spacing_small, spacing_normal, spacing_large
from .helpers import draw_centered_text, draw_smooth_curve, draw_dotted_line

BASE_DIR = Path(__file__).resolve().parent.parent

# new function that is on top of the screen and shows the temperatur curve and rain from now for the next 48h.
# Plus daily maximum and minimum temperatur with a weather picture
def display_weather_graph(draw, image, df_hourly, df_daily, x_start, y_start):
    y = y_start
    graph_height = 150
    print_hour = 1
    x_day_start = []
    
    now = datetime.datetime.now()
    now_hour = now.hour
        
    # Draw widget title
    draw.text((x_start, y), 'Weather Forecast', font=font_large, fill=fill_main)
    y += spacing_large + spacing_small + spacing_normal
    
    # calulate hour spacing on the graph
    hour_spacing = (1200 - x_start * 2) / 48
    
    # draw top horizontal line of the graph
    draw.line([(x_start, y), (1200-x_start, y)], fill= fill_main, width = 0)
    
    #draw vertical line at beginning of graph
    draw.line([(x_start, y),(x_start, y + graph_height)], fill= fill_main, width = 0)
    
    y += graph_height
    
    # draw graph
    for i in range(0, 49):
        hour = now_hour + i
        
        # Reduce hour to 24h format
        if hour > 48:
            hour -= 48
        elif hour > 24:
            hour -= 24
        
        # Add leading zero for hour smaller 10
        if hour < 10:
            hour = '0' + str(hour)       
        else:
            hour = str(hour)
        
        # Draw vertical line where the day ends
        if hour == '24':
            draw.line([(x_start + i * hour_spacing, y),(x_start + i * hour_spacing, y - graph_height)], fill= fill_main, width = 0)
            x_day_start.append(x_start + i * hour_spacing)
        
        draw.line([(x_start + i * hour_spacing, y), (x_start + i * hour_spacing, y - 5)], fill= fill_main, width = 0)
        
        # Draw text at every second hour    
        if  print_hour == 1:
            draw_centered_text(draw, hour + ':00',(x_start + i * hour_spacing - 20, y + 5, x_start + i * hour_spacing + 20, y + 15), font_very_small, fill_main)
            print_hour = 0
        else:
            print_hour = 1
            
    # draw bottom horizontal line of the graph       
    draw.line([(x_start, y), (1200-x_start, y)], fill= fill_main, width = 0)
    
    y -= graph_height + spacing_small + spacing_normal
    
    # Draw daily weather overview
    draw_daily_wether_decription(draw, df_daily, x_start, y , x_day_start[0], 0)
    draw_daily_wether_decription(draw, df_daily, x_day_start[0], y , x_day_start[1], 1)
    draw_daily_wether_decription(draw, df_daily, x_day_start[1], y , 1200 - x_start, 2)
    
    y +=   spacing_small
    
    # get hourly data from now on
    index = df_hourly[df_hourly['date'].dt.hour == now_hour].index[0]
    df_from_now = df_hourly.loc[index: index+48]
    df_from_now = df_from_now.reset_index(drop=True) 
        
    sunrise = df_daily.loc[1,'sunrise'].hour
    sunset = df_daily.loc[1,'sunset'].hour
    
    draw_weather_icons(image, df_from_now, x_start, y, sunrise, sunset, hour_spacing)
    
    y +=  spacing_normal
    
    draw_rain_graph(draw, df_from_now, x_start, y, graph_height, hour_spacing)
    
    draw_temperature_graph(draw, df_from_now, x_start, y, graph_height, hour_spacing)
    

def draw_daily_wether_decription(draw, df_daily, x_start, y_start, x_end, day):
    x = x_start
    y = y_start
    x_delta = x_end - x_start
    
    
    
    text = str(round(df_daily.loc[day, 'temperature_2m_min'], 1)) + '°C / ' + str(round(df_daily.loc[day, 'temperature_2m_max'], 1)) + '°C'
    
    if x_delta > 200:
        draw_centered_text(draw, text, (x_start, y_start, x_end, y + 20), font_small, fill_main) 
   

def draw_temperature_graph(draw, df_from_now, x_start, y_start, graph_height, hour_spacing):
    offset = 8
    positions_rain = []
    
    # calculate spacing per degree
    temp_min = math.floor(df_from_now['temperature_2m'].min())
    temp_max = math.ceil(df_from_now['temperature_2m'].max())
    temp_delta = math.ceil(temp_max - temp_min)
    degrees_spacing = (graph_height - offset * 2) / temp_delta
    
    # calculate x and y position of every hourly temperature value
    for i in range(0, 49):
        # define X positions of curve
        positions_x = i * hour_spacing + x_start
        
        # define X positions of curve
        temperature = df_from_now.loc[i,'temperature_2m']
        positions_y = (temp_max - temperature) * degrees_spacing + offset + y_start

        positions_rain.append((positions_x, positions_y))
        

    # draw temperature curve    
    draw_smooth_curve(draw, positions_rain, fill_main, 2)
    
    # draw temperature scale
    for i in range(0, temp_delta + 1):
        y = y_start + offset + i * degrees_spacing
        draw.line([(x_start, y),(x_start + 5, y)], fill= fill_main, width = 0)
        
        # draw every second temperature value
        temp = temp_max - i
        if i % 2 == 0:
            draw.text((x_start - 2, y), str(temp), font=font_small, fill=fill_main, anchor= 'rm')
            
        # draw dotted helper lines at every 5°C step
        if temp % 5 == 0:
            draw_dotted_line(draw,(x_start, y ),(1200-x_start, y), dot_length=2, gap=8, fill=fill_main, width=1)
        

def draw_weather_icons(image, df_from_now, x_start, y_start, sunrise, sunset, hour_spacing):
    
    # loop through the next 48h in 2h steps
    for i in range(0, 49, 2):
         
        # define if day or night symbol  
        hour = df_from_now.loc[i, 'date'].hour
        if sunrise < hour < sunset:
            day = True
        else:
            day = False
        
        # get icon path and print it    
        icon_path = get_weather_icon(df_from_now.loc[i,'weather_code'], day)
        icon = Image.open(icon_path).convert("RGBA")
        icon = icon.resize((40, 40))

        x = int((x_start + i * hour_spacing) - icon.width / 2)
        y = int(y_start)
        
        image.paste(icon, (x, y), icon)


def draw_rain_graph(draw, df_from_now, x_start, y_start, graph_height, hour_spacing):
    offset = 20
    
    # calculate spacing per mm precipitation
    rain_max = math.ceil(df_from_now['precipitation'].max())
    rain_spacing = (graph_height - offset) / rain_max
    
    # draw rain bargraph
    for i in range(0, 49):
        precipitation = df_from_now.loc[i,'precipitation']
        x1 = x_start + hour_spacing * i - math.floor(hour_spacing / 2)
        x2 = x_start + hour_spacing * i + math.floor(hour_spacing / 2)
        y1 = y_start + graph_height - precipitation * rain_spacing
        y2 = y_start + graph_height
        draw.rectangle([(x1, y1),(x2, y2)], fill= fill_rain_graph)

    
    # draw rain scale
    if rain_max > 0:
        for i in range(0, rain_max + 1):
            y = y_start + offset + i * rain_spacing
            draw.line([(1200-x_start, y),(1200 - x_start - 5, y)], fill= fill_main, width = 0)
            
            # draw every second rain value
            rain = rain_max - i
            if i % 2 == 0 and rain > 0:
                draw.text((1200- x_start + 2, y), str(rain), font=font_small, fill=fill_main, anchor= 'lm')
            
    draw.line([(1200-x_start, y_start),(1200-x_start, y_start + graph_height)], fill= fill_main, width = 0)

    
def get_weather_icon(code, day):
    match code:
        case 0 | 1:
            if day:
                path = BASE_DIR / "assets" / "weather_symbol" / "clear-day.png"
            else:
                path = BASE_DIR / "assets" / "weather_symbol" / "clear-night.png"
        case 2:
            if day:
                path = BASE_DIR / "assets" / "weather_symbol" / "partly-cloudy-day.png"
            else:
                path = BASE_DIR / "assets" / "weather_symbol" / "partly-cloudy-night.png"
        case 3:
            path = BASE_DIR / "assets" / "weather_symbol" / "cloudy.png"
        case 45 | 48:
            path = BASE_DIR / "assets" / "weather_symbol" / "fog.png"
        case 51 | 53 | 55 | 80:
            if day:
                path = BASE_DIR / "assets" / "weather_symbol" / "showers-day.png"
            else:
                path = BASE_DIR / "assets" / "weather_symbol" / "showers-night.png"
        case 61 | 63 | 65 | 81 | 82:
            path = BASE_DIR / "assets" / "weather_symbol" / "rain.png"
        case 66 | 67:
            if day:
                path = BASE_DIR / "assets" / "weather_symbol" / "rain-snow-showers-day.png"
            else:
                path = BASE_DIR / "assets" / "weather_symbol" / "rain-snow-showers-night.png"
        case 71 | 73 | 85:
            if day:
                path = BASE_DIR / "assets" / "weather_symbol" / "snow-showers-day.png"
            else:
                path = BASE_DIR / "assets" / "weather_symbol" / "snow-showers-night.png"
        case 75 | 77 | 86:
            path = BASE_DIR / "assets" / "weather_symbol" / "snow.png"                
        case 95:                
            path = BASE_DIR / "assets" / "weather_symbol" / "thunder-rain.png"
        case 96 | 99:
            path = BASE_DIR / "assets" / "weather_symbol" / "hail.png"
        case _:    
            path = BASE_DIR / "assets" / "weather_symbol" / "unknown.png"        
            
            
    return path


def get_weather_description(code):

    weather_codes = {
        0: "Klar",
        1: "Überwiegend klar",
        2: "Teilweise bewölkt",
        3: "Bewölkt",

        45: "Nebel",
        48: "Raureifnebel",

        51: "Leichter Nieselregen",
        53: "Mäßiger Nieselregen",
        55: "Starker Nieselregen",

        56: "Leichter gefrierender Nieselregen",
        57: "Starker gefrierender Nieselregen",

        61: "Leichter Regen",
        63: "Mäßiger Regen",
        65: "Starker Regen",

        66: "Leichter gefrierender Regen",
        67: "Starker gefrierender Regen",

        71: "Leichter Schneefall",
        73: "Mäßiger Schneefall",
        75: "Starker Schneefall",

        77: "Schneekörner",

        80: "Leichte Regenschauer",
        81: "Mäßige Regenschauer",
        82: "Starke Regenschauer",

        85: "Leichte Schneeschauer",
        86: "Starke Schneeschauer",

        95: "Gewitter",
        96: "Gewitter mit leichtem Hagel",
        99: "Gewitter mit starkem Hagel"
    }

    return weather_codes.get(code, "Unbekannt")