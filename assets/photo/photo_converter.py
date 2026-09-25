from PIL import Image, ImageOps
from pathlib import Path

input_folder = Path(__file__).resolve().parent
output_folder = input_folder / "resized"

output_folder.mkdir(exist_ok=True)

MAX_SIZE = (800, 533)

for file in input_folder.iterdir():

    if file.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
        continue

    try:
        with Image.open(file) as img:

            # EXIF-Rotation korrigieren
            img = ImageOps.exif_transpose(img)

            # Seitenverhältnis beibehalten
            img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)

            # JPEG benötigt RGB
            img = img.convert("RGB")

            output_file = output_folder / f"{file.stem}.jpg"

            img.save(
                output_file,
                "JPEG",
                quality=80,
                optimize=True
            )

            print(f"{file.name}: {img.size} → {output_file.stat().st_size / 1024:.0f} KB")

    except Exception as e:
        print(f"Fehler bei {file.name}: {e}")

print("Fertig!")