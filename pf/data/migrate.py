import mysql.connector
import pandas as pd
import config

beers = pd.read_csv('beers_revised.csv')
beers = beers.where((pd.notnull(beers)), '')
breweries = pd.read_csv('breweries_revised.csv')
breweries = breweries.where((pd.notnull(breweries)), '')

cnx = mysql.connector.connect(**config.creds)
cursor = cnx.cursor()

for _, row in breweries.iterrows():
	try:
		cursor.execute("""
			INSERT INTO breweries VALUES (%s,%s,%s,%s);
		""", (row['id'],row['name'],row['city'],row['state']))
	except mysql.connector.errors.IntegrityError:
		continue

for _, row in beers.iterrows():
	try:
		cursor.execute("""
			INSERT INTO beers VALUES(%s,%s,%s);
		""", (row['name'],row['style'],row['brewery_id']))
	except:
		continue

if not input('Press enter if okay'):
	cnx.commit()

cursor.close()
cnx.close()

