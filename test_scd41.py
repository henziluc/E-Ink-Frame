import time
import board
import adafruit_scd4x

from PIL import Image, ImageDraw, ImageFont

from display import epd13in3E


# --------------------------------------------------
# SCD41
# --------------------------------------------------

i2c = board.I2C()
scd41 = adafruit_scd4x.SCD4X(i2c)

scd41.start_periodic_measurement()

print("SCD41 started")
print("Waiting for first measurement...")


# --------------------------------------------------
# Display
# --------------------------------------------------

epd = epd13in3E.EPD()

epd.init()

# White background
image = Image.new("RGB", (1600, 1200), "white")
draw = ImageDraw.Draw(image)

font_large = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    100
)

font_medium = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    60
)

font_small = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    40
)


# --------------------------------------------------
# Main loop
# --------------------------------------------------

while True:

    if scd41.data_ready:

        co2 = scd41.CO2
        temperature = scd41.temperature
        humidity = scd41.relative_humidity

        print(
            f"CO2: {co2} ppm | "
            f"Temperature: {temperature:.1f} °C | "
            f"Humidity: {humidity:.1f} %"
        )

        # Clear image
        image = Image.new("RGB", (1600, 1200), "white")
        draw = ImageDraw.Draw(image)

        # Title
        draw.text(
            (100, 80),
            "SCD41 Sensor",
            font=font_medium,
            fill="black"
        )

        # CO2
        draw.text(
            (100, 250),
            f"{co2} ppm",
            font=font_large,
            fill="black"
        )

        draw.text(
            (100, 380),
            "CO₂",
            font=font_small,
            fill="black"
        )

        # Temperature
        draw.text(
            (100, 550),
            f"{temperature:.1f} °C",
            font=font_large,
            fill="black"
        )

        draw.text(
            (100, 680),
            "Temperature",
            font=font_small,
            fill="black"
        )

        # Humidity
        draw.text(
            (850, 550),
            f"{humidity:.1f} %",
            font=font_large,
            fill="black"
        )

        draw.text(
            (850, 680),
            "Humidity",
            font=font_small,
            fill="black"
        )

        # Update display
        epd.display(epd.getbuffer(image))

        print("Display updated")

        # SCD41 measurements are roughly every 5 seconds
        time.sleep(5)

    else:
        time.sleep(1)