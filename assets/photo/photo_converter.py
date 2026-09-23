from PIL import Image
from pathlib import Path

input_folder = Path(__file__).resolve().parent
output_folder = input_folder / "resized"

output_folder.mkdir(exist_ok=True)

MAX_SIZE = (1200, 800)

for file in input_folder.iterdir():

    if file.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
        continue

    try:
        img = Image.open(file)

        # Seitenverhältnis beibehalten
        img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)

        output_file = output_folder / file.name

        # JPEG als platzsparende Datei speichern
        if file.suffix.lower() in [".jpg", ".jpeg"]:
            img.save(output_file, quality=80, optimize=True)
        else:
            img.save(output_file, optimize=True)

        print(f"{file.name}: {img.size}")

    except Exception as e:
        print(f"Fehler bei {file.name}: {e}")

print("Fertig!")