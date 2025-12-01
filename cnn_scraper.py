from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from retrieve_summarization import generate_summarization
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

def scrape_CNN(portal_name, url, driver):
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    # Wait for at least one headline to appear
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cd__headline a")))
    except:
        print("No headline found — page may not have loaded fully or structure changed")
        return []

    # Now fetch all headline links
    headline_links = driver.find_elements(By.CSS_SELECTOR, ".cd__headline a")
    print("Found", len(headline_links), "headline links")

    news_items = []
    visited = set()

    for link_el in headline_links:
        href = link_el.get_attribute("href")
        title = link_el.text.strip()
        if not href or not title or href in visited:
            continue
        visited.add(href)

        # Optionally skip non-article links
        if "/" not in href or "video" in href.lower():  # or other heuristics
            continue

        # Open the article
        driver.get(href)
        # wait for article body or at least some <p> tag
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))
        except:
            description = ""
        else:
            paragraphs = driver.find_elements(By.TAG_NAME, "p")
            description = " ".join(p.text for p in paragraphs if p.text.strip())

        # Get published time if exists
        try:
            published_time = driver.find_element(By.TAG_NAME, "time").text.strip()
        except:
            published_time = "N/A"

        # Add to list
        news_items.append({
            "newspaper_name": portal_name,
            "title": title,
            "link": href,
            "description": description,
            "published_time": published_time
        })

        # Go back to homepage to continue
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cd__headline a")))
        time.sleep(0.5)