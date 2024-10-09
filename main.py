from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

class AITutor:
    def __init__(self):
        self.topics = {
            "Python Basics": "Introduction to variables, data types, and basic operations.",
            "Control Structures": "Learn about if statements, loops, and functions.",
            "Data Structures": "Explore lists, dictionaries, sets, and tuples.",
            "Object-Oriented Programming": "Understand classes, objects, and inheritance.",
            "Error Handling": "Learn how to handle exceptions and errors in Python."
        }
        self.api_url = "https://api.gemini.com/v1/some_endpoint"  # Replace with actual endpoint
        self.api_key = "YOUR_API_KEY"  # Replace with your actual API key

    def fetch_additional_info(self, topic_name):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        try:
            response = requests.get(self.api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Failed to fetch data from the API."}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

tutor = AITutor()

@app.route('/')
def home():
    return render_template('index.html', topics=tutor.topics)

@app.route('/topic/<topic_name>')
def topic(topic_name):
    if topic_name in tutor.topics:
        content = tutor.topics[topic_name]
        api_data = tutor.fetch_additional_info(topic_name)
        return render_template('topic.html', topic_name=topic_name, content=content, api_data=api_data)
    else:
        return redirect(url_for('home'))

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.form.get('question')
    topic_name = request.form.get('topic_name')
    # Here you can process the question further or call another function to handle it
    answer = f"Answering your question about {topic_name}: '{question}'"
    return render_template('answer.html', topic_name=topic_name, question=question, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
