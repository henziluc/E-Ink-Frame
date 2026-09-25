import random
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance

from .fonts import font_small, font_normal, font_small_italic, font_large, fill_main, spacing_small, spacing_normal, spacing_medium, spacing_large

BASE_DIR = Path(__file__).resolve().parent.parent


import os
import psutil

process = psutil.Process(os.getpid())

def mem(label):
    print(f"{label}: {process.memory_info().rss / 1024 / 1024:.1f} MB")


def display_photo(draw, image, x_start, y_start, x_end):
    photo_list = []
    
    # define photo size
    x_size = x_end - x_start
    y_size = int(x_size / 1.5)
    mem("before photo")
    # count number of photos
    folder = BASE_DIR / "assets" / "photo" / "resized"
    photo_count = sum(
        1 for file in folder.iterdir()
        if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
    )
    
    # get a list of all photo in a list
    for file in folder.iterdir():
        if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
            photo_list.append(file.name)
    mem("after analizing photo folder")    
    # get random number between 1 and number of photos
    random_photo_number = random.randint(1, photo_count - 1)
    
    random_photo = photo_list[random_photo_number]
    
    photo_path = BASE_DIR / "assets" / "photo" / "resized" / random_photo
    
    # Get picture and rotate
    picture = Image.open(photo_path).convert("RGBA")
    mem("after Image.open")
    
    # Resize picture
    picture = ImageOps.fit(picture, (x_size, y_size), method=Image.Resampling.LANCZOS)
    mem("after resize")
    
    picture = ImageOps.exif_transpose(picture)
    mem("after transpose")
    
    # Improve photo colors
    picture = ImageEnhance.Contrast(picture).enhance(1.1)
    picture = ImageEnhance.Color(picture).enhance(1.4)
    picture = ImageEnhance.Sharpness(picture).enhance(1.3)
    picture = ImageEnhance.Brightness(picture).enhance(1.1)
    mem("after color improvment")    
    
    
    image.paste(picture, (x_start, y_start))
    mem("after pasting")
    # Add frame around picture
    draw.rectangle([(x_start, y_start),(x_end, y_start + y_size)], outline ="black", width = 3)
    
    text_parts = random_photo.split("_")
    
    if len(text_parts) >= 3:
        location = str(text_parts[0])
        month = str(text_parts[1])
        year = str(text_parts[2][:4])
        picture_description = location + '  ' + month + ' ' + year
        draw.text((x_start, y_start + y_size + 7), picture_description ,font=font_small, fill=fill_main)