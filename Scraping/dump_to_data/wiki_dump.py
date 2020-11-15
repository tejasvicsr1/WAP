import codecs
from cleaner import Cleaner
from iterate import iterate
from tqdm import tqdm
import multiprocessing
from time import sleep
from xml.etree import ElementTree

cleaner = Cleaner()



def itr_chunks(path):

    dump = codecs.open(path, 'r', 'utf8')

    while True:
        line = dump.readline()
        line = line.strip()
        
        if line == '<page>':
            content = [line]
            
            num_pages = 0

            while num_pages != 5000:
                line = dump.readline()
                line = line.strip()

                content.append(line)
                if line == '</page>':
                    num_pages += 1
            
            yield content

def save_deet(page):
    tree = ElementTree.fromstring(page)
    title_elem = tree.find('title')
    text_elem = tree.find('revision/text')
    
    if title_elem == None or text_elem == None:
        return
    
    text, links = cleaner.build_links(text_elem.text)
    # print(links)

def multiprocessing_func(content):
    page = None
    for line in content:
        if line == '<page>':
            page = [line]
        elif line == '</page>':
            page.append(line)
            page = '\n'.join(page)
            # print(page)
            save_deet(page)
            page = None
        else:
            page.append(line)
        
    print("done")

if __name__ == '__main__':
    path_to_dump_xml = 'D:\\College\\enwiki-20200401-pages-articles-multistream.xml'
    processes = []
    i = 0
    for content in tqdm(itr_chunks(path_to_dump_xml)):
        p = multiprocessing.Process(target=multiprocessing_func, args=(content,))
        processes.append(p)
        p.start()
        i += 1

        if i == 0:
            break

    for process in processes:
        process.join()