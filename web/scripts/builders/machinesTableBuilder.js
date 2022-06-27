
async function buildMachinesTable() {
    let tbl = document.getElementById("machinesTable");
    clearTable(tbl);

    let response = await callEndpoint("GET", `/machines/getMy`);
    if (response.ERROR == null) {
        let machines = response.MACHINES;

        for (let i = 0; i < machines.length; i++) {
            let machine = machines[i];

            addHeader(tbl, [
                {"text": machine.NAME},
            ]);

            addRow(tbl, [
                {"text": "IP"},
                {"text": machine.IP}
            ]);
            addRow(tbl, [
                {"text": "Platform"},
                {"text": machine.PLATFORM}
            ]);
            addRow(tbl, [
                {"text": "User Agent"},
                {"text": machine.USER_AGENT}
            ]);
        }
    }
    else {
        showErrorAlert(response.ERROR, alertTime);
    }
}