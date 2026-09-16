import math
import pandas as pd
from datetime import datetime

from .helpers import draw_smooth_curve
from .fonts import font_small, font_normal, font_medium, font_large, fill_main, spacing_small, spacing_normal, spacing_medium, spacing_large

def display_room_climate_widget(draw, x_start, y_start, df):
    y = y_start
    graph_height = 100
    graph_width = 1200 - x_start - 30  # Adjust the width based on your layout
        
    draw.text((x_start, y), "Room Climate", font=font_large, fill=fill_main)
    y += spacing_large
    
    # Draw temperature
    draw.text((x_start, y), "Temperature", font=font_normal, fill=fill_main)
    y += spacing_normal + graph_height
    draw_room_climate_graph(draw, x_start, y, graph_width, graph_height, df, "temperature", fill_main) 
    y += spacing_small
    
    # Draw Humidity
    draw.text((x_start, y), "Humidity", font=font_normal, fill=fill_main)
    y += spacing_normal + graph_height
    draw_room_climate_graph(draw, x_start, y, graph_width, graph_height, df, "humidity", fill_main)
    y += spacing_small
        
    # Draw CO2
    draw.text((x_start, y), "CO2", font=font_normal, fill=fill_main)
    y += spacing_normal + graph_height
    draw_room_climate_graph(draw, x_start, y, graph_width, graph_height, df, "co2", fill_main)
    
    
    
    
def draw_room_climate_graph(draw, x_start, y_start, graph_width, graph_height, data, value_key, color):
    offset = 3
    positions = []
    datapoints = 12
    data = data.tail(datapoints + 1)  # Get the last 12 data points

    if len(data) < 2:
        return  # Not enough data to draw a graph
    
    min_value = math.floor(data[value_key].min())  # Ensure the minimum value is at least 0
    max_value = math.ceil(data[value_key].max())  # Ensure the maximum value is at least 1 to avoid division by zero
    delta = max_value - min_value
    y_spacing = (graph_height - offset * 2) / delta
    x_spacing = graph_width / datapoints
    
    if min_value == max_value:
        return  # Avoid division by zero
    
    draw.line((x_start, y_start, x_start, y_start - graph_height), fill=fill_main, width=2)
    draw.line((x_start, y_start, x_start + graph_width, y_start), fill=fill_main, width=2)
    draw.text((x_start - 2, y_start - offset), str(min_value), font=font_small, fill=fill_main, anchor= 'rm')
    draw.text((x_start - 2, y_start - graph_height - offset), str(max_value), font=font_small, fill=fill_main, anchor= 'rm')
    
    start_time = data.iloc[0]["date"].strftime("%H:%M")
    end_time = data.iloc[-1]["date"].strftime("%H:%M")
    draw.text((x_start , y_start + 5), str(start_time), font=font_small, fill=fill_main, anchor= 'mt')
    draw.text((x_start + graph_width , y_start + 5), str(end_time), font=font_small, fill=fill_main, anchor= 'mt')
    x_increment = 0    
    
    for i in range(len(data)):
        value = data.iloc[i][value_key]
        
        x = x_start + x_increment * x_spacing
        y = y_start - offset - (value - min_value) * y_spacing
        positions.append((x, y))
        x_increment += 1
    
    # Draw the graph line
    draw_smooth_curve(draw, positions, fill_main, 2)