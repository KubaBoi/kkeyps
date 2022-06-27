

let address = "http://frogie.cz:7969";
var userName = getCookie("login");
var password = getCookie("password");
login(userName, password);
updateTable();

let loginButt = document.getElementById("loginButt");
let logoutButt = document.getElementById("logoutButt");
let updateButt = document.getElementById("updateButt");
let addPassButt = document.getElementById("addPassButt");
let generateButt = document.getElementById("generateButt");
let createPassButt = document.getElementById("createPassButt");
let closeAddPassButt = document.getElementById("closeAddPassButt");

loginButt.addEventListener("click", newLogin);
logoutButt.addEventListener("click", logout);
updateButt.addEventListener("click", updateTable);
addPassButt.addEventListener("click", showAddDialog);
generateButt.addEventListener("click", randomPass);
createPassButt.addEventListener("click", createPass);
closeAddPassButt.addEventListener("click", closeAddDialog);

async function updateTable() {
    let tbl = document.getElementById("passTable");
    clearTable(tbl);

    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    let web = tab.url.split("/");
    web = `${web[0]}//${web[2]}`;

    let response = await callEndpoint("GET", `${address}/passwords/getByWeb?web=${web}`);
    if (response.ERROR == null) {
        document.getElementById("errorP2").innerHTML = "";
        let psws = response.PASSWORDS;

        addHeader(tbl, [{"text": "User name"}]);

        for (let i = 0; i < psws.length; i++) {
            let psw = psws[i];

            addRow(tbl, [
                {"text": psw.USER_NAME},
                {"text": `<button id="${psw.USER_NAME}">Copy</button>`}
            ]);

            let butt = document.getElementById(`${psw.USER_NAME}`);
            butt.addEventListener("click", copyPass);
        }

        if (psws.length == 0) {
            document.getElementById("errorP2").innerHTML = "There are not any storred passwords for this website";
        }
    }
    else {
        document.getElementById("errorP2").innerHTML = response.ERROR.DESCRIPTION;
        console.log(response.ERROR);
    }
} 

async function copyPass() {
    let userName = this.id;
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    let web = tab.url.split("/");
    web = `${web[0]}//${web[2]}`;

    let response = await callEndpoint("GET", `${address}/passwords/show?web=${web}&userName=${userName}`);
    if (response.ERROR == null) {
        document.getElementById("errorP2").innerHTML = "";

        navigator.clipboard.writeText(response.PASSWORD);
    }
    else {
        document.getElementById("errorP2").innerHTML = response.ERROR.DESCRIPTION;
        console.log(response.ERROR);
    }
}

async function createPass() {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    let web = tab.url.split("/");
    web = `${web[0]}//${web[2]}`;

    let userName = document.getElementById("addUserNameInp").value;
    let pass = document.getElementById("addPassInp").value;

    req = {
        "WEB": web,
        "USER_NAME": userName,
        "PASSWORD": pass
    };

    let response = await callEndpoint("POST", `${address}/passwords/create`, req);
    if (response.ERROR == null) {
        closeAddDialog();
        updateTable();
    }
    else {
        document.getElementById("errorP2").innerHTML = response.ERROR.DESCRIPTION;
        console.log(response.ERROR);
    }
}

function showAddDialog() {
    document.getElementById("addDiv").style.visibility = "visible";
}

function closeAddDialog() {
    document.getElementById("addDiv").style.visibility = "hidden";
}

function randomPass() {
    let length = 20;
    let result = "";
    let characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_@.$&";
    let charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    console.log(result);
    document.getElementById("addPassInp").value = result;
}