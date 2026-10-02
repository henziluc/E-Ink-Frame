import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Waveshare display library
from display.e_ink_lib import epd13in3E



print("1 - importing done")

epd = epd13in3E.EPD()

print("2 - EPD object created")

epd.Init()

print("3 - EPD initialized")

print("Width:", epd.width)
print("Height:", epd.height)

print("4 - about to create image")

from PIL import Image, ImageDraw

image = Image.new("RGB", (epd.width, epd.height), "white")

print("5 - image created")

draw = ImageDraw.Draw(image)

draw.rectangle((100, 100, 500, 300), fill="black")
draw.text((150, 150), "TEST", fill="white")

print("6 - drawing done")

print("7 - about to display")

epd.display(epd.getbuffer(image))

print("8 - display done")

epd.sleep()

print("9 - finished")