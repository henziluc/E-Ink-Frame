import random
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw

from .fonts import font_small, font_normal, font_small_italic, font_large, fill_main, spacing_small, spacing_normal, spacing_medium, spacing_large

BASE_DIR = Path(__file__).resolve().parent.parent
icon_path = BASE_DIR / "assets" / "photo" / "resized" / "location.png"

import os
import psutil

process = psutil.Process(os.getpid())

def mem(label):
    print(f"{label}: {process.memory_info().rss / 1024 / 1024:.1f} MB")


def display_photo(draw, image, x_start, y_start, x_end, y_end):
    photo_list = []
    
    # define photo size
    x_size = x_end - x_start
    y_size = y_end - y_start
    mem("before photo")
    # count number of photos
    folder = BASE_DIR / "assets" / "photo" / "resized"
    photo_count = sum(
        1 for file in folder.iterdir()
        if file.suffix.lower() in [".jpg", ".jpeg", ".webp"]
    )
    
    # get a list of all photo in a list
    for file in folder.iterdir():
        if file.suffix.lower() in [".jpg", ".jpeg", ".webp"]:
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
    picture = rounded_image(picture, (x_size, y_size), radius=20)
    mem("after rounded_image")
    
    image.paste(picture, (x_start, y_start))
    mem("after pasting")
       
    
    text_parts = random_photo.split("_")
    
    if len(text_parts) >= 3:
        location = str(text_parts[0])
        month = str(text_parts[1])
        year = str(text_parts[2][:4])
        picture_description = location + ', ' + month + ' ' + year
        padding_x = 20
        padding_y = 10
        bbox = draw.textbbox((0, 0), picture_description, font=font_small)

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        boxheight = text_height + 2 * padding_y
        boxwidth = text_width + 2 * padding_x    
        
        x_position = x_start + 20
        y_position = y_start + y_size - boxheight - 20
        
        box = (
            x_position,
            y_position,
            x_position + boxwidth,
            y_position + boxheight
        )

        draw.rounded_rectangle(
            box,
            radius=15,
            fill="white"
        )

        draw.text(
            (x_position + padding_x, y_position + padding_y - 3),
            picture_description,
            font=font_small,
            fill=fill_main
        )
        
        
        
        
        
        
        
        
        
        
def rounded_image(image, size, radius):
    image = image.resize(size)

    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        (0, 0, size[0], size[1]),
        radius=radius,
        fill=255
    )

    result = Image.new("RGBA", size, (255, 255, 255, 0))
    result.paste(image, (0, 0), mask)

    return result