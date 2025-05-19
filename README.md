![License](https://img.shields.io/badge/license-MIT-blue.svg)

# EngageBot: Dynamic Learning Chatbot

## Overview

This project is a dynamic-learning chatbot designed for a teams internal webpage. The chatbot simulates an intelligent assistant that proactively appears after a period of inactivity, guides users to relevant documents, and collects feedback for continuous improvement. The demo is deployed as a Streamlit application, and a separate integration code is provided for deploying the chatbot on the Endor AI platform for advanced dynamic learning and adaptive conversation flows.

## Features

- **Proactive Engagement:**  
  For this demo, the chatbot activates after 10 seconds of inactivity to simulate a proactive, helpful assistant—whereas in the standard release, it typically waits 45–60 seconds before appearing.

- **Interactive Chat Interface:**  
  A user-friendly interface built with HTML, CSS, and JavaScript is embedded into a Streamlit app. Users can type questions, receive simulated intelligent responses, and provide feedback via thumbs up/down buttons.

- **Dynamic Learning Simulation:**  
  The demo uses a simulated knowledge base combined with a call to a "smart model" API to generate responses. User feedback is logged to simulate reinforcement learning (RLHF) for future model improvements.

- **Dark Theme:**  
  The application features a dark background with white text for a modern, professional look.

- **Future Endor AI Integration:**  
  A separate Python code snippet is provided to demonstrate how the chatbot could be deployed on the Endor AI platform. This integration includes:
  - Data collection and preprocessing using spaCy.
  - Model training via Endor's API.
  - Adaptive conversation flows using a state machine (via the `transitions` library).
  - A Flask web application exposing an endpoint for real-time chatbot interactions.

## Technology Stack

- **Front-end:** HTML, CSS, and JavaScript for the interactive chatbot interface.
- **Back-end/Demo:** Python with Streamlit for rapid prototyping and demonstration.
- **NLP:** spaCy (and NLTK, if needed) for text processing and feature extraction.
- **State Management:** The `transitions` library to manage conversation states.
- **Web Framework:** Flask is used in the Endor integration for serving the chatbot API.
- **HTTP Requests:** The `requests` library for communicating with Endor’s API.
- **Deployment:** Streamlit app hosted via Google Colab with pyngrok for public access.

## Installation and Setup

### For the Streamlit Demo - Installation and Setup

**Step 1: Clone the Repository**

git clone https://github.com/your-username/EngageBot.git
cd EngageBot

**Step 2: (Optional) Run Locally**

Make sure you have Python installed, then install Streamlit:

pip install streamlit

Run the app with:

streamlit run chatbot.py

**Step 3: Running on Google Colab**

1. **Upload your repository folder** to Google Drive.

2. **Mount your Drive** in a Colab notebook:

from google.colab import drive
drive.mount('/content/drive')
%cd /content/drive/MyDrive/EngageBot

3. **Install Dependencies**:

!pip install streamlit pyngrok

4. **Launch the Streamlit App and Expose it with ngrok**:

from pyngrok import ngrok
import time

ngrok.set_auth_token("YOUR_NGROK_AUTHTOKEN")  # Replace with your actual authtoken
public_url = ngrok.connect(8501, proto="http")
print("Your Streamlit app is available at:", public_url)

!streamlit run chatbot.py &
time.sleep(5)



