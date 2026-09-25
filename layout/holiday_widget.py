import datetime
from PIL import Image, ImageOps, ImageEnhance
from logger import logger
from pathlib import Path
from .helpers import draw_centered_text
from .fonts import font_small, font_normal, font_medium, font_large, fill_main, spacing_small, spacing_normal, spacing_medium, spacing_large

BASE_DIR = Path(__file__).resolve().parent.parent
PHOTO_FOLDER = BASE_DIR / "assets" / "holiday_photos" 

def display_holiday(draw, image, df, x_start, y_start):
    picture_width = 100
    picture_height = picture_width * 1.5
    y = y_start
    next_holiday = 1
    now = datetime.datetime.now()
    # Draw widget title
    draw.text((x_start, y_start), 'Next Holiday', font=font_large, fill=fill_main)
    
    y += spacing_large
    # loop trough the first four elements which are today or later of the holiday list
    for _, row in df[df['start_date'] > now].head(3).iterrows():
        
        # Calculate amount of days till holidays start
        delta = row['start_date'] - now
        days = delta.days
        
        # First element is printed bigger
        if next_holiday == 1:
            photo_path = get_holiday_photo(row['location'])
            picture = Image.open(photo_path).convert("RGBA")
            # Resize picture
            picture = ImageOps.fit(picture, (picture_width, picture_height), method=Image.Resampling.LANCZOS)
            # Improve photo colors
            picture = ImageEnhance.Contrast(picture).enhance(1.1)
            picture = ImageEnhance.Color(picture).enhance(1.4)
            picture = ImageEnhance.Sharpness(picture).enhance(1.3)
            picture = ImageEnhance.Brightness(picture).enhance(1.1)
            
            image.paste(picture, (x_start, y_start))
            draw.text((x_start + picture_width, y), row['location'], font=font_medium, fill=fill_main)
            y += spacing_medium
            draw.text((picture_width, y), f"{days} days to go", font=font_normal, fill=fill_main)
            y += spacing_normal
            draw.text((picture_width, y), str(row['start_date']), font=font_normal, fill=fill_main)
            y += spacing_normal
            next_holiday = 0
        # Other elements are printed smaller    
        else:
            draw.text((x_start, y), row['location'], font=font_small, fill=fill_main)
            draw.text((x_start + 130, y), f"{days} days to go", font=font_small, fill=fill_main)
            y += spacing_small
            
    return y
 
 
 
 
def safe_filename(location):
    """
    Convert a location into a safe filename.
    """

    filename = location.replace(" ", "_")
    filename = re.sub(r"[^a-zA-Z0-9_-]", "", filename)

    return filename + ".jpg"
 
 
def get_holiday_photo(location):

    filename = safe_filename(location)
    photo_path = PHOTO_FOLDER / filename

    if photo_path.exists():
        return photo_path

    logger.warning(f"No holiday photo found for {location}")
    return None 