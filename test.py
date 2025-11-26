import ollama
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from mzamin import scrap_mzamin
from selenium.webdriver.chrome.options import Options
# response = ollama.chat(
#     model="llama3.2:3b",  
#     messages=[
#         {"role": "system", "content": "You are a helpful AI summarizer. You will summarize the given text and try to keep the length of summarized text as small as possible.That's your work"},
#         {"role": "user", "content": "রাজধানী ঢাকায় আজ সোমবার সকালে শীতের হালকা আমেজ আরো কিছুটা অনুভূত হয়েছে। সঙ্গে ছিল হালকা কুয়াশা। রোববার ঢাকার সর্বনিম্ন তাপমাত্রা ছিল ..."}
#     ]
# )

# print(response["message"]["content"])

portal_name2="mzamin"
url2="https://mzamin.com/category.php?cat=1#gsc.tab=0"
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument("--headless")

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
list_=scrap_mzamin(portal_name2,url2,driver)
# all_news_list.append(list_)
driver.quit()

print(list_)