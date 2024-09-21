from flask import Flask, render_template
import feedparser
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime

app = Flask(__name__)

# News providers with their RSS feeds
news_provider = {
    "https://www.securityweek.com/feed/": "Security Week",
    "https://www.darkreading.com/rss.xml": "Dark Reading",
    "https://threatpost.com/feed/": "Threat Post",
    "https://krebsonsecurity.com/feed/": "Krebs on Security",
    "https://feeds.feedburner.com/TheHackersNews": "The Hacker News",
}

# Fetch news articles
def fetch_news():
    all_news = []
    for url, provider_name in news_provider.items():
        feed = feedparser.parse(url)
        if feed.entries:
            for post in feed.entries[:5]:  # Get the latest 5 entries from each provider
                try:
                    soup = BeautifulSoup(post.summary, "html.parser")
                    summary_text = soup.get_text()
                    timestamp = post.published
                    date_obj = parser.parse(timestamp)
                    date_str = date_obj.strftime("%Y-%m-%d")
                    time_str = date_obj.strftime("%H:%M:%S")

                    # Check for media content like images
                    image = post.media_content[0]['url'] if 'media_content' in post else None
                    
                    news_item = {
                        'title': post.title,
                        'link': post.link,
                        'date': date_str,
                        'time': time_str,
                        'summary': summary_text,
                        'provider': provider_name,
                        'image': image
                    }
                    all_news.append(news_item)
                except Exception as e:
                    print(f"Error processing {provider_name}: {e}")
    return all_news

@app.route('/')
def home():
    news_items = fetch_news()
    current_time = datetime.now().strftime('%A, %B %d, %Y - %I:%M %p')
    return render_template('index.html', news_items=news_items, current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True)
