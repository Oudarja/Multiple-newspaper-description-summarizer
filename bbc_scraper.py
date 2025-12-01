from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from retrieve_summarization import generate_summarization
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_BBC(portal_name, url, driver):
    driver.get(url)
    driver.implicitly_wait(5)
    news_items = []

    # Get all cards first
    cards = driver.find_elements(
        By.CSS_SELECTOR,
        '[data-testid="dundee-card"], [data-testid="westminster-card"], [data-testid="manchester-card"]'
    )

    print(f"Found {len(cards)} news cards (BBC)")

    # Process each card immediately
    for card in cards:
        try:
            a_tag = card.find_element(By.TAG_NAME, "a")
            link = a_tag.get_attribute("href")
            title = card.find_element(By.TAG_NAME, "h2").text.strip()
        except Exception:
            link, title = "N/A", "N/A"

        try:
            time_el = card.find_element(By.TAG_NAME, "span")
            published_time = time_el.text.strip()
        except Exception:
            published_time = "N/A"

        description_text, summarized_description = "N/A", "N/A"

        if link and link != "N/A" and "/news/" in link:
            try:
                try:
                    driver1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                    driver1.set_page_load_timeout(20)
                    driver1.get(link)

                    # Wait for article tag
                    WebDriverWait(driver1, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "article"))
                    )
                    article = driver1.find_element(By.TAG_NAME, "article")
                    description_text = " ".join(
                        p.text.strip() for p in article.find_elements(By.TAG_NAME, "p") if p.text.strip()
                    )
                finally:
                    driver1.quit()

                if description_text:
                    summarized_description = generate_summarization(portal_name, description_text)
                time.sleep(0.5)
            except Exception as e:
                print(f"Skipping link {link}: {e}")

        news_items.append({
            "newspaper_name": portal_name,
            "title": title,
            "link": link,
            "description": description_text,
            "summarized_description": summarized_description,
            "published_time": published_time
        })

    return news_items