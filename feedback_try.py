import json

def save_feedback(feedback):
    try:
        with open('feedbacks.json', 'r+') as f:
            # Load existing data or initialize it if the file is empty
            try:
                json_data = json.load(f)
            except json.JSONDecodeError:
                json_data = []
            
            # Append new feedback and write back to file
            json_data.append(feedback)
            f.seek(0)  # Rewind file to the beginning
            json.dump(json_data, f)
            f.truncate()  # Truncate file to new length if necessary
    except FileNotFoundError:
        # If file does not exist, create it and write the feedback
        with open('feedbacks.json', 'w') as f:
            json.dump([feedback], f)

def load_feedbacks():
    try:
        with open('feedbacks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist

# Example feedback to save
feedback = {"snippet_id": "123", "description": "This code snippet is well-written.", "rating": 5}
save_feedback(feedback)
loaded_feedbacks = load_feedbacks()
print(loaded_feedbacks)
