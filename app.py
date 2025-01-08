import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)

# Load environment variables (e.g., OPENAI_API_KEY from a .env file)
_ = load_dotenv(find_dotenv())
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/generate_story", methods=["POST"])
def generate_story():
    data = request.get_json(force=True)

    # Extract the parameters from the JSON body
    genre = data.get("genre", "")
    topic = data.get("topic", "")
    main_characters = data.get("main_characters", "")
    conflict = data.get("conflict", "")
    narrative_style = data.get("narrative_style", "")
    story_length = data.get("story_length", "")

    # Build the prompt/messages for OpenAI
    messages = [
        {
            "role": "system",
            "content": "You are an imaginative story generator that creates engaging narratives."
        },
        {
            "role": "user",
            "content": (
                f"Genre: {genre}\n"
                f"Topic: {topic}\n"
                f"Main Characters: {main_characters}\n"
                f"Conflict: {conflict}\n"
                f"Narrative Style: {narrative_style}\n"
                f"Story Length: {story_length}\n\n"
                "Write a compelling story incorporating these details. "
                "Maintain a cohesive narrative with the specified perspective and length."
            )
        }
    ]

    try:
        # Call OpenAI's ChatCompletion
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        story = response.choices[0].message.content.strip()
        return jsonify({"story": story})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run locally (for testing) t
    app.run(host="0.0.0.0", port=3000, debug=True)
