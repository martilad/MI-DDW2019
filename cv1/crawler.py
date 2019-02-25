import requests
import time
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'DDW',
}
def crawler(seed):
    frontier=[seed]
    crawled=[]
    while frontier:
        page=frontier.pop()
        try:
            time.sleep(1)
            print('Crawled:'+page)
            if page not in crawled:

                 source = requests.get(page, headers=headers).text
            
                 soup=BeautifulSoup(source, "html5lib")
                 
                 links=soup.findAll('a',href=True)
                 
                 for link in links:
                     
                     if page not in crawled:
                          if link['href'].split("/")[1] == "city":
                               print("City: " + link['href'].split("/")[-1])
                          if link['href'].split("/")[1] == "person":
                               print("Person: " + link['href'].split("/")[-1])
                          frontier.append(seed + link['href'])
                 crawled.append(seed + link['href'])

        except Exception as e:
            print(e)
    return crawled

crawler('http://127.0.0.1:8000')
