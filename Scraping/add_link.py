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

def add_links(link,to_add_link): # Arguents (Name of the Link, Array of the Links in the wiki page of that link)
	query = "CREATE TABLE IF NOT EXISTS %s(LinkName VARCHAR(256))" % (link)
	cur.execute(query)
	for linkname in to_add_link:
		query = "INSERT INTO %s VALUES('%s')" % (link,linkname)
		cur.execute(query)


connect()
add_links("Siddhant",["Genius","Sucker"])