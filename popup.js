

let address = "http://frogie.cz:7969";
var userName = getCookie("login");
var password = getCookie("password");
login(userName, password);
updateTable();

let loginButt = document.getElementById("loginButt");
let logoutButt = document.getElementById("logoutButt");
let updateButt = document.getElementById("updateButt");

loginButt.addEventListener("click", newLogin);
logoutButt.addEventListener("click", logout);
updateButt.addEventListener("click", updateTable);

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