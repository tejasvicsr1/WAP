import requests 
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pickle
import time
from datetime import datetime

import pymysql
import pymysql.cursors

def connect():
	username = "root"
	password = "aad"
	global con
	con = pymysql.connect(host='localhost',
								  port=3306,
	                              user=username,
	                              password=password,
	                              db='Links',
	                              cursorclass=pymysql.cursors.DictCursor)
	global cur
	cur = con.cursor()

connect()

# while True:
# 	cur.execute("SHOW TABLES;")
# 	tables = cur.fetchall()
# 	con.commit()
# 	now = datetime.now()
# 	current_time = now.strftime("%H:%M:%S")
# 	print(current_time, ":\t", len(tables))
# 	time.sleep(10)

# cur.execute("SELECT * from Czechs;")
cur.execute("SHOW TABLES;")

dicti = {}

tables = cur.fetchall()
print(len(tables))
for x in tables:
    dicti[x["Tables_in_Links"]] = 1

with open('table_names.pickle', 'wb') as handle:
    pickle.dump(dicti, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('table_names.pickle', 'rb') as handle:
    b = pickle.load(handle)

print(b==dicti)

# while True:
# 	cur.execute("SHOW TABLES;")
# 	tables = cur.fetchall()
# 	now = datetime.now()
# 	current_time = now.strftime("%H:%M:%S")
# 	print(current_time, ":\t", len(tables))
# 	time.sleep(10)