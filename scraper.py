from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class Scraper():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver  = webdriver.Chrome('chromedriver',options=chrome_options)
        self.driver.implicitly_wait(5)
    
    def quote_scraper(self,tag):
        qlist = []
        try:
            url = f"https://quotes.toscrape.com/tag/{tag}/"
            self.driver.get(url)
            cond = True
            while(cond):
                sleep(1)
                page = BeautifulSoup(self.driver.page_source, 'html.parser')
                quotes = page.find_all("div", {"class": "quote"})
                for q in quotes:
                    qlist.append({
                        'text' : q.find("span", {"class": "text"}).text.strip()[1:-1],
                        'author' : q.find("small", {"class": "author"}).text.strip()
                    })
                try:
                    self.driver.find_element(By.CLASS_NAME,'next').find_element(By.TAG_NAME,'a').click()
                except:
                    cond = False
        except:
            print('No quotes found for this tag.')

        return qlist
    
    def quit_scraper(self):
        self.driver.quit()
