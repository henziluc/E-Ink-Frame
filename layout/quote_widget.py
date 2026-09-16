
import random

from .fonts import font_small, font_normal, font_medium, font_large, fill_main, spacing_small, spacing_normal, spacing_medium, spacing_large
from .helpers import  wrap_text_to_width

def display_quote_widget(draw, x_start, y_start, quote_data):
    y = y_start
    # Draw quote data
    draw.text((x_start, y), "Quote", font=font_large, fill=fill_main)
    y += spacing_large
    quote = random.choice(quote_data)  # Select a random quote

    draw.text((x_start, y), quote['title'], font=font_normal, fill=fill_main)
    y += spacing_normal
    
    lines = wrap_text_to_width(
        quote['description'],
        font_small,
        max_width=320,
        draw=draw,
        max_lines=3
    )
    
    for line in lines:
        draw.text((x_start, y), line, font=font_small, fill=fill_main)
        y += spacing_small
                
    