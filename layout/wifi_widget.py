import qrcode
import os

from .fonts import font_small, font_normal, font_medium, font_large, fill_main, spacing_small, spacing_normal, spacing_large
from .helpers import draw_centered_text

def display_wifi_qr_code(draw, image, x_start, y_start):
    qr_size = 80
    wifi_string = os.getenv("wifi_string")
    y = y_start
    # Generate QR code for Wi-Fi
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )
    qr.add_data(wifi_string)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Resize the QR code image to fit in the widget area
    qr_img = qr_img.resize((qr_size, qr_size))

    # Paste the QR code onto the main image
    
    draw_centered_text(draw, "Wi-Fi", (x_start, y,x_start + qr_size, y + spacing_normal - 10),font_normal, fill_main)
    y += spacing_normal
    
    image.paste(qr_img, (x_start, y))