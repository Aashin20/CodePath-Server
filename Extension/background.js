const API_BASE_URL = 'http://localhost:8000';

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
  fetch(`${API_BASE_URL}/api/save-content`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      content: content,
      timestamp: new Date().toISOString()
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icon.png',
        title: 'Success',
        message: 'Content saved successfully!'
      });
    }
  })
  .catch((error) => {
    console.error('Error:', error);
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icon.png',
      title: 'Error',
      message: 'Failed to save content.'
    });
  });
}