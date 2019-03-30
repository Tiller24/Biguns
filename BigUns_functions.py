#!/usr/bin/env python3

import os
import psycopg2
import json
import urllib.parse as urlparse

class Functions:

	url = urlparse.urlparse(os.environ['DATABASE_URL'])
	dbname = url.path[1:]
	user = url.username
	password = url.password
	host = url.hostname
	port = url.port


	try:
		conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )
	except:
		print ("I am unable to connect to the database")
		exit()
	
	curse = conn.cursor()																	# Used in executing queries
	
	
	weeks  = [];																			# The UI Friendly week names
	yt_ids = [];
	titles = [];
	curse.execute("SELECT NAME FROM WEEKS ORDER BY ID DESC;")								# Get all the database table names
	week = curse.fetchall()																	# The database table names
	
	
	
	def new_request(self,index):															# Build a new playlist based on the week clicked
		iframe = self.playlist()
		iframe_src = 'https://www.youtube.com/embed/' + iframe
		json_arr = json.dumps(self.titles)
		
		return '{"iframe" : "%s", "titles" : %s}' % (iframe_src,json_arr)	
			
			
	def playlist(self):																		# Build the new playlist
		iframe = self.yt_ids[0] + '?playlist=' #open tag
		for v in self.yt_ids[1:]:
			iframe += v + ','
		iframe = iframe[:-1]		#remove trailing comma after the loop
		return iframe
	
	def set_weeks(self):																	# Display the UI Friendly names																
		for w in self.week:
			# print(w[0])
			self.weeks.append(w[0])
		return self.weeks
		
	def set_yt_ids(self,index):																# Display the new videos
		self.yt_ids = []
		self.curse.execute("SELECT YT_ID FROM SONGS WHERE WEEK = '" + self.week[index][0].replace("'","''") + "' ORDER BY RANK")
		# print(self.week[index][0].replace("'","''"))
		y = self.curse.fetchall()
		
		for x in y:
			# print(x[0])
			self.yt_ids.append(x[0])
		return self.yt_ids
	
	def set_titles(self,index):																# Display new titles
		self.titles = []
		self.curse.execute("SELECT TITLE FROM SONGS WHERE WEEK = '" + self.week[index][0].replace("'","''") + "' ORDER BY RANK" )
		# print(self.week[index][0].replace("'","''"))
		t = self.curse.fetchall()
		for x in t:
			self.titles.append(x[0].replace("&#39;","").replace("&quot;",""))
		return self.titles
	


	#constructor
	def __init__(self, y = 0, t = 0):
		self.weeks  = self.set_weeks()
		self.yt_ids = self.set_yt_ids(y)
		self.titles = self.set_titles(t)
		
	
