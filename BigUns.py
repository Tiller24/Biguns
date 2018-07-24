#!/usr/bin/env python3

import requests								#to get the website html
import re									#regex to search for <p> tags starting with #
import json
import os
from datetime import date					#to get the date
from datetime import timedelta				#to do math on the date
from bs4 	  import BeautifulSoup			#to parse the html

from yt_id    import yt_id					#obtain the youtube id's of each video found

from flask import Flask, render_template, request, jsonify
application = Flask(__name__)

urls   = []		#holds the pages to scrape for songs
weeks  = []		#holds the title of the page being scraped
titles = []		#the song titels of the videos
max    = 0
curr   = 2
iframe = ""

@application.route('/')
def loading():
	return render_template("loading.html")

@application.route('/prev_biguns/', methods=['POST','GET'])
def prev_biguns():
	"""Create the index page, with latest biguns as the first video displayed"""
	global iframe,urls,weeks,titles,max,curr
	
	urls   = [] #resets are for when index.html is refreshed
	weeks  = [] #reset
	titles = [] #reset
	max    = 0  #reset
	curr   = 2  #reset
	iframe = "" #reset
	
	latest_biguns = first_page()
	new_playlist(latest_biguns)
	
	return render_template("index.html",iframe = iframe,weeks = weeks,titles = titles)
 


def first_page():
	global max, urls, weeks
	
	all_biguns = 'http://hardrockdaddy.com/category/siriusxm-octane-big-uns-countdown/'		#domain
	response = requests.get(all_biguns,headers={'User-Agent':'Mozilla/5.0'})				#request the webpage html
	soup = BeautifulSoup(response.text,"html.parser")										#parse response
	nums = soup.findAll("a", {"class" : "page-numbers"})									
	max = int(nums[-2].getText())															#max page numbers to scrape
	
	blog_items = soup.findAll("div", {"class" : "home-blog-post-item"})						#find all the bigun links on first page
	for b in blog_items:
		urls.append(b.find("h2").find("a")['href'])											#add url to list of urls
		weeks.append(b.find("h2").find("a").getText())										#the week names
		
	return urls[3] #starting from Week of 6/30/18; because they changed their html for the most recent week. Change index to match Week of 6/30/18!

def new_playlist(url):
	global iframe,titles
	songlist  = scrape(url)
	vid 	  = yt_id(songlist)
	titles	  = vid.get_titles()
	videos    = vid.get_videos()
	iframe    = playlist(videos)
	
def scrape(website):
	songlist = []	#store the songs and artist name
	
	response = requests.get(website,headers={'User-Agent':'Mozilla/5.0'})				#request the webpage html
	soup = BeautifulSoup(response.text,"html.parser")									#parse response
	songs = soup.findAll(text=re.compile("^#"))											#find the countdown of songs
	
	#the website had different formats for their html, 
	#so I just made two ways to handle that for now
	if len(songs) != 0:
		for s in songs:
			song = s[5:]
			song = song.replace('–'," ")
			songlist.append(song.replace(u'\xa0',u'') + str(s.next.text.strip() + " official music video"))			#store songs and artists
			
		print (songlist)
		return songlist
	else:
		list = soup.findAll('ol')[0].text
		songlist = list.strip().split("\n")
		
		return songlist
	
def playlist(videos):
	iframe = videos[0] + '?playlist=' #open tag
	for v in videos[1:]:
		iframe += v + ','
	iframe = iframe[:-1]		#remove trailing comma after the loop
	return iframe	
	
	
@application.route('/load_more/', methods = ['GET','POST'])
def load_more():
	global max, urls, weeks, curr
	all_biguns = 'http://hardrockdaddy.com/category/siriusxm-octane-big-uns-countdown/'
	size = len(weeks)
	
	if request.method == 'POST' and curr <= max:
		
		all_biguns += '/page/' + str(curr) + '/'
		response = requests.get(all_biguns,headers={'User-Agent':'Mozilla/5.0'})		#request the webpage html
		soup = BeautifulSoup(response.text,"html.parser")								#parse response
		blog_items = soup.findAll("div", {"class" : "home-blog-post-item"})
		for b in blog_items:
			urls.append(b.find("h2").find("a")['href'])									#grabs the urls of the pages to parse
			weeks.append(b.find("h2").find("a").getText())								#the names of the biguns
		curr+=1
		return jsonify(weeks[size:])
	else:
		return "none"

@application.route('/new_request/',methods=['GET','POST'])		
def new_request():
	if request.method == 'POST':
		index = int(request.form['index'])
		url = urls[index] 																#grab desired index
		new_playlist(url)																#url of the desired biguns week
		iframe_src = 'https://www.youtube.com/embed/' + iframe
		json_arr = json.dumps(titles)
		
		return jsonify('{"iframe" : "%s", "titles" : %s}' % (iframe_src,json_arr))

if __name__ == "__main__":
	ON_HEROKU = os.environ.get('ON_HEROKU')						#see if Heroku is running app
	if ON_HEROKU:
		application.run(debug = False)
	else:
		port = 80
		application.run(debug = True, port = port, host = '0.0.0.0')
	
