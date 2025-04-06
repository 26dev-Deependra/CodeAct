from flask import Flask, request, jsonify
from phi.agent import Agent
from phi.model.groq import Groq
import os 
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Phidata Web Agent
web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=["BE HUMOROUS"],
    markdown=True,
)

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_query = data.get("query", "")
        
        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        # Run the query using the agent
        response = web_agent.run(user_query)

        # ✅ Extract just the assistant's message text
        assistant_reply = response.content if hasattr(response, "content") else str(response)

        return jsonify({
            "query": user_query,
            "response": assistant_reply
        })

    except Exception as e:
        print("🔥 Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
