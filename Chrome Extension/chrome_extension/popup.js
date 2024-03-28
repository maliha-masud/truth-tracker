// Add an event listener for when the DOM content is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Add an event listener for when the search button is clicked
  document.getElementById('searchButton').addEventListener('click', function() {
    // Get the value of the search input and trim any leading/trailing whitespace
    let searchText = document.getElementById('searchInput').value.trim();
    // Check if the search text is not empty
    if (searchText.length > 0) {
      // Make a POST request to a local server for text classification
      fetch('http://127.0.0.1:5000/classify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json' // Set request header to JSON
        },
        body: JSON.stringify({ text: searchText }) // Send search text data in JSON format
      })
      // Parse response as JSON
      .then(response => {
        // Check if the response status is not OK
        if (!response.ok) {
          // Throw an error with the response status text
          throw new Error('Network response was not ok ' + response.statusText);
        }
        // Return the response as JSON
        return response.json();
      })
      // Handle the classified data
      .then(data => {
        // Find the result text paragraph
        var resultText = document.getElementById('resultText');
        // Set its text content to the classification result
        resultText.textContent = `Classification: ${data.classification}`;
      })
      // Handle any errors that occur during the fetch operation
      .catch(error => {
        console.error('Error:', error);
        // Optionally update the result text to show the error
        var resultText = document.getElementById('resultText');
        resultText.textContent = 'Error: Could not classify text.';
      });
    }
  });
});
