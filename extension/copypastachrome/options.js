// Copyright (c) 2012 Copypasta

// Saves settings to localStorage.
function save_settings() {

  var codebox = document.getElementById("secretcode");
  var secretcode = codebox.value;
  localStorage["secretcode"] = secretcode;
  
  var userbox = document.getElementById("user");
  var user = userbox.value;
  localStorage["user"] = user;

  // Update status once saved
  var status = document.getElementById("status");
  status.innerHTML = "Settings were saved.";
  setTimeout(function() {
    status.innerHTML = "";
  }, 750);
}

function clear_settings() {

  localStorage["secretcode"] = "";
  var codebox = document.getElementById("secretcode");
  codebox.value = "";
  
  localStorage["user"] = "";
  var userbox = document.getElementById("user");
  userbox.value = "";
  
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
	var codebox = document.getElementById("secretcode");
	codebox.value = secretcode;
  }
  
  var user = localStorage["user"];
  if (!user) {
    return;
  } else {
	var userbox = document.getElementById("user");
	userbox.value = user;
  }
}

document.addEventListener('DOMContentReady', restore_settings);
document.querySelector('#save').addEventListener('click', save_settings);
document.querySelector('#clear').addEventListener('click', clear_settings);
document.querySelector('#close').addEventListener('click', close_settings);
restore_settings();
