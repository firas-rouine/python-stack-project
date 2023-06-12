
                        // chatbox display


class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        
        }

        this.state = false;
        this.messages =[];
      
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))
        openButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup",({key})=>{
            if (key === "Enter"){
                this.onSendButton(chatBox)
            }
        })

      

     
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if (this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

   
   
    
}
const chatbox = new Chatbox();
chatbox.display();


                          // Function to highlight code using highlight.js library

setInterval(highlightAll,1000);

function highlightAll() {
  document.querySelectorAll("pre code").forEach(block => {
    hljs.highlightBlock(block);
  });
}

    const chatBox = document.querySelector(".chat-box");
    const messageInput = document.querySelector("#message-input");
    const sendBtn = document.querySelector("#send-btn");

    function addMessage(message, isUserMessage) {
      const messageDiv = document.createElement("div");



      messageDiv.innerHTML = `
        <p class="messages__item messages__item--operator ">${message}</p>
        `;

      chatBox.appendChild(messageDiv);
      chatBox.scrollTop = chatBox.scrollHeight;
    }




    function sendMessage() {
      const message = messageInput.value.trim();

      if (message !== "") {
        addMessage(message, true);

        fetch("/api", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ message })
        })
          .then(response => response.json())
          .then(data => {
                      messageInput.value = "";
            const messageDiv = document.createElement("div");
            const content = data.content;
            
            // Check if the content has code block
            const hasCodeBlock = content.includes("```");
            if (hasCodeBlock) {
              // If the content has code block, wrap it in a <pre><code> element
              const codeContent = content.replace(/```([\s\S]+?)```/g, '</p><pre><code>$1</code></pre><p>');

              messageDiv.innerHTML = `<p class="messages__item messages__item--visitor ">${codeContent}</p>`
            }
            else{
              messageDiv.innerHTML = `<p class="messages__item messages__item--visitor ">${content}</p>`
            }
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;

          })
          .catch(error => console.error(error));
      }
    }

    
    sendBtn.addEventListener("click", sendMessage);
    messageInput.addEventListener("keydown", event => {
      if (event.keyCode === 13 && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
      }
    });



    // pagination


var currentPage = 1;
var itemsPerPage = 9;
var views = document.querySelectorAll("#pub-uni .view1 ");
var totalPages = Math.ceil(views.length / itemsPerPage);

function showPage(page) {
  var startIndex = (page - 1) * itemsPerPage;
  var endIndex = startIndex + itemsPerPage;

  for (var i = 0; i < views.length; i++) {
    if (i >= startIndex && i < endIndex) {
      views[i].style.display = "block";
    } else {
      views[i].style.display = "none";
    }
  }
}

function previousPage() {
  if (currentPage > 1) {
    currentPage--;
    showPage(currentPage);
  }
}

function nextPage() {
  if (currentPage < totalPages) {
    currentPage++;
    showPage(currentPage);
  }
}
showPage(currentPage);






