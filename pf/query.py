import mysql.connector
import json

class SQLHelper:
	def __init__(self, creds):
		'''Constructor.'''
		self.cnx = mysql.connector.connect(**creds)
		self.cursor = self.cnx.cursor(buffered=True, dictionary=True)
	
	#
	def execute(self, state, style):
		'''Executes a sql serch with the input state (abreviated ex "GA") and style (ex: "ipa").'''

		state = '%' + state + '%'
		style = '%' + style + '%'
		#sql query to execute
		self.cursor.execute(
				"""select beers.name, breweries.name as brewery, city, style
				from beers 
				inner join breweries on beers.brewery_id = breweries.id
				where state like %s and style like %s
				order by brewery;""", (state,style))
		
		res = self.cursor.fetchall()
		return json.dumps(res) if res else ''

	
	def executeMAP(self, state):
		'''Executes a sql search for all bereweries in a state that the user inputs.'''
		state = '%' + state + '%'
		#sql query to execute, will return latitude (lat) and longitude (lng) for our google maps api to procces on the font end 
		self.cursor.execute(
				"""select name, city, state, lat, lng
				from breweries
				where state like %s;""", (state,))
		
		res = self.cursor.fetchall()
		return json.dumps(res) if res else ''

	def __del__(self):
		'''Desturctor.'''
		self.cursor.close()
		self.cnx.close()

