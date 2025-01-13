from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os


class Crawler:
    def __init__(self, baseUrl:str):
        self.baseUrl=baseUrl
        self._visited=set()
        self._queue=list()
        self._data_loc= "./data/"
        dir=os.path.dirname(self._data_loc)
        if  dir and not os.path.exists(dir):
            os.makedirs( dir)
    def _crawl(self,currUrl:str=None):
        if currUrl==None:
            currUrl=self.baseUrl
        page=requests.get(currUrl)
        soup= BeautifulSoup(page.text,'html.parser')
        for link in soup.find_all('a', href=True):
                fullUrl = urljoin(currUrl, link['href']) 
                if fullUrl not in self._visited and fullUrl.startswith("http"):
                    self._visited.add(fullUrl)
                    self._queue.append(fullUrl)
        return soup.prettify()
    def crawl_n(self,n:int):
        self._queue.append(self.baseUrl)
        for i in range(n):
            currUrl= self._queue.pop()
            print(f"Crawling from:{currUrl}\n")
            soup=self._crawl(currUrl)
            f = open(f"{self._data_loc}data_{i}.txt", "w",encoding="utf-8")
            f.write(soup)
            f.close()
        print(f"Crawled {n} pages succesfully.\n")

if __name__=="__main__":
    url="https://www.joghr.org/article/94931-understanding-key-factors-for-strengthening-nepal-s-healthcare-needs-health-systems-perspectives"
    crawler=Crawler(baseUrl=url)
    crawler.crawl_n(2)