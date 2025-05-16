import streamlit as st
import streamlit.components.v1 as components

st.title("Chatbot Demo")

html_content = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>PMO Chatbot Demo</title>
  <style>
    /* 
      1) Make the entire page text white on a dark background.
         You can adjust the colors as desired.
    */
    body {
      color: #fff;
      background-color: #000; /* Dark background */
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 0;
    }

    /* Chatbot container styling */
    #chatbot {
      display: none; /* Hidden by default until inactivity triggers it */
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 320px;
      background-color: #333; /* Dark background for the chatbot itself */
      border: 1px solid #555; /* Slightly lighter border */
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }
    
    /* 
      2) Header styling with minimize button 
         Removed the avatar <img> to avoid the broken image icon
    */
    #chatbot-header {
      font-size: 16px;
      font-weight: bold;
      padding: 10px;
      border-bottom: 1px solid #444;
      background-color: #222; 
      border-top-left-radius: 8px;
      border-top-right-radius: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    /* Body styling including chat window and input area */
    #chatbot-body {
      padding: 10px;
    }
    
    /* Chat window styling */
    #chat-window {
      height: 150px;
      overflow-y: auto;
      background-color: #222;
      padding: 10px;
      border: 1px solid #444;
      margin-bottom: 10px;
      border-radius: 4px;
    }
    
    /* Chat message styling */
    .chat-msg {
      margin: 5px 0;
      padding: 6px 8px;
      border-radius: 4px;
      max-width: 90%;
      clear: both;
    }
    .bot-msg {
      background-color: #444; /* Darker background for bot messages */
      float: left;
    }
    .user-msg {
      background-color: #555; /* Slightly different dark background for user messages */
      float: right;
      text-align: right;
    }
    
    /* Chat input area styling */
    #chat-input {
      display: flex;
      border-top: 1px solid #444;
      padding-top: 5px;
    }
    #user-input {
      flex: 1;
      padding: 8px;
      border: 1px solid #444;
      border-radius: 4px;
      font-size: 14px;
      background-color: #222;
      color: #fff;
    }
    #send-btn {
      padding: 8px 12px;
      margin-left: 5px;
      font-size: 14px;
      border: none;
      border-radius: 4px;
      background-color: #007aff;
      color: #fff;
      cursor: pointer;
    }
    
    /* Feedback buttons (hidden initially) */
    #feedback {
      text-align: center;
      margin-top: 10px;
      display: none; /* Only show after bot response */
    }
    .feedback-button {
      cursor: pointer;
      border: none;
      background: none;
      font-size: 20px;
      margin: 0 5px;
      color: #fff;
    }
    
    /* Minimize button styling */
    #minimize-btn {
      background: none;
      border: none;
      font-size: 16px;
      cursor: pointer;
      color: #fff;
    }
  </style>
</head>
<body>
  <h1>Welcome to Our Demo Webpage</h1>
  <p>Interact with the page. The chatbot will pop up after 10 seconds of inactivity.</p>

  <!-- Chatbot Popup Container -->
  <div id="chatbot">
    <div id="chatbot-header">
      <span>PMO Chatbot</span>
      <!-- Minimize button: toggles the chat body -->
      <button id="minimize-btn" onclick="toggleChatbotMinimize()">▼</button>
    </div>
    <!-- Chatbot body -->
    <div id="chatbot-body">
      <!-- Chat Window -->
      <div id="chat-window">
        <p class="chat-msg bot-msg">Can I help you find something?</p>
      </div>
      <!-- Chat Input Area -->
      <div id="chat-input">
        <input type="text" id="user-input" placeholder="Type your question here..." />
        <button id="send-btn" onclick="sendMessage()">Send</button>
      </div>
      <!-- Feedback Buttons -->
      <div id="feedback">
        <button class="feedback-button" onclick="handleFeedback('up')">&#128077;</button>
        <button class="feedback-button" onclick="handleFeedback('down')">&#128078;</button>
      </div>
    </div>
  </div>

  <script>
    let chatbotShown = false;
    let timer;
    let minimized = false;

    const knowledgeBase = {
      "dm template": "You can find the DM Template in the Documents > Templates section.",
      "invoice": "For invoice-related queries, please refer to the Invoicing Guide in the Process Documents.",
      "invoicing": "For invoice-related queries, please refer to the Invoicing Guide in the Process Documents.",
      "training": "To schedule training for new suppliers, use the Training Request Form available on our website.",
      "paid team": "The PAID team handles all preventative maintenance tasks, data management, and invoicing.",
      "fsc team": "The FSC team handles all corrective maintenance tasks."
    };

    function getDynamicResponse(userMessage) {
      let message = userMessage.toLowerCase();
      for (let key in knowledgeBase) {
        if (message.includes(key)) {
          return knowledgeBase[key];
        }
      }
      return "I'm sorry, I couldn't find an exact answer. Please contact support for further assistance.";
    }

    function getSmartResponse(userMessage) {
      return fetch('https://api.example.com/generate-response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userMessage })
      })
      .then(response => response.json())
      .then(data => {
        if (data && data.answer) {
          return data.answer;
        } else {
          return getDynamicResponse(userMessage);
        }
      })
      .catch(error => {
        console.error("Error fetching smart response:", error);
        return getDynamicResponse(userMessage);
      });
    }

    function setupInactivityTimer() {
      function resetTimer() {
        if (!chatbotShown) {
          clearTimeout(timer);
          timer = setTimeout(showChatbot, 10000);
        }
      }
      window.onload = resetTimer;
      document.onclick = resetTimer;
      document.onmousemove = resetTimer;
      document.onkeypress = resetTimer;
    }

    function showChatbot() {
      document.getElementById('chatbot').style.display = 'block';
      chatbotShown = true;
    }

    function toggleChatbotMinimize() {
      const chatBody = document.getElementById('chatbot-body');
      const minBtn = document.getElementById('minimize-btn');
      if (minimized) {
        chatBody.style.display = 'block';
        minBtn.innerText = '▼';
      } else {
        chatBody.style.display = 'none';
        minBtn.innerText = '▲';
      }
      minimized = !minimized;
    }

    function handleFeedback(type) {
      const chatWindow = document.getElementById('chat-window');
      const messages = chatWindow.getElementsByClassName('bot-msg');
      const lastBotMsg = messages[messages.length - 1]
        ? messages[messages.length - 1].innerText
        : "No response captured";
      const feedbackData = {
        feedback: type,
        botResponse: lastBotMsg,
        timestamp: new Date().toISOString()
      };
      console.log("User Feedback:", feedbackData);
      if (type === 'up') {
        alert("Thanks for your positive feedback! (Feedback logged)");
      } else {
        alert("Thanks for your feedback! We'll work on improving. (Feedback logged)");
      }
    }

    function appendMessage(message, sender) {
      const chatWindow = document.getElementById('chat-window');
      const msgPara = document.createElement('p');
      msgPara.classList.add('chat-msg');
      msgPara.classList.add(sender === 'user' ? 'user-msg' : 'bot-msg');
      msgPara.innerText = message;
      chatWindow.appendChild(msgPara);
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    async function sendMessage() {
      const userInput = document.getElementById('user-input');
      const message = userInput.value.trim();
      if (message !== "") {
        appendMessage(message, 'user');
        userInput.value = "";
        const botResponse = await getSmartResponse(message);
        appendMessage(botResponse, 'bot');
        document.getElementById('feedback').style.display = 'block';
      }
    }

    setupInactivityTimer();
  </script>
</body>
</html>
"""

components.html(html_content, height=700)
