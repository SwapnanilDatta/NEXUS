let id, x, y;

function match(element) {
    id = element; // Capture the match element clicked
    window.location.href = 'pool.html'; // Redirect to pool.html
}

function predict() {
    // Declare x and y outside the if-else block
    if (id === "1") {
        x = "A";
        y = "B";
    } else if (id === "2") {
        x = "C";
        y = "D";
    } else {
        x = "E";
        y = "F";
    }

    // You cannot manipulate the DOM and redirect simultaneously.
    // Move the navigation after DOM manipulation or use localStorage.
    window.location.href = 'predict.html'; // Redirects to predict.html

    // The DOM manipulation should be on the predict.html page, 
    // after the redirection
}

// On predict.html, after loading the page
window.onload = function() {
    // Check if id, x, and y values are passed from previous page
    let parent = document.getElementById("1");
    if (parent && x && y) {
        let info1 = `<label>Who will win the match?</label>
                     <input type="radio" name="match-winner" value="Team ${x}" required> Team ${x}
                     <input type="radio" name="match-winner" value="Team ${y}"> Team ${y}
                     <input type="radio" name="match-winner" value="Draw"> Draw!!!!!!!!!!`;
        parent.innerHTML = info1;
    }
};
