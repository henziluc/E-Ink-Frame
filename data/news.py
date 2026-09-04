import requests
import xml.etree.ElementTree as ET

NEWS_FEEDS = {
    "swiss": [
        "https://www.srf.ch/news/bnf/rss/1890",
    ],

    "world": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
    ],

    "random": [
        "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
    ],
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
    }
    
    return news


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