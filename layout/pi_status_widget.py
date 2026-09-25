import shutil
import psutil
from pathlib import Path

from .fonts import font_small, font_normal, font_small_italic, font_large, fill_main, spacing_small, spacing_normal, spacing_medium, spacing_large


def display_pi_status(draw, x_start, y_start):
    y = y_start
    
    pi_status = get_pi_status()
    
    draw.text((x_start, y), "Pi Status", font=font_large, fill=fill_main)
    y += spacing_large
    draw.text((x_start, y), f"CPU usage: {pi_status['cpu_percent']}%", font=font_small, fill=fill_main)
    y += spacing_small
    draw.text((x_start, y), f"RAM : {pi_status['ram_used']}/{pi_status['ram_total']} MB", font=font_small, fill=fill_main)
    y += spacing_small
    draw.text((x_start, y), f"Storage : {pi_status['storage_used']}/{pi_status['storage_total']} GB", font=font_small, fill=fill_main)
    y += spacing_small

def get_pi_status():

    # CPU temperature
    try:
        temp = Path(
            "/sys/class/thermal/thermal_zone0/temp"
        ).read_text()

        cpu_temp = round(int(temp) / 1000, 1)

    except Exception:
        cpu_temp = None


    # RAM
    try:
        ram = psutil.virtual_memory()

        ram_used = round(ram.used / 1024**2)
        ram_total = round(ram.total / 1024**2)
        ram_percent = ram.percent

    except Exception:
        ram_used = None
        ram_total = None
        ram_percent = None


    # Storage
    try:
        storage = shutil.disk_usage("/")

        storage_used = round(storage.used / 1024**3, 1)
        storage_total = round(storage.total / 1024**3, 1)
        storage_percent = round(
            storage.used / storage.total * 100,
            1
        )

    except Exception:
        storage_used = None
        storage_total = None
        storage_percent = None


    # CPU usage
    try:
        cpu_percent = psutil.cpu_percent(interval=1.0)

    except Exception:
        cpu_percent = None


    return {
        "cpu_temp": cpu_temp,
        "cpu_percent": cpu_percent,

        "ram_used": ram_used,
        "ram_total": ram_total,
        "ram_percent": ram_percent,

        "storage_used": storage_used,
        "storage_total": storage_total,
        "storage_percent": storage_percent,
    }
    