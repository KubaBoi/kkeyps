
var userName = getCookie("login");
var password = getCookie("password");

var loadingDiv = document.getElementById("loaderDiv");

if (login(userName, password)) {
    buildPassTable();
    buildMachinesTable();
}