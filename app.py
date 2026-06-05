from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")

# Connect to Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# --- Home Route ---
@app.route("/")
def home():
    return render_template("index.html")


# --- Ask Anything Route ---
@app.route("/ask", methods=["POST"])
def ask():
    try:
        question = request.form.get("question")

        if not question:
            return jsonify({"response": "Please enter a question."})

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=question
        )

        return jsonify({
            "response": response.text
        })

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})


# --- Summarize Email Route ---
@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        email_text = request.form.get("email")

        if not email_text:
            return jsonify({"response": "Please enter email text."})

        prompt = f"""Summarize the following email in 2-3 concise sentences:

{email_text}"""

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return jsonify({
            "response": response.text
        })

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})


# --- Run the App ---
if __name__ == "__main__":
    app.run(debug=True)