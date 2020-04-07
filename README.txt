//TODO: Redo this readme file

Biguns Project is a project that finds the top 15 songs of the week 
from Serius XM's Octane (channel 37)

In the future I will change it to store the song IDs and other info
in a database. This is because they are too inconsistent with
the way they format their HTML. Plus, I'll be able to query
much more quickly, and edit videos that are not accurate.

So far, there really isn't much videos that are inaccurate

 

Here is how each file works:

=============================
loading.html

This is the template pulled up by loading() in Biguns.py

The only function of this page is to show a loading gif while /prev_biguns/
in Biguns.py is loading the first page of Bigun countdowns.

=============================
Biguns.py

When the app loads up, Biguns.py renders the template 'loading.html',
which just pulls up a cute loading screen.

prev_biguns() 
			  holds all the urls, name of the countdown (weeks),
			  title of the videos, and max number of pages to scrape.
			  
			  first_page() grabs the front page of
			  http://hardrockdaddy.com/category/siriusxm-octane-big-uns-countdown/
			  That page contains the current countdown and the previous few weeks.
			  Returns the latest countdown.
			  
			  new_playlist() uses the first countdown obtained from first_page()
			  and scrapes it for the song titles. It stores the titles and resulting
			  iframe
			  

first_page()  
			  grabs the front page of
			  http://hardrockdaddy.com/category/siriusxm-octane-big-uns-countdown/
			  BeautifulSoup is used to scrape the webpage for the countdown.
			  
			  max is used to store the amount of pages we will scrape in the future.
			  
			  Returns the most recent countdown songs, but I currently set it to
			  return only from Week of 6/30/18 and earlier because they changed
			  the HTML of the weeks after that. CHANGE return urls[i] TO MATCH THAT Week
			  IF YOU ARE TESTING.
			  
 
 new_playlist() 
			  Accepts the url of the particular Countdown you are creating
			  a playlist for, and Scrapes that url for the countdown. 

			  Passes the songlist to yt_id.py, which queries using the YouTube API
			  to find the video IDs and video Titles.
			  
			  Once it has that, playlist() is called to put the video IDs into
			  a iframe.
			  
scrape()	
			  Scapes the url for the song list using BeautifulSoup.
			  There are two ways to scrape because they don't have consistent
			  html layout. Which is why I will eventually put scraped videos
			  into a database and query from there instead

load_more()   
			  This method is called when the 'Load more' button is pressed
			  from the home page. Loads the page number indicated by 'curr' variable
			  as long as curr < max #of pages.
			  
new_request()
			  When a 'Week of' title is pressed on the right of the screen,
			  this method grabs the index of that item and finds the url for 
			  that week, and creates the playlist

=============================			  
yt_id.py

This is the program that handles the Youtube API

__init__ constructor()
			  The constructor is given the songlist scraped from the website.
			  It also has the video IDs, and the video Titles
			  
youtube_search()
			  searches youtube by querying the songlist titles.
			  Once it searches, it grabs the top result, and gets
			  its ID and Title and stores them

=============================
index.html

The load more button just shows more of the previous bigun weeks. 
Clicking on one of those weeks loads the videos for that week.

=============================


