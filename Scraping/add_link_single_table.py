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

def add_link(link,to_add_link):
	connect()
	query = "CREATE TABLE IF NOT EXISTS AllLinks(LinkName VARCHAR(1024),ConnectedLink VARCHAR(1024))"
	cur.execute(query)
	for linkname in to_add_link:
		query = """INSERT INTO AllLinks VALUES("%s","%s")""" % (link,linkname)
		cur.execute(query)
		con.commit()

add_link("Aman",['Genius','Best'])
