from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from database import SessionLocal
from model import LatestNews  # Your SQLAlchemy model

def scrape_prothomalo():
    portal_name = "Prothom Alo"
    url = "https://en.prothomalo.com/collection/latest"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    wait = WebDriverWait(driver, 15)

    news_list = []

    # Two separate card classes
    card_classes = ["news_with_item", "wide-story-card"]

    for card_class in card_classes:
        try:
            cards = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, card_class))
            )
            print(f"Found {len(cards)} cards with class `{card_class}`")
        except Exception as e:
            print(f"Failed to find cards with class `{card_class}`: {e}")
            continue

        for i, card in enumerate(cards[:5]):  # top 5 per class
            try:
                # Title and link
                try:
                    title_el = card.find_element(By.CSS_SELECTOR, "h3 a, h2 a")
                    title = title_el.text.strip()
                    link = title_el.get_attribute("href")
                except:
                    title = "N/A"
                    link = "N/A"

                # Published time
                try:
                    time_el = card.find_element(By.CSS_SELECTOR, "span.time, time")
                    published_time = time_el.text.strip()
                except:
                    published_time = "N/A"

                # Description / summary
                try:
                    description = card.find_element(By.CSS_SELECTOR, "p.story-card-summary").text
                except:
                    description = "N/A"

                # # Image alt
                # try:
                #     img_alt = card.find_element(By.TAG_NAME, "img").get_attribute("alt")
                # except:
                #     img_alt = "N/A"

                img_el = card.find_element(By.CSS_SELECTOR, ".qt-image.image")
                img_alt = img_el.get_attribute("alt")  

                news_item = {
                    "newspaper_name": portal_name,
                    "title": title,
                    "link": link,
                    "description": img_alt,
                    "published_time": published_time,
                }
                news_list.append(news_item)

            except Exception as e:
                print(f"Error processing card #{i} of class `{card_class}`: {e}")
                continue

    driver.quit()
    return news_list

def save_news_to_db(news_items):
    db = SessionLocal()
    try:
        for item in news_items:
            news_entry = LatestNews(
                newspaper_name=item['newspaper_name'],
                title=item['title'],
                link=item['link'],
                description=item['description'],
                published_time=item['published_time'],
                image_alt=item['description']  # make sure your model has this column
            )
            db.add(news_entry)
        db.commit()
        print(f"Saved {len(news_items)} news items to database.")
    except Exception as e:
        db.rollback()
        print(f"Error saving to DB: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    news = scrape_prothomalo()
    print(f"\nTotal news scraped: {len(news)}")
    save_news_to_db(news)
