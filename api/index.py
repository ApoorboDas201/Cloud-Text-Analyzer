from flask import Flask, render_template_string, request
from textblob import TextBlob

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    sentiment = ""
    word_count = 0
    subjectivity = ""
    
    if request.method == 'POST':
        user_text = request.form.get('text_input')
        if user_text:
            blob = TextBlob(user_text)
            
            # 1. Sentiment Analysis
            polarity = blob.sentiment.polarity
            if polarity > 0: sentiment = "Positive 😊"
            elif polarity < 0: sentiment = "Negative ☹️"
            else: sentiment = "Neutral 😐"
            
            # 2. Subjectivity (Fact vs Opinion)
            sub = blob.sentiment.subjectivity
            if sub > 0.5: subjectivity = "Opinion-based 💭"
            else: subjectivity = "Fact-based 📊"
            
            # 3. Basic Logic
            word_count = len(user_text.split())

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cloud Intelligence Demo</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-dark text-white p-5">
        <div class="container bg-secondary p-5 rounded shadow" style="max-width: 800px;">
            <h1 class="text-warning">☁️ Cloud Text Intelligence</h1>
            <p>PaaS Demo: Serverless Sentiment & Logic Analysis</p>
            <hr>
            <form method="POST">
                <textarea name="text_input" class="form-control mb-3" rows="4" placeholder="Type a sentence here..." required></textarea>
                <button class="btn btn-warning w-100 fw-bold">ANALYZE IN CLOUD</button>
            </form>
            
            {% if sentiment %}
            <div class="mt-4 p-3 bg-dark rounded">
                <h4 class="text-warning">Cloud Processing Results:</h4>
                <p><strong>Sentiment:</strong> {{ sentiment }}</p>
                <p><strong>Perspective:</strong> {{ subjectivity }}</p>
                <p><strong>Cloud Word Count:</strong> {{ word_count }} words</p>
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    ''', sentiment=sentiment, subjectivity=subjectivity, word_count=word_count)
