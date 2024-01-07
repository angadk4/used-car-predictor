import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
class Scraper:
    def __init__(self):
        chrome_options = Options()
        # Using WebDriver Manager to handle the driver binaries
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.url = "http://www.kijijiautos.ca/"
        self.hrefs= []
        self.features = []

    def get_features(self, url):
        self.get_info(url)
        return self.features
    def get_hrefs(self):
        return self.hrefs
    def load_url(self):
        self.driver.get(self.url + 'cars/sedan')

    def scroll_down(self):
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

    def read_data(self):
        main = self.driver.find_element(By.XPATH, '//*[@id="root"]/div[3]/div/section[5]/div/div/div[2]')
        soup = bs(main.get_attribute("innerHTML"), "html.parser")
        print(len(soup.findAll('a',{'class':'bcNN7t'})))
        for elem in soup.findAll('a',{'class':'bcNN7t'}):
            #print(elem.div['data-test-ad-id'])
            self.hrefs.append('vip/{}'.format(str(elem.div['data-test-ad-id'])))

    def get_info(self, url):
        self.driver.get(url)
        time.sleep(1)
        cf = self.driver.find_element(By.XPATH, '//*[@id="tabpanel-features"]/div/aside/div[1]/div/div[1]/div[2]/ul')
        soup = bs(cf.get_attribute("innerHTML"), "html.parser")
        for li in soup.find_all('li'):
            txt = li.text
            if 'Make' in txt:
                ma = (str(txt)[5:].strip())
            if 'Model' in txt:
                mo = (str(txt)[6:].strip())
            if 'Year' in txt:
                ye = (str(txt)[5:].strip())
        self.features.append([ma, mo, ye])


