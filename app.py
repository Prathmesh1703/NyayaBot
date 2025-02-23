import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)

# Configure GenAI model
genai.configure(api_key=os.getenv("api_key"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are an advanced legal assistant named Nyayabot, trained to provide accurate, concise, and reliable legal information.",
)

history = []  # Keep track of chat history

@app.route("/")
def index():
    return render_template("index.html")  # Load the frontend

@app.route("/chat", methods=["POST"])
def chat():
    global history  # Keep conversation context

    data = request.get_json()
    user_input = data.get("message", "")

    # Start chat session with history
    chat_session = model.start_chat(history=history)

    # Get response from the AI
    response = chat_session.send_message(user_input)
    model_response = response.text

    # Update history
    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [model_response]})

    return jsonify({"response": model_response})  # Send response to frontend

if __name__ == "__main__":
    app.run(debug=True)
