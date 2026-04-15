from flask import Flask, render_template_string, request
from textblob import TextBlob

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    sentiment = ""
    
    if request.method == 'POST':
        user_text = request.form.get('text_input')
        if user_text:
            # The "Cloud Logic": Analyzing text sentiment and translating
            blob = TextBlob(user_text)
            
            # 1. Sentiment Analysis (Is the text positive or negative?)
            polarity = blob.sentiment.polarity
            if polarity > 0: sentiment = "Positive 😊"
            elif polarity < 0: sentiment = "Negative ☹️"
            else: sentiment = "Neutral 😐"
            
            # 2. Translation (Example: Translate to Spanish)
            try:
                result = str(blob.translate(to="es"))
            except:
                result = "Translation service busy, but analysis complete!"

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
            <p>Paste text below to analyze sentiment and translate via Cloud APIs.</p>
            <hr>
            <form method="POST">
                <textarea name="text_input" class="form-control mb-3" rows="4" placeholder="Type something..."></textarea>
                <button class="btn btn-warning w-100 fw-bold">PROCESS IN CLOUD</button>
            </form>
            
            {% if sentiment %}
            <div class="mt-4 p-3 bg-dark rounded">
                <h4>Results:</h4>
                <p><strong>Sentiment:</strong> {{ sentiment }}</p>
                <p><strong>Spanish Translation:</strong> {{ result }}</p>
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    ''', sentiment=sentiment, result=result)
