from flask import Flask, render_template_string, request
from textblob import TextBlob

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    analysis = None
    
    if request.method == 'POST':
        user_text = request.form.get('text_input')
        if user_text:
            blob = TextBlob(user_text)
            
            # Advanced Detection Logic
            polarity = blob.sentiment.polarity
            # Detect Sentiment
            if polarity > 0.1: sentiment = "Positive 😊"
            elif polarity < -0.1: sentiment = "Negative ☹️"
            else: sentiment = "Neutral 😐"
            
            # Detect Language (The Cloud 'Detects' the source)
            try:
                lang = blob.detect_language()
            except:
                lang = "Unknown"

            # Detect Key Phrases (Noun Phrases)
            tags = blob.noun_phrases

            analysis = {
                "sentiment": sentiment,
                "score": round(polarity, 2),
                "language": lang.upper(),
                "phrases": ", ".join(tags) if tags else "None detected",
                "subjectivity": "Opinion" if blob.sentiment.subjectivity > 0.5 else "Fact"
            }

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cloud Intelligence Engine</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            .cloud-card { background: #1e293b; border: 1px solid #334155; border-radius: 15px; padding: 30px; margin-top: 50px; }
            .stat-box { background: #334155; padding: 15px; border-radius: 10px; text-align: center; }
            .highlight { color: #38bdf8; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container" style="max-width: 700px;">
            <div class="cloud-card shadow-lg">
                <h2 class="text-center mb-4">☁️ Serverless NLP Engine</h2>
                <p class="text-center text-muted">B.Tech Demo | Vercel PaaS Implementation</p>
                
                <form method="POST">
                    <textarea name="text_input" class="form-control bg-dark text-white border-secondary mb-3" rows="4" placeholder="Enter text for deep cloud analysis..." required></textarea>
                    <button class="btn btn-primary w-100 fw-bold py-2">RUN CLOUD INFERENCE</button>
                </form>
                
                {% if analysis %}
                <div class="mt-5">
                    <h5 class="mb-3 highlight">Analysis Results:</h5>
                    <div class="row g-3">
                        <div class="col-6"><div class="stat-box"><h6>Sentiment</h6><span class="highlight">{{ analysis.sentiment }}</span></div></div>
                        <div class="col-6"><div class="stat-box"><h6>Confidence</h6><span class="highlight">{{ analysis.score }}</span></div></div>
                        <div class="col-6"><div class="stat-box"><h6>Language</h6><span class="highlight">{{ analysis.language }}</span></div></div>
                        <div class="col-6"><div class="stat-box"><h6>Type</h6><span class="highlight">{{ analysis.subjectivity }}</span></div></div>
                    </div>
                    <div class="mt-3 p-3 bg-dark rounded border border-secondary">
                        <strong>Key Phrases Detected:</strong> <span class="text-info">{{ analysis.phrases }}</span>
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
    </body>
    </html>
    ''', analysis=analysis)
