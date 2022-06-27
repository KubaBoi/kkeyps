let color = "#3aa757";

chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.sync.set({ color });
    
    /*var context = "selection";
    var title = "KKeyps menu";
    chrome.contextMenus.create(
        {
            "title": title,
            "id": "context" + context,
            "contexts": ["editable"] 
        }
    );*/
    
    console.log("Running");
});

//chrome.contextMenus.onClicked.addListener(onClickHandler);

async function onClickHandler(info, tab) {
    console.log(info);

    /*let web = tab.url.split("/");
    web = `${web[0]}//${web[2]}`;

    let response = await callEndpoint("GET", `${address}/passwords/byWeb?web=${web}`);
    console.log(response);*/
};