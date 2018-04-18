/*
On startup, connect to the "ping_pong" app.
*/
var port = browser.runtime.connectNative("ping_pong");

/*
Listen for messages from the app.
*/
port.onMessage.addListener(response => {
    console.log("Received: " + response);
});

/*
On a click on the browser action, send the app a message.
*/
browser.browserAction.onClicked.addListener(() => {
    console.log("Sending:  ping");
    port.postMessage("ping");
});

// Detect the event of opening a new tab and try to open that URL in the default browser
browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (
        changeInfo.status == "loading" &&
        changeInfo.url &&
        !tab.pinned &&
        changeInfo.url.indexOf("http") == 0
    ) {
        port.postMessage(JSON.stringify({ url: changeInfo.url }));
        browser.tabs.remove(tabId);
    }
});
