
let changeColor = document.getElementById("changeColor");
let address = "http://localhost";

changeColor.addEventListener("click", async () => {
    /*let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: setPageBackgroundColor,
    });*/
    chrome.storage.sync.get("color", ({ color }) => {
        changeColor.style.backgroundColor = color;
    });
});
  
function setPageBackgroundColor() {
    chrome.storage.sync.get("color", ({ color }) => {
        document.body.style.backgroundColor = color;
    });
}

async function login() {
    authorization = `${userName}:${password}`;

    setCookie("login", userName, loginCookiesDuration);
    setCookie("password", password, loginCookiesDuration);

    var response = await callEndpoint("GET", `${address}/users/login`);
    if (!response.ERROR) {
        console.log(response);
    } 
    else {
        showErrorAlert(response.ERROR, alertTime);
    }
}

function newLogin() {
    var userName = document.getElementById("nameInp").value;
    var password = document.getElementById("passInp").value;

    login(userName, password);
}