import datetime
from .helpers import draw_centered_text
from .fonts import font_small, font_normal, font_medium, font_large, fill_main, spacing_small, spacing_normal, spacing_medium, spacing_large

def display_holiday(draw, df, x_start, y_start):
    y = y_start
    next_holiday = 1
    now = datetime.datetime.now()
    # Draw widget title
    draw.text((x_start, y_start), 'Next Holiday', font=font_large, fill=fill_main)
    
    y += spacing_large
    # loop trough the first four elements which are today or later of the holiday list
    for _, row in df[df['start_date'] > now].head(4).iterrows():
        
        # Calculate amount of days till holidays start
        delta = row['start_date'] - now
        days = delta.days
        
        # First element is printed bigger
        if next_holiday == 1:
            draw_centered_text(draw, row['location'], (x_start , y, x_start + 280, y + 38), font_medium, fill_main)
            y += spacing_medium
            draw_centered_text(draw, f"{days} days to go", (x_start, y, x_start + 280, y + 29), font_normal, fill_main)
            next_holiday = 0
            y += spacing_normal
        # Other elements are printed smaller    
        else:
            draw.text((x_start, y), row['location'], font=font_small, fill=fill_main)
            draw.text((x_start + 120, y), f"{days} days to go", font=font_small, fill=fill_main)
            y += spacing_small
 