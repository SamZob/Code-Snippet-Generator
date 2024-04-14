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
        let words = formattedCode.split(' ');
        // let responseDiv = document.getElementById('response');
       

        // Function to append words one by one
        let index = 0
        function appendWord() {
            let lines = data.code.split('\n'); // Split by lines instead of words
            if (index < lines.length) {
                responseDiv.innerHTML += lines[index] + '<br>';
                index++;
                setTimeout(appendWord, 100); // Adjust time as needed
            } else {
                responseDiv.innerHTML += `</p>
                <label for="feedback">Rating:</label>
                <input type="number" id="rating" name="rating" min="1" max="5">
                <label for="feedback">Feedback:</label>
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
        document.getElementById('feedback').value = ''; // Clear feedback input after submission
        document.getElementById('rating').value = '1'; // Reset rating
    });

}

function listSnippets() {
    fetch('/snippets/')
    .then(response => response.json())
    .then(data => {
        const listArea = document.getElementById('snippetList');
        listArea.innerHTML = '';
        data.forEach(snippet => {
            listArea.innerHTML += `<div class="snippet-item" onclick="viewSnippet('${snippet.id}')">
                                    ${snippet.description}
                                    <span class="delete-button" onclick="deleteSnippet('${snippet.id}', event)">✖</span>
                                   </div>`;
        });
    });
}

function viewSnippet(snippetId) {
    fetch(`/snippet/${snippetId}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(snippet => {
        if (snippet.error) {
            alert(snippet.error);
        } else {
            let responseDiv = document.getElementById('response');
            responseDiv.innerHTML = `<p>${snippet.description} : `
            responseDiv.innerHTML += `<pre>${snippet.code.replace(/\\n/g, '<br>').replace(/   /g, '&nbsp;&nbsp;&nbsp;')}</pre>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to fetch snippet data: ' + error.message);
    });
}


function deleteSnippet(snippetId, event) {
    event.stopPropagation(); // Prevents the list item's click event
    fetch(`/snippets/${snippetId}`, { method: 'DELETE' })
    .then(response => response.json())
    .then(() => {
        alert('Snippet deleted successfully');
        listSnippets(); // Refresh the list after deletion
    });
}

    
