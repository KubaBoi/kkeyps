
async function login(userName, password) {
    authorization = `${userName}:${password}`;

    setCookie("login", userName, loginCookiesDuration);
    setCookie("password", password, loginCookiesDuration);

    var response = await callEndpoint("GET", "/users/login");
    if (!response.ERROR) {
        if (window.location.pathname != "/") {
            window.location = "/";
        }
        else {
            return true;
        }
    } 
    else {
        if (window.location.pathname == "/") {
            window.location = "login.html";
        }
        else if (response.ERROR == "Wrong credentials") {
            showTimerAlert("Error", "Wrong credentials", alertTime, "divWrongAlert",
                {"name": "okShowAlert", "duration": "0.5s"},
                {"name": "okHideAlert", "duration": "0.5s"}
            );
        }
        else if (alert) {
            showErrorAlert(response.ERROR, alertTime);
        }
    }
}

function newLogin() {
    var userName = document.getElementById("nameInp").value;
    var password = document.getElementById("passInp").value;

    login(userName, password);
}

function logout() {
    setCookie("userName", "", 0);
    setCookie("password", "", 0);
    location.reload();
}