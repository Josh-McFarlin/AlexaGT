import feedparser


def get_news(count):
    url = "http://www.news.gatech.edu/rss/all"
    feed = feedparser.parse(url)
    entries = feed['entries']
    articles = [entry['title'] + "..." for entry in entries]
    return articles[:count]


def get_events(count):
    url = "http://www.calendar.gatech.edu/feeds/events.xml"
    feed = feedparser.parse(url)
    entries = feed['entries']
    articles = [entry['title'] + "..." for entry in entries]
    return articles[:count]

if __name__ == "__main__":
    n = get_news(4)
    print(n)

    e = get_events(3)
    print(e)
