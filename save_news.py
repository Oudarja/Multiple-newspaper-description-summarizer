from database import SessionLocal
from model import LatestNews

def save_news_to_db(news_items,scrape_id):
    db = SessionLocal()
    for item in news_items:
        news_entry = LatestNews(
            scrape_id=scrape_id,
            newspaper_name=item['newspaper_name'],
            title=item['title'],
            link=item['link'],
            description=item['description'],
            summarized_description=item['summarized_description'],
            published_time=item['published_time']
        )
        db.add(news_entry)
    db.commit()
    db.close()