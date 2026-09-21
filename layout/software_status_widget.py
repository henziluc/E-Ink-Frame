from PIL import Image, ImageOps
from pathlib import Path

from .fonts import font_small, font_normal, font_medium, font_large, fill_main, fill_error,spacing_small, spacing_normal, spacing_medium, spacing_large

BASE_DIR = Path(__file__).resolve().parent.parent
path_weather = BASE_DIR / "assets" / "status_symbol" / "partly-cloudy-day.png"
path_transport = BASE_DIR / "assets" / "status_symbol" / "train.png"
path_health = BASE_DIR / "assets" / "status_symbol" / "heart.png"
path_moon = BASE_DIR / "assets" / "status_symbol" / "moon.png"
path_news = BASE_DIR / "assets" / "status_symbol" / "news.png"
path_quote = BASE_DIR / "assets" / "status_symbol" / "quote.png"
path_birthday = BASE_DIR / "assets" / "symbol" / "cake.png"

def display_software_status(draw, image, x_start, y_start, status_data):
    icon_size = 20
    x = x_start - icon_size
    
    icon_weather = Image.open(path_weather).convert("RGBA")
    icon_weather = icon_weather.resize((icon_size, icon_size)) 
    image.paste(icon_weather, (x, y_start), icon_weather)
    if status_data['weather'] is False:
        draw.line((x , y_start, x + icon_size, y_start + icon_size), fill=fill_error, width=2)
        draw.line((x , y_start + icon_size, x + icon_size, y_start), fill=fill_error, width=2)

    x -= icon_size + 5
    
    icon_transport = Image.open(path_transport).convert("RGBA")
    icon_transport = icon_transport.resize((icon_size, icon_size))
    image.paste(icon_transport, (x, y_start), icon_transport)
    if status_data['transport'] is False:
        draw.line((x , y_start, x + icon_size, y_start + icon_size), fill=fill_error, width=2)
        draw.line((x , y_start + icon_size, x + icon_size, y_start), fill=fill_error, width=2)
    
    x -= icon_size + 5
    
    icon_health = Image.open(path_health).convert("RGBA")
    icon_health = icon_health.resize((icon_size, icon_size))
    image.paste(icon_health, (x, y_start), icon_health)
    if status_data['health'] is False:
        draw.line((x , y_start, x + icon_size, y_start + icon_size), fill=fill_error, width=2)
        draw.line((x , y_start + icon_size, x + icon_size, y_start), fill=fill_error, width=2)
        
    x -= icon_size + 5
    
    icon_moon = Image.open(path_moon).convert("RGBA")
    icon_moon = icon_moon.resize((icon_size, icon_size))
    icon_moon = ImageOps.mirror(icon_moon)
    image.paste(icon_moon, (x, y_start), icon_moon)
    if status_data['moon'] is False:
        draw.line((x , y_start, x + icon_size, y_start + icon_size), fill=fill_error, width=2)
        draw.line((x , y_start + icon_size, x + icon_size, y_start), fill=fill_error, width=2)
        
    x -= icon_size + 5
    
    icon_news = Image.open(path_news).convert("RGBA")
    icon_news = icon_news.resize((icon_size, icon_size))
    image.paste(icon_news, (x, y_start), icon_news)
    if status_data['news'] is False:
        draw.line((x , y_start, x + icon_size, y_start + icon_size), fill=fill_error, width=2)
        draw.line((x , y_start + icon_size, x + icon_size, y_start), fill=fill_error, width=2)
        
    x -= icon_size + 5
    
    icon_quote = Image.open(path_quote).convert("RGBA")
    icon_quote = icon_quote.resize((icon_size, icon_size))
    image.paste(icon_quote, (x, y_start), icon_quote)
    if status_data['quote'] is False:
        draw.line((x , y_start, x + icon_size, y_start + icon_size), fill=fill_error, width=2)
        draw.line((x , y_start + icon_size, x + icon_size, y_start), fill=fill_error, width=2)

    x -= icon_size + 5
        
    icon_birthday = Image.open(path_birthday).convert("RGBA")
    icon_birthday = icon_birthday.resize((icon_size, icon_size))
    image.paste(icon_quote, (x, y_start), icon_birthday)
    if status_data['birthday'] is False:
        draw.line((x , y_start, x + icon_size, y_start + icon_size), fill=fill_error, width=2)
        draw.line((x , y_start + icon_size, x + icon_size, y_start), fill=fill_error, width=2)
    
    