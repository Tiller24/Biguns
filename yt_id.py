#!/usr/bin/env python3

import os
from googleapiclient.discovery import build

# from apiclient.errors import HttpErrorpip install google-api-python-client

if "YOUTUBE_API_KEY" in os.environ:
    DEVELOPER_KEY = os.environ.get(
        "YOUTUBE_API_KEY")  # the youtube api key, stored in environment variable. Need your own to run!
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


class Yt_id:
    """This class goes and searches for the youtube videos
	   returning the id of each video it finds
	   It utilizes from the YouTube Data API
	   https://developers.google.com/youtube/v3/code_samples/python"""

    videos = []  # store the video id's
    titles = []  # store video title

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    def youtube_search(self, query, max):

        search_response = self.youtube.search().list(
            # Call the search.list method to retrieve results matching the specified
            q=query,  # query term.
            part="id,snippet",
            maxResults=max
        ).execute()
        # loop through the returned search results
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                self.videos.append("%s" % (search_result["id"]["videoId"]))  # grab the video id
                self.titles.append("%s" % (search_result["snippet"]["title"]))
                break  # only grab the top search result

    def get_videos(self):
        return self.videos

    def get_titles(self):
        return self.titles

    # constructor
    def __init__(self, songlist):
        self.songlist = songlist
        self.videos = []
        self.titles = []

        for song in self.songlist:
            self.youtube_search(song, 25)  # search for the song
    # print (self.videos)
