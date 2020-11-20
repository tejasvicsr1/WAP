import pymysql
import pymysql.cursors

def connect():
	username = "root"
	password = "blahblah"
	global con
	con = pymysql.connect(host='localhost',
	                              user=username,
	                              password=password,
	                              db='Links',
	                              cursorclass=pymysql.cursors.DictCursor)
	global cur
	cur = con.cursor()

def return_link(link):
	connect()
	query = """SELECT ConnectedLink FROM AllLinks WHERE LinkName = "%s" """ % (link)
	cur.execute(query)
	dict = {}
	dict = cur.fetchall()
	connected_links = []
	for linkname in dict:
		connected_links.append(linkname['ConnectedLink'])
	return connected_links

return_link("Aman")

