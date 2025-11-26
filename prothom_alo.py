from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from retrieve_summarization import generate_summarization
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape_prothomalo(portal_name ,url,driver):

    driver.get(url)
    wait = WebDriverWait(driver, 15)

    news_list = []

    # Two separate card classes
    card_classes = ["content-area"]

    for card_class in card_classes:
        try:
            cards = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, card_class))
            )
            print(f"Found {len(cards)} cards with class `{card_class}`")
        except Exception as e:
            print(f"Failed to find cards with class `{card_class}`: {e}")
            continue

        for i, card in enumerate(cards):  # top 5 per class
            try:
                # Title and link
                try:
                    link_el = card.find_element(By.TAG_NAME, "a")
                    link = link_el.get_attribute("href")
                    title = card.find_element(By.TAG_NAME,"span").text.strip()
                except:
                    title = "N/A"
                    link = "N/A"

                # Published time
                try:
                    time_el = card.find_element(By.TAG_NAME, "time")
                    published_time = time_el.text.strip()
                except:
                    published_time = "N/A"

                # Description / summary
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
                    description_text = "N/A"
                    summarized_description="N/A"

                news_item = {
                    "newspaper_name": portal_name,
                    "title": title,
                    "link": link,
                    "description":description_text,
                    "summarized_description":summarized_description,
                    "published_time": published_time
                    }
                news_list.append(news_item)

            except Exception as e:
                print(f"Error processing card #{i} of class `{card_class}`: {e}")
                continue
            
    return news_list