import random
from flask import Flask, request, render_template, jsonify
from collections import Counter
from flask import Flask
app = Flask(__name__)
# Simple tokenizer using string operations
def tokenize(text):
    # Convert to lowercase and split on whitespace/punctuation
    text = text.lower()
    for char in [',', '.', '!', '?']:
        text = text.replace(char, ' ')
    return text.split()
# Symptom detection without NLTK
def detect_symptom(text):
    tokens = tokenize(text)
    for symptom, keywords in symptom_keywords.items():
        if any(word in tokens for word in keywords):
            return symptom
    return 'default'
# Medical data structures
symptom_keywords = {
    'cold': ['cough', 'sneeze', 'cold', 'congested', 'runny', 'nose'],
    'fever': ['fever', 'temperature', 'hot', 'chills', 'sweating'],
    'headache': ['headache', 'migraine', 'head', 'pain', 'throbbing'],
    'stomach': ['stomach', 'nausea', 'vomit', 'diarrhea', 'cramp'],
}
responses = {
    'cold': [
        "Sounds like you're experiencing cold-like symptoms.",
        "That could be a common cold — make sure to rest and hydrate.",
        "Do you also feel tired or have a sore throat?"
    ],
    'fever': [
        "Fever can be a sign of infection. Monitor your temperature closely.",
        "Make sure to stay hydrated and rest. Consider consulting a doctor if it persists.",
        "Is the fever accompanied by any other symptoms?"
    ],
    'headache': [
        "Headaches can be triggered by many things. Are you getting enough rest?",
        "Try staying hydrated and taking a break from screens.",
        "Do you have any light sensitivity or nausea?"
    ],
    'stomach': [
        "Stomach issues can be tricky. Have you eaten anything unusual recently?",
        "Make sure to stay hydrated. If it continues, you might want to seek medical help.",
        "Keep an eye on your symptoms — persistent issues need a check-up."
    ],
    'default': [
        "Can you describe your symptoms in more detail?",
        "I'll do my best to help. What's bothering you today?",
        "Let's try to figure this out together. Tell me more about how you're feeling."
    ]
}
follow_ups = {
    'cold': ["Are you also feeling fatigued?", "Have your symptoms lasted more than a few days?"],
    'fever': ["When did the fever start?", "Are you taking any medication?"],
    'headache': ["Have you had similar headaches before?", "Any recent stress or dehydration?"],
    'stomach': ["Is it localized pain or general discomfort?", "Any recent changes in diet?"],
    'default': ["Please share more so I can assist you better.", "Tell me everything you're feeling."]
}
resources = {
    'cold': "https://www.nhs.uk/conditions/common-cold/",
    'fever': "https://www.nhs.uk/conditions/flu/",
    'headache': "https://www.nhs.uk/conditions/headaches/",
    'stomach': "https://www.nhs.uk/conditions/stomach-ache/"
}
affirmations = [
    "You're taking the right steps by asking questions.",
    "Listening to your body is so important.",
    "It's okay to seek help — you're not alone.",
    "Your health matters. You're doing great by being proactive."
]
app.run(debug=True, use_reloader=False)
# Storage
symptom_log = []
chat_history = []
# Routes
@app.route("/")
def index():
    return render_template('index.html', history=chat_history)

@app.route("/get_response", methods=['POST'])
def get_response():
    try:
        user_input = request.form['user_input']
        chat_history.append(f"You: {user_input}")
        
        symptom = detect_symptom(user_input)
        symptom_log.append(symptom)
        reply = random.choice(responses.get(symptom, responses['default']))
        follow_up = random.choice(follow_ups.get(symptom, follow_ups['default']))
        affirmation = random.choice(affirmations)
        resource = resources.get(symptom, "")

        full_response = f"{reply} {follow_up}\n\n💬 {affirmation}"
        if resource:
            full_response += f"\n\n📎 Here's a helpful resource: <a href='{resource}' target='_blank'>Learn more</a>"

        chat_history.append(f"Bot: {full_response}")
        return render_template('index.html', history=chat_history)
    except Exception as e:
        return f"Anerror occurred: {str(e)}", 500
@app.route("/summary")
def summary():
    if not symptom_log:
        summary_text = "No symptoms logged yet — let's talk!"
    else:
        summary = Counter(symptom_log)
        summary_text = "Symptom Tracker:\n" + "\n".join([f"{sym.capitalize()}: {count}" for sym, count in summary.items()])
    return jsonify({'summary': summary_text})

if _name_ == '_main_':
    app.run(debug=True, port=5000, host="127.0.0.1")