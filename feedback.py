import ollama
import json

best_snippets_db = []
# Loading feedbacks from a file
def load_snippets():
    try:
        with open('snippets_db.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def assess_feedback_sentiment(feedback):
    # Dummy sentiment analysis; in real applications, use NLP libraries like TextBlob or NLTK
    if any(word in feedback.lower() for word in ['good', 'excellent', 'positive']):
        return 'good'
    elif any(word in feedback.lower() for word in ['bad', 'poor', 'negative']):
        return 'bad'
    return 'neutral'

def generate_better_code(description):
    # Use Ollama to generate better code based on description
    response = ollama.chat(model='codellama', messages=[{'role': 'user', 'content': description}])
    return response['message']['content']

def process_feedbacks():
    for feedback in feedbacks:
        sentiment = assess_feedback_sentiment(feedback['description'])
        if sentiment == 'bad':
            snippet = next((s for s in snippets_db if s['id'] == feedback['snippet_id']), None)
            if snippet:
                new_code = generate_better_code(snippet['description'])
                new_snippet = {
                    'id': snippet['id'],
                    'request': snippet['description'],
                    'snippet': snippet['code'],
                    'feedback': feedback['description'],
                    'new_snippet': new_code
                }
                best_snippets_db.append(new_snippet)

        else:
            snippet = next((s for s in snippets_db if s['id'] == feedback['snippet_id']), None)
            if snippet:
                new_code = snippet['code']
                new_snippet = {
                    'id': snippet['id'],
                    'request': snippet['description'],
                    'snippet': snippet['code'],
                    'feedback': feedback['description'],
                    'new_snippet': new_code
                }
                best_snippets_db.append(new_snippet)


if __name__ == '__main__':
    # process_feedbacks()
    print(feedbacks)
    print("Updated best_snippets_db with new code improvements.")
