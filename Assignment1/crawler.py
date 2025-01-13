from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os


class Crawler:
    def __init__(self, baseUrl:str):
        self.baseUrl=baseUrl
        self.visited=set()
        self.queue=list()
        self.data_loc= "./data/"
        dir=os.path.dirname(self.data_loc)
        if  dir and not os.path.exists(dir):
            os.makedirs( dir)
    def _crawl(self,currUrl:str=None):
        if currUrl==None:
            currUrl=self.baseUrl
        page=requests.get(currUrl)
        soup= BeautifulSoup(page.text,'html.parser')
        for link in soup.find_all('a', href=True):
                full_url = urljoin(currUrl, link['href']) 
                if full_url not in self.visited and full_url.startswith("http"):
                    self.visited.add(full_url)
                    self.queue.append(full_url)
        return soup.prettify()
    def crawl_n(self,n:int):
        self.queue.append(self.baseUrl)
        for i in range(n):
            currUrl= self.queue.pop()
            print(f"Crawling from:{currUrl}\n")
            soup=self._crawl(currUrl)
            f = open(f"{self.data_loc}data_{i}.txt", "w",encoding="utf-8")
            f.write(soup)
            f.close()
        print(f"Crawled {n} pages succesfully.\n")

if __name__=="__main__":
    url="https://www.joghr.org/article/94931-understanding-key-factors-for-strengthening-nepal-s-healthcare-needs-health-systems-perspectives"
    crawler=Crawler(baseUrl=url)
    crawler.crawl_n(2)