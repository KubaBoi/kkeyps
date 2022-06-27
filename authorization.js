async function login(userName, password) {
    authorization = `${userName}:${password}`;

    setCookie("login", userName, 5);
    setCookie("password", password, 5);

    var response = await callEndpoint("GET", `${address}/users/login`);
    if (!response.ERROR) {
        document.getElementById("errorP").innerHTML = `Logged as ${userName} :)`;
        console.log(response);

        document.getElementById("loginDiv").remove();
        document.getElementById("loggedDiv").style.visibility = "visible";
    } 
    else {
        document.getElementById("errorP").innerHTML = response.ERROR.DESCRIPTION;
        console.log(response.ERROR);
    }
}

function newLogin() {
    var userName = document.getElementById("nameInp").value;
    var password = document.getElementById("passInp").value;

    login(userName, password);
}

function logout() {
    setCookie("login", "", 0);
    setCookie("password", "", 0);

    location.reload();
}