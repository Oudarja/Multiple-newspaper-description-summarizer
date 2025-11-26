from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from retrieve_summarization import generate_summarization
import time




def scrap_mzamin(portal_name ,url,driver):
    driver.get(url)
    driver.implicitly_wait(5)

    news_items = []

    try:
        container = driver.find_element(By.CLASS_NAME, "container")
        cards = container.find_elements(By.CLASS_NAME, "row")
        print(f"Found {len(cards)} news cards in {portal_name}")
    except Exception as e:
        print(f"Failed to find news container: {e}")
        driver.quit()
        return []

    for card in cards:  
        # Title from <h4>
        try:
            title_el = card.find_element(By.TAG_NAME, "h4")
            title = title_el.text.strip()
        except:
            title = "N/A"

        # Published time from <p class="desktopTime">
        try:
            time_el = card.find_element(By.TAG_NAME, "p")
            published_time = time_el.text.strip()
        except:
            published_time = "N/A"

        # Link from <a> inside <h4>
        try:
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            link = "N/A"

        # EXtract description 

        try:
            try:
                driver1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                driver1.set_page_load_timeout(20)  # Maximum time to wait for page load
                driver1.get(link)
    
                # Optional: wait a few seconds for JS content to load if needed
                driver1.implicitly_wait(20)  # Not strictly necessary, but can help
    
                # Scrape all <p> text
                description_text = " ".join(
                    p.text.strip()
                    for p in driver1.find_elements(By.TAG_NAME, "p")
                    if p.text.strip()
                )
            finally:
                driver1.quit()  # Ensure driver closes even if error occurs

            summarized_description=generate_summarization(portal_name,description_text)
            time.sleep(0.5)
        except:
            description_text="N/A"
            summarized_description="N/A"

        news_items.append({
            "newspaper_name": portal_name,
            "title": title,
            "link": link,
            "description": description_text,
            "summarized_description":summarized_description,
            "published_time": published_time
        })
    return news_items
