
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "extract") {

      const tdElement = document.querySelector('td.ant-descriptions-item-content');
      
      if (tdElement) {
 
        const content = tdElement.querySelector('div p');
        
        if (content) {
          const questionText = content.innerHTML
            .split('<br>')[1] 
            .trim(); 
          
          // Send the extracted content to the background script
          chrome.runtime.sendMessage({
            action: "saveToMongo",
            content: questionText
          });
        }
      }
    }
  });