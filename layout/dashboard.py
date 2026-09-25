#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
picdir = "picdir/"
libdir = "e_ink_lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

from display.e_ink_lib import epd13in3E
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

from logger import logger
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
from .fonts import font_small, font_medium, font_large, fill_main, fill_gray


def make_dashbord(data):
    widget_spacing = 10
    epd = epd13in3E.EPD()
    try:
        
        epd.Init()
        
        # Set background to white
        image = Image.new("RGB", (1200, 1600), "white")
        draw = ImageDraw.Draw(image)
        
        # Last refresh info
        now = datetime.datetime.now()
        if now.minute < 10:
            minute = '0' + str(now.minute)
        else:
            minute = str(now.minute)
        now_str = str(now.hour) + ':' + minute + '   ' + str(now.strftime("%d.%m.%Y"))
        draw.text((30, 1575),"Last refresh: " + now_str, font=font_small,fill=fill_main)
        
        # Draw welcome message
        try:
            display_welcome(draw, image, 30, 30, data['moon_data'])
        except:
            logger.exception("display_welcome failed")
                             
        # Draw Wi-Fi QR code
        try:
            display_wifi_qr_code(draw, image, 1040, 10)
        except:
            logger.exception("display_wifi_qr_code failed")
                    
        # Draw weather curve
        try:
            display_weather_graph(draw, image, data['weather_hourly'], data['weather_daily'], 30, 150)
        except:
            logger.exception("display_weather_graph failed")
        
        # draw random picture
        try:
            display_photo(draw, image, 30, 430, 800)
        except:
            logger.exception("display_photo failed")
        
        draw.line([(30, 980), (830, 980)], fill= fill_main, width = 1)
        
        # Draw next holidays
        y = 990
        try:
            y = display_holiday(draw, image, holidays, 30, y)
            y += widget_spacing
        except:
            logger.exception("display_holiday failed")
                      
        # draw room climate data
        try:
            display_room_climate_widget(draw, image, 30, y, [])
        except:
            logger.exception("display_room_climate_widget failed")
        
        draw.line([(340, 1010), (340, 1550)], fill= fill_main, width = 1)
                    
        # draw news data
        try:
            display_news_widget(draw, image, 370, 990, data['news_data'])
        except:
            logger.exception("display_news_widget failed")
        
        draw.line([(860, 165), (860, 1550)], fill= fill_main, width = 1)
        
        # Draw transport schedule
        y = 150
        try:
            y = display_schedule_complet(draw, image, 'Seen', data['departures_seen'], 'Etzberg', data['departures_etzberg'], 890, y)
            y += widget_spacing
        except:
            logger.exception("display_schedule_complete failed")
                            
        # draw birthday data
        try:
            y = display_birthday_widget(draw, image, 890, y, data['birthday_data'])
            y += widget_spacing
        except:
            logger.exception("display_birthday_widget failed")
                    
        # draw quote data
        try:
            data['quote_data'], y = display_quote_widget(draw,  890, y, data['quote_data'])
            y += widget_spacing
        except:
            logger.exception("display_quote_widget failed")
        
        
        # draw health data
        try:
            display_health_widget(draw, image, 890, y, data['health_data'])
        except:
            logger.exception("display_health_widget failed")            
        
                    
        # draw software status
        display_software_status(draw, image, 1170, 1575, data['status'])
        
        # Draw helper grid
        # draw = draw_grid(draw, 20, 1600, 1200)
        
        # Write picture on to screen
        epd.display(epd.getbuffer(image))

        print("goto sleep...")
        epd.sleep()
        
    except Exception:
        print("ERROR:")
        traceback.print_exc()
        epd.sleep()
        raise
    
    return data
