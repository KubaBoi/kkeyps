
var userName = getCookie("login");
var password = getCookie("password");

var loadingDiv = document.getElementById("loaderDiv");

login(userName, password);