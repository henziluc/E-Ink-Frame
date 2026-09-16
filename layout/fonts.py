from PIL import ImageFont

font_massiv = ImageFont.truetype(
    "fonts/RobotoCondensed-Bold.ttf",
    80
)

font_large = ImageFont.truetype(
    "fonts/RobotoCondensed-Bold.ttf",
    60
)

font_medium = ImageFont.truetype(
    "fonts/RobotoCondensed-Regular.ttf",
    40
)

font_normal = ImageFont.truetype(
    "fonts/RobotoCondensed-Regular.ttf",
    30
)

font_small = ImageFont.truetype(
    "fonts/RobotoCondensed-Regular.ttf",
    20
)

font_very_small = ImageFont.truetype(
    "fonts/RobotoCondensed-Regular.ttf",
    15
)


fill_main = 'black'

fill_rain_graph = 'gray'

fill_error = 'red'


spacing_small = font_small.size + 10

spacing_normal = font_normal.size + 10

spacing_medium = font_medium.size + 10

spacing_large = font_large.size + 10