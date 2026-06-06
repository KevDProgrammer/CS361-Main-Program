// this sent any music requests (from html) to the flask.
function transmitMusicRequest(action, title) {
    fetch("/music", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({action: action, title: title})
    });
}

// Order of operation: 
// 1. html makes action (make js script call)
// 2. js transmit request to flask
// 3. request.txt gets updated
// 4. MS executes playback of slections
// 5. using flask, connect execution back to html.