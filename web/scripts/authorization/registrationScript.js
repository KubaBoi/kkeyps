
async function register() {
    let mail = document.getElementById("mailInp").value;
    let password = document.getElementById("regPass1Inp").value;
    let password2 = document.getElementById("regPass2Inp").value;

    if (password != password2) {
        showTimerAlert("Error", "Passwords are not same", alertTime, "divWrongAlert",
            {"name": "okShowAlert", "duration": "0.5s"},
            {"name": "okHideAlert", "duration": "0.5s"}
        );
        return;
    }

    if (!validateEmail(mail)) {
        showTimerAlert("Error", "Email is in wrong format", alertTime, "divWrongAlert",
            {"name": "okShowAlert", "duration": "0.5s"},
            {"name": "okHideAlert", "duration": "0.5s"}
        );
        return;
    }

    request = {
        "MAIL": mail,
        "PASSWORD": password
    }

    var response = await callEndpoint("POST", "/users/register", request);
    if (!response.ERROR) {
        showTimerAlert("Registration", "Check your email and confirm registration", alertTime, "divOkAlert",
            {"name": "okShowAlert", "duration": "0.5s"},
            {"name": "okHideAlert", "duration": "0.5s"}
        );
    } 
    else if (response.ERROR != "User with this login already exists") {
        showErrorAlert(response.ERROR, alertTime);
    }
    else {
        showTimerAlert("Error", "This email is already registered", alertTime, "divWrongAlert",
            {"name": "okShowAlert", "duration": "0.5s"},
            {"name": "okHideAlert", "duration": "0.5s"}
        );
    }
}

function validateEmail(email) {
    return email.match(
      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};