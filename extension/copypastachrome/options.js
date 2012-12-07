// Copyright (c) 2012 Copypasta

// Saves settings to localStorage.
function save_settings() {

  var textbox = document.getElementById("secretcode");
  var secretcode = textbox.value;
  localStorage["secretcode"] = secretcode;

  // Update status once saved
  var status = document.getElementById("status");
  status.innerHTML = "Settings were saved.";
  setTimeout(function() {
    status.innerHTML = "";
  }, 750);
}

function clear_settings() {

  localStorage["secretcode"] = "";
  var textbox = document.getElementById("secretcode");
  textbox.value = "";
  
  // Update status once saved
  var status = document.getElementById("status");
  status.innerHTML = "Settings were cleared.";

  setTimeout(function() {
    status.innerHTML = "";
  }, 750);
 
}

function close_settings() {
	window.close()
}

// Restores select box state to saved value from localStorage.
function restore_settings() {

  var secretcode = localStorage["secretcode"];
  if (!secretcode) {
    return;
  } else {
	var textbox = document.getElementById("secretcode");
	textbox.value = secretcode;
  }
}

document.addEventListener('DOMContentReady', restore_settings);
document.querySelector('#save').addEventListener('click', save_settings);
document.querySelector('#clear').addEventListener('click', clear_settings);
document.querySelector('#close').addEventListener('click', close_settings);
restore_settings();
