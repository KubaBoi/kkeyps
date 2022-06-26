
async function login(userName, password) {
    authorization = `${userName}:${password}`;

    var response = await callEndpoint("GET", "/users/login");
    if (!response.ERROR) {
        loggedUser = response.USER;
        succLogin(response);
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

    setCookie("login", userName, 5);
    setCookie("password", password, 5);

    login(userName, password);
}

async function succLogin(response) {
    document.getElementById("singInButt").setAttribute("disabled", "");
    document.getElementById("regButt").setAttribute("disabled", "");
    document.getElementById("forgPassButt").setAttribute("disabled", "");

    window.location = "/";
}

function logout() {
    setCookie("userName", "", 0);
    setCookie("password", "", 0);
    location.reload();
}