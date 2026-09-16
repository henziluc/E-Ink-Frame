import random
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance

BASE_DIR = Path(__file__).resolve().parent.parent


def display_photo(draw, image, x_start, y_start, x_end):
    photo_list = []
    
    # define photo size
    x_size = x_end - x_start
    y_size = int(x_size / 0.75)
    
    # count number of photos
    folder = BASE_DIR / "assets" / "photo"
    photo_count = sum(
        1 for file in folder.iterdir()
        if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
    )
    
    # get a list of all photo in a list
    for file in folder.iterdir():
        if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
            photo_list.append(file.name)
        
    # get random number between 1 and number of photos
    random_photo_number = random.randint(1, photo_count - 1)
    
    photo_path = BASE_DIR / "assets" / "photo" / photo_list[random_photo_number]
    
    # Get picture and rotate
    picture = Image.open(photo_path).convert("RGBA")
    picture = ImageOps.exif_transpose(picture)
    
    # Improve photo colors
    picture = ImageEnhance.Contrast(picture).enhance(1.1)
    picture = ImageEnhance.Color(picture).enhance(1.4)
    picture = ImageEnhance.Sharpness(picture).enhance(1.3)
    picture = ImageEnhance.Brightness(picture).enhance(1.1)    
    
    # Resize picture
    picture = ImageOps.fit(picture, (x_size, y_size), method=Image.Resampling.LANCZOS)
    
    image.paste(picture, (x_start, y_start))
    
    # Add frame around picture
    draw.rectangle([(x_start, y_start),(x_end, y_start + y_size)], outline ="black", width = 3)