
async function buildPassTable() {
    let tbl = document.getElementById("passTable");
    clearTable(tbl);

    let response = await callEndpoint("GET", `/passwords/getMy`);
    if (response.ERROR == null) {
        let psws = response.PASSWORDS;

        addHeader(tbl, [
            {"text": ""},
            {"text": "Web"},
            {"text": "User name"},
            {"text": "Password"}
        ]);

        for (let i = 0; i < psws.length; i++) {
            let psw = psws[i];

            addRow(tbl, [
                {"text": `<img src="https://s2.googleusercontent.com/s2/favicons?domain=${psw.WEB}">`},
                {"text": psw.WEB, "attributes": [{"name": "id", "value": `webTd${i}`}]},
                {"text": psw.USER_NAME, "attributes": [{"name": "id", "value": `userNameTd${i}`}]},
                {"text": psw.PASSWORD, "attributes": [{"name": "id", "value": `passTd${i}`}, {"name": "class", "value": "passTd"}]},
                {"text": `<img src='/images/showPass.png' onclick=showPass(${i})>`, "attributes": [{"name": "id", "value": `showTd${i}`}]},
                {"text": `<img src='/images/removePass.png' onclick=removePass(${i})>`}
            ]);
        }
    }
    else {
        showErrorAlert(response.ERROR, alertTime);
    }
}