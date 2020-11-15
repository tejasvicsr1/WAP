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

def add_links(link,to_add_link): # Arguents (Name of the Link, Array of the Links in the wiki page of that link)
	query = "CREATE TABLE IF NOT EXISTS %s(LinkName VARCHAR(256))" % (link)
	cur.execute(query)
	for linkname in to_add_link:
		print(linkname)
		query = "INSERT INTO %s ( LinkName ) VALUES('%s')" % (link,linkname)
		cur.execute(query)
		print(query)
	con.commit()


connect()
add_links("asdf",["Genius","Sucker"])