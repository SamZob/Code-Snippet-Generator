function generateCode() {
    const description = document.getElementById('description').value;
    fetch('/generate-code/', {
        method: 'POST',
        body: new URLSearchParams({'description': description})
    })
    .then(response => response.json())
    .then(data => {
    let formattedCode = `<pre>${data.code.replace(/\`\`\`/g, '<br>').replace(/\>/g, ' ')}</pre>`;
    let words = formattedCode.split(' '); // Split the code into words
    let responseDiv = document.getElementById('response');
    responseDiv.innerHTML = 'Generating code...<p>';

    // Function to append words one by one
    let index = 0;
    function appendWord() {
        if (index < words.length) {
            responseDiv.innerHTML += words[index] + ' ';
            index++;
            setTimeout(appendWord, 100); // Adjust time as needed
        } else {
            responseDiv.innerHTML += `</p>
            <label for="feedback">Feedback:</label>
            <input type="number" id="rating" name="rating" min="1" max="5">
            <button onclick="submitFeedback('${data.id}')">Submit Rating</button>
            <input type="text" id="feedback" name="feedback">
            <button onclick="submitFeedback('${data.id}')">Submit Feedback</button>`;
        }
    }

    appendWord(); // Start appending words
});
}


function submitFeedback(snippetId) {
    const feedback = document.getElementById('feedback').value;
    const rating = document.getElementById('rating').value; // Get rating value
    fetch('/submit-feedback/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({'snippet_id': snippetId, 'feedback': feedback, 'rating': rating})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('response').innerHTML = '';
    });
}
