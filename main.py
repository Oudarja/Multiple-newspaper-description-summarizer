from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from amarsomy import scrape_amadershomoy
from bhorer_kagoj import scrape_bhorerkagoj
from ittefaq import scrape_ittefaq
from samakal import scrape_samakal
from prothom_alo import scrape_prothomalo
from mzamin import scrap_mzamin
from  save_news import save_news_to_db
from database import SessionLocal
from model import LatestNews
from selenium.webdriver.chrome.options import Options

def scrap_and_summarize():
    portal_name1 = "Dainik Amader Shomoy"
    url1 = "https://www.dainikamadershomoy.com/latest/all"
    
    portal_name2="Bhorer Kagoj"
    url2="https://www.bhorerkagoj.com/latest"

    portal_name3="Ittefaq"
    url3="https://www.ittefaq.com.bd/latest-news"

    portal_name4="Samakal"
    url4="https://samakal.com/latest/news"

    portal_name5 = "Prothom Alo"
    url5 = "https://en.prothomalo.com/collection/latest"

    portal_name6="mzamin"
    url6="https://mzamin.com/category.php?cat=1#gsc.tab=0"

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--headless")

    all_news_list=[]

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        list_=scrape_amadershomoy(portal_name1,url1,driver)
        all_news_list.append(list_)
        driver.quit()
    except Exception as e:
        print(f"Error found as {e}")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        list_=scrape_bhorerkagoj(portal_name2,url2,driver)
        all_news_list.append(list_)
        driver.quit()
    except Exception as e:
        print(f"Error found as {e}")
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        list_=scrape_ittefaq(portal_name3,url3,driver)
        all_news_list.append(list_)
        driver.quit()
    except Exception as e:
        print(f"Error found as {e}")
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        list_=scrape_samakal(portal_name4,url4,driver)
        all_news_list.append(list_)
        driver.quit()
    except Exception as e:
        print(f"Error found as {e}")
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        list_=scrape_prothomalo(portal_name5,url5,driver)
        all_news_list.append(list_)
        driver.quit()
    except Exception as e:
        print(f"Error found as {e}")
    

      
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        list_=scrape_prothomalo(portal_name5,url6,driver)
        all_news_list.append(list_)
        driver.quit()
    except Exception as e:
        print(f"Error found as {e}")
    


    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        list_=scrap_mzamin(portal_name6,url6,driver)
        all_news_list.append(list_)
        driver.quit()
    except Exception as e:
        print(f"Error found as {e}")


    

    
    db = SessionLocal()
    # Get the last inserted row based on id (primary key)
    last_row = db.query(LatestNews).order_by(LatestNews.id.desc()).first()

    if last_row:
        scrape_id = last_row.scrape_id+1
    else:
        scrape_id = 1
    
    for list_dict in all_news_list:
            save_news_to_db(list_dict,scrape_id) 

if __name__ == "__main__":
    scrap_and_summarize()