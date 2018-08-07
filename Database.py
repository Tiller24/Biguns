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
	

	def first_page(self):
		urls = []
		latest_biguns = 'http://hardrockdaddy.com/category/siriusxm-octane-big-uns-countdown/'		# domain
		response = requests.get(latest_biguns,headers={'User-Agent':'Mozilla/5.0'})					# request the webpage html
		soup = BeautifulSoup(response.text,"html.parser")											# parse response											
		blog_items = soup.findAll("div", {"class" : "home-blog-post-item"})							# find all the bigun links on first page
		for b in blog_items:
			urls.append(b.find("h2").find("a")['href'])												# add url to list of urls
			self.weeks.append(b.find("h2").find("a").getText())										# the week names
		return urls[0]
	
	
	def new_playlist(self,url):

		songlist  = self.scrape(url)																# Scrape for the songlist
		vid 	  = yt_id(songlist)																	# use the Youtube API to search for songs
		titles	  = vid.get_titles()																# titles obtained from Youtube API
		videos    = vid.get_videos()																# video IDs obtained from Youtube API
		
		renamed = "_" + self.rename(weeks[0])														# Rename the UI Friendly week name to be used in the database
	
		self.curse.execute("SELECT * FROM WEEKS;")
		insert_index = len(self.curse.fetchall())	
	
		insert_query = "INSERT INTO WEEKS (ID,NAME,UIFRIENDLY) VALUES (" + str(insert_index) + ",\'" + renamed.lower() + "\',\'" + weeks[0].replace("'","''").replace("–","-").replace("‘","''") + "\')"
		self.curse.execute(insert_query)
		self.conn.commit()
		
		create_query = "CREATE TABLE " + renamed + """												
						(ID INT PRIMARY KEY NOT NULL,
						QUERY TEXT NOT NULL,
						YT_ID TEXT NOT NULL,
						TITLE TEXT NOT NULL);"""
		self.curse.execute(create_query)															# Create new table for the recent biguns
		self.conn.commit()
	
		self.insert(songlist,videos,renamed,titles)													# add the songs to the newly created table
	
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
			# print(songlist)
			return songlist[::-1] 																	# reverse the list because this html format requires it
	
	def rename(self,w):																				# take out illegal characters, renaming the Week to database friendly name
		w = w.replace("‘","")
		w = w.replace("– ","")
		w = w.replace(":","")
		w = w.replace(" ","_")
		w = w.replace("/","_")
		w = w.replace("-","_")
		w = w.replace("'","")
		return w;
		
	def insert(self,songlist,videos,renamed,titles):												# adds the songs to the new table
		if len(songlist) == len(videos):
			size = len(songlist)
			for i in range(size):
				insert_query = "INSERT INTO " + renamed + " VALUES (" + str(i) + ",\'" + songlist[i] + "\',\'" + videos[i] + "\',\'" + titles[i].replace("'","") + "\');"
				print("query tits ",insert_query)
				self.curse.execute(insert_query)
				self.conn.commit()
		else:
			print("Inserting new playlist failed")

	
