import requests
import xml.etree.ElementTree as ET
from datetime import datetime

url = "https://fixquotes.com/feeds/qotd.rss"

def get_quote(qoutes):
    if qoutes:
        return qoutes
    
    response = requests.get(url)
    response.raise_for_status()
    
    root = ET.fromstring(response.text)
    
    for item in root.findall(".//item"):
        title = item.findtext("title")
        description = item.findtext("description")

        qoutes.append({
            "title": title,
            "description": description,
        })
    
    
    now = datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    
    return qoutes, formatted_datetime