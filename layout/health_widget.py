from PIL import Image
from pathlib import Path
import math

from .fonts import font_small, font_normal, font_medium, font_large, fill_main, fill_gray, spacing_small, spacing_normal, spacing_medium, spacing_large

BASE_DIR = Path(__file__).resolve().parent.parent
# Define all icon paths
step_icon_path = BASE_DIR / "assets" / "sport_symbol" / "shoe-prints.png"
battery_full_icon_path = BASE_DIR / "assets" / "sport_symbol" / "battery-full.png"
battery_three_quarters_icon_path = BASE_DIR / "assets" / "sport_symbol" / "battery-three-quarters.png"
battery_half_icon_path = BASE_DIR / "assets" / "sport_symbol" / "battery-half.png"
battery_quarter_icon_path = BASE_DIR / "assets" / "sport_symbol" / "battery-quarter.png"
battery_empty_icon_path = BASE_DIR / "assets" / "sport_symbol" / "battery-empty.png"   
sleep_icon_path = BASE_DIR / "assets" / "sport_symbol" / "bed.png"
running_icon_path = BASE_DIR / "assets" / "sport_symbol" / "person-running.png"
swimming_icon_path = BASE_DIR / "assets" / "sport_symbol" / "person-swimming.png"
gym_icon_path = BASE_DIR / "assets" / "sport_symbol" / "dumbbell.png"
fire_icon_path = BASE_DIR / "assets" / "sport_symbol" / "fire.png"
arrows_icon_path = BASE_DIR / "assets" / "sport_symbol" / "arrows.png"
hourglass_icon_path = BASE_DIR / "assets" / "sport_symbol" / "hourglass.png"
speed_icon_path = BASE_DIR / "assets" / "sport_symbol" / "gauge.png"
stress_icon_path = BASE_DIR / "assets" / "sport_symbol" / "stress.png"
intensity_icon_path = BASE_DIR / "assets" / "sport_symbol" / "intensity.png"



def display_health_widget(draw, image, x_start, y_start, health_data):
    if health_data is None:
        return y_start
    frame_offset = 10
    y = y_start + frame_offset
    icon_size = 25
    y_1 = 0
    y_2 = 0
    draw.text((x_start + frame_offset, y), 'Health', font = font_large, fill = fill_main)
    y += spacing_large
    display_health_titles(draw, x_start + frame_offset, y)
    if 'Luca' in health_data:
        if health_data['Luca'] is not None and len(health_data['Luca']) > 1:
            y_1 = display_personal_health(draw, image, x_start + 100 + frame_offset, y, health_data['Luca'], "Luca")
          
    if 'Jojo' in health_data:
        if health_data['Jojo'] is not None and len(health_data['Jojo']) > 1:
            y_2 = display_personal_health(draw, image, x_start + 200 + frame_offset, y, health_data['Jojo'], "Jojo")
            
    y_max = max(y_1, y_2)
    
    y = y_max + frame_offset
    draw.rounded_rectangle(
                (x_start, y_start, 1200 - 30, y),
                radius=20,
                outline=fill_main,
            ) 
    return y
    
def seconds_to_hours(seconds):
    
    time_h = math.floor(seconds / 3600)
    
    time_m = round((seconds / 3600 - time_h) * 60)
    
    if time_m < 10:
        time_m = '0' + str(time_m)
    else:
        time_m = str(time_m)
    
    time = str(time_h) + ':' + time_m
    
    return time

def display_health_titles(draw, x_start, y_start):
    y = y_start + spacing_medium
    draw.text((x_start, y), 'Steps', font = font_small, fill = fill_main)
    y += spacing_small + 15
    draw.text((x_start, y), 'Battery', font = font_small, fill = fill_main)
    y += spacing_small
    draw.text((x_start, y), 'Sleep', font = font_small, fill = fill_main)
    y += spacing_small
    draw.text((x_start, y), 'Intensity', font = font_small, fill = fill_main)
    y += spacing_small
    draw.text((x_start, y), 'Stress', font = font_small, fill = fill_main)
    
    
    
    
    

def display_personal_health(draw, image, x_start, y_start, health_data, name):
    icon_size = 25
    y = y_start
    draw.text((x_start, y), name, font = font_medium, fill = fill_main)
    y += spacing_medium
    
    # Draw actual steps / target steps    
    actual_steps = str(health_data['steps'])
    target_steps = str(health_data['step_goal'])
    draw.text((x_start + icon_size + 5, y), actual_steps + ' / ' + target_steps, font = font_small, fill = fill_main )
    
    y += spacing_small
    
    # Draw body battery
    body_battery = health_data['body_battery']
    draw.text((x_start + icon_size + 5, y), str(body_battery) + '%', font = font_small, fill = fill_main )
    
    y += spacing_small
    
    # Draw sleep
    sleep_hours = str(int(health_data['sleep_hours']))
    sleep_minutes = int(health_data['sleep_hours'] % 1 * 60)
    if sleep_minutes < 10:
        sleep_minutes = '0' + str(sleep_minutes)
    else:
        sleep_minutes = str(sleep_minutes)
    
    sleep_score = str(health_data['sleep_score'])
    
    draw.text((x_start + icon_size + 5, y), sleep_hours + ':' + sleep_minutes + 'h->' + sleep_score + 'P' , font = font_small, fill = fill_main )

    y += spacing_small
    
    
    # Draw intensity minutes
    draw.text((x_start + icon_size + 5, y), str(health_data['intensity_minutes']) + ' / ' + str(health_data['intensity_minutes_goal']) + 'min', font = font_small, fill = fill_main )
    
    y += spacing_small
    
    # Draw stress
    draw.text((x_start + icon_size + 5, y), str(health_data['stress']) + ' / 100', font = font_small, fill = fill_main )

    y += spacing_small

    # Draw Activity
    draw.text((x_start + icon_size + 5, y), 'Last Activity', font = font_small, fill = fill_main)    

    y += spacing_small
    
    # Draw activity duration  
    draw.text((x_start + icon_size + 5, y), seconds_to_hours(health_data['activity_duration']) + ' h', font = font_small, fill = fill_main)
    
    y += spacing_small
    
    # Draw activity distance if value is not None
    if health_data['activity_distance'] != None or health_data['activity_distance'] != 0:    
        activity_distance = str(round(health_data['activity_distance'] / 1000, 1))
        draw.text((x_start + icon_size + 5, y), activity_distance + ' km', font = font_small, fill = fill_main)    
        
        y += spacing_small
    
    # Draw activity calorie
    activity_calories = str(round(health_data['activity_calories'],))
    draw.text((x_start + icon_size + 5, y), activity_calories + ' cal', font = font_small, fill = fill_main)    

    y += spacing_small
    
    # Draw activity pace if value is not None
    if health_data['activity_pace'] != None:
        draw.text((x_start + icon_size + 5, y), health_data['activity_pace'] + ' min/km', font = font_small, fill = fill_main)
        y += spacing_small
        
    return y   