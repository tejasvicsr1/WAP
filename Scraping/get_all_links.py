import pymysql
import pymysql.cursors

def connect():
	username = "root"
	password = "aad"
	hostname = '4.tcp.ngrok.io'
	portno = 17891
	con = pymysql.connect(host=hostname,
	                              user=username,
	                              password=password,
	                              db='Links',
	                              port=portno,
	                              cursorclass=pymysql.cursors.DictCursor)
	global cur
	cur = con.cursor()

def get_all_links():
	connect()
	query = "show tables"
	cur.execute(query)
	dict = {}
	dict = cur.fetchall()
	for linkname in dict:
		print(linkname['Tables_in_Links'])
	

get_all_links()