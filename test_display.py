import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Waveshare display library
from display.e_ink_lib import epd13in3E


# ---------------------------------------------------------
# Display setup
# ---------------------------------------------------------

epd = epd13in3E.EPD()

print("Initializing display...")
epd.Init()

print(f"Display size: {epd.width} x {epd.height}")


# ---------------------------------------------------------
# Create image
# ---------------------------------------------------------

image = Image.new("RGB", (epd.width, epd.height), "white")
draw = ImageDraw.Draw(image)


# ---------------------------------------------------------
# Fonts
# ---------------------------------------------------------

try:
    font_large = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70
    )
    font_medium = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45
    )
    font_small = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30
    )
except:
    print("Could not load fonts, using default font")
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()


# ---------------------------------------------------------
# Draw test screen
# ---------------------------------------------------------

w = epd.width
h = epd.height

# Outer border
draw.rectangle(
    (20, 20, w - 20, h - 20),
    outline="black",
    width=5
)

# Title
draw.text(
    (60, 50),
    "E-INK DISPLAY TEST",
    font=font_large,
    fill="black"
)

# Horizontal line
draw.line(
    (60, 140, w - 60, 140),
    fill="black",
    width=4
)


# ---------------------------------------------------------
# Current time
# ---------------------------------------------------------

now = datetime.now()

draw.text(
    (60, 180),
    f"Date: {now.strftime('%Y-%m-%d')}",
    font=font_medium,
    fill="black"
)

draw.text(
    (60, 240),
    f"Time: {now.strftime('%H:%M:%S')}",
    font=font_medium,
    fill="black"
)


# ---------------------------------------------------------
# Color test
# ---------------------------------------------------------

draw.text(
    (60, 340),
    "COLOR TEST",
    font=font_medium,
    fill="black"
)

colors = [
    ("BLACK", "black"),
    ("WHITE", "white"),
    ("RED", "red"),
    ("YELLOW", "yellow"),
    ("BLUE", "blue"),
    ("GREEN", "green"),
]

x = 60
y = 410

box_width = 210
box_height = 100
gap = 25

for i, (name, color) in enumerate(colors):

    col = i % 3
    row = i // 3

    x1 = x + col * (box_width + gap)
    y1 = y + row * (box_height + gap)
    x2 = x1 + box_width
    y2 = y1 + box_height

    draw.rectangle(
        (x1, y1, x2, y2),
        fill=color,
        outline="black",
        width=3
    )

    # Text color
    if color in ["black", "blue", "red"]:
        text_color = "white"
    else:
        text_color = "black"

    # Center text
    bbox = draw.textbbox(
        (0, 0),
        name,
        font=font_small
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    tx = x1 + (box_width - text_width) / 2
    ty = y1 + (box_height - text_height) / 2

    draw.text(
        (tx, ty),
        name,
        font=font_small,
        fill=text_color
    )


# ---------------------------------------------------------
# Additional shapes
# ---------------------------------------------------------

draw.text(
    (60, 700),
    "GRAPHICS TEST",
    font=font_medium,
    fill="black"
)

# Circle
draw.ellipse(
    (60, 780, 180, 900),
    outline="black",
    width=5
)

# Triangle
draw.polygon(
    [
        (250, 900),
        (320, 780),
        (390, 900)
    ],
    outline="black",
    fill="yellow"
)

# Lines
draw.line(
    (470, 800, 700, 900),
    fill="red",
    width=10
)

draw.line(
    (470, 900, 700, 800),
    fill="blue",
    width=10
)


# ---------------------------------------------------------
# Display
# ---------------------------------------------------------

print("Sending image to display...")

epd.display(epd.getbuffer(image))

print("Display updated successfully.")
print("Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    print("Putting display to sleep...")
    epd.sleep()

print("Done.")
