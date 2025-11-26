from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from retrieve_summarization import generate_summarization



def scrape_ittefaq(portal_name ,url,driver):
    # portal_name = "Ittefaq"
    # url = "https://www.ittefaq.com.bd/latest-news"

    # Chrome options to enable auto-translate from Bangla to English
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "translate_whitelists": {"bn": "en"},  # translate Bangla to English
        "translate": {"enabled": "true"}
    })

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    # Wait a few seconds for translation to complete
    time.sleep(5)  # can adjust if needed

    wait = WebDriverWait(driver, 15)

    news_list = []

    # Scrape news under class 'col'
    try:
        cards = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "col"))
        )
        print(f"Found {len(cards)} cards with class `col`")
    except Exception as e:
        print(f"Failed to find cards with class `col`: {e}")
        driver.quit()
        return []

    for i, card in enumerate(cards):  # top 5 news
        try:
            # Title and link from class 'title'
            try:
                title_el = card.find_element(By.CLASS_NAME, "title")
                title = title_el.text.strip()
                link = title_el.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                title = "N/A"
                link = "N/A"

            # Published time, optional
            try:
                time_el = card.find_element(By.CSS_SELECTOR, "span.time, time")
                published_time = time_el.text.strip()
            except:
                published_time = "N/A"


            # Description
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
            print(f"Error processing card #{i}: {e}")
            continue

    # driver.quit()
    # save_news_to_db(news_list)
    return news_list


