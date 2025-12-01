from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from retrieve_summarization import generate_summarization



def scrape_amadershomoy(portal_name ,url,driver):
    
    driver.get(url)
    driver.implicitly_wait(5)

    news_items = []

    cards = driver.find_elements(By.CSS_SELECTOR, ".random-news")
    print(f"Found {len(cards)} news cards (Amader Shomoy)")

    # Scrape top 5 news
    for card in cards:   
        try:
            content = card.find_element(By.CSS_SELECTOR, ".content")
        except:
            continue

        # Extract link + title (inside <a>)
        try:
            a_tag = content.find_element(By.TAG_NAME, "a")
            link = a_tag.get_attribute("href")
            title = a_tag.text.strip()
        except:
            link = "N/A"
            title = "N/A"

        # Extract published time
        try:
            time_el = content.find_element(By.CSS_SELECTOR, ".inf")
            published_time = time_el.text.strip()
        except:
            published_time = "N/A"

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


