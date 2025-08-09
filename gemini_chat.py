from flask import Flask, render_template_string, request, session
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = "egy_titkos_kulcs_ide"  # ezt cseréld le biztonságos értékre!

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", "AIzaSyDTKf_PGQiUU9ijHHDNdFG1x2hLu3jd4Oc"))
model = genai.GenerativeModel("gemini-2.5-flash")

HTML = """
<!DOCTYPE html>
<html lang="hu">
<head>
    <meta charset="UTF-8">
    <title>Chatbot</title>
    <style>
        body { background: linear-gradient(135deg, #00BFA5 0%, #23272F 100%); color: #eee; font-family: 'Segoe UI', sans-serif; }
        .container { max-width: 480px; margin: 60px auto; background: #23272Fcc; border-radius: 18px; padding: 32px; box-shadow: 0 8px 32px #0006; display: flex; flex-direction: column; height: 600px; }
        h2 { text-align: center; margin-bottom: 24px; color: #00BFA5; }
        .chat { margin-top: 12px; display: flex; flex-direction: column; max-height: 400px; overflow-y: auto; flex: 1; }
        .bubble { margin-bottom: 16px; padding: 14px 18px; border-radius: 14px; max-width: 80%; }
        .user { background: #00BFA5; color: #23272F; text-align: right; align-self: flex-end; }
        .bot { background: #181A20; color: #00BFA5; text-align: left; border: 1px solid #00BFA5; align-self: flex-start; }
        form { display: flex; gap: 8px; margin-top: 16px; }
        input[type=text] { flex: 1; padding: 12px; border-radius: 10px; border: none; background: #333; color: #eee; font-size: 1em; }
        button { padding: 12px 24px; border-radius: 10px; border: none; background: #00BFA5; color: white; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #009e88; }
        .footer { color: #616161; font-size: 10pt; text-align: center; margin-top: 16px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🤖Chatbot</h2>
        <div class="chat" id="chatbox">
            {% for msg in messages %}
                {% if msg.role == 'user' %}
                    <div class="bubble user">🧑 {{ msg.text }}</div>
                {% else %}
                    <div class="bubble bot">🤖 {{ msg.text }}</div>
                {% endif %}
            {% endfor %}
        </div>
        <form method="POST">
            <input type="text" name="user_input" placeholder="Írj ide valamit..." required autocomplete="off">
            <button type="submit">Küldés</button>
        </form>
        <div class="footer">Készítette: Kiss Gergő</div>
    </div>
    <script>
        window.onload = function() {
            var chatDiv = document.getElementById('chatbox');
            chatDiv.scrollTop = chatDiv.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if "messages" not in session:
        session["messages"] = []
    messages = session["messages"]
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            messages.append({"role": "user", "text": user_input})
            try:
                response = model.generate_content(user_input)
                bot_text = response.text.strip()
            except Exception as e:
                bot_text = f"Hiba történt: {e}"
            messages.append({"role": "bot", "text": bot_text})
        session["messages"] = messages
    return render_template_string(HTML, messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
