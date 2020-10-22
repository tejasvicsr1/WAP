import requests 
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_links(wiki_link):
    # Assuming wiki_link to be of the form /wiki/page_name

    link_to_fetch = 'https://en.wikipedia.org' + wiki_link

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    r = session.get(link_to_fetch)


    # r = requests.get(link_to_fetch)

    if r.status_code != 200:
        return []
    
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find(id="mw-content-text")

    links = div.find_all('a', href=True)
    filtered_links = []

    to_remove = [':', '(', ')', '%', '#']

    for link in links:
        if  '/wiki/' == link['href'][:6] and len(link['href']) < 31:
            
            flag=False

            for sym in to_remove:
                if sym in link['href']:
                    flag=True
                    break 
        
            if flag:
                continue

            filtered_links.append(link['href'])

    filtered_links = list(dict.fromkeys(filtered_links))

    return filtered_links[:20]

def format_link_to_name(link):
    name = link[6:]
    name = name.replace("_", " ")
    return name

init_link = '/wiki/Adolf_Hitler'
finish_link = '/wiki/United_States'
new_link = init_link
score = 0

while 1:
    if(new_link == finish_link):
        break

    score = score + 1
    links = get_links(new_link)
    for i, link in enumerate(links):
        print(i, format_link_to_name(link))

    print()
    chosen = int(input("Choose a link (Enter number): "))
    new_link = links[chosen] 

print("Congrats! you reached your destination in " + str(score) + " Clicks")