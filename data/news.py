import requests
import xml.etree.ElementTree as ET
from datetime import datetime

NEWS_FEEDS = {
    "swiss": [
        "https://www.srf.ch/news/bnf/rss/1890",
    ],

    "world": [
        "https://www.srf.ch/news/bnf/rss/1922",
    ],

    "random": [
        "https://www.srf.ch/news/bnf/rss/630",
    ],
    "sport": [
        "https://www.srf.ch/news/bnf/rss/718",
    ],
    "economie": [
        "https://www.srf.ch/news/bnf/rss/1926",
    ]
}


def get_news():
    
    news = {
        "swiss": parse_feed(
            get_feed(NEWS_FEEDS["swiss"][0])
        ),
        "world": parse_feed(
            get_feed(NEWS_FEEDS["world"][0])
        ),
        "random": parse_feed(
            get_feed(NEWS_FEEDS["random"][0])
        ),
        "economie": parse_feed(
            get_feed(NEWS_FEEDS["economie"][0])
        )
    }
    
    now = datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    
    return news, formatted_datetime


def get_feed(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.text


def parse_feed(xml_data, limit=5):

    root = ET.fromstring(xml_data)

    articles = []

    for item in root.findall(".//item")[:limit]:
        title = item.findtext("title")
        link = item.findtext("link")

        articles.append({
            "title": title,
            "link": link,
        })

    return articles