function new_request(i){
	document.getElementById('loading').style.display = 'block'; //show loading gif

	// create request object
	let request = new Request('/new_request/', {
		method: 'POST',
		body: JSON.stringify({'index' : i}),
		headers: new Headers({
			'Content-Type': 'application/json'
		})
	});

	// pass request object to `fetch()`
	fetch(request)
		.then(res => res.json())
		.then(function(data){
			var json = JSON.parse(data);
			var titles = json.titles;
			new_titles(titles);
			document.getElementById('playlist').setAttribute('src',json.iframe);
			document.getElementById('loading').style.display = 'none'; //hide loading gif
			onYouTubeIframeAPIReady();
		});
}

function new_titles(titles){
	document.getElementById('titles').innerHTML = "";
	var table = document.getElementById("titles");
	var size  = titles.length;
	var tab   = "\u00a0\u00a0\u00a0\u00a0\u00a0";

	for (t in titles){
		var tr = document.createElement("tr");
		var td = document.createElement("td");
		var txt = document.createTextNode("#" + size + tab + titles[t]);
		size--;
		td.appendChild(txt);
		tr.appendChild(td);
		table.appendChild(tr);
	}
}