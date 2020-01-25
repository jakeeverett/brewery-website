import mysql.connector
import requests
import config
import json

BASE_URL_SEARCH = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
BASE_URL_DETAILS = 'https://maps.googleapis.com/maps/api/place/details/json'

cnx = mysql.connector.connect(**config.creds)
cursor = cnx.cursor(dictionary=True)

cursor.execute("""
		select * from breweries;""")

for row in cursor.fetchall():
	payload = {
			'key': config.GOOG_KEY, 
			'input': row['name'] + '+' + row['city'] + '+' + row['state'],
			'inputtype': 'textquery'
	}
	search = requests.get(BASE_URL_SEARCH, params=payload).json()
	
	# arr = json.loads(search)
	try:
		payload2 = {
			'key': config.GOOG_KEY,
			'place_id': search['candidates'][0]['place_id']
		}
	except IndexError:
		print(row['name'])
		continue
	search2 = requests.get(BASE_URL_DETAILS, params=payload2).json()
	
	lat = search2['result']['geometry']['location']['lat']
	lng = search2['result']['geometry']['location']['lng']
	'''
	print(row['name'] + ' in ' + row['city'] + ', ' + row['state']
			+ ' is at lat ' + str(lat) + ' and lng ' + str(lng))
	'''
	cursor.execute("""
		update breweries set lat = %s, lng = %s where name = %s and city = %s;
	""", (lat, lng, row['name'], row['city']))

cnx.commit()
cursor.close()
cnx.close()
