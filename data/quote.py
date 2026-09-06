import requests
import xml.etree.ElementTree as ET

url = "https://fixquotes.com/feeds/qotd.rss"

def get_quote():
    response = requests.get(url)
    response.raise_for_status()
    
    root = ET.fromstring(response.text)
    quoutes = []
    
    
    for item in root.findall(".//item"):
        title = item.findtext("title")
        description = item.findtext("description")

        quoutes.append({
            "title": title,
            "description": description,
        })
    
    return quoutes