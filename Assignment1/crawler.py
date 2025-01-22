from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os

class Crawler:
    def __init__(self, baseUrl:str):
        self.baseUrl=baseUrl
        # self.header = {
        #         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #         "accept-encoding": "gzip, deflate, br",
        #         "accept-language": "en-US,en;q=0.9",
        #         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        #         "connection": "keep-alive",
        #         "cache-control": "no-cache",
        #     }
        self._exclude=[
            "section",  "for-authors", 
            "editorial-board", "about", "issues", 
            "posts", "toggle", "view=desktop","search"
        ]
        self._visited=set()
        self._queue=list()
        self._data_loc= "./data/"
        dir=os.path.dirname(self._data_loc)
        if  dir and not os.path.exists(dir):
            os.makedirs( dir)
    def _crawl(self,currUrl:str=None):
        if currUrl==None:
            currUrl=self.baseUrl
        try:
            page=requests.get(currUrl)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {currUrl}: {e}")
            return None
        soup= BeautifulSoup(page.text,'html.parser')
        for link in soup.find_all('a', href=True):
                fullUrl = urljoin(currUrl, link['href']) 
                if fullUrl not in self._visited and fullUrl.startswith("http") and not any(keyword in fullUrl for keyword in self._exclude) :
                    self._visited.add(fullUrl)
                    self._queue.append(fullUrl)
        return soup
    def crawl_n(self,n:int):
        self._queue.append(self.baseUrl)
        i=0
        while i < n:
            currUrl= self._queue.pop(0)
            print(f"Crawling from:{currUrl}\n")
            soup=self._crawl(currUrl)
            f = open(f"{self._data_loc}data_{i}.txt", "a",encoding="utf-8")
            text_found=False
            for text in soup.find_all('div'):
                curr_text=text.get_text()
                if curr_text:
                    f.write(curr_text)
                    text_found=True
            f.close()
            if text_found:
                i+=1
        print(f"Crawled {n} pages succesfully.\n")

if __name__=="__main__":
    url="https://www.joghr.org/article/94931-understanding-key-factors-for-strengthening-nepal-s-healthcare-needs-health-systems-perspectives"
    crawler=Crawler(baseUrl=url)
    crawler.crawl_n(40)