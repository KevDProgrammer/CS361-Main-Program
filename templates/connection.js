// the following will send all gallery browsing requests (from html) to the flask.
// (button actions will be more on the front end)
function transmitImageRequest(action, title, id) {
    fetch("/gallery", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({action: action, title: title, request_id: Date.now()}) // ps. not to confuse request_id with id (image)...
        // ...this one stores a unique id (current time cuz always changing) for each request, allowing repeated same execution.
    })
    .then(response => response.text()) //get ONLY the text info itself from the response fetched
    .then(display => {
    document.getElementById(id).src = "/" + display;
    });
}