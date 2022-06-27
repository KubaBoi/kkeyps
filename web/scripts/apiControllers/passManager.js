
function addPassword() {
    let addPassDiv = document.getElementById("addPassDiv");
    addPassDiv.style.visibility = "visible";
}

function closeAddPassword() {
    let addPassDiv = document.getElementById("addPassDiv");
    addPassDiv.style.visibility = "hidden";
}

async function createPassword() {
    let web = document.getElementById("webInp").value;
    let userName = document.getElementById("userNameInp").value;
    let pass = document.getElementById("passInp").value;

    req = {
        "WEB": web,
        "USER_NAME": userName,
        "PASSWORD": pass
    };

    let response = await callEndpoint("POST", "/passwords/create", req);
    if (response.ERROR == null) {
        closeAddPassword();
        buildPassTable();
    }
    else {
        showErrorAlert(response.ERROR, alertTime);
    }
}

function randomPass(length=20) {
    let result = '';
    let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_@.$&';
    let charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    document.getElementById("passInp").value = result;
}

async function copyPass(index) {
    if (!window.isSecureContext) {
        showWrongAlert("Non secured window", "Sorry, for copying into clipboard is needed 'https' or 'localhost' :/", alertTime);
        return;
    }
    let web = document.getElementById(`webTd${index}`).innerHTML;
    let userName = document.getElementById(`userNameTd${index}`).innerHTML;
    
    let response = await callEndpoint("GET", `/passwords/show?web=${web}&userName=${userName}`);
    if (response.ERROR == null) {
        navigator.clipboard.writeText(response.PASSWORD);
        showOkAlert("Copied :)", "Password has been inserted into your clipboard", alertTime);
    }
    else {
        showErrorAlert(response.ERROR, alertTime);
    }
}

async function showPass(index) {
    let web = document.getElementById(`webTd${index}`).innerHTML;
    let userName = document.getElementById(`userNameTd${index}`).innerHTML;
    
    let response = await callEndpoint("GET", `/passwords/show?web=${web}&userName=${userName}`);
    if (response.ERROR == null) {
        document.getElementById(`passTd${index}`).innerHTML = response.PASSWORD;
        document.getElementById(`showTd${index}`).innerHTML = `<img src='/images/hidePass.png' onclick=hidePass(${index})>`;
    }
    else {
        showErrorAlert(response.ERROR, alertTime);
    }
}

function hidePass(index) {
    document.getElementById(`passTd${index}`).innerHTML = "••••••••••";
    document.getElementById(`showTd${index}`).innerHTML = `<img src='/images/showPass.png' onclick=showPass(${index})>`;
}

function removePass(index) {
    showConfirm("Really?", "Do you really want to remove this password?", function() {removePassR(index);});
}

async function removePassR(index) {
    let web = document.getElementById(`webTd${index}`).innerHTML;
    let userName = document.getElementById(`userNameTd${index}`).innerHTML;

    let response = await callEndpoint("GET", `/passwords/remove?web=${web}&userName=${userName}`);
    if (response.ERROR == null) {
        showOkAlert("Done :)", "Password has been removed.", alertTime);
        buildPassTable();
    }
    else {
        showErrorAlert(response.ERROR, alertTime);
    }
}