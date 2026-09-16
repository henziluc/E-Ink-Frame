from .fonts import font_small, font_normal, font_medium, font_large, fill_main, spacing_small, spacing_normal, spacing_medium, spacing_large
import qrcode
from PIL import Image
import random
from .helpers import wrap_text_to_width


def display_news_widget(draw, image, x_start, y_start, news_data):
    y = y_start
    
    
    # Draw news title
    draw.text((x_start, y), "News", font=font_large, fill=fill_main)
    y += spacing_large
    
    
    random_news = {
    category: random.choice(articles)
    for category, articles in news_data.items()
}
    
    
    
    # Draw news items
    for item in random_news.values():
        # Draw QR code for the news item
        qr_code_image = generate_qr(item['link'])
        qr_code_image = qr_code_image.resize((80, 80))  # Resize QR code to fit in the widget
        image.paste(qr_code_image, (x_start + 380, y))
        
        
        lines = wrap_text_to_width(
        item["title"],
        font_small,
        max_width=370,
        draw=draw,
        max_lines=3
)       
        line_counter = 0
        for line in lines:
            draw.text((x_start, y), line, font=font_small, fill=fill_main)
            y += spacing_small
            line_counter -= 1
        
        line_counter += 3    
        y += 20 + (line_counter * spacing_small)  # Add extra space after each news item
        
        
        
    


def generate_qr(url):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=2,
        border=1,
    )

    qr.add_data(url)
    qr.make(fit=True)

    return qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGBA")


