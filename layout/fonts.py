from PIL import ImageFont
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FONT_DIR = BASE_DIR / "display" / "fonts"

font_massiv = ImageFont.truetype(
    FONT_DIR / "Inter_18pt-Bold.ttf",
    60
)

font_large = ImageFont.truetype(
    FONT_DIR / "Inter_18pt-Bold.ttf",
    40
)

font_medium = ImageFont.truetype(
    FONT_DIR / "Inter_18pt-Regular.ttf",
    30
)

font_normal = ImageFont.truetype(
    FONT_DIR / "Inter_18pt-Regular.ttf",
    25
)

font_small_italic = ImageFont.truetype(
    FONT_DIR / "Inter_18pt-Italic.ttf",
    20
)

font_small = ImageFont.truetype(
    FONT_DIR / "Inter_18pt-Regular.ttf",
    20
)

font_very_small = ImageFont.truetype(
    FONT_DIR / "Inter_18pt-Thin.ttf",
    19
)


fill_main = 'black'

fill_gray = 'gray'

fill_error = 'red'


spacing_small = font_small.size + 10

spacing_normal = font_normal.size + 10

spacing_medium = font_medium.size + 10

spacing_large = font_large.size + 10

spacing_massive = font_massiv.size + 10