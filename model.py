# models.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text
from database import Base
from database import engine

class LatestNews(Base):
    __tablename__ = "latest_news"

    id = Column(Integer, primary_key=True, index=True)
    scrape_id = Column(Integer, default=1)  # Default value 1
    newspaper_name = Column(String(100))  # Newspaper/Portal name
    title = Column(String(500))
    link = Column(String(2000))
    description = Column(Text)  # Long text
    summarized_description = Column(Text)  # Long text
    published_time = Column(String(100))
    saved_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

