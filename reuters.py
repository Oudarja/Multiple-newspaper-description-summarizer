from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from retrieve_summarization import generate_summarization
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

def scrape_Reuters(portal_name, url, driver):
    driver.get(url)
    driver.implicitly_wait(5)

    news_items = []

    # Wait until at least one StoryCard is present
    try:
        wait = WebDriverWait(driver, 15)
        all_cards = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "[data-testid='StoryCard'], [data-testid='common/single-section-blockStoryCard']")
            )
        )
    except:
        print("No news cards found on Reuters")
        return []

    print(f"Found {len(all_cards)} news cards ({portal_name})")

    for card in all_cards:
        # Extract title
        try:
            title = card.find_element(By.CSS_SELECTOR, "[data-testid='TitleHeading']").text.strip()
        except:
            title = "N/A"

        # Extract link
        try:
            link = card.find_element(By.CSS_SELECTOR, "[data-testid='TitleLink']").get_attribute("href")
        except:
            link = "N/A"

        # Extract published time
        try:
            published_time = card.find_element(By.CSS_SELECTOR, "[data-testid='DateLineText']").text.strip()
        except:
            published_time = "N/A"

        # Extract description
        try:
            description_text = card.find_element(By.CSS_SELECTOR, "[data-testid='Description']").text.strip()
        except:
            description_text = "N/A"

        # If you want full article scraping
        if link != "N/A":
            try:
                driver1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                driver1.set_page_load_timeout(20)
                driver1.get(link)
                driver1.implicitly_wait(5)

                # Scrape all divs with article text
                description_text = " ".join(
                    el.text.strip() for el in driver1.find_elements(By.CSS_SELECTOR, ".text-module__text__0GDob") if el.text.strip()
                )
            finally:
                driver1.quit()

        # Generate summary
        try:
            summarized_description = generate_summarization(portal_name, description_text)
        except:
            summarized_description = "N/A"

        news_items.append({
            "newspaper_name": portal_name,
            "title": title,
            "link": link,
            "description": description_text,
            "summarized_description": summarized_description,
            "published_time": published_time
        })

    return news_items