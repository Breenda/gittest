#coding=utf-8
import requests
import time
from bs4 import BeautifulSoup
import random
from fake_useragent import UserAgent
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
class spider:
    def __init__(self):
        self.ip_url = "http://218.24.50.100:23456/?key=abcdefg12345678"
        # self.f_data = open("data.txt", "w", encoding="utf8")
        # ua = UserAgent()
        # self.headers = {
        #     'User-Agent': ua.random,
        #     'Connection': 'close'
        # }
        self.browser = webdriver.Chrome(executable_path="C:\\Users\Administrator\AppData\Local\Programs\Python\Python36\chromedriver.exe")
        self.split_sign="+=+="
        self.origin="tatoeba.org"
        self.chrome_options=webdriver.ChromeOptions()
    def start(self,temp_dict):
        page_number=None
        language1 = temp_dict[list(temp_dict.keys())[0]]
        language2 = temp_dict[list(temp_dict.keys())[1]]
        link = "https://tatoeba.org/cmn/sentences/search?from=" + language1 + "&to=" + language2
        try:
            page_number = self.get_page_number(link)
        except Exception as e:
            print(e)
            return
        else:
            if page_number==None:
                return
            for i in range(2, page_number + 1):
                new_link = link + "&page=" + str(i)
                html = self.get_html(new_link)
                self.get_data(html)

    def get_data(self,html):
        all_div_part=html.find_all("div","sentence-and-translations ng-scope md-whiteframe-1dp")
        for single_div in all_div_part:
            all_sents=single_div.find_all("div","text flex")
            first_sent=all_sents[0].get_text().strip()
            other_sents=all_sents[1:]
            for other_sent in other_sents:
                new_line=first_sent+self.split_sign+other_sent.get_text().strip()+self.split_sign+self.origin
                print(new_line)
    def get_page_number(self,link):
        html=self.get_html(link)
        if html==None:
            return
        page_number_part=html.find("ul","paging").find_all("a")
        page_number=page_number_part[-2].get_text()
        self.get_data(html)
        return int(page_number)
    def get_random_ip(self):
        data=requests.get(self.ip_url)
        useful_data=json.loads(data.text)['ip']
        return random.sample(useful_data,1)
    def get_html(self, link):
        temp_ip=self.get_random_ip()[0]
        temp_ip_line="--proxy-server=http:"+temp_ip
        self.chrome_options.add_argument(temp_ip_line)
        self.browser.chrome_options=self.chrome_options
        self.browser.get(link)
        useful_data=None
        while 1:
            start_time=time.clock()
            try:
                useful_data=self.browser.find_element_by_class_name("section")
            except:
                continue
            else:
                print("已经定位到元素")
                end=time.clock()
                break
        print("定位耗时：",str(end-start_time))
        if useful_data==None:
            return None
        else:
            print(useful_data)
            return BeautifulSoup(useful_data,"html.parser")

    def get_ip(self):
        for i in range(5):
            try:
                html=requests.get("http://218.24.50.100:23456/?key=abcdefg12345678")
                useful_dict=json.loads(html.text)
            except:
                continue
            else:
                return random.sample(useful_dict["ip"],1)


if __name__ == "__main__":
    temp_dict = {'中文': 'cmn', '印尼': 'ind'}
    spider().start(temp_dict)