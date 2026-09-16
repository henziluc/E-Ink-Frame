from pathlib import Path
from datetime import date
from PIL import Image


from .fonts import font_small, font_normal, font_medium, font_large, fill_main, spacing_small, spacing_normal, spacing_medium, spacing_large


BASE_DIR = Path(__file__).resolve().parent.parent


def display_birthday_widget(draw, image, x_start, y_start, birthday_data):
    cake_icon_path = BASE_DIR / "assets" / "symbol" / "cake.png"
    icon_size = 25
    y = y_start
    upcoming_birthdays = get_upcoming_birthdays(birthday_data, 5)

    draw.text((x_start, y_start), 'Birthdays', font=font_large, fill=fill_main)
    
    y += spacing_large
    
    for person in upcoming_birthdays:
        icon = Image.open(cake_icon_path).convert("RGBA")
        icon = icon.resize((icon_size, icon_size))
        image.paste(icon, (x_start, y), icon)
        name = person["name"]
        birthday_date =  person["next_birthday"].strftime("%d.%m.")
        days_until = str((person["next_birthday"] - date.today()).days)
        draw.text((x_start + icon_size + 5, y), name , font = font_small, fill = fill_main )
        draw.text((x_start + icon_size + 100, y), birthday_date , font = font_small, fill = fill_main )
        if int(days_until) < 2:
            draw.text((x_start + icon_size + 170, y), 'in' + days_until + ' days' , font = font_small, fill = fill_main )
        else:
            draw.text((x_start + icon_size + 170, y), 'in ' + days_until + ' days' , font = font_small, fill = fill_main )
        y += spacing_small
  
    
    
    
def get_upcoming_birthdays(birthdays, amount=5):
    today = date.today()
    upcoming = []

    for person in birthdays:
        birthday = person["birthday"]

        next_birthday = date(today.year, birthday.month, birthday.day)

        if next_birthday < today:
            next_birthday = date(
                today.year + 1,
                birthday.month,
                birthday.day
            )

        upcoming.append({
            "name": person["name"],
            "birthday": birthday,
            "next_birthday": next_birthday
        })

    upcoming.sort(key=lambda x: x["next_birthday"])

    return upcoming[:amount]