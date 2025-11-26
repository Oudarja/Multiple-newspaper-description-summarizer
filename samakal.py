from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from retrieve_summarization import generate_summarization




def scrape_samakal(portal_name ,url,driver):
    # portal_name = "Samakal"
    # url = "https://samakal.com/latest/news"

    # Enable Bangla -> English auto-translate
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "translate_whitelists": {"bn": "en"},
        "translate": {"enabled": True}
    })

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    time.sleep(5)  # wait for translation

    wait = WebDriverWait(driver, 15)
    news_list = []

    try:
        cards = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "CatListNews"))
        )
        print(f"Found {len(cards)} Samakal news cards")
    except Exception as e:
        print("Failed to find cards:", e)
        driver.quit()
        return []

    for i, card in enumerate(cards):
        # Extract title and link
        try:
            head = card.find_element(By.CLASS_NAME, "CatListhead")
            title = head.find_element(By.TAG_NAME, "h3").text.strip()
            link_tag = card.find_element(By.TAG_NAME, "a")
            link = link_tag.get_attribute("href")
        except:
            title = "N/A"
            link = "N/A"

        # Extract publish time
        try:
            time_tag = card.find_element(By.CLASS_NAME, "publishTime")
            # time_font = time_tag.find_element(By.TAG_NAME, "font")
            # published_time = time_font.find_element(By.TAG_NAME, "font").get_attribute("innerText").strip()
            published_time = time_tag.get_attribute("innerText").strip()
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

        news_list.append({
            "newspaper_name": portal_name,
            "title": title,
            "link": link,
            "description":description_text,
            "summarized_description":summarized_description,
            "published_time": published_time
        })

    # driver.quit()
    return news_list
    # save_news_to_db(news_list)

