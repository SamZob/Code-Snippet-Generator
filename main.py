from flask import Flask, request, jsonify
# from flask_cors import CORS
from uuid import uuid4
import ollama
from flask import Flask, render_template


app = Flask(__name__)
# CORS(app)

# Mock database for storing snippets
snippets_db = []
requests_db = []
feedbacks = []

def generate_code_with_codellama(prompt):
    response = ollama.chat(model='codellama', messages=[{'role': 'user', 'content': prompt}])
    return response # Adjust based on actual response structure

@app.route('/generate-code/', methods=['POST'])
def generate_code():
    description = request.values.get('description')
    requests_db.append(description)
    generated_code = generate_code_with_codellama(description)
    snippet = {"id": str(uuid4()), "description": description, "code": generated_code['message']['content']}
    snippets_db.append(snippet)

    return jsonify(snippet)


@app.route('/submit-feedback/', methods=['POST'])
def submit_feedback():
    snippet_id = request.values.get('snippet_id')
    description = request.values.get('feedback')
    
    # Find the snippet by ID
    snippet = next((item for item in snippets_db if item['id'] == snippet_id), None)
    if not snippet:
        return jsonify({"error": "Snippet not found"}), 404

    feedback = {"snippet_id": snippet_id, "description": description}
    feedbacks.append(feedback)

    return jsonify({"message": "Feedback received"})

@app.route('/snippets/', methods=['GET'])
def list_snippets():
    return jsonify(snippets_db)

@app.route('/feedbacks/',methods = ['GET'])
def list_feedbacks():
    return jsonify(feedbacks)

@app.route('/requests/',methods = ['GET'])
def list_requestss():
    return jsonify(requests_db)


@app.route('/snippets/<snippet_id>', methods=['DELETE'])
def delete_snippet(snippet_id):
    global snippets_db
    snippets_db = [snippet for snippet in snippets_db if snippet['id'] != snippet_id]
    return jsonify({"message": "Snippet deleted"})


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
