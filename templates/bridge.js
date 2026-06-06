// the following is responsible for sending any request from the html to flask (hence js name, the bridge.)
function transmitRatingRequest(action, title) {
    return fetch("/rating", {
        method: "POST", 
        headers: {
            "Content-Type" : "application/json"
        },
        body: JSON.stringify({action: action, title: title})
    })
    .then(response => response.text()); //get ONLY the text that's in response
}

// responsible for returning the rating for display on current title-page (individual page - when called upon)
function ratingSetter(title) {
    transmitRatingRequest("assigned_rating", title)
    .then(data => {
        const ratingDisplay = document.getElementById("ratingDisplay");
        ratingDisplay.textContent = data;
    })
}

// responsible for returning the highest-to-lowest ranked ratings for display (sorted page - when called upon)
function rankedSetter() {
    transmitRatingRequest("sorted_ratings", "list_all")
    .then(data => {
        const rankedDisplay = document.getElementById("rankedDisplay");
        // make every line seperate, each holding title and rating.
        const lines = data.trim().split("\n");
        let pair = "";
        for (const line of lines) {
            const[title, rating] = line.split("~");
            pair += `<p>${title} | ${rating}</p>`;
        }
        rankedDisplay.innerHTML = pair;
    })
}