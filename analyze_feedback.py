import json
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("stopwords")


def load_data(filename):
    """Load JSON data from a file."""
    with open(filename, "r") as file:
        return json.load(file)


# analyzes the patterns and common themes of feedbacks
def analyze_feedback(data):
    """Analyze feedback to find common themes."""
    feedback_texts = [item["feedback"] for item in data]
    all_text = " ".join(feedback_texts).lower()
    tokens = word_tokenize(all_text)
    tokens = [
        token for token in tokens if token.isalpha()
    ]  # Remove non-alphabetic tokens

    # Remove common stopwords
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if not word in stop_words]

    # Frequency distribution of words
    freq_dist = Counter(filtered_tokens)
    return freq_dist.most_common(10)  # Return top 10 common words


# Load the JSON data
data = load_data("snippets_db.json")

# Analyze the feedback
common_themes = analyze_feedback(data)
print("Common themes in feedback:", common_themes)
