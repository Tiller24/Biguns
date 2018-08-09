#!/usr/bin/env python3

import os

from BigUns_functions import Functions
from Database import Database

# Flask is the web app, render_template loads html pages with python data
# request for GET/POST requests, and jsonify to send json data
from flask import Flask, render_template, request, jsonify
application = Flask(__name__)

biguns = Functions()


@application.route('/')
def loading():
	return render_template("loading.html")

@application.route('/latest_biguns/', methods=['POST','GET'])
def latest_biguns():
	"""Create the index page, with latest biguns as the first playlist displayed"""
	
	weeks  = biguns.weeks										# The entirety of biguns in history
	yt_ids = biguns.yt_ids										# Most recent video IDs
	titles = biguns.titles										# Most recent titles of the videos found
	iframe = biguns.playlist()									# The playlist of most recent songs
	
	return render_template("index.html",iframe = iframe,weeks = weeks,titles = titles)
 	
	
@application.route('/new_request/',methods=['GET','POST'])		
def new_request():
	if request.method == 'POST':
		index = int(request.form['index'])						# The week clicked
		biguns.set_yt_ids(index)								# Set new video IDs
		biguns.set_titles(index)								# Set new video titles
		return jsonify(biguns.new_request(index))				# Send data as JSON
	


if __name__ == "__main__":
	ON_HEROKU = os.environ.get('ON_HEROKU')						# see if Heroku is running app
	if ON_HEROKU:
		application.run(debug = False)
	else:														# Else, app is running in localhost
		port = 80												# TODO: run it using waitress
		application.run(debug = True, port = port, host = '0.0.0.0')
	
