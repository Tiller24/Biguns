#!/usr/bin/env python3
import requests								#to get the website html
import re		
from bs4 	  import BeautifulSoup
import psycopg2
import os
import urllib.parse as urlparse
from yt_id    import yt_id					#obtain the youtube id's of each video found

class Database:

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
	
	curse = conn.cursor()
	
	weeks = []
	name  = ""

	def first_page(self):
		urls = []
		latest_biguns = 'http://hardrockdaddy.com/category/siriusxm-octane-big-uns-countdown/'		# domain
		response = requests.get(latest_biguns,headers={'User-Agent':'Mozilla/5.0'})					# request the webpage html
		soup = BeautifulSoup(response.text,"html.parser")											# parse response											
		blog_items = soup.findAll("div", {"class" : "home-blog-post-item"})							# find all the bigun links on first page
		for b in blog_items:
			urls.append(b.find("h2").find("a")['href'])												# add url to list of urls
			self.weeks.append(b.find("h2").find("a").getText())										# the week names
		
		self.name = self.weeks[0].replace("'","''").replace("–","-").replace("‘","''")				# name of the week
		self.curse.execute("SELECT * FROM WEEKS WHERE name = '" + self.name + "'")					# see if we already added the recent week
		
		if len(self.curse.fetchall()) < 1:
			return urls[0]
		else:
			return None																				# if we did, don't return anything
	
	
	def new_playlist(self,url):
		
		songlist  = self.scrape(url)																# Scrape for the songlist
		vid 	  = yt_id(songlist)																	# use the Youtube API to search for songs
		titles	  = vid.get_titles()																# titles obtained from Youtube API
		videos    = vid.get_videos()																# video IDs obtained from Youtube API
		
		self.curse.execute("SELECT * FROM WEEKS;")
		insert_index = len(self.curse.fetchall())	
		
		insert_query = "INSERT INTO WEEKS (ID,NAME) VALUES (" + str(insert_index) + ",\'" + self.name + "\')"
		
		self.curse.execute(insert_query)
		# self.conn.commit()
		
		self.insert(songlist,videos,titles)															# add the songs to the newly created table
	
	def scrape(self,website):
		songlist = []	#store the songs and artist name
		response = requests.get(website,headers={'User-Agent':'Mozilla/5.0'})						# request the webpage html
	
		soup = BeautifulSoup(response.text,"html.parser")											# parse webpage								
		songs = soup.findAll('tr')																	# finds the table of songs
	
		if len(songs) != 0:
			for s in songs[1:]:
				c      = s.contents
				song   = c[5].text.lower().strip().replace("’","").replace("'","")
				artist = c[3].text.lower().strip().replace("’","").replace("'","")
				songlist.append(song + " - " + artist + " official music video")					# add song and artist to songlist

			return songlist[::-1] 																	# reverse the list because this html format requires it
	
		
	def insert(self,songlist,videos,titles):														# adds the songs to the new table
		
		if len(songlist) == len(videos):
			size = len(songlist)
			for i in range(size):
				insert_query = "INSERT INTO SONGS VALUES (" + str(i+1) + ",\'" + songlist[i] + "\',\'" + videos[i] + "\',\'" + titles[i].replace("'","") + "\',\'" + self.name +"\');"
				
				self.curse.execute(insert_query)
			self.conn.commit()
		else:
			print("Inserting new playlist failed")

	
