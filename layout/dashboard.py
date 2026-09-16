#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
picdir = "picdir/"
libdir = "e_ink_lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

import epd13in3E
import time
import datetime
import traceback
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
from PIL import Image
import pandas as pd
import json

from .welcome_widget import display_welcome
from .transport_widget import display_schedule_complet
from .weather_widget import  display_weather_graph
from .helpers import draw_grid
from .holiday_widget import display_holiday
from .photo_widget import display_photo
from .health_widget import display_health_widget
from .birthday_widget import display_birthday_widget
from .news_widget import display_news_widget
from assets.holiday_data import holidays
from .wifi_widget import display_wifi_qr_code
from .quote_widget import display_quote_widget
from .software_status_widget import display_software_status
from .room_climate_widget import display_room_climate_widget
from .fonts import font_small, font_medium, font_large, fill_main


def make_dashbord(weather_hourly,
                  weather_daily,
                  departures_seen,
                  departures_etzberg,
                  health_data_1,
                  health_data_2,
                  birthday_data,
                  moon_data,
                  news_data,
                  quote_data,
                  status_data,
                  room_climate_data):

    epd = epd13in3E.EPD()
    try:
        
        epd.Init()
        
        # Set background to white
        image = Image.new("RGB", (1200, 1600), "white")
        draw = ImageDraw.Draw(image)
        
        # Last refresh info
        now = datetime.datetime.now()
        now_str = str(now.hour) + ':' + str(now.minute) + ' ' + str(now.strftime("%d.%m.%Y"))
        draw.text((30, 1575),"Last refresh: " + now_str, font=font_small,fill=fill_main)
        
        # Draw welcome message
        display_welcome(draw, image, 30, 30, moon_data)
        
        # Draw Wi-Fi QR code
        display_wifi_qr_code(draw, image, 1040, 10)
        
        # Draw weather curve
        display_weather_graph(draw, image, weather_hourly, weather_daily, 30, 120)
        
        # Draw transport schedule
        display_schedule_complet(draw, image, 'Seen', departures_seen, 'Etzberg', departures_etzberg, 30, 450)
        
        # Draw next holidays
        display_holiday(draw, holidays, 30, 910)
        
        # draw random picture
        display_photo(draw, image, 365, 460, 830)
        
        # draw health data
        display_health_widget(draw, image, 30, 1170, health_data_1, health_data_2)
        
        # draw news data
        display_news_widget(draw, image, 365, 1090, news_data)
        
        # draw birthday data
        display_birthday_widget(draw, image, 850, 450, birthday_data)
        
        # draw quote data
        display_quote_widget(draw,  850, 680, quote_data)
        
        # draw room climate data
        display_room_climate_widget(draw, 850, 870, room_climate_data)
        
        # draw software status
        display_software_status(draw, image, 1170, 1575, status_data)
        
        # Draw helper grid
        # draw = draw_grid(draw, 20, 1600, 1200)
        
        # Write picture on to screen
        epd.display(epd.getbuffer(image))
        time.sleep(30)

        print("clearing...")
        epd.Clear()

        print("goto sleep...")
        epd.sleep()
        
    except Exception:
        print("ERROR:")
        traceback.print_exc()
        epd.sleep()

    return
