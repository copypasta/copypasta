// Copyright (c) 2012 Copypasta
 var clipboard = ""
 var selected = ""

function copytoclipboard() {

    $('#' + selected).select();
	document.execCommand('copy');
}

function paste() {
    var result = '',
        clipboard = $('#clipboard').val('').select();
    if (document.execCommand('paste')) {
        result =  $("#clipboard").val();
		clipboard = $('#clipboard').select();
    }
    return result;
}

paste();

$('textarea[id^="priorclip"]').click(function() {
	$('textarea[id^="priorclip"]').css({"border-color": "#5F78AB"});
	$('textarea[id^="priorclip"]').css({"background-color": "#FFFFFF"});
	$(this).css({"border-color": "#A08754"});
	$(this).css({"background-color": "#DDEEF6"});
	
	selected = $(this).attr('id');
});

document.querySelector('#copy').addEventListener('click', copytoclipboard);




