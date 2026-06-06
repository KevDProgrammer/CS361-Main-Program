// To handle specific sound design features

function clickSE(event) {
    event.preventDefault();

    const sound = document.getElementById("click-sound");

    sound.play()

    const link = event.currentTarget.href;

    setTimeout(() => {
        window.location.href = link;
    }, 800); // change this depending on SE duration
}

// N UI 1 duration: 800-1000ms
// N UI 2 duration: 700-800ms
// N UI 3 duration: 800-900ms
// N UI 4 duration: 1000ms