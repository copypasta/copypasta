// Copyright (c) 2012 Copypasta
 var clipboard = ""
 var selected = ""

function copytoclipboard() {
	
	result =  $('#' + selected).val();

	if (result != "")	{
		$('#' + selected).select();
		document.execCommand('copy');
		
		var status = document.getElementById("status");
		status.innerHTML = "Copied.&nbsp;&nbsp;&nbsp;";
		
		setTimeout(function() {
			window.close();
		}, 500); 

	} else	{
		var status = document.getElementById("status");
		status.innerHTML = "Empty.";
		
		setTimeout(function() {
			status.innerHTML = ""
		}, 500); 
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

document.querySelector('#copy').addEventListener('click', copytoclipboard);




