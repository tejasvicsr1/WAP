import pymysql
import pymysql.cursors

def connect():
	username = "root"
	password = "blahblah"
	con = pymysql.connect(host='localhost',
	                              user=username,
	                              password=password,
	                              db='Links',
	                              cursorclass=pymysql.cursors.DictCursor)
	global cur
	cur = con.cursor()

def return_link(link):
	connect()
	query = """SELECT * FROM `%s`""" % (link)
	cur.execute(query)
	dict = {}
	dict = cur.fetchall()
	connected_links = []
	for link_name in dict:
		connected_links.append(link_name['LinkName'])
	return connected_links

return_link("Aman")



