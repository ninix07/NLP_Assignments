from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os
import brotli

class Crawler:
    def __init__(self, baseUrl:str=None,keywords:list=None):
        self.baseUrl=baseUrl
        self.header = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "connection": "keep-alive",
                "cache-control": "no-cache",
            }
        self._exclude=[
            "section",  "for-authors", 
            "editorial-board", "about", "issues", 
            "posts", "toggle", "view=desktop","search"
        ]
        self._keywords= [
    
                "healthcare", "health", "hospital", "clinic", "emergency", "primary care",
                "disease", "infection", "symptoms", "diagnosis", "treatment", "therapy",
                "chronic", "acute", "mental health", "cancer", "diabetes", "cardiology",
                "clinical trial", "meta-analysis", "systematic review", "case study",
                "epidemiology", "randomized controlled trial", "biostatistics",
                "nutrition", "exercise", "stress", "prevention", "self-care", "fitness",
                "vaccination", "immunization", "screening",
                
                "health policy", "public health", "health reform", "universal healthcare",
                "insurance", "health equity", "pandemic", "quarantine", "outbreak"
            ]
        self._visited=set()
        self.queue=list()
        self._data_loc= "./data/"
        dir=os.path.dirname(self._data_loc)
        if  dir and not os.path.exists(dir):
            os.makedirs( dir)
    def _crawl(self,currUrl:str=None):
        if currUrl==None:
            if self.baseUrl:
                currUrl=self.baseUrl
            else:
                currUrl=self.queue.pop(0)
        try:
            page=requests.get(currUrl,headers=self.header)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {currUrl}: {e}")
            return None
        soup= BeautifulSoup(page.text,'html.parser')
        for link in soup.find_all('a', href=True):
                fullUrl = urljoin(currUrl, link['href']) 
                if fullUrl not in self._visited and fullUrl.startswith("http") and not any(keyword in fullUrl for keyword in self._exclude) :
                    self._visited.add(fullUrl)
                    self.queue.append(fullUrl)
        return soup
    def crawl_n(self,n:int):
        i=0
        while i < n:
            currUrl= self.queue.pop(0)
            print(f"Crawling from:{currUrl}\n")
            soup=self._crawl(currUrl)
            f = open(f"{self._data_loc}data_{i}.txt", "a",encoding="utf-8")
            if soup:
                curr_text=soup.get_text()
            else:
                 continue
            if curr_text and any(keyword in curr_text for keyword in self._keywords):
                    f.write(curr_text)
                    i+=1
            f.close()
                
        print(f"Crawled {n} pages succesfully.\n")

if __name__=="__main__":
    # url="https://www.joghr.org/article/94931-understanding-key-factors-for-strengthening-nepal-s-healthcare-needs-health-systems-perspectives"
    crawler=Crawler()
    crawler.queue.append("https://pmc.ncbi.nlm.nih.gov/articles/PMC8285156/")
    crawler.crawl_n(300)