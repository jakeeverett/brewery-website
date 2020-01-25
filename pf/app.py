from query import SQLHelper
import config
from pprint import pprint

#routing array of our different webpages
ROUTES = [
	'/pf/',
	'/pf/locator',
	'/pf/matcher'
]

def application(env,start_response):
	'''Serves webpages and executes sql queries with user input.'''
	
	#open our index/home page
	html = open('index.html','r').read()
	pprint(env) #TODO coment out/just for testing
	start_response('200 OK', [('Content-Type', 'text/html')])

	#get user inputed query string
	request = env["QUERY_STRING"]
	
	if env["REQUEST_METHOD"] == "GET":
		#swap to matcher.html if fount that user has clicked hyperlink
		if env["PATH_INFO"] == ROUTES[2]:
			print("matcher: true") #TODO Remove later/just for testing
			#open page
			html = open('matcher.html').read()

			#if user enters a requesr via user input it is procesed here and then executes a sql search via the query.py function execute()
			if request: 
				helper = SQLHelper(config.creds)
				input = request.split("&")
				_, state = input[0].split("=")
				_, style = input[1].split("=")
				print() #TODO remove just for testing
				print(state)
				print(style)
				print()
				values = helper.execute(state, style)#sql search with state and style


				del helper
				
				start_response('200 OK', [('Content-Type', 'text/json')])
				return values.encode() # encodeng results for front end

			start_response('200 OK', [('Content-Type', 'text/html')])
			return html.encode()
		#swap to matcher.html if fount that user has clicked hyperlink
		if env["PATH_INFO"] == ROUTES[1]:
			print("locator: true")#	TODO remove later used for testing
			html = open('locator.html').read()
			#if user enters a requesr via user input it is procesed here and then executes a sql search via the query.py function executeMAP()
			if request: 
				helper = SQLHelper(config.creds)
				_, state = request.split("=")
				print()
				print(state)
				print()
				values = helper.executeMAP(state)#sql search with the user input state


				del helper
				
				start_response('200 OK', [('Content-Type', 'text/json')])
				return values.encode() # encodeng results for front end

			start_response('200 OK', [('Content-Type', 'text/html')])
			return html.encode()

	return html.encode()

