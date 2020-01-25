import mysql.connector
import config

cnx = mysql.connector.connect(**config.creds)
cursor = cnx.cursor(dictionary=True)

cursor.execute("""
	select name from breweries where lat is null;
""")

for row in cursor.fetchall():
	cursor.execute("""
		delete from beers where brewery_id = (
			select id from breweries
			where name = %s);
	""", (row['name'],))
	cursor.execute("""
		delete from breweries where name = %s;
	""", (row['name'],))

cnx.commit()
cursor.close()
cnx.close()

