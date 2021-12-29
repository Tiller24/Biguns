/*Variables*/
var prevIndex;

/*Initialize iFrame API*/
var tag = document.createElement('script');
//tag.id = 'iframe-script';
tag.src = 'https://www.youtube.com/iframe_api';
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


/*Functions*/
var player;
function onYouTubeIframeAPIReady() {
	prevIndex = 0;
	player = new YT.Player('playlist', {
	height: '390',
    width: '640',
    videoId: firstSong,
	playerVars: {
            'playlist': 'WBYNG4NW6m4,EpNsusxlJms,J1G9DU4Rc9c'
          },
	events: {
		'onReady': onPlayerReady,
		'onStateChange': onPlayerStateChange
		}
	});
}

function onPlayerReady(event) {
	nowPlaying(0);
}

function onPlayerStateChange(){
	var songLoading = -1;
	if (player.getPlayerState() == songLoading){
		nowPlaying(player.getPlaylistIndex());
	}
}

/*Hightlight the song playing*/
function nowPlaying(index){
	titles = document.getElementById('titles').rows;
	//remove highlight of prev song
	titles[prevIndex].style.backgroundColor = "";
	prevIndex = index;

	titles[index].style.backgroundColor = "#694e03";
}