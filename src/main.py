import spacy
import requests
import json
from transitions import Machine
from flask import Flask, request, jsonify

# Load the spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize Flask app
app = Flask(__name__)

# Endor API settings
# redacted for security purposes, but connect to your API in this section

# Chatbot State Machine
class Chatbot:
    states = ['greeting', 'query_handling', 'escalation', 'farewell']

    def __init__(self):
        self.machine = Machine(model=self, states=Chatbot.states, initial='greeting')
        self.machine.add_transition(trigger='process_query', source='greeting', dest='query_handling')
        self.machine.add_transition(trigger='escalate', source='query_handling', dest='escalation')
        self.machine.add_transition(trigger='finish', source='*', dest='farewell')

    def current_state(self):
        return self.state

chatbot_instance = Chatbot()

# Feature Extraction with spaCy
def extract_features(text):
    doc = nlp(text)
    return {
        "num_tokens": len(doc),
        "entities": [ent.label_ for ent in doc.ents]
    }

# Train Model Function
def train_model(training_data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.post(f"{API_URL}/train", headers=headers, json=training_data)
    if response.status_code == 200:
        print("Model training initiated successfully!")
        return response.json()
    else:
        print("Error during training:", response.text)
        return None

# Predict Function
def get_prediction(user_input):
    features = extract_features(user_input)
    payload = {"features": features}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.post(f"{API_URL}/predict", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error during prediction:", response.text)
        return None

# Flask Route for Chat
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    prediction = get_prediction(user_message)
    if prediction and prediction.get("sentiment") == "negative":
        chatbot_instance.escalate()
        reply = "I’m sorry to hear that. Let me connect you with a support specialist."
    else:
        chatbot_instance.process_query()
        reply = "Thanks for sharing that. What else can I help you with?"
    return jsonify({"reply": reply, "state": chatbot_instance.current_state()})

if __name__ == "__main__":
    app.run(debug=True)
