// Copyright (c) 2012 Copypasta
	var clipboard = ""
	var selected = ""
	var host = "http://127.0.0.1:8080"	
	var req;
	
function getclips() {
	var status = document.getElementById("status");
	req = new XMLHttpRequest();
	req.open(
		"GET",
		 host + "/getclips",
		true);
	var requestcode =  "user=" +localStorage["user"] + "&code=" + localStorage["secretcode"];

	req.setRequestHeader("X-Copypasta-Code", requestcode);
	req.onreadystatechange = function(){
		if (this.readyState==4)	{
			if (this.status==200) {

				processclips(this.responseText);
				
			}
			else {	
				status.innerHTML = "Error " + this.status;
				setTimeout(function() {
					status.innerHTML = ""
				}, 750); 
			}
		}
	}
	req.send(null);
} 

function postclip() {
	var status = document.getElementById("status");
	req = new XMLHttpRequest();
	req.open(
		"POST",
		 host + "/postclip",
		true);
	var requestcode =  "user=" +localStorage["user"] + "&code=" + localStorage["secretcode"];

	req.setRequestHeader("X-Copypasta-Code", requestcode);
	req.onreadystatechange = function(){
		if (this.readyState==4)	{
			if (this.status==200) {
				var result = $.parseJSON(this.responseText);
				status.innerHTML = result.status;
				setTimeout(function() {
					location.reload();
				}, 750); 
			}
			else {	
				status.innerHTML = "Error " + this.status;
				setTimeout(function() {
					location.reload();
				}, 750); 
			}
		}
	}
	
	data = $.base64.encode($("#clipboard").val());
	req.send(data);
} 

function deleteclip(id) {
	var status = document.getElementById("status");
	req = new XMLHttpRequest();
	req.open(
		"POST",
		 host + "/deleteclip",
		true);
	var requestcode =  "user=" +localStorage["user"] + "&code=" + localStorage["secretcode"];

	req.setRequestHeader("X-Copypasta-Code", requestcode);
	req.onreadystatechange = function(){
		if (this.readyState==4)	{
			if (this.status==200) {
				var result = $.parseJSON(this.responseText);
				status.innerHTML = result.status;
				setTimeout(function() {
					location.reload();
				}, 750); 
			}
			else {	
				status.innerHTML = "Error " + this.status;
				setTimeout(function() {
					location.reload();
				}, 750); 
			}
		}
	}
	req.send(id);
}

function processclips(content) {
	var clips = $.parseJSON(content);
	var htmlcontent = ""
	var iClip = 0;
	
	for (clip in clips){
		iClip = parseFloat(clip) + 1;
		
		if (iClip == 1)
		{
			htmlcontent +=  "<div style=\"font-size:10px;font-weight:bold;padding:2px;\">Prior Clips</div>";
		} 

		title = clips[clip].title.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
		content = clips[clip].content.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
		
		id = clips[clip].id;
		
		htmlcontent +=  "<div style=\"position:absolute;right:41px;\"><button style=\"position:absolute;padding:0;font-size:9px\" id=\"delete" + iClip + "\" name=\"" + id + "\">Delete</button></div>";
		
		htmlcontent +=  "<div id=\"title" + iClip + "\" style=\"font-size:10px;padding:2px;\">" + title + "</div>";
		htmlcontent +=  "<textarea id=\"priorclip"  + iClip + "\" cols=\"30\" rows=\"3\">" + content + "</textarea>";

	}
	
	if (iClip >= 1) {
		htmlcontent += "<button id=\"copy\">Copy selected clipboard</button>";
	}
	
	htmlcontent += "<div id=\"status\" style=\"padding:5px;font-size:11px; float:right\"></div>"
	
	$('#oldclipboards').html(htmlcontent);
	
	$('button[id^="delete"]').click(function() {
		deleteclip(this.name);
	});
	
	$('textarea[id^="priorclip"]').click(function() {
		$('textarea[id^="priorclip"]').css({"border-color": "#5F78AB","background-color": "#FFFFFF"});
		$('#clipboard').css({"border-color": "#5F78AB","background-color": "#FFFFFF"});

		$(this).css({"border-color": "#A08754"});
		$(this).css({"background-color": "#DDEEF6"});
		
		selected = $(this).attr('id');
	});

	$('#clipboard').click(function() {
		$('textarea[id^="priorclip"]').css({"border-color": "#5F78AB"});
		$('textarea[id^="priorclip"]').css({"background-color": "#FFFFFF"});
		$(this).css({"border-color": "#A08754"});
		$(this).css({"background-color": "#DDEEF6"});
		
		selected = $(this).attr('id');
	});
	
	if (iClip >= 1) { 
		document.querySelector('#copy').addEventListener('click', copytoclipboard);
	}
}
 
function copytoclipboard() {
	
	result =  $('#' + selected).val();

	if (result != "")	{
		$('#' + selected).select();
		document.execCommand('copy');
		
		var status = document.getElementById("status");
		status.innerHTML = "Copied.&nbsp;&nbsp;&nbsp;";
		
		setTimeout(function() {
			window.close();
		}, 750); 

	} else	{
		var status = document.getElementById("status");
		status.innerHTML = "Empty.";
		
		setTimeout(function() {
			status.innerHTML = ""
		}, 750); 
	}	
}

function paste() {
    var result = '',
        clipboard = $('#clipboard').val('').select();
    if (document.execCommand('paste')) {
        result =  $("#clipboard").val();
		clipboard = $('#clipboard').select();
    }
}

paste();

document.querySelector('#post').addEventListener('click', postclip);

getclips();


