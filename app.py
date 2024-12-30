from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("api_key"))

# Create the model
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
    system_instruction="You are an advanced legal assistant named Nyayabot, trained to provide accurate, concise, and reliable legal information. Your primary goal is to assist users in understanding legal concepts, processes, and guidelines, and provide tailored responses based on user queries. You specialize in categorizing legal questions, offering step-by-step guidance, and directing users to appropriate legal resources.\n\nYou must maintain a professional and neutral tone at all times, avoiding speculation or personal opinions. Ensure that your responses are easy to understand, but detailed enough to provide value. If a query is unclear or outside the scope of your knowledge, politely request clarification or recommend seeking professional legal advice. Provide a consize answer try answering any query in a word, a line or two",
)

# Initialize Flask app
app = Flask(__name__)

# Chat history
history = []


@app.route("/")
def index():
    """Render the chatbot UI."""
    return render_template("index.html")  # Ensure index.html is in the 'templates' folder


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat requests."""
    user_input = request.json.get("message")  # Get the user's message from the frontend

    # Start a new chat session or continue existing history
    chat_session = model.start_chat(history=history)

    # Generate a response from Gemini
    response = chat_session.send_message(user_input)

    # Extract the model's response
    model_response = response.text

    # Append to the chat history
    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [model_response]})

    return jsonify({"response": model_response})  # Send response back to the frontend


if __name__ == "__main__":
    app.run(debug=True)
