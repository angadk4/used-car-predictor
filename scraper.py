import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
class Scraper:
    def __init__(self):
        chrome_options = Options()
        # Using WebDriver Manager to handle the driver binaries
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.url = "http://www.kijijiautos.ca/"
        self.hrefs= []
        self.features = []

    def get_hrefs(self):
        return self.hrefs
    def load_url(self):
        self.driver.get(self.url + 'cars/sedan')
    def scroll_down(self):
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    def get_proxies(self):
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr'):
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
        return proxies

    def read_data(self):
        main = self.driver.find_element(By.XPATH, '//*[@id="root"]/div[3]/div/section[5]/div/div/div[2]')
        soup = bs(main.get_attribute("innerHTML"), "html.parser")
        print(len(soup.findAll('a',{'class':'bcNN7t'})))
        for elem in soup.findAll('a',{'class':'bcNN7t'}):
            #print(elem.div['data-test-ad-id'])
            self.hrefs.append('vip/{}'.format(str(elem.div['data-test-ad-id'])))

    def get_info(self, url):
        proxies = self.get_proxies()
        print("proxies", proxies)
        proxy_pool = cycle(proxies)
        leng = len(proxies)
        print(leng)
        for i in range(leng):
            # Get a proxy from the pool
            proxy = next(proxy_pool)
            print("Current proxy: ", proxy)
            print("Request #%d" % i)
            try:
                response = requests.get(url, proxies={"http": proxy, "https": proxy})
                print("got response")
                break
            except:
                # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
                # We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
                print("Skipping. Connnection error")


        html = response.text
        soup = bs(html, 'html.parser')

        #self.driver.get(url)
        #cf = self.driver.find_element(By.XPATH, '//*[@id="tabpanel-features"]/div/aside/div[1]/div/div[1]/div[2]/ul')
        #soup = bs(cf.get_attribute("innerHTML"), "html.parser")
        for li in soup.find_all('li'):
            txt = li.text
            if 'Make:' in txt:
                ma = (str(txt)[5:].strip())
            if 'Model:' in txt:
                mo = (str(txt)[6:].strip())
            if 'Year:' in txt:
                ye = (str(txt)[5:].strip())
        print([ma, mo, ye])
        label = soup.find_all("span", {"class": "G2jAym E2jAym p2jAym b2jAym"})
        print(label)
        return [ma, mo, ye], label


