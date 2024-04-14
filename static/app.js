function generateCode() {
    const description = document.getElementById('description').value;
    let responseDiv = document.getElementById('response');
    responseDiv.innerHTML = 'Generating code<span id="dots"></span>'; // Initial loading message

    let dotCount = 0;
    let dots = document.getElementById('dots');
    let interval = setInterval(function() {
        dots.innerHTML += '.';
        dotCount++;
        if (dotCount === 4) {
            dots.innerHTML = ''; // Reset dots after three
            dotCount = 0;
        }
    }, 500); // Update dots every 500 milliseconds

    fetch('/generate-code/', {
        method: 'POST',
        body: new URLSearchParams({'description': description})
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(interval); // Stop the dot animation
        // Format the code to display newlines and triple spaces correctly
        let formattedCode = `<pre>${data.code.replace(/\\n/g, '<br>').replace(/   /g, '&nbsp;&nbsp;&nbsp;')}</pre>`;
        responseDiv.innerHTML = formattedCode
        + `</p>
        <label for="feedback">Rating :</label>
        <input type="number" id="rating" name="rating" min="1" max="5">
        <label for="feedback">Feedback :</label>
        <input type="text" id="feedback" name="feedback">
        <button onclick="submitFeedback('${data.id}')">Submit Feedback</button>`;
    });
}


    // Function to append words one by one
    let index = 0;
    function appendWord() {
        if (index < words.length) {
            responseDiv.innerHTML += words[index] + ' ';
            index++;
            setTimeout(appendWord, 100); // Adjust time as needed
        } else {
            responseDiv.innerHTML += `</p>
            <label for="feedback">Rating :</label>
            <input type="number" id="rating" name="rating" min="1" max="5">
            <label for="feedback">Feedback :</label>
            <input type="text" id="feedback" name="feedback">
            <button onclick="submitFeedback('${data.id}')">Submit Feedback</button>`;
        }
    }

    appendWord(); // Start appending words




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
            document.getElementById('feedback').value = ''; // Clear feedback input after submission
            document.getElementById('rating').value = '1'; // Reset rating
        });
    }
    
