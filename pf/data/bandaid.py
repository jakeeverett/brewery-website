import mysql.connector
import config

cnx = mysql.connector.connect(**config.creds)
cursor = cnx.cursor(dictionary=True)

cursor.execute("""select * from breweries;""")

for row in cursor.fetchall():
	state = row['state'].strip()
	cursor.execute("""update breweries
			set state = %s
			where name = %s;""", (state, row['name']))
	
cnx.commit()
cursor.close()
cnx.close()

