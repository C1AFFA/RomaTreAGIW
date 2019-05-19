from selenium import webdriver
import time
import math
from bs4 import BeautifulSoup
import re


class Extractor():
    def __init__(self , ratio = 1.55):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome("/usr/bin/chromedriver" , options=options)
        self.current_page_url = None
        self.url_img_extracted = None
        self.ratio = ratio
    
    def extract(self, page):
        self.current_page_url = page
        self.driver.get(self.current_page_url)
        time.sleep(3)
        images = self.driver.find_elements_by_tag_name('img')
        half = math.floor(len(images))
        images = images[:half]
        prevWidth = 0
        for image in images :
            size = image.size
            if size["height"] > 0 and size["width"] > 0:
                ratio = (size["width"]/size["height"] if size["width"] > size["height"] else size["height"]/size["width"])
                if abs(1 - ratio) < self.ratio and prevWidth < size["width"]:
                    prevWidth = size["width"]
                    self.url_img_extracted = image.get_attribute("src")

    def get_body_text(self, page):
        self.current_page_url = page
        self.driver.get(self.current_page_url)
        time.sleep(3)
        body = self.driver.find_elements_by_tag_name('html')[0]
        html = body.get_attribute('innerHTML')
        soup = BeautifulSoup(html)
        body = soup.find('body')
        [x.extract() for x in body.findAll('script')]
        [x.extract() for x in body.findAll('style')]
        text=re.sub("\s\s+", " ", body.get_text())
        return text


    def stop(self):
        self.driver.close()