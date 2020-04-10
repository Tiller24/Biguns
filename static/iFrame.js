var tag = document.createElement('script');
tag.id = 'iframe-script';
tag.src = 'https://www.youtube.com/iframe_api';
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
	player = new YT.Player('playlist', {
	events: {
		'onReady': onPlayerReady,
//		'onStateChange': onPlayerStateChange
		}
	});
}
function onPlayerReady(event) {
	document.getElementById('playlist').style.borderColor = '#FF6D00';
}
