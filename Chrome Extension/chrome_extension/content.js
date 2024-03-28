// content.js

// Add an event listener for the 'mouseup' event, which occurs when the mouse button is released after clicking
document.addEventListener('mouseup', function(event) {
    // Retrieve the selected text from the current webpage
    let selectedText = window.getSelection().toString().trim();
    // Check if any text is selected
    if (selectedText !== '') {
        // Send a message to the background script to classify the selected text
        chrome.runtime.sendMessage({action: "classifyText", text: selectedText});
    }
});
