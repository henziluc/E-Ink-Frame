import datetime
from datetime import datetime
from PIL import Image, ImageOps
from pathlib import Path

from .fonts import font_massiv, font_normal, fill_main, spacing_massive, spacing_normal, fill_gray
from .helpers import draw_centered_text

BASE_DIR = Path(__file__).resolve().parent.parent
moon_full_icon_path = BASE_DIR / "assets" / "moon_symbol" / "moon-phases_1.png"
moon_3_4_icon_path = BASE_DIR / "assets" / "moon_symbol" / "moon-phases_2.png"
moon_half_icon_path = BASE_DIR / "assets" / "moon_symbol" / "moon-phases_3.png"
moon_1_4_icon_path = BASE_DIR / "assets" / "moon_symbol" / "moon-phases_4.png"

def display_welcome(draw, image, x_start, y_start, moon_data):
    y = y_start
    
    now = datetime.now()   
    now_hour = now.hour
    
    # Determine the appropriate greeting based on the current hour
    if 4 <= now_hour < 12:
        text = 'Good Morning'
    elif 12 <= now_hour < 18:
        text = 'Good Afternoon'
    elif 18 <= now_hour < 21:
        text = 'Good Evening'
    else:
        text = 'Good Night'
        # Display moon phase icon if it's night time
        display_moon_phase(image, 370, y_start + 13, moon_data)
        
    draw.text((x_start, y), text, font=font_massiv, fill=fill_main)
    y += spacing_massive + 5
    
    weekday = datetime.now().strftime("%A")
    datum = datetime.now().strftime("%d.%m.%Y")
    date_string = weekday +  ', ' + datum
    
    draw.text((x_start, y), date_string, font=font_normal, fill=fill_main)
    y += spacing_normal
    
    draw.line([(x_start, y), (1200-x_start, y)], fill= fill_main, width = 1)

    
def display_moon_phase(image, x_start, y_start, moon_data):
    icon_size = 50
    illumination = moon_data['illumination']
    
    if moon_data['phase'] == 'unkown':
        return
    
    # Choose path of moon icon based on illumination
    if illumination > 87:
        moon_icon_path = moon_full_icon_path
    elif illumination > 62:
        moon_icon_path = moon_3_4_icon_path
    elif illumination > 37:
        moon_icon_path = moon_half_icon_path
    else:
        moon_icon_path = moon_1_4_icon_path
    
    # Display moon icon if illumination is greater than 2%
    if illumination > 2:
        moon_icon = Image.open(moon_icon_path).convert("RGBA")    
        moon_icon = moon_icon.resize((icon_size, icon_size))
        
        # Mirror the moon icon if it's waxing
        if not moon_data['waxing']:
            moon_icon = ImageOps.mirror(moon_icon)
            
        image.paste(moon_icon, (x_start, y_start), moon_icon)