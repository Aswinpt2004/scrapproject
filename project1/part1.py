import requests
import requests.exceptions
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from collections import deque

class crawl():
    def __init__(self, url , key_word) -> None:
        self.new_url=deque([(url,0)])
        self.all_url_log = open("self.all_url_log.txt","w+")
        self.processed_urls = set()
        self.key_word = key_word

    def bfs_url_crawler(self):
        url_count = 0
        stop_flag = 0
        local_urls = set()

        while len(self.new_url) and not stop_flag:
            if len(self.new_url) > 1000:
                stop_flag = 1
            # pop the url and put all the neigbour in the queue
            pop_val = self.new_url.popleft()
            url, cur_level = pop_val
            #url, cur_level = self.new_url.popleft()
            info =f"url: {url} - depth level: {cur_level}\n" 
            self.all_url_log.write(info)
            self.processed_urls.add(url)

            url_count += 1
            #log writter for cli

            if cur_level > 3:
                print("url out of scope")
                continue
             
            try:
                response = requests.get(url) 
            except:
                print("broken url 404")
                continue

            url_parts = urlsplit(url)
            base_url = "{0.scheme}://{0.netlock}".format(url_parts)
            soup =BeautifulSoup(response.text,'lxml')

            for link in soup.find_all("a"):
                anchor_link = link.get('href')
                if not anchor_link.startswith('/') and self.key_word not in anchor_link:
                   continue 
                
                local_link = f"{base_url}{anchor_link}"
                print(local_link)

                if local_link not in self.processed_urls:
                    self.new_url.append((anchor_link, cur_level+1))


if __name__ == "__main__":
    url = "https://www.mayoclinic.org/diseases-conditions"
    path_level = ["index"]
    key_word = ["diseases-conditions"]
    
    crawler= crawl(url)
    crawler.bfs_url_crawler()

