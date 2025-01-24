from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os
import csv

class Crawler:
    def __init__(self, baseUrl: str = None, keywords: list = None):
        self.baseUrl = baseUrl
        self.header = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "connection": "keep-alive",
            "cache-control": "no-cache",
        }
        self._exclude = [
            "section", "for-authors",
            "editorial-board", "about", "issues",
            "posts", "toggle", "view=desktop", "search"
        ]
        self._keywords = keywords or [
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
        self._visited = set()
        self.queue = []
        self._data_loc = "./data/"
        os.makedirs(self._data_loc, exist_ok=True)

    def _crawl(self, currUrl: str = None):
        """Fetch a webpage and return its BeautifulSoup object."""
        try:
            page = requests.get(currUrl, headers=self.header)
            page.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {currUrl}: {e}")
            return None
        soup = BeautifulSoup(page.text, 'html.parser')

        # Add links to the queue for further crawling
        for link in soup.find_all('a', href=True):
            fullUrl = urljoin(currUrl, link['href'])
            if fullUrl not in self._visited and fullUrl.startswith("http") and not any(keyword in fullUrl for keyword in self._exclude):
                self._visited.add(fullUrl)
                self.queue.append(fullUrl)

        return soup

    def crawl_n(self, n: int):
        """Crawl n documents and save each as a CSV file."""
        count = 0

        while count < n and self.queue:
            currUrl = self.queue.pop(0)
            print(f"Crawling: {currUrl}")

            soup = self._crawl(currUrl)
            if not soup:
                continue

            # Extract the title
            title = soup.title.string.strip() if soup.title else "No Title"

            # Extract and clean the content
            content = soup.get_text(separator=' ')
            content = content.replace("\n", " ").replace("\r", " ").strip()

            # Check for relevant keywords in the content
            if any(keyword in content.lower() for keyword in self._keywords):
                # Save the data to a CSV file
                csv_file = os.path.join(self._data_loc, f"data{count + 1}.csv")
                with open(csv_file, mode='w', encoding='utf-8', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=["URL", "Title", "Content"])
                    writer.writeheader()
                    writer.writerow({
                        "URL": currUrl,
                        "Title": title,
                        "Content": content
                    })
                print(f"Document {count + 1} saved to {csv_file}")
                count += 1

        print(f"Finished crawling {count} documents.")

if __name__ == "__main__":
    # List of starting URLs
    starting_urls = [
        "https://healthcare-digital.com/top10/top-10-healthcare-websites",
        "https://pubmed.ncbi.nlm.nih.gov/",
        "https://www.cdc.gov/"
    ]

    # Initialize and run the crawler
    crawler = Crawler()
    crawler.queue.extend(starting_urls)
    crawler.crawl_n(300)