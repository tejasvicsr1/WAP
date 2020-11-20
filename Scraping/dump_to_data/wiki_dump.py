import pymysql.cursors
import pymysql
import codecs
from cleaner import Cleaner
from iterate import iterate
from tqdm import tqdm
import multiprocessing
from time import sleep
from xml.etree import ElementTree

cleaner = Cleaner()


# FOR DB


def connect():
    username = "root"
    password = "aad"
    global con
    con = pymysql.connect(host='localhost',
                          port=3306,
                          user=username,
                          password=password,
                          db='Links',
                          cursorclass=pymysql.cursors.DictCursor,
                          use_unicode=True,
                          charset='utf8')
    global cur
    cur = con.cursor()


# Arguents (Name of the Link, Array of the Links in the wiki page of that link)
def add_links(link, to_add_link):
    if len(link)>63:
        return
    query = """CREATE TABLE IF NOT EXISTS `%s` (LinkName VARCHAR(63) unique)"""%(link)
    # print(cur.mogrify(query))
    cur.execute(query)
    for linkname in to_add_link:
        if len(linkname)>63:
            continue 
        try:
            query = """INSERT INTO `%s` ( LinkName ) VALUES("%s")"""%(link, linkname)
            cur.execute(query)
        except:
            pass
            # print(link, linkname)
    con.commit()


connect()
# FOR DB END


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
    title = title_elem.text

    # print(title)

    _, links = cleaner.build_links(text_elem.text)
    link_names = []
    for link in links:
        link_names.append(link["link"])
    add_links(title, link_names)


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


if __name__ == '__main__':
    path_to_dump_xml = 'D:\\College\\enwiki-20200401-pages-articles-multistream.xml'
    processes = []
    i = 0
    for content in tqdm(itr_chunks(path_to_dump_xml)):
        p = multiprocessing.Process(
            target=multiprocessing_func, args=(content,))
        processes.append(p)
        p.start()
        i += 1

        if i%5==0:
            print("Joining last 5 processes")
            for x in processes:
                x.join()
            print("Joined last 5 processes")

    for process in processes:
        process.join()
