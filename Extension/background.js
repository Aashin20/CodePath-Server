// Listen for browser action click
chrome.browserAction.onClicked.addListener((tab) => {

    chrome.tabs.sendMessage(tab.id, {
      action: "extract"
    });
  });

  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "saveToMongo") {
      saveToMongoDB(request.content);
    }
  });
  
  function saveToMongoDB(content) {
    
    const MONGODB_API_URL = 'YOUR_MONGODB_API_ENDPOINT';
    
    fetch(MONGODB_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content: content,
        timestamp: new Date(),
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }