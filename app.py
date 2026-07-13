import os
from app import Flask, render_template_string, request, jsonify
from google import genai
from google.genai import types # type: ignore

app = Flask(__name__)

# Initialize the Gemini Gen AI Client (reads GEMINI_API_KEY environment variable)
# Make sure you set your GEMINI_API_KEY before running.
try:
    client = genai.Client()
except Exception:
    # Fallback init if environment variable isn't ready immediately
    client = None

# Single-file HTML UI and JavaScript Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini AI Assistant Platform</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f4f9; margin: 0; padding: 20px; display: flex; height: 90vh; gap: 20px; }
        .module-container { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); display: flex; flex-direction: column; }
        .data-panel { width: 30%; }
        .chat-panel { width: 70%; flex-grow: 1; }
        h2 { color: #1a73e8; margin-top: 0; border-bottom: 2px solid #e8f0fe; padding-bottom: 8px; }
        label { font-weight: bold; margin-top: 10px; display: block; color: #4a4a4a; }
        input, textarea { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #dadce0; border-radius: 6px; box-sizing: border-box; }
        .chat-box { flex-grow: 1; border: 1px solid #dadce0; border-radius: 6px; padding: 15px; overflow-y: auto; background-color: #f8f9fa; margin-bottom: 15px; max-height: 60vh; }
        .message { margin-bottom: 12px; padding: 10px 14px; border-radius: 8px; max-width: 80%; line-height: 1.4; }
        .user-msg { background-color: #e8f0fe; color: #1a73e8; align-self: flex-end; margin-left: auto; }
        .ai-msg { background-color: #ffffff; color: #3c4043; border: 1px solid #e0e0e0; }
        .input-group { display: flex; gap: 10px; }
        .input-group input { flex-grow: 1; margin: 0; }
        button { background-color: #1a73e8; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; transition: background 0.2s; }
        button:hover { background-color: #1557b0; }
    </style>
</head>
<body>

    <!-- DATA INFORMATION MODULE -->
    <div class="module-container data-panel">
        <h2>User Info Module</h2>
        <p style="font-size: 13px; color: #666;">This contextual data will be sent alongside your query to customize Gemini's behavior.</p>
        
        <label for="userName">User Name:</label>
        <input type="text" id="userName" value="Alex R.">
        
        <label for="userRole">Profession/Role:</label>
        <input type="text" id="userRole" value="Software Developer">
        
        <label for="userContext">Extra Directives / Preferences:</label>
        <textarea id="userContext" rows="5" style="resize: none;">Prefers concise architectural blueprints instead of high-level overviews. Focuses heavily on clean code.</textarea>
    </div>

    <!-- AI CHAT ASSISTANT MODULE -->
    <div class="module-container chat-panel">
        <h2>Gemini AI Assistant</h2>
        <div class="chat-box" id="chatBox">
            <div class="message ai-msg">Hello! I am initialized with your user module profile data. How can I help you today?</div>
        </div>
        <div class="input-group">
            <input type="text" id="userInput" placeholder="Ask Gemini something..." onkeydown="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const inputField = document.getElementById('userInput');
            const userText = inputField.value.trim();
            if (!userText) return;

            // Clear input field
            inputField.value = '';

            // Render user message visually
            const chatBox = document.getElementById('chatBox');
            chatBox.innerHTML += `<div class="message user-msg">${userText}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;

            // Gather structural information from the User Module
            const userData = {
                name: document.getElementById('userName').value,
                role: document.getElementById('userRole').value,
                context: document.getElementById('userContext').value
            };

            // Call the python backend
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userText, user_info: userData })
                });

                const data = await response.json();
                
                if (data.error) {
                    chatBox.innerHTML += `<div class="message ai-msg" style="color: red;"><strong>Error:</strong> ${data.error}</div>`;
                } else {
                    chatBox.innerHTML += `<div class="message ai-msg">${data.response}</div>`;
                }
            } catch (err) {
                chatBox.innerHTML += `<div class="message ai-msg" style="color: red;"><strong>Connection Error:</strong> ${err.message}</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    global client
    if client is None:
        try:
            client = genai.Client()
        except Exception:
            return jsonify({"error": "Gemini API client not initialized. Make sure GEMINI_API_KEY environment variable is set."}), 500

    data = request.json
    user_message = data.get('message')
    user_info = data.get('user_info', {})

    # Formulate structural System Directives using the incoming Data Information Module
    system_instruction = (
        f"You are a specialized Gemini AI tool. Interacting user profile details:\n"
        f"- Name: {user_info.get('name')}\n"
        f"- Role: {user_info.get('role')}\n"
        f"- User Context & Constraints: {user_info.get('context')}\n"
        f"Tailor all generated responses to adhere strictly to this user context profile."
    )

    try:
        # Request content from the official gemini model using new google-genai SDK standards
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Start the Flask web app locally
    app.run(debug=True, port=5000)