function new_request(i){
	$("#loading").show();
	$.post("/new_request/",{
		"index" : i
	},
    function(data, status){
		var json = JSON.parse(data);
		var titles = json.titles;
		new_titles(titles);
		document.getElementById('playlist').setAttribute('src',json.iframe);
		$("#loading").hide();
    });
}

function new_titles(titles){
	$("#titles tr").remove(); //clear all previous
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