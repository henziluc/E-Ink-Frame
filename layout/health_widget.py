from PIL import Image
from pathlib import Path
import math

from .fonts import font_small, font_normal, font_medium, font_large, fill_main, spacing_small, spacing_normal, spacing_medium, spacing_large

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



def display_health_widget(draw, image, x_start, y_start, health_data1, health_data2):
    y = y_start
    icon_size = 25
   
    draw.text((x_start, y), 'Health Stats', font = font_large, fill = fill_main)
    
    y += spacing_large
    
    display_personal_health(draw, image, x_start, y, health_data1, "Luca")
    display_personal_health(draw, image, x_start + 160, y, health_data2, "Jojo")


    
def seconds_to_hours(seconds):
    
    time_h = round(seconds / 3600)
    
    time_m = round((seconds / 3600 - time_h) * 60)
    
    if time_m < 10:
        time_m = '0' + str(time_m)
    else:
        time_m = str(time_m)
    
    time = str(time_h) + ':' + time_m
    
    return time



def display_personal_health(draw, image, x_start, y_start, health_data, name):
    icon_size = 25
    y = y_start
    draw.text((x_start, y), name, font = font_medium, fill = fill_main)
    y += spacing_medium
    
    # Draw actual steps / target steps    
    step_icon = Image.open(step_icon_path).convert("RGBA")
    step_icon = step_icon.resize((icon_size, icon_size))
    image.paste(step_icon, (x_start, y), step_icon)
    
    actual_steps = str(health_data['steps'])
    target_steps = str(health_data['step_goal'])
    draw.text((x_start + icon_size + 5, y), actual_steps + ' / ' + target_steps, font = font_small, fill = fill_main )
    
    y += spacing_small
    
    # Draw body battery
    body_battery = health_data['body_battery']
    
        # Choose which battery icon depening on body battery
    if body_battery >= 90:
        battery_icon = Image.open(battery_full_icon_path).convert("RGBA")
    elif body_battery >= 60:
        battery_icon = Image.open(battery_three_quarters_icon_path).convert("RGBA")
    elif body_battery >= 40:
        battery_icon = Image.open(battery_half_icon_path).convert("RGBA")
    elif body_battery >= 10:
        battery_icon = Image.open(battery_quarter_icon_path).convert("RGBA")
    else:       
        battery_icon = Image.open(battery_empty_icon_path).convert("RGBA")
    
    battery_icon = battery_icon.resize((icon_size, icon_size))
    image.paste(battery_icon, (x_start, y), battery_icon)    
    
    draw.text((x_start + icon_size + 5, y), str(body_battery) + '%', font = font_small, fill = fill_main )
    
    y += spacing_small
    
    # Draw sleep
    sleep_icon = Image.open(sleep_icon_path).convert("RGBA")
    
    sleep_icon = sleep_icon.resize((icon_size, icon_size))
    image.paste(sleep_icon, (x_start, y), sleep_icon)
    
    sleep_hours = str(health_data['sleep_hours'])
    sleep_score = str(health_data['sleep_score'])
    
    draw.text((x_start + icon_size + 5, y), sleep_hours + 'h -> ' + sleep_score + 'P' , font = font_small, fill = fill_main )

    y += spacing_small
    
    # Draw Activity
    activity_type = health_data['activity_type']
    
    # Change icon depening on activity
    if activity_type == 'running':
        activity_icon = Image.open(running_icon_path).convert("RGBA")
    elif activity_type == 'strength_training':
        activity_icon = Image.open(gym_icon_path).convert("RGBA")
    elif activity_type == 'swimming':
        activity_icon = Image.open(swimming_icon_path).convert("RGBA")
    else:
        activity_icon = Image.open(running_icon_path).convert("RGBA")
        
    activity_icon = activity_icon.resize((icon_size, icon_size))
    image.paste(activity_icon, (x_start, y), activity_icon)
    draw.text((x_start + icon_size + 5, y), 'Last Activity', font = font_small, fill = fill_main)    

    y += spacing_small
    
    # Draw activity duration  
    duration_icon = Image.open(hourglass_icon_path).convert("RGBA")
    duration_icon = duration_icon.resize((icon_size, icon_size))
    image.paste(duration_icon, (x_start, y), duration_icon)
    
    draw.text((x_start + icon_size + 5, y), seconds_to_hours(health_data['activity_duration']) + ' h', font = font_small, fill = fill_main)
    
    y += spacing_small
    
    # Draw activity distance if value is not None
    if health_data['activity_distance'] != None:    
        distance_icon = Image.open(arrows_icon_path).convert("RGBA")
        distance_icon = distance_icon.resize((icon_size, icon_size))
        image.paste(distance_icon, (x_start, y), distance_icon)   
        
        activity_distance = str(round(health_data['activity_distance'] / 1000, 1))
        draw.text((x_start + icon_size + 5, y), activity_distance + ' km', font = font_small, fill = fill_main)    
        
        y += spacing_small
    
    # Draw activity calorie
    calories_icon = Image.open(fire_icon_path).convert("RGBA")
    calories_icon = calories_icon.resize((icon_size, icon_size))
    image.paste(calories_icon, (x_start, y), calories_icon)   
    
    activity_calories = str(round(health_data['activity_calories'],))
    draw.text((x_start + icon_size + 5, y), activity_calories + ' cal', font = font_small, fill = fill_main)    

    y += spacing_small
    
    # Draw activity pace if value is not None
    if health_data['activity_pace'] != None:
        speed_icon = Image.open(speed_icon_path).convert("RGBA")
        speed_icon = speed_icon.resize((icon_size, icon_size))
        image.paste(speed_icon, (x_start, y), speed_icon)   
        
        draw.text((x_start + icon_size + 5, y), health_data['activity_pace'] + ' min/km', font = font_small, fill = fill_main)   