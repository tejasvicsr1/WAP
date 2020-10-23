import requests 
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pickle

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

saved_data = {}

try:
    with open('database.pickle', 'rb') as handle:
        saved_data = pickle.load(handle)
except:
    print("No saved data, starting fresh\n\n")

def get_links(wiki_link):
    # Assuming wiki_link to be of the form /wiki/page_name

    if(wiki_link in saved_data.keys()):
        return saved_data[wiki_link]


    link_to_fetch = 'https://en.wikipedia.org' + wiki_link

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

    saved_data[wiki_link] = filtered_links[:5]

    with open('database.pickle', 'wb') as handle:
        pickle.dump(saved_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


    return saved_data[wiki_link]

def format_link_to_name(link):
    name = link[6:]
    name = name.replace("_", " ")
    return name




init_link = '/wiki/India'
finish_link = '/wiki/Deadmau5'
new_link = init_link
score = 0

print("Task: go from "+format_link_to_name(init_link)+" to "+format_link_to_name(finish_link))
print()

while 1:
    if(new_link == finish_link):
        break

    score = score + 1
    links = get_links(new_link)
    print("Links found on "+new_link)
    print("------------------------------")
    for i, link in enumerate(links):
        print(i, format_link_to_name(link))

    print()
    chosen = int(input("Choose a link (Enter number): "))
    new_link = links[chosen] 

print("Congrats! you reached your destination in " + str(score) + " Clicks")


print("\n\nSolving for shortest path...\n\n")

link_mapper = {
    init_link: 1,
}

node_mapper = {
    1: init_link,
}

num = 2
queue = [(1, 0)]

while 1:
    cur_node, dist = queue[0]
    queue.pop(0)

    print("Current link: "+node_mapper[cur_node])

    if node_mapper[cur_node] == finish_link:
        print(dist)
        break
    
    links = get_links(node_mapper[cur_node])

    for link in links:
        if link in link_mapper.keys():
            continue
        link_mapper[link] = num
        node_mapper[num] = link
        
        queue.append((num, dist+1))
        num += 1

