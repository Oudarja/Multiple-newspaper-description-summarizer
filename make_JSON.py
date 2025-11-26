from database import SessionLocal
from model import LatestNews
import json

db = SessionLocal()

# Fetch where description is not NULL and not empty
all_news = (
    db.query(LatestNews)
    .filter(LatestNews.description.isnot(None))
    .filter(LatestNews.description != "")
    .all()
)

news_list = []
for news in all_news:
    news_list.append({
        "id": news.id,
        "newspaper_name": news.newspaper_name,
        "title": news.title,
        "link": news.link,
        "description": news.description,
        "summarized_description": news.summarized_description,
        "published_time": news.published_time,
        "saved_at": str(news.saved_at)
    })

with open("latest_news.json", "w", encoding="utf-8") as f:
    json.dump(news_list, f, ensure_ascii=False, indent=2)

print("Data saved to latest_news.json")
