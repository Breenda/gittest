#coding=utf-8
import time
import requests
import random
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class spider:
    def __init__(self):
        self.ip_url="http://218.24.50.100:23456/?key=abcdefg12345678"
        ua=UserAgent()
        self.headers={
            'User-Agent': ua.random,
            'Connection': 'close'
        }
        self.split_sign="+=+="
    def start(self,language_dict):
        file_name="_".join(language_dict.keys())+".txt"
        # file_io=open(file_name,"w",encoding="utf8")#打开句对文件io
        language1=language_dict[list(temp_dict.keys())[0]]
        language2=language_dict[list(temp_dict.keys())[1]]
        link="https://tatoeba.org/cmn/sentences/search?from="+language1+"&to="+language2
        try:
            page_number=self.get_page_number(link)
        except Exception as e:
            print(e)
            return
        else:
            for i in range(2,page_number+1):
                new_link=link+"&page="+str(i)
                html=self.get_html(new_link)
                self.get_data(html)

    def get_page_number(self,link):
        html=self.get_html(link)
        page_part=html.find("ul","paging").find_all("a")[-2]
        self.get_data(html)
        return int(page_part.get_text())
    def get_data(self,html):
        sents=html.find_all("div","sentence-and-translations ng-scope md-whiteframe-1dp")
        for sent in sents:
            main_sent=sent.find("div","direct translations layout-column").find("div","text flex").get_text()
            other_sents=sent.find_all("div","text flex")[1:]
            for other_sent in other_sents:
                new_text=main_sent+self.split_sign+other_sent.get_text()+self.split_sign+"https://tatoeba.org/eng/sentences/show/"
                print(new_text)
    def get_html(self, link):
        print(link)
        for i in range(5):
            try:
                ip = self.get_random_ip()
                print(ip)
                proxies = {'http': ip}
                html = requests.get(link, headers=self.headers, proxies=proxies, timeout=20)
            except Exception as e:
                print(e)
            else:
                if html.status_code!=200:
                    continue
                html = BeautifulSoup(html.content, "html.parser")
                if html==None:
                    return 0
                return html
    def get_random_ip(self):
        data=requests.get(self.ip_url)
        useful_data=json.loads(data.text)['ip']
        return random.sample(useful_data,1)

    def __del__(self):
        pass
if __name__=="__main__":
    temp_dict={'中文': 'cmn', '印尼': 'ind'}
    spider().start(temp_dict)

