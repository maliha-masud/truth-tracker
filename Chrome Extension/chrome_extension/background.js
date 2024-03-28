// Add listener for messages from the extension popup or content script
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  // Check if the message action is to classify text
  if (request.action === "classifyText") {
    // Extract the text to be classified from the request
    let queryText = request.text;

    // Make a POST request to a local server for text classification
    fetch('http://127.0.0.1:5000/classify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json' // Set request header to JSON
      },
      body: JSON.stringify({ text: queryText }) // Send text data in JSON format
    })
    // Parse response as JSON
    .then(response => response.json())
    // Send the classification result back to the sender
    .then(data => {
      sendResponse({ result: data.classification });
    })
    // Handle any errors that occur during the fetch operation
    .catch(error => {
      console.error('Error:', error);
    });

    // Ensure the message channel remains open for asynchronous response
    return true;
  }
});
