from flask import Flask, request, jsonify

# from flask_cors import CORS
from uuid import uuid4
import ollama
from flask import Flask, render_template
import json
from utils.analyzeFeedback import analyze_feedback, load_data


app = Flask(__name__)
# CORS(app)

# Mock database for storing snippets
snippets_db = []
requests_db = []
feedbacks = []


# Appending snippet to a JSON file
def save_snippets(snippet):
    try:
        with open("snippets_db.json", "r+") as f:
            # Load existing data or initialize it if the file is empty
            try:
                json_data = json.load(f)
            except json.JSONDecodeError:
                json_data = []
            # print(type(json_data))
            # Append new feedback and write back to file
            json_data.append(snippet)
            f.seek(0)  # Rewind file to the beginning
            json.dump(json_data, f)
            f.truncate()  # Truncate file to new length if necessary
    except FileNotFoundError:
        # If file does not exist, create it and write the feedback
        with open("snippets_db.json", "w") as f:
            json.dump([snippet], f)


def refine_prompt(description, common_themes):
    # Incorporate common themes into the prompt
    for theme, _ in common_themes:
        if "error" in theme:  # Example condition based on feedback theme
            description += " Include detailed error handling."
        if "documentation" in theme:
            description += " Ensure thorough documentation is provided."
    return description


# Assuming 'common_themes' is retrieved from 'analyze_feedback'
data = load_data("snippets_db.json")
common_themes = analyze_feedback(data)


def generate_code_with_codellama(prompt):
    response = ollama.chat(
        model="codellama", messages=[{"role": "user", "content": prompt}]
    )
    return response  # Adjust based on actual response structure


@app.route("/generate-code/", methods=["POST"])
def generate_code():
    description = request.form.get("description")
    requests_db.append(description)
    refined_description = refine_prompt(description, common_themes)
    generated_code = generate_code_with_codellama(refined_description)
    snippet = {
        "id": str(uuid4()),
        "description": description,
        "code": generated_code["message"]["content"],
    }
    snippets_db.append(snippet)
    # save_snippets(snippet)

    return jsonify(snippet)


@app.route("/submit-feedback/", methods=["POST"])
def submit_feedback():
    snippet_id = request.form.get("snippet_id")
    feedback = request.form.get("feedback")
    rating = request.form.get("rating")  # Get rating from the request

    # Validation for rating (ensure it's between 1 and 5)
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return jsonify({"error": "Rating must be between 1 and 5"}), 400
    except ValueError:
        return jsonify({"error": "Invalid rating value"}), 400

    for snippet in snippets_db:
        if snippet["id"] == snippet_id:
            snippet["feedback"] = feedback
            snippet["rating"] = rating
            save_snippets(snippet)
            # Store feedback with the snippet
            return jsonify({"message": "Feedback received", "snippet_id": snippet_id})
    return jsonify({"error": "Snippet not found"}), 404


@app.route("/snippets/", methods=["GET"])
def list_snippets():
    return jsonify(snippets_db)


@app.route("/feedbacks/", methods=["GET"])
def list_feedbacks():
    return jsonify(feedbacks)


@app.route("/requests/", methods=["GET"])
def list_requests():
    return jsonify(requests_db)


@app.route("/snippets/<snippet_id>", methods=["DELETE"])
def delete_snippet(snippet_id):
    global snippets_db
    snippets_db = [snippet for snippet in snippets_db if snippet["id"] != snippet_id]
    return jsonify({"message": "Snippet deleted"})

@app.route("/snippet/<snippet_id>", methods=["GET"])
def get_snippet(snippet_id):
    snippet = next((s for s in snippets_db if s["id"] == snippet_id), None)
    if snippet:
        return jsonify(snippet)
    return jsonify({"error": "Snippet not found"}), 404



@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
